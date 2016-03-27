/*
	ReadManchester.h library for read manchester code from an encoder Manchester
	Created by Erco Trispa Frebruary 10 2016
	Released into the public domain
*/

#include "Arduino.h"
#include "ReadManchester.h"

/*********DEBUT********/
volatile int oldVal = 0;
volatile int newVal = 0;
volatile unsigned long now = 0;
unsigned long timeToChange = 0;
unsigned long timebetweenNowToChange = 0;
char bits[128];
char* chainecopie = '\0';
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
ReadManchester::ReadManchester(int pinManchester){
	
	pinMode(pinManchester, INPUT);
	this->_pinManchester = pinManchester;
 	this->enableInterrupt(true);	
  this->enableManchester();
  
}


void   ReadManchester::getMaschesterBits()
{	
	  if(this->_enableManchester){
  		if(bitAllowed){
      //Serial.println(now);
      //delayMicroseconds(13);
      newVal = digitalRead(_pinManchester);
      //digitalWrite(13, newVal);
      
      timebetweenNowToChange = now - timeToChange;
      //Serial.println(timebetweenNowToChange, DEC);
      if(oldVal == HIGH){
        if(timebetweenNowToChange > 20 && timebetweenNowToChange < 80 ){ // on vise envirion 44{
          bits[indice++]= '1';
        }else if (timebetweenNowToChange > 130 && timebetweenNowToChange < 175){ //on vise environ 144
          bits[indice++]= '1';
          bits[indice++]= '1';
        }
      }else if (oldVal == LOW){
          if (timebetweenNowToChange > 90 && timebetweenNowToChange < 150){ //on vise environ 108
               bits[indice++]= '0';
          }else if (timebetweenNowToChange > 200 && timebetweenNowToChange < 250){ //on vise environ 212
               bits[indice++]= '0';
               bits[indice++]= '0';
          }
          
      }
      
      if(indice > 128){
        this->_chaineCopie = bits;
        indice = 0;
        this->enableInterrupt(false); 
        this->disableManchester();
     
        
      }
     
      timeToChange = now;
      oldVal = newVal;
      bitAllowed = 0;
    }
 
	 }
	 
}

char* ReadManchester::getChaineCopie(){
  return this->_chaineCopie;
  
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
  this->enableInterrupt(true);
}

