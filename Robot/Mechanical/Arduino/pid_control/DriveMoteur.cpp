/*
  DriveMoteur.cpp
*/

#include "Arduino.h"
#include "DriveMoteur.h"


volatile unsigned long freqEnco1 = 0;
volatile unsigned long startCounting = 0;
volatile unsigned long endCounting = 0;
volatile unsigned long nbPulse = 0;
int limitNbPulse = 150;


static void fctInterrupt()
	{
		if(nbPulse >= limitNbPulse)
  		{
    		endCounting = micros();
    		freqEnco1 = (1000000*nbPulse/(endCounting - startCounting));
    		startCounting = endCounting;
    		nbPulse = 0;
  		}
  		else if(nbPulse < limitNbPulse)
   			 nbPulse ++;
	}

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
	input = 1000;
	output = 1000;
	setpoint = 1000;
	
	myPID.SetMode(AUTOMATIC);
	myPID.SetOutputLimits(550, 2760);
	interrupAttach =false;
	digitalWrite(_pin1, LOW);
	digitalWrite(_pin2, LOW);

}
//0 = CW -- 1 = CCW
void DriveMoteur::driveMoteur(double speed, int direction)
{
  //On active l'interrup pour l'encodeur du moteur
	//On analogWrite avec un pwm passer prealablement dans lasservissement
	Serial.print("Vitesse desire : "); Serial.print(speed);
	Serial.print("   Vitesse reel : "); Serial.print(encoFreqToSpeed(input));
	Serial.print("   Output : "); Serial.println(encoFreqToSpeed(output));
	if(speed > 0)
		{
			if(!interrupAttach)
				{
					interrupAttach = true;
					setInterrupForEnco(interrupAttach);
				}
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
			setpoint = speedToEncoFreq(speed);
			asservissement();
		}
	//On desactive l'interrup de lencodeur
	//On analogWrite 0 pour arreter l'envoi des pwm et imobiliser le moteur
	else
		{
			interrupAttach = false;
			setInterrupForEnco(interrupAttach);
			analogWrite(_pinMoteur, 0);
			setpoint = 0;
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
	if(freq <= 1840)
		return int(0.039*freq+8.805);
	else
		return int(0.00007081 * freq * freq - 0.155 * freq + 117.931);
}

double DriveMoteur::PWMToEncoFreq(int PWM)
{
//pwm to freq : (-0,062 * PWM^2 + 25,853 * PWM + 16,571) = freq
	return -0,062 * PWM * PWM + 25,853 * PWM + 16,571;
}

void DriveMoteur::asservissement()
{
	input = freqEnco1;
	myPID.Compute();
	analogWrite(_pinMoteur, encoFreqToPWM(output));
	Serial.print("Vitesse desire : "); Serial.print(encoFreqToSpeed(setpoint));
	Serial.print("   Vitesse reel : "); Serial.print(encoFreqToSpeed(input));
	Serial.print("   Output : "); Serial.println(encoFreqToSpeed(output));
}

double DriveMoteur::getFreqFromEnco()
{
	return freqEnco1;
}

void DriveMoteur::setInterrupForEnco(boolean attach)
{
//Pin dinterruption arduino mega 18, 19, 20, 21
	if(attach)
		attachInterrupt(digitalPinToInterrupt(_pinEnco), fctInterrupt, RISING);
	else
		detachInterrupt(digitalPinToInterrupt(_pinEnco)); 
}

boolean DriveMoteur::isRunning()
{
	return setpoint != 0;
}



