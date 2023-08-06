import unittest
import time as _time
import numpy as np
from AMTIUSBDeviceWrapper import AMTIUSBDevice as amti

amti.AMTIUSBDevice.InitializeLibrary(dll_path="./tests/bin/AMTIUSBDevice - 64.dll")

class TestAMTIUSBDevice(unittest.TestCase):
    deviceNum = 3
    it = 20
    
    def test_init_default(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        self.assertTrue(a.isDLLInitComplete() == a.DLL_INIT_SUCCESS and a.setupCheck() == a.CONFIG_MAINTAINED and
                a._config_save_status)
        del a
        
    def test_getdevices(self):
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        self.assertEqual(a.getDeviceCount(), TestAMTIUSBDevice.deviceNum)
        
    def test_init_default_define_dll_directory(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        self.assertTrue(a.isDLLInitComplete() == a.DLL_INIT_SUCCESS and a.setupCheck() == a.CONFIG_MAINTAINED and
                a._config_save_status)
        del a
        
    # @unittest.skip("Skip")
    def test_getdataint_get_values(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        a.broadcastStart()
        val = None
        cols = 8*a.getDeviceCount()
        
        try:
            self.assertTrue(a._data_acquisition_status)
            val, samples = a._getDataInt()
            
            self.assertTrue(val is not None)
            self.assertTrue(val.size is not None and val.shape[1] == cols)
            self.assertTrue(samples > 0 and val.shape[0] == samples*a.DLL_PACKET_SET_NUM)
        except Exception as e:
            a.broadcastStop()
            del a

            self.fail("Exception caught while capturing data, test Failed!")
       
        a.broadcastStop()
        
        self.assertTrue(not a._data_acquisition_status)
        # self.assertTrue(a._getDataInt().size == 0)
        
    def test_getdataint_get_many_values(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        a.broadcastStart()
        val = None
        cols = 8*a.getDeviceCount()
        
        for i in range(TestAMTIUSBDevice.it):
            try:
                self.assertTrue(a._data_acquisition_status)
                val, samples = a._getDataInt()
                
                self.assertTrue(val is not None)
                self.assertTrue(val.size is not None and val.shape[1] == cols)
                self.assertTrue(samples > 0 and val.shape[0] == samples*a.DLL_PACKET_SET_NUM)
            except Exception as e:
                a.broadcastStop()
                del a

                self.fail("Exception caught while capturing data, test Failed!")
            
            _time.sleep(0.05)
            
        a.broadcastStop()
        
        self.assertTrue(not a._data_acquisition_status)
        # self.assertTrue(a._getDataInt().size == 0)
    
    def test_getdataext_get_values(self):
       
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        a.broadcastStart()
        
        val = None
        cols = 8*a.getDeviceCount()
        
        try:
            self.assertTrue(a._data_acquisition_status)
            val, samples = a._getDataExt()
            
            self.assertTrue(val is not None)
            self.assertTrue(val.size is not None and val.shape[1] == cols)
            self.assertTrue(samples > 0 and val.shape[0] == samples*a.DLL_PACKET_SET_NUM)
        except Exception as e:
            a.broadcastStop()
            del a

            self.fail("Exception caught while capturing data, test Failed!")
       
        a.broadcastStop()
        
        self.assertTrue(not a._data_acquisition_status)
        # self.assertTrue(a._getDataExt().size == 0)
        
    def test_getdataext_get_many_values(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        a.broadcastStart()
        val = None
        cols = 8*a.getDeviceCount()
        
        for i in range(TestAMTIUSBDevice.it):
            try:
                self.assertTrue(a._data_acquisition_status)
                val, samples = a._getDataExt()
                
                self.assertTrue(val is not None)
                self.assertTrue(val.size is not None and val.shape[1] == cols)
                self.assertTrue(samples > 0 and val.shape[0] == samples*a.DLL_PACKET_SET_NUM)
                
            except Exception as e:
                a.broadcastStop()
                del a

                self.fail("Exception caught while capturing data, test Failed!")
            
            _time.sleep(0.05)
            
        a.broadcastStop()
        
        self.assertTrue(not a._data_acquisition_status)
        # self.assertTrue(a._getDataExt().size == 0)
    
    # Caller allocates memory for the data
    def test_getdata_option1(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        a.broadcastStart()
        val = None
        cols = 8*a.getDeviceCount()
        
        try:
            self.assertTrue(a._data_acquisition_status)
            val, samples = a.getData(opt=1)
            
            self.assertTrue(val is not None)
            self.assertTrue(val.size is not None and val.shape[1] == cols)
            self.assertTrue(samples > 0 and val.shape[0] == samples*a.DLL_PACKET_SET_NUM)
        except Exception as e:
            a.broadcastStop()
            del a

            self.fail("Exception caught while capturing data, test Failed!")
       
        a.broadcastStop()
        
        self.assertTrue(not a._data_acquisition_status)
        # self.assertTrue(a.getData(opt=1).size == 0)
        
    # Callee allocates memory for the data
    def test_getdata_option0(self):
        
        a = amti.AMTIUSBDevice("gen5")
        a.init()
        a.broadcastStart()
        val = None
        cols = 8*a.getDeviceCount()
        
        try:
            self.assertTrue(a._data_acquisition_status)
            val, samples = a.getData(opt=0)
            
            self.assertTrue(val is not None)
            self.assertTrue(val.size is not None and val.shape[1] == cols)
            self.assertTrue(samples > 0 and val.shape[0] == samples*a.DLL_PACKET_SET_NUM)
        except Exception as e:
            a.broadcastStop()
            del a

            self.fail("Exception caught while capturing data, test Failed!")
       
        a.broadcastStop()
        
        self.assertTrue(not a._data_acquisition_status)
        # self.assertTrue(a.getData(opt=0).size == 0)
    
    @unittest.skip("Skipping this test until save setting methods are implemented")
    def test_init_new_params(self):
        a = amti.AMTIUSBDevice("gen5")
        a.init(use_prev=False, run_mode=a.DLL_RUN_METRIC_MSA6, genlock_mode=a.DLL_GENLOCK_OFF, rate=2000, data_format_mode=0)
        
        self.assertEqual(a.isDLLInitComplete(), a.DLL_INIT_SUCCESS)
        del a

if __name__ == '__main__':
    unittest.main()
