from wurlitzer import pipes
from pathlib import Path
import cv2

# 현재 스크립트의 디렉토리 경로를 얻음
script_dir = Path(__file__).parent

# 비디오 파일의 전체 경로를 구성
PATH1 = script_dir / "2023-09-01 03_33_35.273.mp4"
PATH2 = script_dir / "2023-09-01 03_35_36.265.mp4"
PATH3 = script_dir / "2023-09-01 03_37_36.358.mp4"

# OpenCV를 사용하여 비디오 캡처 시작
cap = cv2.VideoCapture(str(PATH2))
window_name = "frame"


# wurlitzer를 사용하여 C++ 레이어의 출력을 캡처
with pipes() as (out, err):
    cap = cv2.VideoCapture(str(PATH2))
    window_name = "frame"

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(window_name, frame)

        wait_key = cv2.waitKey(1)
        if wait_key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# C++ 레벨의 에러 메시지 읽기
c_error = err.read()
if "moov atom not found" in c_error:
    print("Error: moov atom not found in the video file.")
    # 필요한 오류 처리 로직을 여기에 추가하세요.