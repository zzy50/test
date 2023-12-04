import cv2
import subprocess
import re

# FILE_PATH = "C:/Users/ZZY/Desktop/한국옥외광고센터_행주대교_1번카메라/2023-10-26 06_59_31.446.mp4"
# FILE_PATH = "C:/Users/ZZY/Desktop/한국옥외광고센터_행주대교_1번카메라/2023-10-26 10_21_44.896.mp4"
FILE_PATH = "C:/Users/ZZY/Desktop/한국옥외광고센터_행주대교_1번카메라/2023-10-26 10_23_44.989.mp4"

cap = cv2.VideoCapture(FILE_PATH)
total_frame_num_meta = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(f"meta frame num: {total_frame_num_meta}")

cmd = [
    "ffprobe",
    "-v", "error",
    "-select_streams", "v:0",
    "-show_entries", "stream=avg_frame_rate",
    "-of", "default=noprint_wrappers=1:nokey=1",
    FILE_PATH
]

process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = process.stdout.strip()

matches = re.search(r'(\d+)/(\d+)', output)
if matches:
    num, den = map(int, matches.groups())
    fps = num / den if den != 0 else num
    print(f"fps from ffprobe: {fps}")
else:
    print("Could not determine fps from ffprobe output.")

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1

cap.release()

print(f"real frame num: {count}")
