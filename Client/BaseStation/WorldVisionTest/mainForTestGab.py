from Client.BaseStation.WorldVision.worldImage import WorldImage
import os
import base64
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2


if __name__ == '__main__':

    # pictureSources = ['Photos/3105/table 5/Jour/rideau ferme/Picture 1.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ferme/Picture 2.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ferme/Picture 3.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ouvert/Picture 22.jpg',
    #                   'Photos/3105/table 5/Jour/rideau ouvert/Picture 23.jpg',
    #                     'Photos/3105/table 5/Jour/rideau ouvert/Picture 24.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ferme/Picture 18.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ferme/Picture 19.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ferme/Picture 20.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ouvert/Picture 20.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ouvert/Picture 21.jpg',
    #                     'Photos/3105/table 6/Jour/rideau ouvert/Picture 22.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ferme/Picture 12.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ferme/Picture 13.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ferme/Picture 14.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ouvert/Picture 10.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ouvert/Picture 11.jpg',
    #                     'Photos/3109/Table1/Jour/rideau ouvert/Picture 12.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ferme/Picture 14.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ferme/Picture 15.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ferme/Picture 16.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ouvert/Picture 8.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ouvert/Picture 9.jpg',
    #                     'Photos/3109/table 2/Jour/rideau ouvert/Picture 10.jpg',
    #                     'Photos/3109/table3/Jour/rideau ferme/Picture 16.jpg',
    #                     'Photos/3109/table3/Jour/rideau ferme/Picture 17.jpg',
    #                     'Photos/3109/table3/Jour/rideau ferme/Picture 18.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 4.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 5.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 6.jpg',
    #                     'Photos/3109/table3/Jour/rideau ouvert/Picture 7.jpg']
    #camera = cv2.VideoCapture(1)
    #camera.set(3, 720)
    #camera.set(4, 720)
    #ret, frame = camera.read()

    #frame = cv2.imread('Photos/3105/table 5/jour/rideau ouvert/Picture 22.jpg')
    #frame = cv2.imread('Images/Test6.jpg')
    #geometricalImage = WorldImage(frame)
    #worldVision = worldVision()
    phoposToVerified = ['177', '176', '175', '173','171',
                        '164', '160', '145', '142', '141',
                        '130', '118', '117','115', '114',
                        '108', '105', '104', '103', '99',
                        '92', '86', '84', '82', '79', '70',
                        '69', '67', '64', '61', '59', '58',
                        '57', '56', '51', '49', '48', '43',
                        '41', '40', '39', '38', '34', '29',
                        '28', '23', '22', '17', '5', '4', '2']
    for photoNumber in phoposToVerified:
        frame = cv2.imread('Photo-Test/Frames/Picture ' + photoNumber + '.jpg')
        geometricalImage = WorldImage(frame)
        geometricalImage.setMap(frame)
        geometricalImage.addLabels(frame)
        worldImage = geometricalImage.drawMapOnImage(frame)
        #print(geometricalImage.getMap().robot.findCenterOfMass())
        cv2.imshow('Picture ' + photoNumber, worldImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

    cv2.waitKey(0)

    # while(True):
    #     #ret, frame = camera.read()
    #     #frame = cv2.imread('Photos/3105/table 5/Jour/rideau ferme/Picture 1.jpg')
    #
    #     geometricalImage = WorldImage(frame)
    #     geometricalImage.setMap(frame)
    #     geometricalImage.addLabels(frame)
    #     worldImage = geometricalImage.drawMapOnImage(frame)
    #     #print(geometricalImage.getMap().robot.findCenterOfMass())
    #     cv2.imshow("Monde", worldImage)
    #     # geometricalImage = WorldImage(frame)
    #     # geometricalImage.setMap()
    #     # geometricalImage.defineShapesColor()
    #     # geometricalImage.addLabels()
    #     # worldImage = geometricalImage.drawMapOnImage()
    #
    #     # geometricalImage = WorldImage(frame)
    #     # geometricalImage.setMap()
    #     # geometricalImage.addLabels()
    #     # worldImage = geometricalImage.drawMapOnImage()
    #
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #cap.release()


