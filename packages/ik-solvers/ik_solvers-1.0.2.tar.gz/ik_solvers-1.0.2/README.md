# ik_solvers
This project provides a python wrapper for the inverse kinematics solvers originally from [cartesian_controllers](https://github.com/fzi-forschungszentrum-informatik/cartesian_controllers). The ROS dependencies from the [original package](https://github.com/fzi-forschungszentrum-informatik/cartesian_controllers) have been removed. Initial purpose of this package is to facilitate the reimplementation of [cartesian controllers](https://github.com/fzi-forschungszentrum-informatik/cartesian_controllers) in python. Currently only the solver using forward dynamics is implemented. See [this](https://ieeexplore.ieee.org/document/8206325) and [this paper](https://arxiv.org/pdf/1908.06252.pdf) for more details.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* CMake
* Eigen3.3
```bash
sudo apt install libeigen3-dev libtinyxml-dev
```
### Installation
This package can be installed from source or using PyPI

* Install with PyPI
```bash
pip install ik_solvers
```

* Install from source
```bash
git clone <this repository>
cd ik_solvers
pip install .
```

## Usage
```python
from ik_solvers import PyIKSolver
ik_solver = PyIKSolver.load(**params)
```

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>