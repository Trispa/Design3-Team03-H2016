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

#include "ReadManchester.h"

//DriveMoteur dv[4] = {DriveMoteur(4,18, 46, 47), DriveMoteur(5,19, 48, 49), DriveMoteur(6,20, 50, 51), DriveMoteur(7,21, 52, 53)};


ReadManchester rm =  ReadManchester(2,3);
CommandReceiver cmdR = CommandReceiver(&rm);



char* maChaine;

void setup() {
  Serial.begin(9600);
  
  
  /*for(int i = 0; i < NB_DRIVEMOTEUR; i++)
    dv[i].driveMoteur(0.2, 0);
  dv[0].driveMoteur(0.2, 0);
  dv[3].driveMoteur(0.2, 1);
  */
}

void loop() 
{
  
  //cmdR.process();
  
  maChaine = rm.getMaschesterBits();
  if(maChaine != '\0')
  Serial.println(maChaine);
  
  /*for(int i = 0; i < NB_DRIVEMOTEUR; i++)
  {
      if(cmdRec.dm[i].isRunning())
      {
        cmdRec.dm[i].asservissement();
      }
  }
  */

}


