from resultChecker import ResultChecker


if __name__ == '__main__':
    for pictureNumber in range(7, 60):
        myResultChecker = ResultChecker(pictureNumber)
        print("Picture " + str(pictureNumber))
        myResultChecker.checkNumberOfShapesFound()
        myResultChecker.checkIfLimitFound()
        myResultChecker.checkIfRobotFound()
        print("\n")