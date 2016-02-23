/*
  DriveMoteur.h
*/
#ifndef DriveMoteur_h
#define DriveMoteur_h

#include "Arduino.h"
#include "PID_v1.h"




class DriveMoteur
{
  public:
	DriveMoteur();
    DriveMoteur(int pinMoteur, int enco, int pin1, int pin2);
	void driveMoteur(double speed, int direction);
	void asservissement();
	double getFreqFromEnco();
	double speedToEncoFreq(double speed);
	double encoFreqToSpeed(double freq);
	int encoFreqToPWM(double freq);
	double PWMToEncoFreq(int PWM);
	boolean isRunning();
  int getPinEncoInterrup();
  double* getInput();
  double* getOutput();
  double* getSetpoint();
  void setInput(double i);


  private:
    int _pinMoteur;
    int _pinEnco;
	int _pin1, _pin2;
	double input, output, setpoint;

};

#endif
