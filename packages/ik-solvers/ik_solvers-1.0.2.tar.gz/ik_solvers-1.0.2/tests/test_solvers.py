import os
import unittest
class TestLoad(unittest.TestCase):
    def test_load(self):
        urdf_file = os.path.join(os.path.dirname(__file__), "ur10e.urdf")
        try:
            from ik_solvers import PyIKSolver, PyKDL, PyKDL_Parser
            base_link = "base_link"
            eef_link = "ft_sensor"
            robot_chain = PyKDL_Parser.treeFromFile(urdf_file).getChain(base_link, eef_link)
            ik_solver = PyIKSolver.ForwardDynamicsSolver()
            ik_solver.init(robot_chain, PyKDL.JntArray(6), PyKDL.JntArray(6))
            # ik_solver = PyIKSolver.load("forward_dynamics",urdf_file,"base_link","ft_sensor",[-3.14,-3.14,-3.14,-3.14,-3.14,-3.14], [3.14,3.14,3.14,3.14,3.14,3.14])
            ik_solver.setStartState([0,0,0,0,0,0],[0,0,0,0,0,0])
        except Exception as e:
            self.fail(f"PyIKSolver.load() raised Exception: {e.msg}")

if __name__ == '__main__':
    unittest.main()

