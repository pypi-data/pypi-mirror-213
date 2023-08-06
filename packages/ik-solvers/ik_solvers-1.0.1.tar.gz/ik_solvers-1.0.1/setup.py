import os
import re
import sys
import platform
import subprocess

from os import path
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        if platform.system() == "Windows" or platform.system() == "darwin":
            Extension.__init__(self, name, sources=[], include_dirs=[
                # Path to pybind11 headers
                get_pybind_include(),
                get_pybind_include(user=True)])
        else:
            Extension.__init__(self, name, sources=[])

        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(build_ext):
    def run(self):
        if path.exists('.git'):
            subprocess.check_call(['git', 'submodule', 'update', '--init', '--recursive'])

        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    @staticmethod
    def which(program, env=os.environ):
        def isExe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
        fpath, fname = os.path.split(program)
        if fpath:
            if isExe(program):
                return program
        else:
            for path in env.get("PATH", "").split(os.pathsep):
                path = path.strip("\"")
                exe = os.path.join(path, program)
                if isExe(exe):
                    return exe
        return None

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
                           '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir),
                           '-DEXAMPLES=OFF']
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())

        if self.which('ninja', env) is not None:
            cmake_args += ['-GNinja']

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)

__version__ = "1.0.1"


setup(
    name="ik_solvers",
    version=__version__,
    author="Zongyao Yi",
    author_email="zongyao.yi@dfki.de",
    url="https://github.com/jongyaoY/ik_solvers",
    license='MIT',
    description="IKSolver Python wrapper",
    long_description='''
    A Python wrapper of the inverse kinematics solvers orignially from https://github.com/fzi-forschungszentrum-informatik/cartesian_controllers.git
    ''',
    ext_modules=[CMakeExtension("ik_solvers/PyIKSolver")],
    build_requires=["pybind11"],
    setup_requires=['setuptools_scm', 'pybind11>=2.10.1'],
    options={'build': {'build_base': 'build-setuptools'}},
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    python_requires=">=3.7",
)
