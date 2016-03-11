from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2

def printPosition(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        resultFile = open(resultFileName, 'a')
        resultFile.write("("+str(x)+","+str(y)+")")
        resultFile.close()

pictureNumber = 13
resultFileName = 'Results/Picture ' + str(pictureNumber) + '.txt'
frameFileName = 'Frames/Picture ' + str(pictureNumber) + '.jpg'
resultFile = open(resultFileName, 'w')
resultFile.write("CenterOfMass:")
resultFile.close()
frame = cv2.imread(frameFileName)
cv2.namedWindow('image')
cv2.setMouseCallback('image',printPosition)


while(True):
    cv2.imshow('image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

