import cv2
import datetime
from moviepy.editor import *
from pathlib import Path
from tqdm import tqdm

INPUT_ROOT = "C:/Users/ZZY/Desktop/0_cityeyelab/data/analysis_video/compress_sample/input"
OUTPUT_ROOT = "C:/Users/ZZY/Desktop/0_cityeyelab/data/analysis_video/compress_sample/output"
VIDEO_NAME = "2022-09-22 06_59_21.155.mp4"
input_path = Path(INPUT_ROOT) / VIDEO_NAME
output_root_path = Path(OUTPUT_ROOT)
output_root_path.mkdir(parents=True, exist_ok=True)

now_str = datetime.datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
cap = cv2.VideoCapture(str(input_path))
 
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'H265')
output_file_name_opencv = output_root_path / f"output_{now_str}_opencv.mp4"
vid_out = cv2.VideoWriter(str(output_file_name_opencv), fourcc, fps, (w, h))

frame_cnt = 0

pbar = tqdm(total = cap.get(cv2.CAP_PROP_FRAME_COUNT))
while cap.isOpened():
    run, frame = cap.read()
    if not run:
        break
    img = cv2.cvtColor(frame, cv2.IMREAD_COLOR)
    # cv2.imshow('video', frame)    
    vid_out.write(img)
    pbar.update(1)
    if cv2.waitKey(15) & 0xFF == ord('q'):
        break
 

 
# print('fps = ' , fps)
vid_out.release()
cap.release()
cv2.destroyAllWindows()
 
# output_file_name_moviepy = output_file_name_opencv.with_name(f"output_{now_str}_moviepy.mp4")
# video_clip = VideoFileClip(str(output_file_name_opencv))
# video_clip.write_videofile(str(output_file_name_moviepy))