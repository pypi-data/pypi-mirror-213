import time as _time
import numpy as np
from AMTIUSBDeviceWrapper import AMTIUSBDevice as amti

amti.AMTIUSBDevice.InitializeLibrary(dll_path="./tests/bin/AMTIUSBDevice - 64.dll")
a = amti.AMTIUSBDevice("gen5")

TEST_RATE = 2000

setup_maintained, config_code = a.init()

if(not setup_maintained):
    a.saveConfig()

a.broadcastAcquisitionRate(rate=TEST_RATE)
a.broadcastResetSoftware()

print(f"Device registered rate: {a.getAcquisitionRate()}")

a.broadcastStart()

samples = 0

for i in range(0, 10):
    _time.sleep(0.1)
    
    _, b = a.getData(opt=1)
    samples += b

a.broadcastStop()

print(f"Samples collected in one second: {samples}")
print(f"Aproximate sampling frequency in Hz: {samples*amti.AMTIUSBDevice.DLL_PACKET_SET_NUM}")
    
del a
