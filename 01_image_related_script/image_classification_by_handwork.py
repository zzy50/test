from cgitb import text
import cv2 
from glob import glob 
import os 
import shutil 
import numpy as np 

# path = 현재 검수할 폴더명을 써주세요.
path = "./car/"

save_path = "./"


car_type = ['car', 'bus', 'truck_s_a', "truck_s_b", "truck_m_3W", "truck_m_4W", "truck_m_5W", "truck_4W_ST", "truck_4W_FT", "truck_5W_ST", "truck_5W_FT", "truck_6W_ST", 'etc']

imgs = glob(os.path.join(path, "*.jpg"))
window_name = "qwe"


# cv2.imshow("asd", text_img)
for img_path in imgs:
    text_img = np.zeros((1080,1920,3), dtype=np.uint8)
    s1 = f"{car_type}"
    s2 = f"      0 {' ' * len(car_type[0])}   1{' ' * len(car_type[1])}    2{' ' * len(car_type[2])}   " \
     f"3{' ' * len(car_type[3])}    4 {' ' * len(car_type[4])}   5 {' ' * len(car_type[5])}   " \
     f"6{' ' * len(car_type[6])}   7 {' ' * len(car_type[7])}   8 {' ' * len(car_type[8])}  9 {' ' * len(car_type[9])}  " \
     f"/{' ' * len(car_type[10])}    * {' ' * len(car_type[11])} -{' ' * len(car_type[12])}" \

    s3 = f"current path : {path}    End Button : ESC    Next Image Button : ->"
    cv2.putText(text_img, s1,(200,250),1,1,(255,255,255),1)
    cv2.putText(text_img, s2,(200,230),1,1,(255,255,255),1)
    cv2.putText(text_img, s3,(200,190),1,2,(255,255,255),1)
    img = cv2.imread(img_path)
    img_name = os.path.basename(img_path)
    h,w,c =  img.shape

    text_height, text_width, _ = text_img.shape
    start_y = int((text_height - h) / 2)
    start_x = int((text_width - w) / 2)
    end_y = start_y + h
    end_x = start_x + w
    scale_factor = 2  # 크기를 키우기 위한 스케일 팩터
    resized_img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)
    resized_h, resized_w, _ = resized_img.shape
    text_img[start_y:start_y+resized_h, start_x:start_x+resized_w, :] = resized_img

    cv2.imshow(window_name,text_img)
    cv2.moveWindow(window_name,0,0)
    key = cv2.waitKey(0)
    if key == 27:  # 27은 'esc' 키의 아스키 코드 값입니다
        # 'esc' 키를 눌렀을 때 프로그램 종료
        cv2.destroyAllWindows()
        break
    elif key >= 48 and key <= 57:
        shutil.move(img_path, os.path.join(save_path, car_type[int(str(key))], img_name))
    elif key in [47, 42, 45]:
        if key == ord('/'):
            shutil.move(img_path, os.path.join(save_path, car_type[10], img_name))
        elif key == ord('*'):
            shutil.move(img_path, os.path.join(save_path, car_type[11], img_name))
        elif key == ord('-'):
            shutil.move(img_path, os.path.join(save_path, car_type[12], img_name))
    else:
        pass