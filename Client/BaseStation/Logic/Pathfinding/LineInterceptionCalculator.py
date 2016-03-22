class LineInterceptionCalculator:
    def findInterception(self, pointA1, pointA2, pointB1, pointB2):
        line1 = self.__line(pointA1, pointA2)
        line2 = self.__line(pointB1, pointB2)
        determinant  = (line1[0]*line2[1]) - (line1[1]*line2[0])
        determinantX = (line1[2]*line2[1]) - (line1[1]*line2[2])
        determinantY = (line1[0]*line2[2]) - (line1[2]*line2[0])
        if determinant != 0:
            intersectionX = determinantX / determinant
            intersectionY = determinantY / determinant
            return (intersectionX,intersectionY)
        else:
            return False


    def __line(self, point1, point2):
        CoefficientA = (point1[1] - point2[1])
        CoefficientB = (point2[0] - point1[0])
        CoefficientC = (point1[0] * point2[1] - point2[0] * point1[1])
        return CoefficientA, CoefficientB, -CoefficientC