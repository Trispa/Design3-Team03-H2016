import numpy as np

import ReferentialConverter


class SpeedCalculator:
    VITESSE = 20 #constante vitesse scalaire

    def __init__(self, positionRobotX, positionRobotY, orientation):
        #envoyer une valeur pour identifier le channel de chaque roue
        #self.horizontalWheelFront = Wheel(1)
        #self.horizontalWheelBack = Wheel(2)
        #self.verticalWheelLeft = Wheel(3)
        #self.verticalWheelRight = Wheel(4)
        self.referentialConverter = ReferentialConverter(positionRobotX, positionRobotY, orientation)
        self.isMoving = False
        self.orientation = (float(orientation%360))/180
        self.positionWorldX = positionRobotX
        self.positionWorldY = positionRobotY

    def moveTo(self, pointToMoveTo):
        deplacementXWorld = pointToMoveTo.__getitem__(0) - self.positionWorldX
        deplacementYWorld = pointToMoveTo.__getitem__(1) - self.positionWorldY

        print self.orientation,np.cos(self.orientation*np.pi),-np.sin(self.orientation*np.pi)
        matrixDeplacementWorld = np.array([[deplacementXWorld], [deplacementYWorld]])
        matrixRotation = np.array( [[np.cos(self.orientation*np.pi), -np.sin(self.orientation*np.pi)],
                                    [np.sin(self.orientation*np.pi), np.cos(self.orientation*np.pi)]] )
        matrixDeplacementRobot = matrixRotation.dot(matrixDeplacementWorld)

        deplacementXRobot = matrixDeplacementRobot.__getitem__(0)
        deplacementYRobot = matrixDeplacementRobot.__getitem__(1)
        deplacementTotal = deplacementXRobot + deplacementYRobot
        vitesseX = deplacementXRobot/deplacementTotal
        vitesseY = deplacementYRobot/deplacementTotal
        print deplacementXWorld, deplacementYWorld
        print deplacementXRobot, deplacementYRobot




        #self.horizontalWheelFront.setVitesse(vitesseX)
        #self.horizontalWheelBack.setVitesse(vitesseX)
        #self.verticalWheelLeft.setVitesse(vitesseY)
        #self.verticalWheelRight.setVitesse(vitesseY)


    def setPosition(self, positionX, positionY):
        self.positionWorldX = positionX
        self.positionWorldY = positionY

mouv = SpeedCalculator(0, 0, 45)
mouv.moveTo((10,0))