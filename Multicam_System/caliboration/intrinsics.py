# intrinsics.py
import pyrealsense2 as rs
#device_name = ['745612070185', '819112071065', '745212070452']
serial = '745612070185' # <-- change this!
w = 640
h = 480
cfg = rs.config()
cfg.enable_device(serial)
cfg.enable_stream(rs.stream.depth, w, h, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, w, h, rs.format.rgb8, 30)
pipe = rs.pipeline()
selection = pipe.start(cfg)
depth_stream = selection.get_stream(rs.stream.depth).as_video_stream_profile()
color_stream = selection.get_stream(rs.stream.color).as_video_stream_profile()
id = depth_stream.get_intrinsics()
ic = color_stream.get_intrinsics()
e = depth_stream.get_extrinsics_to(color_stream)
print("{:s}".format(serial))
print("depth:")
print(" intrinsics:", id)
print("color")
print(" intrinsics:", ic)
print("extrinsics (depth to color):")
print(" rotation:", e.rotation)
print(" translation:", e.translation)
print("")
