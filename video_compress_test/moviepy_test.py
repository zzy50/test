import cv2
import datetime
from moviepy.editor import *
 
now = datetime.datetime.now()
cap = cv2.VideoCapture('video/input/2023-01-05 07_29_47.861.mp4')
 
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
file_name = 'video/output/output_'+ now.strftime('%Y.%m.%d-%H_%M_%S') +'.mp4'
vid_out = cv2.VideoWriter(file_name, fourcc, fps, (w, h))

frame_cnt = 0

while cap.isOpened():
    run, frame = cap.read()
    if not run:
        print("fail to open video")
        break
    img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
    # cv2.imshow('video', frame)    
    vid_out.write(img)
    
    if cv2.waitKey(15) & 0xFF == ord('q'):
        break
 

 
# print('fps = ' , fps)
vid_out.release()
cap.release()
cv2.destroyAllWindows()
 
video_clip = VideoFileClip(file_name)
video_clip.write_videofile('video/output/output_'+ now.strftime('%Y.%m.%d-%H_%M_%S') +'_moviepy.mp4')