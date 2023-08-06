////////////////////////////////////////////////////////////////////////////////
// Copyright 2019 FZI Research Center for Information Technology
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice,
// this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice,
// this list of conditions and the following disclaimer in the documentation
// and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its
// contributors may be used to endorse or promote products derived from this
// software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.
////////////////////////////////////////////////////////////////////////////////

//-----------------------------------------------------------------------------
/*!\file    IKSolver.cpp
 *
 * \author  Stefan Scherzinger <scherzin@fzi.de>
 * \date    2016/02/14
 *
 */
//-----------------------------------------------------------------------------
#include <IKSolver.h>
// other
#include <map>
#include <sstream>
#include <algorithm>

// KDL
#include <kdl/jntarrayvel.hpp>
#include <kdl/framevel.hpp>
namespace ik_solvers
{
  IKSolver::IKSolver()
  {
  }

  IKSolver::~IKSolver(){}

  const std::vector<double> IKSolver::getEndEffectorPose6D() const
  {
    std::vector<double> pose;
    auto pos = m_end_effector_pose.p;
    auto rot = m_end_effector_pose.M.GetRot();
    pose.push_back(pos.x());
    pose.push_back(pos.y());
    pose.push_back(pos.z());
    pose.push_back(rot.x());
    pose.push_back(rot.y());
    pose.push_back(rot.z());
    return pose;
  }

  const KDL::Frame& IKSolver::getEndEffectorPose() const
  {
    return m_end_effector_pose;
  }
  const std::vector<double> IKSolver::forwardKinematics(const std::vector<double>& joint_positions, const std::string& segment_name)
  {
    KDL::JntArray j_pos(m_number_joints);
    KDL::Frame segment_pose;
    std::vector<double> segment_pose_6d;
    for(int i = 0; i < m_number_joints; i++)
    {
      j_pos(i) = joint_positions[i];
    }
    m_fk_pos_solver->JntToCart(j_pos, segment_pose);
    auto pos = segment_pose.p;
    auto rot = segment_pose.M.GetRot();
    segment_pose_6d.push_back(pos.x());
    segment_pose_6d.push_back(pos.y());
    segment_pose_6d.push_back(pos.z());
    segment_pose_6d.push_back(rot.x());
    segment_pose_6d.push_back(rot.y());
    segment_pose_6d.push_back(rot.z());
    return segment_pose_6d;
  }
  const ctrl::Vector6D& IKSolver::getEndEffectorVel() const
  {
    return m_end_effector_vel;
  }

  const KDL::JntArray& IKSolver::getPositions() const
  {
    return m_current_positions;
  }

  bool IKSolver::init(const KDL::Chain& chain,
                      const KDL::JntArray& upper_pos_limits,
                      const KDL::JntArray& lower_pos_limits)
  {
    // Initialize
    m_chain = chain;
    m_number_joints              = m_chain.getNrOfJoints();
    m_current_positions.data     = ctrl::VectorND::Zero(m_number_joints);
    m_current_velocities.data    = ctrl::VectorND::Zero(m_number_joints);
    m_current_accelerations.data = ctrl::VectorND::Zero(m_number_joints);
    m_last_positions.data        = ctrl::VectorND::Zero(m_number_joints);
    m_last_velocities.data       = ctrl::VectorND::Zero(m_number_joints);
    m_upper_pos_limits           = upper_pos_limits;
    m_lower_pos_limits           = lower_pos_limits;

    // Forward kinematics
    m_fk_pos_solver.reset(new KDL::ChainFkSolverPos_recursive(m_chain));
    m_fk_vel_solver.reset(new KDL::ChainFkSolverVel_recursive(m_chain));

    return true;
  }
  void IKSolver::updateKinematics()
  {
    // Pose w. r. t. base
    m_fk_pos_solver->JntToCart(m_current_positions,m_end_effector_pose);

    // Absolute velocity w. r. t. base
    KDL::FrameVel vel;
    m_fk_vel_solver->JntToCart(KDL::JntArrayVel(m_current_positions,m_current_velocities),vel);
    m_end_effector_vel[0] = vel.deriv().vel.x();
    m_end_effector_vel[1] = vel.deriv().vel.y();
    m_end_effector_vel[2] = vel.deriv().vel.z();
    m_end_effector_vel[3] = vel.deriv().rot.x();
    m_end_effector_vel[4] = vel.deriv().rot.y();
    m_end_effector_vel[5] = vel.deriv().rot.z();
  }

  void IKSolver::applyJointLimits()
  {
    for (int i = 0; i < m_number_joints; ++i)
    {
      if (std::isnan(m_lower_pos_limits(i)) || std::isnan(m_upper_pos_limits(i)))
      {
        // Joint marked as continuous.
        continue;
      }
      m_current_positions(i) = ctrl::clip(
          m_current_positions(i),m_lower_pos_limits(i),m_upper_pos_limits(i));
    }
  }
  bool IKSolver::setStartState(const std::vector<double>& joint_positions, const std::vector<double>& joint_velocities)
  {
    // Copy into internal buffers.
    for (size_t i = 0; i < joint_positions.size(); ++i)
    {
      m_current_positions(i)      = joint_positions[i];
      m_current_velocities(i)     = joint_velocities[i];
      m_current_accelerations(i)  = 0.0;

      m_last_positions(i)         = m_current_positions(i);
      m_last_velocities(i)        = m_current_velocities(i);
    }
    return true;
  }


  void IKSolver::synchronizeJointPositions(const std::vector<double>& joint_positions)
  {
    for (size_t i = 0; i < joint_positions.size(); ++i)
    {
      m_current_positions(i) = joint_positions[i];
      m_last_positions(i)    = m_current_positions(i);
    }
  }
}