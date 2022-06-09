#arrange.py
import os

total_cam_num = 2               # <-- Change This !!!
timestamp_diff_threshold = 5    # <-- You can change this as you want
timestamps = []

def align(filePath):
    for filename in os.listdir(filePath):
        timestamp = filename[9:-4]  # Slave
        flag = 1
        for i in range(len(timestamps)):
            if(abs(int(timestamp)-int(timestamps[i][0])) < timestamp_diff_threshold):
                timestamps[i][1]+=1
                timestamps[i].append((filePath,timestamp))
                flag = 0
                break
        if(flag):
            os.remove(filePath+'RGBimage_'+timestamp+'.png')
            DepthPath = 'Depthimage'+filePath[8:]
            os.remove(DepthPath+'Depthimage_'+timestamp+'.png')

def delete():
    for i in range(len(timestamps)):
        if(int(timestamps[i][1])<2):
            os.remove('RGBimage0/RGBimage_'+timestamps[i][0]+'.png')
            os.remove('Depthimage0/Depthimage_'+timestamps[i][0]+'.png')
            idx = 2
            while(idx<len(timestamps[i])):
                os.remove(timestamps[i][idx][0]+'RGBimage_'+timestamps[i][idx][1]+'.png')
                DepthPath = 'Depthimage'+timestamps[i][idx][0][8:]
                os.remove(DepthPath+'Depthimage_'+timestamps[i][idx][1]+'.png')
                idx+= 1


# Build reference from master
filePath  = 'RGBimage0/'    # Master

for filename in os.listdir(filePath):
    timeStamp = filename[9:-4]
    #print(timeStamp)
    timestamps.append([timeStamp,0])

for i in range(total_cam_num):
    idx = i+1
    align('RGBimage'+str(idx)+'/')
delete()
