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

double kp = 1.3;
double ki = 5.25;
double kd = 0.08;
long listNbTicks[4] = {0, 0, 0, 0};
long listEndCounting[4] = {0,0,0,0};
long listStartCounting[4] = {0,0,0,0};


DriveMoteur dv[4] = {DriveMoteur(4,18, 46, 47), DriveMoteur(5,19, 48, 49), DriveMoteur(6,20, 50, 51), DriveMoteur(7,21, 52, 53)};

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
    listPID[i].SetOutputLimits(550, 2760);
  }
//  dv[2].driveMoteur(0.03, 0);

}

void loop() 
{
  cmdRec.process();
  updateFreqEnco();
  for(int i = 0; i < NB_DRIVEMOTEUR; i++)
  {
      if(dv[i].isRunning())
      {
        listPID[i].Compute();
        dv[i].asservissement();
      }
  }
   
}




void updateFreqEnco()
{
  for(int i = 0; i < NB_DRIVEMOTEUR; i++)
  {
  listEndCounting[i] = micros();
  dv[i].setInput(1000000*listNbTicks[i]/(listEndCounting[i] - listStartCounting[i]));
  listStartCounting[i] = listEndCounting[i];
  listNbTicks[i] = 0;
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


