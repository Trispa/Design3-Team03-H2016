from Client.BaseStation.WorldVision import worldVision as WV
import cv2

if __name__ == '__main__':
    myWorldVision = WV.WorldVision(cv2.imread("Images\easyPicture.png", 1))
    myWorldVision.printDrawnWorld()