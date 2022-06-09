# Run vicalib

export ID0=745612070185     # <= change this
export ID1=819112071065     # <= change this

'''
if you have this error 
error while loading shared libraries: libcalibu.so: cannot open shared object file: No such file or directory
Try this!
'''
LD_LIBRARY_PATH=/home/d435/calibration/arpg/releases/lib
export LD_LIBRARY_PATH

'''
if you have this error 
error while loading shared libraries: libmessage_filters.so: cannot open shared object file: No such file or directory
Try this!
'''
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/d435/calibration/arpg/releases/lib:/opt/ros/melodic/lib

$HOME/calibration/arpg/releases/bin/vicalib \
-grid_preset medium \
-frame_skip 8 \
-num_vicalib_frames 64 \
-output $HOME/calibration/$ID0-$ID1.xml \
-cam convert://realsense2:[id0=$ID0,id1=$ID1,size=640x480,depth=0]// \
-nocalibrate_intrinsics \
-model_files $HOME/calibration/$ID0.xml,$HOME/calibration/$ID1.xml

'''
!!! Notice !!!
MSE need to < 0.15
if MSE > 0.15
try to increase frame_skip & num_vicalib_frames 
'''


# ========================================================================================================== #

# Run ROS 3D-Point Cloud

export ID1=745612070185     # <= change this, recommond let ID1 be master
export ID2=819112071065     # <= change this
export MASTER=745612070185  # <= change this

roslaunch realsense2_camera rs_camera.launch serial_no:=$ID1 camera:=$ID1 depth_width:=640 depth_height:=480 color_width:=640 color_height:=480 depth_fps:=30 color_fps:=30 align_depth:=true

roslaunch realsense2_camera rs_camera.launch serial_no:=$ID2 camera:=$ID2 depth_width:=640 depth_height:=480 color_width:=640 color_height:=480 depth_fps:=30 color_fps:=30 align_depth:=true

rosrun tf static_transform_publisher 0.0000000 0.0000000 0.0000000 0.0000000 0.0000000 0.0000000 ${MASTER}_color_optical_frame world 30

rosrun tf static_transform_publisher -0.1665806 -0.5024542  0.3916981  1.2372657  0.6420380  0.0879005 ${MASTER}_color_optical_frame ${ID2}_color_optical_frame 30

