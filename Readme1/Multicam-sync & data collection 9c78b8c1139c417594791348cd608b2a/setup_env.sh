# Change this to your own path
export PATH=$PATH:/home/d435/Documents 
 
# Install Librealsense
sudo apt-get install lsb-release software-properties-common
# This command need to wait for awhile
sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u
sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils
sudo apt-get install librealsense2-dev

echo "====================librealsense installed===================="

#Install Vicalib
sudo apt install \
wget \
cmake \
build-essential \
libeigen3-dev \
libgoogle-glog-dev \
libtinyxml2-dev \
libopencv-dev \
libprotobuf-dev \
protobuf-compiler \
libglew-dev \
freeglut3-dev

# Create root directory.
mkdir -p $HOME/calibration

echo "====================Root directory created successfully===================="

# Install ceres-solver-1.14.0.
cd $HOME/calibration
wget http://ceres-solver.org/ceres-solver-1.14.0.tar.gz
tar -zxvf ceres-solver-1.14.0.tar.gz
cd ceres-solver-1.14.0 && mkdir -p release && mkdir -p build && cd build
cmake .. \
-DCMAKE_BUILD_TYPE=RELEASE \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/ceres-solver-1.14.0/release
make -j8
make install

echo "====================ceres-solver installed successfully===================="

# Create ARPG install directory.
cd $HOME/calibration
mkdir -p arpg && cd arpg
mkdir -p releases && mkdir -p builds

echo "====================ARPG directory installed successfully===================="

# Update environment variables.
export PATH=$HOME/calibration/arpg/releases/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=$HOME/calibration/arpg/releases/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export LIBRARY_PATH=$HOME/calibration/arpg/releases/lib${LIBRARY_PATH:+:${LIBRARY_PATH}}
export C_INCLUDE_PATH=$HOME/calibration/arpg/releases/include${C_INCLUDE_PATH:+:${C_INCLUDE_PATH}}
export CPLUS_INCLUDE_PATH=$HOME/calibration/arpg/releases/include${CPLUS_INCLUDE_PATH:+:${CPLUS_INCLUDE_PATH}}

echo "====================environment variables updated successfully===================="

# Install Sophus.
cd $HOME/calibration/arpg
git clone https://github.com/arpg/Sophus
mkdir -p builds/Sophus && cd builds/Sophus
cmake ../../Sophus \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/arpg/releases
make -j8
make install

echo "====================Sophus installed successfully===================="

# Install Calibu.
cd $HOME/calibration/arpg
git clone https://github.com/arpg/Calibu
mkdir -p builds/Calibu && cd builds/Calibu
cmake ../../Calibu \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/arpg/releases
make -j8
make install

echo "====================Calibu install successfully===================="

# Install CVars.
cd $HOME/calibration/arpg
git clone https://github.com/arpg/CVars
mkdir -p builds/CVars && cd builds/CVars
cmake ../../CVars \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/arpg/releases
make -j8
make install

echo "====================cvars installed successfully===================="

# Install HAL.
cd $HOME/calibration/arpg
git clone https://github.com/arpg/HAL
mkdir -p builds/HAL && cd builds/HAL
cmake ../../HAL \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/arpg/releases
make -j8
make install
# If there is fatal error, update the enviroment variables again in line 60.

echo "====================HAL installed successfully===================="

# Install Pangolin.
cd $HOME/calibration/arpg
git clone https://github.com/arpg/Pangolin
mkdir -p builds/Pangolin && cd builds/Pangolin
cmake ../../Pangolin \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/arpg/releases
make -j8
make install

echo "====================pangolin installed successfully===================="

# Install vicalib.
cd $HOME/calibration/arpg
git clone https://github.com/arpg/vicalib
if [[ $(lsb_release -rs) == "18.04" ]]; then
sed -i 's/Eigen::VectorXd params_(calibu::Rational6Camera<double>::NumParams);/Eigen::VectorXd params_(10);/g' vicalib/src/vicalib-engine.cc && \
sed -i 's/Eigen::VectorXd params_(calibu::KannalaBrandtCamera<double>::NumParams);/Eigen::VectorXd params_(8);/g' vicalib/src/vicalib-engine.cc && \
sed -i 's/Eigen::VectorXd params_(calibu::LinearCamera<double>::NumParams);/Eigen::VectorXd params_(4);/g' vicalib/src/vicalib-engine.cc
fi
mkdir -p builds/vicalib && cd builds/vicalib
cmake ../../vicalib \
-DCMAKE_INSTALL_PREFIX=$HOME/calibration/arpg/releases \
-DCMAKE_PREFIX_PATH=$HOME/calibration/ceres-solver-1.14.0/release/lib/cmake/Ceres
make -j8
make install

echo "====================vicalib installed successfully===================="

# Install realsense-ros
sudo apt-get install lsb-release curl

sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
sudo apt-get update
sudo apt-get install ros-melodic-desktop-full

echo "source /opt/ros/melodic/setup.bash" >> $HOME/.bashrc
source $HOME/.bashrc

sudo apt-get install ros-melodic-ddynamic-reconfigure

mkdir -p $HOME/catkin_ws/realsense-ros/src
cd $HOME/catkin_ws/realsense-ros/src

git clone https://github.com/IntelRealSense/realsense-ros.git
cd realsense-ros
git checkout `git tag | sort -V | grep -P "^2.\d+\.\d+" | tail -1`
cd ..

catkin_init_workspace
cd ..
catkin_make clean
catkin_make -DCATKIN_ENABLE_TESTING=False -DCMAKE_BUILD_TYPE=Release
catkin_make install

echo "source $HOME/catkin_ws/realsense-ros/devel/setup.bash" >> $HOME/.bashrc
source $HOME/.bashrc

echo "====================realsense-ros installed successfully===================="

# Install terminator
sudo apt-get install terminator
# Installing terminator will change the default terminal. To change it back:
sudo update-alternatives --config x-terminal-emulator

echo "====================terminator installed successfully===================="