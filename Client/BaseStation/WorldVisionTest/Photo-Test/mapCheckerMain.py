from resultChecker import ResultChecker


if __name__ == '__main__':
    totalFound = 0
    totalOnImage = 0
    for pictureNumber in range(1, 116):
        myResultChecker = ResultChecker(pictureNumber)
        print("Picture " + str(pictureNumber))
        found, onImage = myResultChecker.checkNumberOfShapesFound()
        totalFound += found
        totalOnImage += onImage
        myResultChecker.checkIfLimitFound()
        myResultChecker.checkIfRobotFound()
        print("\n")

    ratio = float(float(totalFound) / float(totalOnImage))
    print("Ratio : " + str(ratio))