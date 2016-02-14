#include "cfg_all.h"

#if USE_ReadManchester

#include <Arduino.h>
#include <ReadManchester.h> //!!!Your real ReadManchester Library!!!!
#include "ReadManchesterClass.h"
#include <stdlib.h>

const char* nanpy::ReadManchesterClass::get_firmware_id()
{
    return "ReadManchester";
}

void nanpy::ReadManchesterClass::elaborate( MethodDescriptor* m ) {
    ObjectsManager<ReadManchester>::elaborate(m);

    if (strcmp(m->getName(),"new") == 0) {
        v.insert(new ReadManchester (m->getInt(0), m->getInt(1)));
        m->returns(v.getLastIndex());
    }

    if (strcmp(m->getName(), "getMaschesterBits") == 0) {
        m->returns(v[m->getObjectId()]->getMaschesterBits());
    }
    
    if (strcmp(m->getName(), "enableInterrupt") == 0) {
       v[m->getObjectId()]->enableInterrupt(m->getBool(0));
       m->returns(0);
    }

};

#endif
