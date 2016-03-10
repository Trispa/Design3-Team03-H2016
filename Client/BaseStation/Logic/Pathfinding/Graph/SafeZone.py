class SafeZone:
    def __init__(self, cornerTopLeft, cornerTopRight, cornerBottomLeft):
        self.cornerTopLeft = cornerTopLeft
        self.cornerTopRight = cornerTopRight
        self.cornerBottomLeft = cornerBottomLeft


    def getCenterOfSafeZone(self):

        centerX = (self.cornerTopLeft.__getitem__(0) + self.cornerTopRight.__getitem__(0)) / 2
        centerY = (self.cornerTopLeft.__getitem__(1) + self.cornerBottomLeft.__getitem__(1)) / 2

        return centerX, centerY