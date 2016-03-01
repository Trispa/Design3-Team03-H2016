/*
  DriveMoteur.cpp
*/

#include "Arduino.h"
#include "DriveMoteur.h"


DriveMoteur::DriveMoteur(){}

DriveMoteur::DriveMoteur(int pinMoteur, int enco, int pin1, int pin2)
{
 	pinMode(pinMoteur, OUTPUT);
	pinMode(pin1, OUTPUT);
	pinMode(pin2, OUTPUT);
	_pinMoteur = pinMoteur;
	_pinEnco = enco;
	_pin1 = pin1;
	_pin2 = pin2;
	input = 0;
	output = 0;
	setpoint = 0;
 _run = 0;

  driveMoteur(0,0);
}
//0 = CW
//1 = CCW
void DriveMoteur::driveMoteur(double speed, int direction)
{
	//On analogWrite avec un pwm passer prealablement dans lasservissement
//	Serial.print("Vitesse desire : "); Serial.print(speed);
//	Serial.print("   Vitesse reel : "); Serial.print(encoFreqToSpeed(input));
//	Serial.print("   Output : "); Serial.println(encoFreqToSpeed(output));
	if(speed > 0)
		{
			if(direction == 0)
			{
				digitalWrite(_pin1, LOW);
				digitalWrite(_pin2, HIGH);
			}
			else if(direction == 1)
			{
				digitalWrite(_pin1, HIGH);
				digitalWrite(_pin2, LOW);
			}
      _run = 1;
			setpoint = speedToEncoFreq(speed);
      asservissement();
		}
	//On desactive l'interrup de lencodeur
	//On analogWrite 0 pour arreter l'envoi des pwm et imobiliser le moteur
	else
		{
			analogWrite(_pinMoteur, 0);
			input = 0;
      output = 0;
      setpoint = 0;
      _run = -1;
			digitalWrite(_pin1, LOW);
			digitalWrite(_pin2, LOW);
		}
}

double DriveMoteur::speedToEncoFreq(double speed)
{
//7291.2 valeur calculer pour convertir la freq de lencodeur en m/s
	return speed * 7291.2;
}

double DriveMoteur::encoFreqToSpeed(double freq)
{
//7291.2 valeur calculer pour convertir la freq de lencodeur en m/s
	return freq / 7291.2;
}

int DriveMoteur::encoFreqToPWM(double freq)
{
// freq to pwm : 7.081E^-5 * freq^2 - 0.155 * freq + 117.931

//	return int(0.00007081 * freq * freq - 0.155 * freq + 117.931);
//	if(freq <= 1840)
//		return int(0.039*freq+8.805);
//	else
//		return int(0.00007081 * freq * freq - 0.155 * freq + 117.931);
    if(freq <= 1500)
    return int(0.00001402 * freq * freq + 0.027 * freq + 53.77);
  else
    return int(0.0001619 * freq * freq  - 0.378 * freq + 331.876);
}

double DriveMoteur::PWMToEncoFreq(int PWM)
{
//pwm to freq : (-0,062 * PWM^2 + 25,853 * PWM + 16,571) = freq
	return -0,062 * PWM * PWM + 25,853 * PWM + 16,571;
}

void DriveMoteur::asservissement()
{
  if(_run == 1)
	  analogWrite(_pinMoteur, encoFreqToPWM(output));
//	Serial.print("Vitesse desire : "); Serial.print(encoFreqToSpeed(setpoint));
//	Serial.print("   Vitesse reel : "); Serial.print(encoFreqToSpeed(input));
//	Serial.print("   Output : "); Serial.println(encoFreqToSpeed(output));
}

//1 is running
//0 is not running
//-1 time to change pid constants and is not running
int DriveMoteur::isRunning()
{
//	if(_run == -1)
//    {
//      _run = 0;
//      return -1;
//    }
//  else
//  {
//    return _run;
//  }
    if(_run == -1)
    {
      _run = 0;
      return  1;
    }
    else
      return _run;
}

void DriveMoteur::setInput(double i)
{
  input = i;
}

int DriveMoteur::getPinEncoInterrup()
{
  return _pinEnco;
}

double* DriveMoteur::getInput()
{
 return &input;
}
double* DriveMoteur::getOutput()
{
  return &output;
}
double* DriveMoteur::getSetpoint()
{
  return &setpoint;
}
