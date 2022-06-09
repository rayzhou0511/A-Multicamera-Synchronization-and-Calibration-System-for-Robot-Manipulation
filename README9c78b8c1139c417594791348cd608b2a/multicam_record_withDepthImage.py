import pyrealsense2 as rs
import numpy as np
import cv2
import os
import shutil
import threading
import time
import os.path
from os import path

total_cam_num = 3       # <-- Change This !!!

path = 'serial.txt'
f = open(path, 'w')
for i in range(total_cam_num):
    f.write('cam'+ str(i) + '                    ')
f.write('\n')

device_name = ['745612070185', '819112071065', '745212070452']      # <-- Change This !!!
device_idx = [0]*total_cam_num

ctx = rs.context()

for i in range(len(ctx.devices)):
    sn = ctx.devices[i].get_info(rs.camera_info.serial_number)

    for j in range(0, total_cam_num):
    #print(sn)
        if sn == device_name[j]:
            device_idx[i] = j

# Delete & Create Folder
for i in range(0, total_cam_num):
    route = "RGBimage" + str(i)
    if os.path.exists(route):
        shutil.rmtree('RGBimage' + str(i))
        shutil.rmtree('Depthimage' + str(i))
    os.mkdir('RGBimage' + str(i))
    os.mkdir('Depthimage' + str(i))

 
# Configure depth and color streams
pipeline = [None]*total_cam_num
config = [None]*total_cam_num
for i, name in zip(range(0, total_cam_num), device_name):
    pipeline[i] = rs.pipeline()
    config[i] = rs.config()
    config[i].enable_device(name)
    config[i].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
    config[i].enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)


# Start streaming
sensor = [None]*total_cam_num
cfg = [None]*total_cam_num

# Device_name[0] will be master
master_or_slave = 1
for i in range(0, total_cam_num):
    sensor[i] = ctx.devices[device_idx[i]].query_sensors()[0]
    if i == 0:
        sensor[i].set_option(rs.option.inter_cam_sync_mode, master_or_slave)
        master_or_slave = 2
    else:
        sensor[i].set_option(rs.option.inter_cam_sync_mode, master_or_slave)

    cfg[i] = pipeline[i].start(config[i])


count = 0
frames = [None]*total_cam_num
depth_frame = [None]*total_cam_num	
color_frame = [None]*total_cam_num
depth_image = [None]*total_cam_num
color_image = [None]*total_cam_num
depth_colormap = [None]*total_cam_num
images = [None]*total_cam_num

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        for i in range(0, total_cam_num):
            frames[i] = pipeline[i].wait_for_frames()
            align_frame = rs.align(rs.stream.color).process(frames[i])
            depth_frame[i] = align_frame.get_depth_frame()
            color_frame[i] = align_frame.get_color_frame()
            if not depth_frame[i] or not color_frame[i]:
                continue


        # Get timestamp
        timestamp = []

        for i in range(0, total_cam_num):
            
            timestamp.append(frames[i].get_frame_metadata(rs.frame_metadata_value.backend_timestamp))
            
            f.write(str(timestamp[i]) + '           ')
        f.write('\n')

        #f.write(str(frames1.get_frame_metadata(rs.frame_metadata_value.backend_timestamp)) + '           ' + str(frames2.get_frame_metadata(rs.frame_metadata_value.backend_timestamp)) + '           '+ str(frames3.get_frame_metadata(rs.frame_metadata_value.backend_timestamp)) + '           \n')
 
        # Convert images to numpy arrays
        for i in range(0, total_cam_num):
            depth_image[i] = np.asanyarray(depth_frame[i].get_data())
            color_image[i] = np.asanyarray(color_frame[i].get_data())
            depth_colormap[i] = cv2.applyColorMap(cv2.convertScaleAbs(depth_image[i], alpha=0.03), cv2.COLORMAP_JET)


        # Using cv2.imwrite() method
        # Saving the image
        # Change the route !
        def save_image_color(cam_num, count):
            dir_c = r'/home/d435/Documents/RGBimage' + str(cam_num) + '/RGBimage_'+ str(timestamp[cam_num]) +'.png'
            cv2.imwrite(dir_c, color_image[cam_num])
                
        def save_image_depth(cam_num, count):
            dir_d = r'/home/d435/Documents/Depthimage' + str(cam_num) + '/Depthimage_'+ str(timestamp[cam_num]) +'.png'
            cv2.imwrite(dir_d, depth_colormap[cam_num])
            
        threads = []
        count += 1
        for cam_num in range(0,total_cam_num):
            threads.append(threading.Thread(target = save_image_color, args = (cam_num, count))) # color
            threads.append(threading.Thread(target = save_image_depth, args = (cam_num, count))) # depth

        for i in range(total_cam_num*2):
            threads[i].start() 
  
        for i in range(total_cam_num*2):
            threads[i].join()
 
 

finally:
 
    # Stop streaming
    for i in range(0, total_cam_num):
        pipeline[i].stop()
