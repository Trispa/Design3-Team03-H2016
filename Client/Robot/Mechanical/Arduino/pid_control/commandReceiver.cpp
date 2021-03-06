#include "commandReceiver.h"
#include <stdlib.h>
#define StandardHeaderLenght 5
#define NumberOfBytesInLong 4
#define ASCIIOffset 48
#define NumberOfPIDParameters 4
#define HalfTurnTicks 2064
#define MilimetersToTicks 7.69
#define endingLEDPin 13

 char  *machaine;
CommandReceiver::CommandReceiver()
{

}

CommandReceiver::CommandReceiver(DriveMoteur* d,  ReadManchester* man)
{
  dm = d;
  rm = man;
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
  double tempVoltage;

	switch (commandIndex) {
	case 1: //lightEndingLED
//    double tempVoltage;
    tempVoltage = analogRead(A0) * 5.0 / 1023.0;
    if(callbackRequested == 1){
             sendCallback(long(tempVoltage * 100));
          }
		break;

	case 2: //turnOffEndingLED
		digitalWrite(endingLEDPin, LOW);
		break;

  	case 3: //change speed of a motor
    		dm[parameters[0]-1].driveMoteur(parameters[1]/100.0, parameters[2]);
    		break;


	case 4: // ReadMAnchesterBits
          rm->enableManchester();

          break;
 	case 5:// j'ai changé le 4 en 5 car le 4 appartenais déjà  au ReadManchester
    		for(int i = 0; i<4; i++)
    		{
      			dm[i].driveMoteur(0,0);
    		}
       break;

  case 6: // callback MAnchester
          if(callbackRequested == 1){
             sendCallback(rm->getChaineCopie());
          }
          break;

	case 7:
      double distanceCm;
      distanceCm = parameters[3] / 100;
      double tick;
      tick = distanceCm * 72.912;
		if (parameters[0] == 0) //Axe des X
		{
      
      dm[1].setTickToDo(tick);
      dm[2].setTickToDo(tick);
			if(parameters[2] == 1) //Direction positive
			{
				dm[1].driveMoteur(parameters[1]/100.0, 0);
				dm[2].driveMoteur(parameters[1]/100.0, 1);
			}
			else // Direction negative
			{
				dm[1].driveMoteur(parameters[1]/100.0, 1);
				dm[2].driveMoteur(parameters[1]/100.0, 0);
			}
		}
		else //Axe des Y
		{
      dm[0].setTickToDo(tick);
      dm[3].setTickToDo(tick);
			if(parameters[2] == 1) //Direction positive
			{
				dm[0].driveMoteur(parameters[1]/100.0, 1);
				dm[3].driveMoteur(parameters[1]/100.0, 0);
			}
			else // Direction Negative
			{
				dm[0].driveMoteur(parameters[1]/100.0, 0);
				dm[3].driveMoteur(parameters[1]/100.0, 1);
			}

		}
//   double tempVoltage;
    tempVoltage = analogRead(A0) * 5.0 / 1023.0;
    if(callbackRequested == 1){
             sendCallback(long(tempVoltage * 100));
          }
   break;
    break;

	case 8:
		for(int i = 0; i<4; i++)
			{
          double angle = parameters[2] / 100;
          dm[i].setTickToDo(angle * 4475 / 360);
	  			dm[i].driveMoteur(parameters[0]/100.0, parameters[1]);
			}
//     double tempVoltage;
    tempVoltage = analogRead(A0) * 5.0 / 1023.0;
    if(callbackRequested == 1){
             sendCallback(long(tempVoltage * 100));
          }
   break;
      break;

  case 9:
    //controle electro aiment 00 decharge 10 ou 01 garde la charge 11 pour recharger
    // 0 decharge
    // 1 ou else garde charge
    // 2 recharge
    if(parameters[0] == 0)
    {
      digitalWrite(52, LOW);
      digitalWrite(53, LOW);
    }
    else if(parameters[0] == 2)
    {
      digitalWrite(52, HIGH);
      digitalWrite(53, HIGH);
    }
    else
    {
      digitalWrite(52, HIGH);
      digitalWrite(53, LOW);      
    }
    break;

  //callback de la lecture du condensenteur
  case 10:
//    long voltage;
//    voltage = analogRead(A0);
    if(callbackRequested == 1){
             sendCallback(long(134));
          }
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


void CommandReceiver::sendCallback(char* callbackData) {
  Serial.print('R');
  Serial.print(callbackData);
}
void CommandReceiver::sendCallback(String callbackData) {
  Serial.print('R');
  Serial.print(callbackData);
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
