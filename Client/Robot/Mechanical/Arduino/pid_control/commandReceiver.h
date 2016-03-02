#ifndef COMMANDRECEIVER_H
#define COMMANDRECEIVER_H

#include "Arduino.h"
#include "DriveMoteur.h"

#define MaximumBufferLenght 60
#define MaximumCommandLenght 14
#define MaximumParametersQuantity 5
#define NumberOfData 4

class CommandReceiver {
public:  

  boolean * enableManchester;

  String * manchesterToreturn;
	CommandReceiver();
  CommandReceiver(DriveMoteur* listDriveMoteur, boolean* enableManchester, String * manchesterToreturn);
  void setEnableManchester(boolean b);
	void executeCommand();
	void process();



	void decomposeParameters();
	void decomposeCommand();
	void readPort();
	void dispatchCommand();
	long readULongFromBytes();
	void sendCallback(long callbackData);
  void sendCallback(char* callbackData);
  void sendCallback(String callbackData);
	byte commandWaitingFlag;
	byte commandInProgressFlag;
	volatile long* positionData;
	double* speedData;
	int nextPidCommand;
	int currentPidCommand;
	long pidBuffer[MaximumBufferLenght];

	byte commandIndex;
	byte callbackRequested;
  long parameters[MaximumParametersQuantity];
  

  DriveMoteur* dm;



};

#endif
