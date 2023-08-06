import os
import unittest
class TestLoad(unittest.TestCase):
    def test_load(self):
        urdf_file = os.path.join(os.path.dirname(__file__), "ur10e.urdf")
        try:
            from ik_solvers import PyIKSolver
            ik_solver = PyIKSolver.load("forward_dynamics",urdf_file,"base_link","ft_sensor",[-3.14,-3.14,-3.14,-3.14,-3.14,-3.14], [3.14,3.14,3.14,3.14,3.14,3.14])
            ik_solver.setStartState([0,0,0,0,0,0],[0,0,0,0,0,0])
        except Exception as e:
            self.fail(f"PyIKSolver.load() raised Exception: {e.msg}")

if __name__ == '__main__':
    unittest.main()

