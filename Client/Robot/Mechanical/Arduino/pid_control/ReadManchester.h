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
    ReadManchester(int pinManchester);
    void getMaschesterBits();
    void enableInterrupt(boolean);
    static void readBitInterrupt();
    void disableManchester();
    void enableManchester();
    char* getChaineCopie();
    
    
  private:
    int _pinManchester; 
    boolean _enableManchester ;
    char* _chaineCopie;
};

#endif

