#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>
// #include <SolverLoader.h>
#include <IKSolver.h>
#include <ForwardDynamicsSolver.h>
#include <kdl_parser.hpp>

#define IKSolver_VERSION_STRING "1.0.1"
namespace py = pybind11;
using namespace ik_solvers;

namespace ik_solvers
{
    std::shared_ptr<IKSolver> load(
    const std::string ik_solver_name, 
    const std::string urdf_file_path,
    const std::string robot_base_link,
    const std::string end_effector_link,
    const std::vector<double> joint_limits_lower,
    const std::vector<double> joint_limits_upper)
    {
        std::shared_ptr<ForwardDynamicsSolver> ik_solver;
        if(ik_solver_name == "forward_dynamics")
        {
            ik_solver = std::make_shared<ForwardDynamicsSolver>();
        }
        KDL::Chain robot_chain;
        KDL::Tree   robot_tree;
        kdl_parser::treeFromFile(urdf_file_path, robot_tree);
        robot_tree.getChain(robot_base_link,end_effector_link, robot_chain);
        // Parse joint limits
        KDL::JntArray upper_pos_limits(joint_limits_upper.size());
        KDL::JntArray lower_pos_limits(joint_limits_lower.size());
        for (size_t i = 0; i < 6; ++i)
        {
            upper_pos_limits(i) = joint_limits_upper[i];
            lower_pos_limits(i) = joint_limits_lower[i];
        }
        if(ik_solver != nullptr)
        {
            ik_solver->init(robot_chain, upper_pos_limits, lower_pos_limits);
        }

        return ik_solver;
    }

    class IKSolverPy : public IKSolver
    {
        public:
            using IKSolver::IKSolver; // Inherit constructors
            std::vector<double> getJointControlCmds(
                double period,
                const ctrl::Vector6D& net_force) override 
            {
                PYBIND11_OVERRIDE_PURE(std::vector<double>, IKSolver, getJointControlCmds, period, net_force);
            }
            // bool init(const KDL::Chain& chain,
            //           const KDL::JntArray& upper_pos_limits,
            //           const KDL::JntArray& lower_pos_limits) override
            // {
            //     PYBIND11_OVERRIDE_PURE(bool, IKSolver, init, chain, upper_pos_limits, lower_pos_limits);

            // }
    };
    class ForwardDynamicsSolverPy : public ForwardDynamicsSolver
    {
        public:
            using ForwardDynamicsSolver::ForwardDynamicsSolver;
            std::vector<double> getJointControlCmds(
                double period,
                const ctrl::Vector6D& net_force) override 
            {
                PYBIND11_OVERRIDE_PURE(std::vector<double>, ForwardDynamicsSolver, getJointControlCmds);
            }
    };
    
    PYBIND11_MODULE(PyIKSolver, m)
    {
        m.doc() = "IKSolver Python wrapper"; // optional module docstring
        m.attr("__version__") = IKSolver_VERSION_STRING;
        m.def("load", &ik_solvers::load, 
            py::arg("ik_solver_name"),
            py::arg("urdf_file_path"),
            py::arg("robot_base_link"),
            py::arg("end_effector_link"),
            py::arg("joint_limits_lower"),
            py::arg("joint_limits_upper"),
            py::call_guard<py::gil_scoped_release>()
        );

        py::class_<IKSolver, IKSolverPy, std::shared_ptr<IKSolver>>(m, "IKSolver")
            .def(py::init<>())
            .def("setStartState", 
                &IKSolver::setStartState,
                py::arg("joint_positions"),
                py::arg("joint_velocities"),
                py::call_guard<py::gil_scoped_release>())
            .def("forwardKinematics",
                &IKSolver::forwardKinematics,
                py::arg("joint_positions"),
                py::arg("segment_name"),
                py::call_guard<py::gil_scoped_release>())
            .def("getEndEffectorPose", 
                &IKSolver::getEndEffectorPose6D,
                py::call_guard<py::gil_scoped_release>())
            .def("updateKinematics", &IKSolver::updateKinematics,
                py::call_guard<py::gil_scoped_release>())
            .def("getJointControlCmds",&IKSolver::getJointControlCmds,
                py::arg("period"),
                py::arg("net_force"),
                py::call_guard<py::gil_scoped_release>())
            .def("synchronizeJointPositions", &IKSolver::synchronizeJointPositions,
                py::arg("joint_positions"),
                py::call_guard<py::gil_scoped_release>());
        
        py::class_<ForwardDynamicsSolver, IKSolver, ForwardDynamicsSolverPy, std::shared_ptr<ForwardDynamicsSolver>>(m, "ForwardDynamicsSolver");
    }

}