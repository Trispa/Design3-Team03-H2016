/*
	ReadManchester.h library for read manchester code from an encoder Manchester
	Created by Erco Trispa Frebruary 10 2016
	Released into the public domain
*/

#ifndef ReadManchester_h
#define ReadManchester_h

#include "Arduino.h"


class ReadManchester
{
	public:
		ReadManchester(int pinManchester, int pinClock);
		char booleanToChar(boolean b);
		char* getMaschesterBits();
		void enableInterrupt(boolean  answer);
		static void readBitInterrupt();
		String getChaine();
		
		
		
	private:
		int _pinManchester;
		int _pinClock;
		
		
};

#endif
