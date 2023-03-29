import cv2
import numpy as np
# color 설정
blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)
white_color = (255, 255, 255)

line2_s = (1186, 340)
line2_e = (1568, 999)
line3_s = (1201, 336)
line3_e = (1595, 1002)
cp = (1345, 605)
pp = (1380, 622)

frame = np.zeros((1920, 1920, 3), np.uint8)
# frame.fill(255)
frame = cv2.line(frame, line2_s, line2_e, green_color, 1)
frame = cv2.line(frame, line3_s, line3_e, green_color, 1)
frame = cv2.line(frame, cp, cp, red_color, 5)
frame = cv2.line(frame, pp, pp, red_color, 5)

cv2.imshow("window", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

 
# # 모두 0으로 되어 있는 빈 Canvas(검정색)
# img = np.zeros((384, 384, 3), np.uint8)
# img = cv2.line(img, (10, 10), (350, 10), blue_color, 5)
# img = cv2.line(img, (10, 30), (350, 30), green_color, 5)
# img = cv2.line(img, (10, 50), (350, 50), red_color, 5)
# # line_4
# img = cv2.line(img, (10, 90), (350, 90), blue_color, 5, 4)
# # line_aa
# img = cv2.line(img, (10, 110), (350, 110), green_color, 5, cv2.LINE_AA)
# # shift 1
# img = cv2.line(img, (10, 130), (350, 130), red_color, 5, 4, 1)
# # 점
# img = cv2.line(img, (150, 150), (150, 150), red_color, 5)

# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()