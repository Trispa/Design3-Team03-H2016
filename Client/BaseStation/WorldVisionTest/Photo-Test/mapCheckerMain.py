from resultChecker import ResultChecker


if __name__ == '__main__':
    for pictureNumber in range(7, 21):
        myResultChecker = ResultChecker(pictureNumber)
        print("Picture " + str(pictureNumber))
        myResultChecker.checkNumberOfShapesFound()
        myResultChecker.checkIfLimitFound()
        print("\n")