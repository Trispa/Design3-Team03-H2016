class ColorTarget():
    def __init__(self, target):
        if(target == "rouge"):
            self.target = "Red"
        elif(target == "bleu"):
            self.target = "Blue"
        elif(target == "jaune"):
            self.target = "Yellow"
        elif(target == "vert"):
            self.target = "Green"

    def getShape(self, obstacleList):
        obstacleTarget = None
        for obstacle in obstacleList:
            if obstacle.myColor.colorName == self.target:
                obstacleTarget = obstacle
        return obstacleTarget

class ShapeTarget():
    def __init__(self, target):
        if(target == "pentagone"):
            self.target = "Pentagone"
        elif(target == "cercle"):
            self.target = "Circle"
        elif(target == "triangle"):
            self.target = "Triangle"
        elif(target == "rectangle"):
            self.target = "Square"

    def getShape(self, obstacleList):
        obstacleTarget = None
        for obstacle in obstacleList:
            if obstacle.geometricName == self.target:
                obstacleTarget = obstacle
        return obstacleTarget