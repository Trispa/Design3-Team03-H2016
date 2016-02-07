import Wheel

class Mouvement:
    VITESSE = 20 #constante vitesse scalaire

    def __init__(self, positionRobotX, positionRobotY):
        #envoyer une valeur pour identifier le channel de chaque roue
        self.horizontalWheelFront = Wheel(1)
        self.horizontalWheelBack = Wheel(2)
        self.verticalWheelLeft = Wheel(3)
        self.verticalWheelRight = Wheel(4)

        self.isMoving = False
        self.positionWorldX = positionRobotX
        self.positionWorldY = positionRobotY

    def moveTo(self, pointToMoveTo):
        deplacementX = pointToMoveTo.__getitem__(0) - self.positionWorldX
        deplacementY = pointToMoveTo.__getitem__(1) - self.positionWorldY
        deplacementTotal = float(abs(deplacementX) +abs(deplacementY))

        vitesseX = deplacementX/deplacementTotal
        vitesseY = deplacementY/deplacementTotal

        self.horizontalWheelFront.setVitesse(vitesseX)
        self.horizontalWheelBack.setVitesse(vitesseX)
        self.verticalWheelLeft.setVitesse(vitesseY)
        self.verticalWheelRight.setVitesse(vitesseY)


    def setPosition(self, positionX, positionY):
        self.positionWorldX = positionX
        self.positionWorldY = positionY

