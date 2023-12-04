import cv2
import numpy as np
from pathlib import Path

IMAGE_PATH = "C:/Users/ZZY/Desktop/sample.png"
POINTS = [[[0, 0], [0.21, 0], [0.62, 1], [0, 1]]]


def draw_line(image_path, points):
    # 이미지 불러오기
    image = cv2.imread(image_path)
    image_width = image.shape[1]
    image_height = image.shape[0]

    # points 값 스케일링
    points = np.array(points)
    points[...,0] = (points[...,0] * image_width).astype(int)
    points[...,1] = (points[...,1] * image_height).astype(int)
    points = np.int32([points])

    # 직선 기준 왼쪽 영역 검은색으로 채우기
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, points, (255, 255, 255))
    # fillpoly의 pts(points)파라미터는 3차원 배열이어야 함.
    #   첫번째 차원의 size: 다각형 수
    #   두번째 차원의 size: 각 다각형의 꼭지점 수
    #   세번째 차원의 값: 각 꼭지점의 x,y좌표
    image[mask == 255] = 0

    return image


def main():
    if Path(IMAGE_PATH).exists():
        image = draw_line(IMAGE_PATH, POINTS)
        cv2.imshow("image", image)
        cv2.waitKey(0)
    else:
        raise FileNotFoundError(f"{IMAGE_PATH} is not exist!")
    

if __name__ == "__main__":
    main()