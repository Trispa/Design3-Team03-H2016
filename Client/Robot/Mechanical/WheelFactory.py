from Client.Robot.Mechanical.WheelMotor import WheelMotor

class WheelFactory:
    def __init__(self):
        self = self

    def createWheels(self):
        horizontalWheelFront = WheelMotor(int)
        horizontalWheelBack = WheelMotor(int)
        verticalWheelLeft = WheelMotor(int)
        verticalWheelRight = WheelMotor(int)

        return horizontalWheelFront, horizontalWheelBack, verticalWheelLeft, verticalWheelRight