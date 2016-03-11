import numpy as np
class Path:

    def __init__(self):
        self.nodeList = []
        self.totalDistance = 0

    def append(self, point):
        if self.nodeList.__len__() > 1:
            lastNode = self.nodeList[self.nodeList.__len__() - 1]
            distance = np.sqrt(np.power((lastNode.positionX - point[0]),2)+np.power((lastNode.positionY - point[1]),2))
            self.totalDistance += distance
            self.nodeList.append(point)
        else :
            self.nodeList.append(point)

    def clone(self):
        newPath = Path()
        for compteur in range(0, self.nodeList.__len__()):
            newPath.append(self.nodeList[compteur])
        newPath.totalDistance = self.totalDistance
        return newPath

    def contains(self, node):
        return self.nodeList.__contains__(node)

    def isOpen(self):
        isOpen = False
        lastNode = self.nodeList[self.nodeList.__len__() - 1]
        for compteur in range(0, lastNode.connectedNodes.__len__()):
            if isOpen == False:
                connectedNode = lastNode.connectedNodes[compteur]
                if self.contains(connectedNode) == False:
                    isOpen = True
        return isOpen

    def __len__(self):
        return self.nodeList.__len__()

    def __getitem__(self, item):
        return self.nodeList[item]