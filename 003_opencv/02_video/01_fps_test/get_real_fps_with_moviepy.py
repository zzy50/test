import cv2
from moviepy.editor import VideoFileClip

# FILE_PATH = "C:/Users/ZZY/Desktop/한국옥외광고센터_행주대교_1번카메라/2023-10-26 06_59_31.446.mp4"
# FILE_PATH = "C:/Users/ZZY/Desktop/한국옥외광고센터_행주대교_1번카메라/2023-10-26 10_21_44.896.mp4"
FILE_PATH = "C:/Users/ZZY/Desktop/한국옥외광고센터_행주대교_1번카메라/2023-10-26 10_23_44.989.mp4"

cap = cv2.VideoCapture(FILE_PATH)
fps_cv2 = cap.get(cv2.CAP_PROP_FPS)

clip = VideoFileClip(FILE_PATH, fps_source="fps")
fps_moviepy = clip.fps

print(fps_cv2) # result: 30
print(fps_moviepy) # result: 15.01

# total_frame_num_meta = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# duration = clip.duration

# fps = total_frame_num_meta // duration

# print(f"meta frame num: {total_frame_num_meta}")
# print(f"duration: {duration}")
# print(f"fps: {fps}")

cap.release()
clip.close()