#pragma once

#include <IKSolver.h>
#include <ForwardDynamicsSolver.h>
#include <kdl_parser/kdl_parser.hpp>
#include <urdf/model.h>
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
        urdf::Model robot_model;
        KDL::Tree   robot_tree;
        bool success = robot_model.initFile(urdf_file_path);
        if(success)
        {
            kdl_parser::treeFromUrdfModel(robot_model,robot_tree);
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
        }

        return ik_solver;
    }
}