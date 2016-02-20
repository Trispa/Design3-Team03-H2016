#include "commandReceiver.h"

#define StandardHeaderLenght 5
#define NumberOfBytesInLong 4
#define ASCIIOffset 48
#define NumberOfPIDParameters 4
#define HalfTurnTicks 2064
#define MilimetersToTicks 7.69
#define endingLEDPin 13

CommandReceiver::CommandReceiver()
{

}

CommandReceiver::CommandReceiver(DriveMoteur* d)
{
  dm = d;
}

void CommandReceiver::decomposeParameters() {
	byte numberOfParameters = Serial.read() - ASCIIOffset;
	
	while(Serial.available() < (numberOfParameters * NumberOfBytesInLong) ) {}
	
	long buffer = 0;
	int index = 0;

	while(index < numberOfParameters) {
		parameters[index] = readULongFromBytes();
		index++;
	}
}


void CommandReceiver::decomposeCommand() {
	commandIndex = Serial.read() - ASCIIOffset;

	callbackRequested = Serial.read() - ASCIIOffset;

	decomposeParameters();
}

void CommandReceiver::process() {
	executeCommand();
}

void CommandReceiver::readPort() {
	if(Serial.read() == 'C') {
		while(Serial.available() < StandardHeaderLenght) {}
		decomposeCommand();
		commandWaitingFlag = 1;
	}
}   

//à voir si par roue et s'entendre sur quelle roue est à quel indice
void CommandReceiver::dispatchCommand() {
	long resistance;
	int rotationDirection = 1;

	switch (commandIndex) {
	case 1: //lightEndingLED
		digitalWrite(endingLEDPin, HIGH);
		break;		
		
	case 2: //turnOffEndingLED
		digitalWrite(endingLEDPin, LOW);
		break;

  case 3: //change speed of a motor
    dm[parameters[0]-1].driveMoteur(parameters[1]/100.0, parameters[2]);
    break;

	default: //for test purposes
		if(callbackRequested == 1) {
			sendCallback(parameters[0]);
		}
		break;
	}    
}

void CommandReceiver::sendCallback(long callbackData) {
	Serial.print('R');
	Serial.print(callbackData, DEC);
}


void CommandReceiver::executeCommand() {
	readPort();
	
	if(commandWaitingFlag == 1) {
		dispatchCommand();
		commandWaitingFlag = 0;
	}
}

long CommandReceiver::readULongFromBytes() {
	union u_tag {
		byte bytes[NumberOfBytesInLong];
		long returnLong;
	} bytesToLong;

	bytesToLong.bytes[0] = Serial.read();
	bytesToLong.bytes[1] = Serial.read();
	bytesToLong.bytes[2] = Serial.read();
	bytesToLong.bytes[3] = Serial.read();
	return bytesToLong.returnLong;
}

