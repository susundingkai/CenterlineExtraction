from utils import CenterlineExtraction
import cv2
if __name__ == '__main__':
    img = cv2.imread("4.png", -1)
    res=CenterlineExtraction(img, 0, 5)
    print(res)