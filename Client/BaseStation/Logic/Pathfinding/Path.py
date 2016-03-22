import numpy as np
class Path:

    def __init__(self):
        self.nodeList = []
        self.totalDistance = 0

    def append(self, node):
            self.nodeList.append(node)

    def ajustDistance(self):
        self.totalDistance = 0
        for compteur in range(1, self.nodeList.__len__()):
            lastNode = self.nodeList[compteur - 1]
            currentNode = self.nodeList[compteur]
            distance = np.sqrt(((lastNode.positionX - currentNode.positionX)**2)+((lastNode.positionY - currentNode.positionY)**2))
            self.totalDistance += distance

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
        lastNode = self.nodeList[-1]
        for compteur in range(0, lastNode.connectedNodes.__len__()):
            if isOpen == False:
                connectedNode = lastNode.connectedNodes[compteur]
                if self.contains(connectedNode) == False:
                    isOpen = True
        return isOpen

    def remove(self, node):
        self.nodeList.remove(node)

    def __len__(self):
        return self.nodeList.__len__()

    def __getitem__(self, item):
        return self.nodeList[item]

