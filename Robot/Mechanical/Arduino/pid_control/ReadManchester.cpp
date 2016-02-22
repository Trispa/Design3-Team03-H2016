/*
	ReadManchester.h library for read manchester code from an encoder Manchester
	Created by Erco Trispa Frebruary 10 2016
	Released into the public domain
*/

#include "Arduino.h"
#include "ReadManchester.h"

volatile unsigned int bitAllowed = 0;
volatile unsigned int  indice = 0;
volatile unsigned int data ; 
char chaine[64];
char* chainecopie = '\0';

int volatile trouve = 0;
void ReadManchester::readBitInterrupt(){
	bitAllowed = 1;
	//delayMicroseconds(50);
	
}
ReadManchester::ReadManchester(int pinManchester, int pinClock)
{
	
	pinMode(pinManchester, INPUT);
	pinMode(pinClock, INPUT);
	_pinManchester = pinManchester;
	_pinClock = pinClock;
	enableInterrupt(true);	
}

char ReadManchester::booleanToChar(boolean b)
{
	
	return (b)?'1':'0';
}


char*  ReadManchester::getMaschesterBits()
{	
	
		if(bitAllowed)
		{     
			data =  digitalRead(_pinManchester);
			chaine[indice] = booleanToChar(data);
			
			indice++;
			if(indice == 64)
			  {
				indice = 0 ;
				chainecopie = chaine;
				Serial.println(chaine);
				enableInterrupt(false);	
				
					
			  }
			  
			bitAllowed = 0;
			
		}
	return chainecopie;	
}

void ReadManchester::enableInterrupt(boolean ansewer){
		
		if(ansewer)
			attachInterrupt(digitalPinToInterrupt(_pinClock), readBitInterrupt, RISING); 
		else
			detachInterrupt(digitalPinToInterrupt(_pinClock));

}

