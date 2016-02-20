from Client.BaseStation.WorldVision.worldImage import WorldImage
import cv2


if __name__ == '__main__':
    myImageName = "Images\Test1.jpg"

    cv2.imshow("Drawn world", cv2.imread(myImageName, 1))
    cv2.waitKey(0)

    closingImage = WorldImage(cv2.imread(myImageName, 1))
    closingImage.setMap("ColorBuildByClosing")
    closingImage.addLabels()
    closingMap = closingImage.getMap()
    cv2.imshow("Closing", closingImage.drawMapOnImage())
    cv2.waitKey(0)

    openingImage = WorldImage(cv2.imread(myImageName, 1))
    openingImage.setMap("ColorBuildByOpening")
    openingImage.addLabels()
    openingMap = openingImage.getMap()
    cv2.imshow("Opening", openingImage.drawMapOnImage())
    cv2.waitKey(0)

    geometricalImage = WorldImage(cv2.imread(myImageName, 1))
    geometricalImage.setMap("GeometricalFilter")
    geometricalImage.addLabels()
    geometricalMap = geometricalImage.getMap()
    cv2.imshow("Geometric", geometricalImage.drawMapOnImage())
    cv2.waitKey(0)

    mergedMap = closingMap.mergeShapeList(openingMap)
    print(len(mergedMap.getContourList()))

