#ifndef READMANCHESTER_CLASS
#define READMANCHESTER_CLASS

#include "BaseClass.h"
#include "MethodDescriptor.h"

class ReadManchester;

namespace nanpy {
    class ReadManchesterClass: public ObjectsManager<ReadManchester> {
        public:
            void elaborate( nanpy::MethodDescriptor* m );
            const char* get_firmware_id();
    };
}

#endif
