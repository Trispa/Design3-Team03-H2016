from unittest import TestCase
from mock import MagicMock
import cv2
from Client.BaseStation.Logic.BaseStationDispatcher import BaseStationDispatcher
from Client.BaseStation.WorldVision.allShapes import *
from Client.BaseStation.WorldVision.allColors import *


class BaseStationDispatcherTest(TestCase):

    def setUp(self):
        self.worldVision = MagicMock()
        self.map = MagicMock()
        self.map.robot.center.return_value = (100,100)
        self.map.robot.orientation.return_value = 0
        self.sequencer = MagicMock()
        self.sequencer.handleCurrentState.return_value = None, None, None

        blueSquare = Square("Square", np.array([[]], dtype=np.int32))
        blueSquare.setColor(GenericColor(np.uint8([[[255,0,0]]]), "Blue"))
        redTriangle = Triangle("Triangle", np.array([[]], dtype=np.int32))
        redTriangle.setColor(Red(np.uint8([[[150,179,255]]]), "Red"))
        obstacleList = [blueSquare, redTriangle]

        self.map.getShapesList.return_value = obstacleList
        self.worldVision.getCurrentImage.return_value = cv2.imread("Picture 500.jpg"), self.map

    def test_whenInitialisingWorldDataThenEverythingIsCalledAccordingly(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.initialiseWorldData()

        assert self.worldVision.initializeRound.called
        assert self.worldVision.getCurrentImage.called
        self.assertIsNotNone(testedDispatcher.sequencer)
        self.assertIsNotNone(testedDispatcher.pathfinder)

    def test_whenHandlingCurrentSequencerStateThenEverythingIsCalledAccordingly(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.sequencer = self.sequencer
        testedDispatcher.handleCurrentSequencerState()

        assert self.worldVision.getCurrentImage.called
        assert self.sequencer.handleCurrentState.called

    def test_whenGettingCurrentWorldInformationThenEverythingIsCalledAccordingly(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        info = testedDispatcher.getCurrentWorldInformation()

        self.assertIsNotNone(info['robotPosition'])
        self.assertIsNotNone(info['robotOrientation'])
        self.assertIsNotNone(info['encodedImage'])

    def test_whenStartingFromBeginningThenSequencerStateIsChanged(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.sequencer = self.sequencer
        testedDispatcher.startFromBegining()

        assert self.sequencer.setState.called


    def test_whenStartingFromTreasureThenSequencerStateIsChanged(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.sequencer = self.sequencer
        testedDispatcher.startFromTreasure()

        assert self.sequencer.setState.called


    def test_whenStartingFromTargetThenSequencerStateIsChanged(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.sequencer = self.sequencer
        testedDispatcher.startFromTarget()

        assert self.sequencer.setState.called


    def test_whenSettingTargetOnMapThenWorldVisionCallsSetTarget(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.setTargetOnMap({"forme":"rectangle"})

        assert self.worldVision.setTarget.called

    def test_whenSettingTreasuresThenWorldVisionCallsSetTreasures(self):
        testedDispatcher = BaseStationDispatcher(self.worldVision)
        testedDispatcher.setTreasuresOnMap([48.0])

        assert self.worldVision.setTreasures.called