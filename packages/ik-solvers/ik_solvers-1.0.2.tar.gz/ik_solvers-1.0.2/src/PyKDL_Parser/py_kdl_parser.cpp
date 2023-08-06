#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>

#include <kdl_parser.hpp>

namespace py = pybind11;

namespace kdl_parser
{
    PYBIND11_MODULE(PyKDL_Parser, m)
    {
        m.def("treeFromFile", (bool (*)(const std::string&, KDL::Tree&)) &kdl_parser::treeFromFile,
            py::arg("file"),
            py::arg("tree"));
        m.def("treeFromFile", (KDL::Tree (*) (const std::string&)) &kdl_parser::treeFromFile,
            py::arg("file"));
    }
} // namespace kdl_parser
