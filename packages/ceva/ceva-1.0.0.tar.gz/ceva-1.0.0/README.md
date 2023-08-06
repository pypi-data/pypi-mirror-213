# ContEva - Continuous-time Evaluation

Light-weight package to create b-spline trajectory from 6DOF control points, 

# Prerequisites

Please ensure the following dependencies are met

* Ubuntu 20.04
* ROS noetic
* fmt (install by `sudo apt install ros-noetic-pybind11-catkin libfmt-dev`)

# Download and Compile

```
mkdir -p ~/ceva_ws/src
cd ~/ceva_ws/src
git clone https://github.com/brytsknguyen/ceva
cd ~/ceva
catkin build
source ~/ceva_ws/devel/setup.bash
```

# Test the sample file

```
roscd ceva/scripts
python3 test.py
```
