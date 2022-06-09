from scipy.spatial.transform import Rotation as Rot
import xml.etree.ElementTree as ET
import numpy as np
device_name = ['745612070185', '819112071065', '745212070452']      # <-- Change this!
for i in range(1, len(device_name)):
    file_name = device_name[0] + "-" + device_name[i] + ".xml"
    tree = ET.parse(file_name)    
    root = tree.getroot()
    #root = ET.fromstring(country_data_as_string)
    matrix = root[1][1][0].text
    matrix = matrix.replace('[', '')
    matrix = matrix.replace(']', '')
    matrix = matrix.replace(';', ',')
    matrix = matrix.split(',')
    #print (matrix)
    matrix = np.asarray(matrix)
    #print(np.shape(matrix))

    Traslation_Rotation = []
    for j in range(len(matrix)):
        Traslation_Rotation.append(float(matrix[j]))
    Traslation_Rotation = np.reshape(Traslation_Rotation, (3,4))
    #print(T12)
    t = Traslation_Rotation[:3, 3]
    R = Traslation_Rotation[:3, :3]
    #print(t)
    #print(R)
    e = Rot.from_dcm(R).as_euler('ZYX').astype(np.float32)
    print("--------------------------")
    print(device_name[0] + "-" + device_name[i])
    print('Translation:')
    print(t)
    print('Rotation:')
    print(R)
    print('tf: {:10.7f} {:10.7f} {:10.7f} {:10.7f} {:10.7f} {:10.7f}'.format(*t, *e))
