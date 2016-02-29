#define SAMPLE_MICROS 5000 // 0.005 s
#define DEAD_ZONE 13
#define THRESHOLD 10
#define TOP_SPEED 2.7
#define SPEED_LIM 0.6*TOP_SPEED
#define DEFAULT_INCREMENT 10
#define DIAG_INCREMENT 0.7*DEFAULT_INCREMENT
#define END 7*THRESHOLD
#define NB_DRIVEMOTEUR 4

#include "DriveMoteur.h"
#include "commandReceiver.h"

double kp = 0.7;  //1.506897
double ki = 5; //0.007
double kd = 0.08;
long listNbTicks[4] = {0, 0, 0, 0};
unsigned long listEndCounting[4] = {0,0,0,0};
unsigned long listStartCounting[4] = {0,0,0,0};
bool timeToCompute = false;
unsigned long freq = 0;
unsigned long graphTime = 0;
unsigned int ar = 0;

DriveMoteur dv[4] = {DriveMoteur(4,18, 26, 27), DriveMoteur(5,19, 28, 29), DriveMoteur(6,20, 30, 31), DriveMoteur(7,21, 32, 33)};
ReadManchester rm = ReadManchester(2,3);

PID listPID[4] = {PID(dv[1 - 1].getInput(), dv[1 - 1].getOutput(), dv[1 - 1].getSetpoint(), kp, ki, kd, DIRECT),
                  PID(dv[2 - 1].getInput(), dv[2 - 1].getOutput(), dv[2 - 1].getSetpoint(), kp, ki, kd, DIRECT),
                  PID(dv[3 - 1].getInput(), dv[3 - 1].getOutput(), dv[3 - 1].getSetpoint(), kp, ki, kd, DIRECT),
                  PID(dv[4 - 1].getInput(), dv[4 - 1].getOutput(), dv[4 - 1].getSetpoint(), kp, ki, kd, DIRECT)};


CommandReceiver cmdRec = CommandReceiver(dv);

void updateFreqEnco();


void setup() {
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(dv[1 - 1].getPinEncoInterrup()), fctInterrupt1, RISING);
  attachInterrupt(digitalPinToInterrupt(dv[2 - 1].getPinEncoInterrup()), fctInterrupt2, RISING);
  attachInterrupt(digitalPinToInterrupt(dv[3 - 1].getPinEncoInterrup()), fctInterrupt3, RISING);
  attachInterrupt(digitalPinToInterrupt(dv[4 - 1].getPinEncoInterrup()), fctInterrupt4, RISING);
  
  for(int i = 0; i < NB_DRIVEMOTEUR; i++)
  {
    dv[i].driveMoteur(0, 0);
    listPID[i].SetMode(AUTOMATIC);
    listPID[i].SetOutputLimits(100, 2080);
  }
//  dv[1].driveMoteur(0.15, 1);
//  dv[2].driveMoteur(0.15, 0);
//    analogWrite(5, 0);
//    digitalWrite(28, HIGH);
//    digitalWrite(29, LOW);
//    analogWrite(6, 0);
//    digitalWrite(30, LOW);
//    digitalWrite(31, HIGH);

}

void loop() 
{


  cmdRec.process();
  updateFreqEnco();
    for(int i = 0; i < NB_DRIVEMOTEUR; i++)
    {
      listPID[i].Compute(); // Trouver une facon de compute une fois de plus dans le if quand il ne run pas
        if(dv[i].isRunning())
        {
          
          dv[i].asservissement();
        }
    }

//    updateFreqEnco(1);
//    ar += 5;
//    analogWrite(6, ar);
//    analogWrite(5, ar);
//
//    delay(500);

  
//    graphTime += millis();
//    Serial.print(ar, DEC);
//    Serial.print(",");
//    Serial.println(freq);

}


void updateFreqEnco()
{
  for(int i = 0; i < NB_DRIVEMOTEUR; i++)
  {
      listEndCounting[i] = micros();
//      if((listEndCounting[i] - listStartCounting[i]) > 95000)
//      {
        
        dv[i].setInput(1000000*listNbTicks[i]/(listEndCounting[i] - listStartCounting[i]));
        
        
//        freq = (1000000*listNbTicks[i]/(listEndCounting[i] - listStartCounting[i]));
//        Serial.print(listNbTicks[i]); Serial.print(" -- ");
//        Serial.print(listEndCounting[i]); Serial.print(" -- ");
//        Serial.print(listStartCounting[i]); Serial.print(" -- ");
//        Serial.print(freq); Serial.println(" -- ");
        listStartCounting[i] = listEndCounting[i];
        listNbTicks[i] = 0;
//        }
  }
  

}

void fctInterrupt1()
  {
    listNbTicks[1 - 1]++;
  }

void fctInterrupt2()
  {
    listNbTicks[2 - 1]++;
  }

void fctInterrupt3()
{
  listNbTicks[3 - 1]++;
}

void fctInterrupt4()
  {
    listNbTicks[4 - 1]++;
  }


