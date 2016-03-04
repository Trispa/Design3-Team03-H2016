/*
	ReadManchester.h library for read manchester code from an encoder Manchester
	Created by Erco Trispa Frebruary 10 2016
	Released into the public domain
*/

#include "Arduino.h"
#include "ReadManchester.h"

/*********DEBUT********/
volatile int val = 0;
volatile unsigned long now = 0;
volatile unsigned long timeToChange = 0;
volatile unsigned long timebetweenNowToChange = 0;
char bits[128];
char* chainecopie;
int indice = 0;
/*********** FIN******/

volatile unsigned int bitAllowed = 0;
//volatile unsigned int  indice = 0;
volatile unsigned int data ; 

//int volatile trouve = 0;
void ReadManchester::readBitInterrupt(){
  now = micros();
	bitAllowed = 1;
	
}
ReadManchester::ReadManchester(int pinManchester, boolean allow)
{
	
	pinMode(pinManchester, INPUT);
	this->_pinManchester = pinManchester;
  this->_enableManchester = allow;
	enableInterrupt(true);	
}


char*  ReadManchester::getMaschesterBits()
{	
	  if(this->_enableManchester){
  		if(bitAllowed){
      //Serial.pri ntln(now, DEC);
      val = digitalRead(_pinManchester);
      timebetweenNowToChange = now - timeToChange;
      //Serial.println(timebetweenNowToChange);
      if(val == 0){
        if(timebetweenNowToChange > 150 && timebetweenNowToChange < 250){
          bits[indice++]= '1';
          bits[indice++]= '0';
        }
        else{
          bits[indice++]= '0';
        }
      }
      if(val== 1){
       if(timebetweenNowToChange > 150 && timebetweenNowToChange < 250){
          bits[indice++]= '0';
          bits[indice++]= '1';
        }
        else{
           bits[indice++]= '1';
        }
      }
      if(indice > 128){
        chainecopie = bits;
        indice = 0;
        enableInterrupt(false); 
        this->disableManchester();
        
      }
      timeToChange = now;
      bitAllowed = 0;
      
    }
 
	 }
	 return chainecopie;
}

void ReadManchester::enableInterrupt(boolean ansewer){
		
		if(ansewer)
			attachInterrupt(digitalPinToInterrupt(_pinManchester), readBitInterrupt, CHANGE); 
		else
			detachInterrupt(digitalPinToInterrupt(_pinManchester));

}

void ReadManchester::disableManchester(){
  this->_enableManchester = false;
}
void ReadManchester::enableManchester(){
  this->_enableManchester = true;
}

