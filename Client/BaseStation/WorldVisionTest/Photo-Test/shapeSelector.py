from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2

def printPosition(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)

frame = cv2.imread('Frames/Picture 7.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',printPosition)

while(True):
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

