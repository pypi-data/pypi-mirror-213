import time as _time
import numpy as np
from AMTIUSBDeviceWrapper import AMTIUSBDevice as amti

amti.AMTIUSBDevice.InitializeLibrary(dll_path="./tests/bin/AMTIUSBDevice - 64.dll")
a = amti.AMTIUSBDevice("gen5")

a.init()
_time.sleep(5.0)
index = int()
while True:
    a.selectDeviceIndex(index)
    a.blinkDevice()
    _time.sleep(10.0)
    index = index + 1 if index < 2 else int()