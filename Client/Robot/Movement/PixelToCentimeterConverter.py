class PixelToCentimeterConverter:
    RATIO = (49/9.5) #5.1578

    def convertPixelToCentimeter(self, pointToBeConverted):
        pointConverted = (float(pointToBeConverted[0])/self.RATIO, float(pointToBeConverted[1])/self.RATIO)
        return pointConverted
