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
		ReadManchester(int pinManchester, boolean allow);
		char* getMaschesterBits();
		void enableInterrupt(boolean);
		static void readBitInterrupt();
    void disableManchester();
    void enableManchester();
		
		
	private:
		int _pinManchester;	
    boolean _enableManchester ;
};

#endif

