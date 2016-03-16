from Client.BaseStation.WorldVision.worldImage import WorldImage
from Client.BaseStation.WorldVision.worldVision import worldVision
import cv2

class ResultChecker:

    def __init__(self, pictureNumber):
        resultFileName = 'Results/Picture ' + str(pictureNumber) + '.txt'
        frameFileName = 'Frames/Picture ' + str(pictureNumber) + '.jpg'
        image = cv2.imread(frameFileName)
        self.geometricalImage = WorldImage(image)
        self.geometricalImage.setMap(image)
        resultFile = open(resultFileName, 'r')
        centerOfMassLine = resultFile.readline()
        centerOfMassLine = centerOfMassLine[13:]
        self.centersOfMass = []
        xPosition = ""
        yPosition = ""
        isFirstNumber = True

        for character in centerOfMassLine:
            if character != '(' and character != ',' and character != ')':
                if isFirstNumber:
                    xPosition += character
                else:
                    yPosition += character

            if character == '(':
                isFirstNumber = True

            if character == ',':
                isFirstNumber = False

            if character == ')':
                self.centersOfMass.append((int(xPosition), int(yPosition)))
                xPosition = ""
                yPosition = ""

    def checkNumberOfShapesFound(self):
        shapeFound = 0
        for shape in self.geometricalImage.getMap().getShapesList():
            shapeCenterOfMassX, shapeCenterOfMassY = shape.findCenterOfMass()
            for centerOfMass in self.centersOfMass:
                if abs(shapeCenterOfMassX - centerOfMass[0]) < 10 and abs(shapeCenterOfMassY - centerOfMass[1]) < 10:
                    shapeFound += 1
        print("Number of shapes found : " + str(shapeFound))
        print("Number of shapes present : " + str(len(self.centersOfMass)))

    def checkIfLimitFound(self):
        if self.geometricalImage.getMap().getMapLimit().getArea() < 1:
            print("Limit not found")

    def checkIfRobotFound(self):
        if self.geometricalImage.getMap().robot.getArea() < 1:
            print("Robot not found")



