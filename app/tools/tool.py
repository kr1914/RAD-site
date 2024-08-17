import cv2 as cv
import numpy as np

# 바이트 데이터를 NumPy 배열로 변환하는 함수
def bytes_to_image(byte_data):
    # NumPy 배열로 변환
    np_array = np.frombuffer(byte_data, np.uint8)
    # OpenCV를 사용하여 이미지를 디코딩
    img = cv.imdecode(np_array, cv.IMREAD_COLOR)
    return img