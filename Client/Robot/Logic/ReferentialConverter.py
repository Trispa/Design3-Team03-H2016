import numpy

class ReferentialConverter:

    def __init__(self, positionRobot, orientation):
        self.orientation = (float("{0:.3f}".format(float(orientation%360)/180)))
        self.positionRobotInWorldX = positionRobot.__getitem__(0)
        self.positionRobotInWorldY = positionRobot.__getitem__(1)
        self.rotationMatrix = numpy.array([[numpy.cos(self.orientation*numpy.pi), -numpy.sin(self.orientation*numpy.pi)],
                                           [numpy.sin(self.orientation*numpy.pi), numpy.cos(self.orientation*numpy.pi)]])


    def setPosition(self, positionRobot, orientation):
        self.orientation = (float(orientation%360))/180
        self.positionRobotInWorldX = positionRobot.__getitem__(0)
        self.positionRobotInWorldY = positionRobot.__getitem__(1)
        self.rotationMatrix = numpy.array( [[numpy.cos(self.orientation*numpy.pi), -numpy.sin(self.orientation*numpy.pi)],
                                            [numpy.sin(self.orientation*numpy.pi), numpy.cos(self.orientation*numpy.pi)]])


    def convertWorldToRobot(self, pointToBeConverted):
        deplacementXWorld = pointToBeConverted.__getitem__(0) - self.positionRobotInWorldX
        deplacementYWorld = pointToBeConverted.__getitem__(1) - self.positionRobotInWorldY
        deplacementWorldMatrix = numpy.array([[deplacementXWorld], [deplacementYWorld]])


        matrixDeplacementRobot = self.rotationMatrix.dot(deplacementWorldMatrix)
        matrixDeplacementRobot.__setitem__(0,float("{0:.3f}".format(float(matrixDeplacementRobot.__getitem__(0)))))
        matrixDeplacementRobot.__setitem__(1,float("{0:.3f}".format(float(matrixDeplacementRobot.__getitem__(1)))))
        return matrixDeplacementRobot