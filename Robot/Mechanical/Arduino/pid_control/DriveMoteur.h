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
	void setInterrupForEnco(boolean attach);
	double speedToEncoFreq(double speed);
	double encoFreqToSpeed(double freq);
	int encoFreqToPWM(double freq);
	double PWMToEncoFreq(int PWM);
	boolean isRunning();


  private:
    int _pinMoteur;
    int _pinEnco;
	int _pin1, _pin2;
	boolean interrupAttach;
	double input, output, setpoint;
	double kp = 1.3;
	double ki = 5.25;
	double kd = 0.08;
	PID myPID = PID(&input, &output, &setpoint, kp, ki, kd, DIRECT);

};

#endif
