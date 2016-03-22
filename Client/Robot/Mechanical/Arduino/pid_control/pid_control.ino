#define NB_DRIVEMOTEUR 4

#include "DriveMoteur.h"
//#include "ReadManchester.h"
#include "commandReceiver.h"

/****************MANCHESTER SETUP***********/
uint8_t manchester_pin = 17;
uint8_t clk_pin = 8;
volatile uint8_t code_Manchester = 0;
boolean enableManchester = true;

/****************MANCHESTER FIN***********/
double kp = 1.05;  //1.506897
double ki = 5.25; //0.007
double kd = 0;
void fctInterrupt1();
void fctInterrupt2();
void fctInterrupt3();
void fctInterrupt4();




long listNbTicks[4] = {0, 0, 0, 0};
unsigned long listEndCounting[4] = {0,0,0,0};
unsigned long listStartCounting[4] = {0,0,0,0};
bool timeToCompute = false;
unsigned long freq = 0;
unsigned long graphTime = 0;
unsigned int ar = 0;
unsigned long diffTime = 0;
char* chaine;
DriveMoteur dv[4] = {DriveMoteur(4,18, 26, 27), DriveMoteur(5,19, 28, 29), DriveMoteur(6,20, 30, 31), DriveMoteur(7,21, 32, 33)};


PID listPID[4] = {PID(dv[1 - 1].getInput(), dv[1 - 1].getOutput(), dv[1 - 1].getSetpoint(), kp, ki, kd, DIRECT),
                  PID(dv[2 - 1].getInput(), dv[2 - 1].getOutput(), dv[2 - 1].getSetpoint(), kp, ki, kd, DIRECT),
                  PID(dv[3 - 1].getInput(), dv[3 - 1].getOutput(), dv[3 - 1].getSetpoint(), kp, ki, kd, DIRECT),
                  PID(dv[4 - 1].getInput(), dv[4 - 1].getOutput(), dv[4 - 1].getSetpoint(), kp, ki, kd, DIRECT)};


ReadManchester rm = ReadManchester(2);
CommandReceiver cmdRec = CommandReceiver(dv, &rm);

void updateFreqEnco();


void setup() {

  /****************MANCHESTER SETUP***********/
  //pinMode(manchester_pin,INPUT);
  //pinMode(clk_pin, OUTPUT);
  /****************FIN************************/
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  attachInterrupt(digitalPinToInterrupt(dv[1 - 1].getPinEncoInterrup()), fctInterrupt1, RISING);
  attachInterrupt(digitalPinToInterrupt(dv[2 - 1].getPinEncoInterrup()), fctInterrupt2, RISING);
  attachInterrupt(digitalPinToInterrupt(dv[3 - 1].getPinEncoInterrup()), fctInterrupt3, RISING);
  attachInterrupt(digitalPinToInterrupt(dv[4 - 1].getPinEncoInterrup()), fctInterrupt4, RISING);

  
  for(int i = 0; i < NB_DRIVEMOTEUR; i++)
  {
    dv[i].driveMoteur(0, 0);
    listPID[i].SetMode(AUTOMATIC);
    listPID[i].SetOutputLimits(0, 2080);
  }

}

void loop() 
{

  cmdRec.process();  
  rm.getMaschesterBits();
  //readManchesterBit();
   
    for(int i = 0; i < NB_DRIVEMOTEUR; i++)
    {
        if(dv[i].isRunning() == 1)
        {
          updateFreqEnco();
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
      diffTime = listEndCounting[i] - listStartCounting[i];
      if(diffTime >= 9800)
      {
          dv[i].setInput(1000000*listNbTicks[i]/(listEndCounting[i] - listStartCounting[i]));
          listStartCounting[i] = listEndCounting[i];
          listNbTicks[i] = 0;
        }
  }
  
}



void readManchesterBit(){
  
  if(enableManchester){
    //Serial.print("on est dans le if");
    digitalWrite(clk_pin, HIGH);
    delay(32);
    //Serial.print("ici");
    code_Manchester = (code_Manchester << 1) + (digitalRead(manchester_pin) == 0);
    code_Manchester &= 0xFFFF;
    //Serial.print("ici");
    if((code_Manchester & 0xFF80) == 0xFF00){
      //Serial.print("ici");
      //Serial.print(code_Manchester, BIN);
    }
    digitalWrite(clk_pin, LOW);
    delay(32);
    
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




