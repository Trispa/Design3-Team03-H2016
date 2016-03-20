class LineInterceptionCalculator:
    def findInterception(self, pointA1, pointA2, pointB1, pointB2):
        line1 = self.__line(pointA1, pointA2)
        line2 = self.__line(pointB1, pointB2)
        D  = (line1[0]*line2[1]) - (line1[1]*line2[0])
        Dx = (line1[2]*line2[1]) - (line1[1]*line2[2])
        Dy = (line1[0]*line2[2]) - (line1[2]*line2[0])
        if D != 0:
            x = Dx / D
            y = Dy / D
            return (x,y)
        else:
            return False


    def __line(self, point1, point2):
        CoefA = (point1[1] - point2[1])
        CoefB = (point2[0] - point1[0])
        CoefC = (point1[0] * point2[1] - point2[0] * point1[1])
        return CoefA, CoefB, -CoefC