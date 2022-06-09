import pyrealsense2 as rs
import numpy as np
import cv2
import os
import shutil
import threading
import time
import os.path
from os import path
from datetime import datetime, timedelta
os.environ['TZ'] = 'right/UTC' # TAI scale with 1970-01-01 00:00:10 (TAI) epoch
time.tzset() # Unix
#import ntplib


total_cam_num = 3       # <-- Change This !!!

path = 'serial.txt'
f = open(path, 'w')
for i in range(total_cam_num):
    f.write('cam'+ str(i) + '                    ')
f.write('\n')

device_name = ['745612070185', '819112071065', '745212070452']      # <-- Change This !!!
device_idx = [0]*total_cam_num

ctx = rs.context()

'''device_idx1 = 0
device_name1 = "745612070185"
device_idx2 = 0
device_name2 = "819112071065"
device_idx3 = 0
device_name3 = "745212070452"'''

'''for i, j in zip(range(len(ctx.devices)), range(0, total_cam_num)):
    sn = ctx.devices[i].get_info(rs.camera_info.serial_number)
    #print(sn)
    if sn == device_name[j]:
        device_idx[i] = i'''

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

'''shutil.rmtree('RGBimage1')
shutil.rmtree('RGBimage2')
shutil.rmtree('RGBimage3')
shutil.rmtree('Depthimage1')
shutil.rmtree('Depthimage2')
shutil.rmtree('Depthimage3')

os.mkdir('RGBimage1')
os.mkdir('RGBimage2')
os.mkdir('RGBimage3')
os.mkdir('Depthimage1')
os.mkdir('Depthimage2')
os.mkdir('Depthimage3')'''
 
# Configure depth and color streams
pipeline = [None]*total_cam_num
config = [None]*total_cam_num
for i, name in zip(range(0, total_cam_num), device_name):
    pipeline[i] = rs.pipeline()
    config[i] = rs.config()
    config[i].enable_device(name)
    config[i].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
    config[i].enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)



'''pipeline1 = rs.pipeline()
config1 = rs.config()
config1.enable_device('745612070185')
config1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config1.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)


pipeline2 = rs.pipeline()
config2 = rs.config()
config2.enable_device('819112071065')
config2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config2.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)

pipeline3 = rs.pipeline()
config3 = rs.config()
config3.enable_device('745212070452')
config3.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
config3.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)'''

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
    depth_scale = 1/cfg[i].get_device().first_depth_sensor().get_depth_scale()
    print(f'depth scale {i} = {depth_scale}')

'''sensor1 = ctx.devices[device_idx1].query_sensors()[0]
sensor1.set_option(rs.option.inter_cam_sync_mode, 1)

sensor2 = ctx.devices[device_idx2].query_sensors()[0]
sensor2.set_option(rs.option.inter_cam_sync_mode, 2)

sensor3 = ctx.devices[device_idx3].query_sensors()[0]
sensor3.set_option(rs.option.inter_cam_sync_mode, 2)

cfg1 = pipeline1.start(config1)
cfg2 = pipeline2.start(config2)
cfg3 = pipeline3.start(config3)'''

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

        '''frames1 = pipeline1.wait_for_frames()
        depth_frame1 = frames1.get_depth_frame()
        color_frame1 = frames1.get_color_frame()
        if not depth_frame1 or not color_frame1:
            continue
           
        frames2 = pipeline2.wait_for_frames()
        depth_frame2 = frames2.get_depth_frame()
        color_frame2 = frames2.get_color_frame()
        if not depth_frame2 or not color_frame2:
            continue

        frames3 = pipeline3.wait_for_frames()
        depth_frame3 = frames3.get_depth_frame()
        color_frame3 = frames3.get_color_frame()
        if not depth_frame3 or not color_frame3:
            continue'''

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


        '''depth_image1 = np.asanyarray(depth_frame1.get_data())
        color_image1 = np.asanyarray(color_frame1.get_data())
        
        depth_image2 = np.asanyarray(depth_frame2.get_data())
        color_image2 = np.asanyarray(color_frame2.get_data())
 	
        depth_image3 = np.asanyarray(depth_frame3.get_data())
        color_image3 = np.asanyarray(color_frame3.get_data())
 
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image1, alpha=0.03), cv2.COLORMAP_JET)
       
        depth_colormap2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image2, alpha=0.03), cv2.COLORMAP_JET)
       
        depth_colormap3 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image3, alpha=0.03), cv2.COLORMAP_JET)'''

        # Stack both images horizontally
        
        #images0 = np.hstack((color_image[0], depth_colormap[0]))
       
        #images1 = np.hstack((color_image[1], depth_colormap[1]))
        
        #images3 = np.hstack((color_image3, depth_colormap3))
	

        # Show images
        #cv2.namedWindow('RealSense0', cv2.WINDOW_AUTOSIZE)
        #cv2.namedWindow('RealSense1', cv2.WINDOW_AUTOSIZE)
        #cv2.namedWindow('RealSense2', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('RealSense0', images0)
        #cv2.imshow('RealSense1', images1)
        #cv2.imshow('RealSense3', images3)
     

        # Filename
        

        '''directory1_1 = r'/home/chiu/Documents/RGBimage1'
        directory1_2 = r'/home/chiu/Documents/Depthimage1'

        filename1_1 = 'RGBimage'+ str(count) +'.png'
        filename1_2 = 'Dimage'+ str(count) +'.png'
        
        directory2_1 = r'/home/chiu/Documents/RGBimage2'
        directory2_2 = r'/home/chiu/Documents/Depthimage2'

        filename2_1 = 'RGBimage'+ str(count) +'.png'
        filename2_2 = 'Dimage'+ str(count) +'.png'
  
        directory3_1 = r'/home/chiu/Documents/RGBimage3'
        directory3_2 = r'/home/chiu/Documents/Depthimage3'

        filename3_1 = 'RGBimage'+ str(count) +'.png'
        filename3_2 = 'Dimage'+ str(count) +'.png'
        '''

        # Using cv2.imwrite() method
        # Saving the image
        # Change the route !
        def save_image_color(cam_num, count):
            dir_c = r'/home/d435/Documents/RGBimage' + str(cam_num) + '/RGBimage_'+ str(timestamp[cam_num]) +'.png'
            cv2.imwrite(dir_c, color_image[cam_num])
        '''        
        def save_image_depth(cam_num, count):
            dir_d = r'/home/d435/Documents/Depthimage' + str(cam_num) + '/Depthimage_'+ str(timestamp[cam_num]) +'.png'
            cv2.imwrite(dir_d, depth_colormap[cam_num])
        '''
        def save_image_depth(cam_num,count):
            dir_d = r'/home/d435/Documents/Depthimage' + str(cam_num) + '/Depthimage_'+ str(timestamp[cam_num]) +'.npy'
            with open(dir_d, 'wb') as f:
                np.save(f, depth_image[cam_num])
            
        threads = []
        count += 1
        for cam_num in range(0,total_cam_num):
            threads.append(threading.Thread(target = save_image_color, args = (cam_num, count))) # color
            threads.append(threading.Thread(target = save_image_depth, args = (cam_num, count))) # depth

        for i in range(total_cam_num*2):
            threads[i].start() 
  
        for i in range(total_cam_num*2):
            threads[i].join()

        '''os.chdir(directory1_1)
        cv2.imwrite(filename1_1, color_image1)
        os.chdir(directory1_2)
        cv2.imwrite(filename1_2, depth_colormap1)
 
        
        os.chdir(directory2_1)
        cv2.imwrite(filename2_1, color_image2)
        os.chdir(directory2_2)
        cv2.imwrite(filename2_2, depth_colormap2)
       
        os.chdir(directory3_1)
        cv2.imwrite(filename3_1, color_image3)
        os.chdir(directory3_2)
        cv2.imwrite(filename3_2, depth_colormap3)'''

        #key = cv2.waitKey(1)
        #Press esc or 'q' to close the image window
        #if key & 0xFF == ord('q') or key == 27:
            #cv2.destroyAllWindows()
            #break
 
 

finally:
 
    # Stop streaming
    for i in range(0, total_cam_num):
        pipeline[i].stop()
    #pipeline1.stop()
    #pipeline2.stop()
    #pipeline3.stop()
