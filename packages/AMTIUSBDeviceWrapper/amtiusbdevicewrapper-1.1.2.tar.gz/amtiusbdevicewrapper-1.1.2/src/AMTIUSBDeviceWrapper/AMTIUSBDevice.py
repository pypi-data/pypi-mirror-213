import ctypes as ct
import _ctypes as _ct
import time as _time
import warnings as _warnings
import atexit as _atexit
import numpy as np
from os import path as _path
import platform as plf


"""
Wrapper for AMTI USB Device library. Currently only supported on Windows Systems for 32 and 64 bit versions of the SDK.
Use 64 bit dll if running 64 bit python interpreter and vice versa with 32 bit dll.

Author: Jordy A. Larrea Rodriguez, Jordy.larrearodriguez@gmail.com, @CasuallyAlive -> Github
Date Created: 03/31/2023
Date Revised: 04/09/2023
version: 1.0
"""

def __dllShutDown():
    """DLL will no longer load in current process if called, only call when done with AMTI library in current process!
    """
    dll = AMTIUSBDevice._amti_dll

    if(dll and AMTIUSBDevice._init_status != AMTIUSBDevice.DLL_INIT_INACTIVE):
        AMTIUSBDevice._shutDownDLL()
        _time.sleep(0.5)
        AMTIUSBDevice.__del_handle__()

    print("DLL has been successfully been shut down.")

_atexit.register(__dllShutDown)

class AMTIUSBDevice:
    """Wrapper for AMTI USB Device SDK, abstracts sequential calls and allows for a more streamline interface
                for multiple platforms supported by the SDK. Currently only supports Gen5 platform.

    Raises:
        ValueError: _description_
        OSError: _description_
        ValueError: _description_
        ValueError: _description_
        OSError: _description_
        FileNotFoundError: _description_
        AssertionError: _description_
        AssertionError: _description_
        AssertionError: _description_
        AssertionError: _description_
        AssertionError: _description_
        TimeoutError: _description_
        NotImplementedError: _description_
        NotImplementedError: _description_
        ValueError: _description_
        OSError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        AssertionError: _description_
        AssertionError: _description_

    Returns:
        _type_: _description_
    """
    # static variables
    _amti_dll = None
    _dll_path = None
    _syst = None
    _dll_is_shutdown = False
    _init_status = 0
    _data_acquisition_status = False
    _os = None

    # Wrapper constants
    WRAPPER_DEF_DEVICE = 0
    WRAPPER_DATA_FORMAT_6 = 0
    WRAPPER_DATA_FORMAT_8 = 1

    # ERROR message constants
    PATH_ERROR = "Path for does not exist! Check that dependency paths are correct!"
    
    # Library specific path constants. del when done debugging (add parsing code that matches to AMTIUSBDevice and .dll within parameter path with validation checks)
    PATH_DLL = "./bin/AMTIUSBDevice - 64.dll"

    # System constants
    SYST = 64 # del when done debugging. 64 bit python uses 64 bit DLL and 32 bit python uses 32 bit DLL
    SUPPORTED_PLATFORMS = {"gen5"}
    SUPPORTED_OS = {"Windows", "Linux"}

    # DLL constants, refer to AMTI SDK
    ## DLL DEFAULTS
    DLL_DEF_RATE = 500
    DLL_DEF_DATA_FORMAT = (1, 8) # (1, 8) is the default data format with 1 -> 8 columns of data per sample.
    DLL_VALID_RATES = {2000, 1800, 1500, 1200, 1000, 900, 800, 600, 500, 450, 400, 360, 300, 250, 240, 225, 200, 180, 150,
                    125, 120, 100, 90, 80, 75, 60, 50, 45, 40, 30, 25, 20, 15, 10}
    DLL_PACKET_SIZE = 512
    DLL_PACKET_SET_NUM = 16
    ## DLL INIT statuses
    DLL_INIT_INACTIVE = 0
    DLL_INIT_COMPLETE_NULL = 1
    DLL_INIT_SUCCESS = 2
    ## DLL GENLOCK Modes
    DLL_GENLOCK_OFF = 0
    DLL_GENLOCK_RISING = 1
    DLL_GENLOCK_FALLING = 2
    ## DLL RUN Modes
    DLL_RUN_METRIC_MSA6 = 0
    DLL_RUN_METRIC_FC = 1
    DLL_RUN_ENGLISH_MSA6 = 2
    DLL_RUN_ENGLISH_FC = 3
    DLL_RUN_BITS_MSA6 = 4

    # Config constants
    ## Config statuses
    CONFIG_NO_DEVICES = 0
    CONFIG_MAINTAINED = 1
    CONFIG_NOT_FOUND = 211
    CONFIG_WRONG_SOFTWARE = 213
    CONFIG_CHANGED_NUM_DEVICES = 214
    CONFIG_CHANGED_SERIAL_MISMATCH = 215
    ## Config params
    CONFIG_CURRENT_GAINS = {500, 1000, 2000, 4000}
    CONFIG_CURRENT_EXCITATIONs = {2.5, 5.0, 10.0} # in Volts
    CONFIG_CHANNEL_OFFSET = [-0.99, 0.99] # mechanical range +- 99%, DEFAULT is 0
    CONFIG_PLATFORM_ROTATION = 0 # in degrees

    # Class constructors and destructors
 
    def __init__(self, platform:str, auto_save:bool=True):
        """Constructor for AMTIUSBDevice.

        Args:
            platform (str): type of AMTI platform being interfaced, either Gen5 or HE_Optima
            auto_save (bool, optional): specifies whether the instance attempts to save the AMTI Config file as it comes out of scope. 
            Defaults to True.

        Raises:
            ValueError
            OSError
        """
    
        self.auto_save = auto_save
        self.platform = platform
      
        self._init_status = AMTIUSBDevice.DLL_INIT_INACTIVE  
        self._config_status = None
        self._config_save_status = True # True implies the config file is up to date
        self._data_acquisition_status = False

        self.packet_size = None
        self.data_format = None
        self.rate = None

        self.run_mode = None
        self.genlock_mode = None

        self._sel_device = None            

        # Check if parameters are valid else throw appropriate value error
        if(not str.lower(self.platform) in AMTIUSBDevice.SUPPORTED_PLATFORMS):
            raise ValueError(f'Platform given is not supported! Either instantiate with "Gen5" or "HE_Optima". platform = {platform}')
        
        # Attempt to load library
        try:
            if(AMTIUSBDevice._amti_dll is None):
                AMTIUSBDevice.InitializeLibrary()

            self._amti_dll = AMTIUSBDevice.__getDLL()
        except OSError:
            raise OSError("Unable to load DLL!")


    def __del__(self):
        if(self._init_status != self.DLL_INIT_INACTIVE):
            self.__del_handle()

    @staticmethod
    def InitializeLibrary(syst:int=SYST, dll_path:str=PATH_DLL):
        """Loads library depending on OS at arg path.

        Args:
            syst (int, optional): specifies if using 32 or 64 bit system. Defaults to 64.
            dll_path (str, optional): file path of DLL. Defaults to PATH_DLL.

        Raises:
            ValueError: syst != 32 | 64.
            ValueError: DLL path does not exist.
            OSError: Using OS not supported by API.
            FileNotFoundError: File not found at path.
        """
        if(not (syst == 32 or syst == 64)):
            raise ValueError(f'System param must either be 32 or 64: syst = {syst}')
        if(not _path.exists(dll_path)):
            raise ValueError(f'{AMTIUSBDevice.PATH_ERROR[:9]} AMTI\'s dynamic-link library{AMTIUSBDevice.PATH_ERROR[8:]}')
        try:
            AMTIUSBDevice._amti_dll = ct.CDLL(dll_path) # AMTI DLL uses C calling convention (_cdecl)
            AMTIUSBDevice._os = plf.system()
            if(AMTIUSBDevice._os not in AMTIUSBDevice.SUPPORTED_OS):
                raise OSError("OS not supported by wrapper!")
            
            AMTIUSBDevice._syst = syst
            AMTIUSBDevice._dll_path = dll_path

        except FileNotFoundError:
            raise FileNotFoundError("Could not find DLL at stated directory!") # either FileNotFound or some IOError

    @staticmethod
    def __getDLL():
        if(not AMTIUSBDevice._dll_path and not AMTIUSBDevice._amti_dll):
            return None
        return ct.CDLL(AMTIUSBDevice._dll_path)
    
    @staticmethod
    def _shutDownDLL():
        """Shuts down and cleans up DLL on current process, can no longer use DLL once called.
        Automatically called on process exit.

        Returns:
            bool: True to signify successful shutdown of library.
        """
        if(not AMTIUSBDevice._dll_is_shutdown and AMTIUSBDevice._amti_dll):
            AMTIUSBDevice._amti_dll.fmDLLShutDown()
            AMTIUSBDevice._dll_is_shutdown = True
        return AMTIUSBDevice._dll_is_shutdown
    
    @staticmethod
    def __del_handle__():
        try:
            if(AMTIUSBDevice._os == "Windows"):
                _ct.FreeLibrary(AMTIUSBDevice._amti_dll._handle)
            else:
                _ct.dlclose(AMTIUSBDevice._amti_dll._handle)
        except OSError:
            return False

    def init(self, use_prev:bool=True, run_mode:int=DLL_RUN_METRIC_MSA6, genlock_mode:int=DLL_GENLOCK_OFF, rate:int=DLL_DEF_RATE,
            data_format_mode:int=DLL_DEF_DATA_FORMAT[0], sel_dev:int=WRAPPER_DEF_DEVICE):
        """Encapsulates function calls corresponding to the standard AMTI USB library initialization procedures: i.e., initializes DLL, 
        initializes wrapper, saves configuration file with input parameters if caller opts out of using previous configuration. 
        Assume that this library sets global run-mode, acquisition-rate and selects a default device via the Device Library if it succeeds.

        Args:
            use_prev (bool, optional): query use previous configuration. Defaults to True.
            run_mode (int, optional): configuration run mode. Defaults to DLL_RUN_METRIC_MSA6.
            genlock_mode (int, optional): configuration genlock mode. Defaults to DLL_GENLOCK_OFF.
            rate (int, optional): global acquisition rate, rate is set to closest supported rate. Defaults to DLL_DEF_RATE.
            data_format_mode (int, optional): data format mode. Defaults to DLL_DEF_DATA_FORMAT[0].

        Raises: // remove following testing
            AssertionError: _description_
            AssertionError: _description_
            AssertionError: _description_
            AssertionError: _description_
            AssertionError: _description_

        Returns:
            Tuple(bool, int): (True if configuration represents args (successful DLL initialization) else False, configuration status)
        """
        self.__assertIsDLLShutDown()
        # self.sample_size = sample_size
        
        config_status = self._initDLL() # get config_status and set self.config_status, may raise timeout error
        devices = self.getDeviceCount() # get # of connected devices and set self.devices
        self.setDataFormat(data_format_mode)
        
        if(use_prev and devices > 0):
            # Sets wrapper vars to config values
            self.selectDeviceIndex(self.WRAPPER_DEF_DEVICE) # Select the first device by default
            if(self.getDeviceIndex() != self.WRAPPER_DEF_DEVICE):
                raise AssertionError("Problem with selecting default device!")
            
            self.getRunMode()
            self.getGenlock()
            self.getAcquisitionRate()
            self.setPacketSize() # Set global packet size to default of 512 bytes

            return self.setupCheck() == self.CONFIG_MAINTAINED, self._config_status
        
        # Unit Test This!
        if(config_status != self.CONFIG_NO_DEVICES and self._init_status == self.DLL_INIT_SUCCESS and devices > 0):
            
            self.setPacketSize() # Set global packet size to default of 512 bytes
            
            self.broadcastRunMode(run_mode) # Set global run-mode
            
            self.selectDeviceIndex(sel_dev) # Select the first device by default
            
            self.broadcastGenlock(genlock_mode) # Set global genlock-mode

            success, newRate = self.broadcastAcquisitionRate(rate)  # Set global acquisition rate

            if(not success):
                self.broadcastAcquisitionRate(newRate)
                rate = newRate
             
            if(not self.saveConfig() or not self.broadcastResetSoftware()): # load configuration settings onto devices (temporarily)
                return False, self._config_status
            
            if(self.getAcquisitionRate() != rate): # Verifies new acquisition rate
                _warnings.warn("Problem with setting global acquisition rate!")
                return False, self._config_status
            if(self.getRunMode() != run_mode): # Sets self.run_mode
                _warnings.warn("Problem with setting global run-mode!")
                return False, self._config_status
            if(self.getDeviceIndex() != self.WRAPPER_DEF_DEVICE): # Verifies selected device is default val
                _warnings.warn("Problem with selecting default device!")
                return False, self._config_status
            if(self.getGenlock() != genlock_mode): # Verifies new genlock_mode
                _warnings.warn("Problem with setting global genlock-mode!")
                return False, self._config_status
            
            return True, self._config_status

        return False, self._config_status

    # DLL methods, The fmDLL prefix indicates the function has to do with the current configuration settings of the DLL, 
    # not the signal conditioners.
   
    def isDLLInitComplete(self):
        """Wrapper call for fmDLLIsDeviceInitComplete.

        Returns:
            int: 0 if the DLL hasn't finished initializing, 1 if DLL initialized and no devices are present, and 2 if DLL is initiatized.
        """
        self.__assertIsDLLShutDown()
        return self._amti_dll.fmDLLIsDeviceInitComplete()
    
    def _initDLL(self):
        """Wrapper call for fmDLLInit. Calls DLL to initialize and load configuration file.

        Raises:
            TimeoutError: raised after 5 seconds have elapsed indicating a failed initialization of the DLL.

        Returns:
            int: config setup code.
        """
        self.__assertIsDLLShutDown()
        self._amti_dll.fmDLLInit()
        _time.sleep(0.250) # Wait 250 ms for AMTI library to setup with configuration file, refer to AMTI SDK reference.

        status = self.isDLLInitComplete()
        
        s = _time.time()
        while status == self.DLL_INIT_INACTIVE:
            status = self.isDLLInitComplete()
            if(_time.time() - s > 5):
                raise TimeoutError("Timeout Error! Could not verify that device initiation was successful after 5 seconds. Check hardware and try again.")
        
        self._init_status = status
        AMTIUSBDevice._init_status = status
        return self.setupCheck()

    def setupCheck(self):
        """wrapper call for fmDLLSetupCheck. Compares the last saved DLL configuration file to the current DLL setup 
        and notes any changes or discrepancies which may need attending.

        Returns:
            int: 0 if no Devices were found, 1 if current setup is the same as the last saved config, 211 if config file not found, 
            213 if a config file was found for the wrong ver of the software, 214 if the config has changed: # of devices 
            different from prev saved setup, and 215 if the config has changed: serial #'s of devices don't match the previously 
            saved setup.
        """
        if(self.checkDataAcquisitionStatus()):
            return self._config_status
        
        self._config_status = self._amti_dll.fmDLLSetupCheck() if not AMTIUSBDevice._dll_is_shutdown else self._config_status
        # File is saved if the setup is the same as the last saved config and there are devices present.
        self._config_save_status = self._config_save_status and (self._config_status == self.CONFIG_MAINTAINED or self._config_status == self.CONFIG_NO_DEVICES)
        return self._config_status
    
    def setPacketSize(self):
        """Wrapper call for fmDLLSetUSBPacketSize. Calls DLL to set packet size to default value of 512 bytes.
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        
        if(self.checkDataAcquisitionStatus()):
            return 
        
        size = ct.c_int(self.DLL_PACKET_SIZE)
        self.packet_size = size.value
        self._amti_dll.fmDLLSetUSBPacketSize(self.packet_size)

    def setDataFormat(self, mode:int):
        """ Wrapper call for fmDLLSetDataFormat.

        Args:
            mode (int): 0 -> {Fxyz, Mxyz}; 6 channels of data, 1 -> {frame#, Fxyz, Mxyz, Trigger}; 8 channels of data
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        
        if(self.checkDataAcquisitionStatus()):
            return 
        
        self.data_format = (mode, 8) if mode else (mode, 6)
        self._amti_dll.fmDLLSetDataFormat(ct.c_int(mode))
        self.setupCheck()

    # methods for selected device

    def saveDeviceSettings(self):
        """This function saves the current signal conditioner software settings to non-volatile memory for the currently selected signal conditioner.
            The saved settings are restored whenever the signal conditioner is powered on.

        Returns:
            bool: True if save succeeded, else False.
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        
        if(self.checkDataAcquisitionStatus()):
            return False 
        
        try:
            self._amti_dll.fmSave()
        except:
            return False
        
        _time.sleep(0.5)
        return True
    
    def saveDeviceZeroSettings(self):
        """This function saves the current hardware zero settings to the signal conditioner flash memory. 
            When the signal conditioner is powered on these zero settings will automatically be loaded.

        Returns:
            bool: True if save succeeded, else False
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        
        if(self.checkDataAcquisitionStatus()):
            return False 
        try:
            self._amti_dll.fmApplyLimited()
        except:
            return False
        
        return True
        
    def resetDeviceSoftware(self):
        """This function resets the software state of the currently selected signal conditioner
            When new signal conditioner settings are downloaded, the changes are not implemented until this function is called. 
            First make all the configuration changes (excitations, gains, acquisition rate, etc.), then call this function for the changes to be applied.

        Returns:
            bool: True if reset succeeded, else False
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        
        if(self.checkDataAcquisitionStatus()):
            return False 
        try:
            self._amti_dll.fmResetSoftware()
        except:
            return False
        
        _time.sleep(0.5)
        return True
        

    # Call back methods
    
    def enablePostDataReadyMessages(self, mode:bool):
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        if(self.checkDataAcquisitionStatus()):
            return 

        self.messages_enabled = mode
        mode = ct.c_int(mode)
        self._amti_dll.fmDLLPostDataReadyMessages(mode)
    
    """
    fmDLLPostUserThreadMessages(unsigned int threadID)
    """
    def postUserThreadMessages(self):
        raise NotImplementedError("Function not implemented!")

    """
    fmDLLPostWindowMessages(HWND handle)
    """
    def postWindowMessages(self):
        raise NotImplementedError("Function not implemented!")

    
    def selectDeviceIndex(self, device_index:int):
        """Wrapper call for fmDLLSelectDeviceIndex. Sets DLL to select Device with ID 'device_index'. 
        Required in order to use broadcast type functions or for further AMTI USB device interfacing (signal conditioner specific functions). 
        *ZERO INDEXED*!

        Args:
            device_index (int): Index of device to be selected as head. *Zero Indexed*

        Raises:
            ValueError: If device_index exceeds the number of connected devices.

        Returns:
            bool: True if device is selected successfully, else False.
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return False
        if(self.__checkIsInitCheck()):
            return False
        if(device_index < 0 or device_index > self.devices - 1):
            raise ValueError(f'Expected a valid index number for the device index, received: {device_index}.')
        
        i = ct.c_int(device_index)
        try:
            self._amti_dll.fmDLLSelectDeviceIndex(i)
            self._sel_device = device_index
        except:
            return False
        
        return True 
   
    def saveConfig(self):
        """ Wrapper call for fmDLLSaveConfiguration.
        Returns:
            bool: True if file saved successfully else False.
        """
        if(self.checkDataAcquisitionStatus() or AMTIUSBDevice._dll_is_shutdown):
            return False
        if(self.__checkIsInitCheck()):
            self._config_save_status = True
            return self._config_save_status
        
        self._config_save_status = self._amti_dll.fmDLLSaveConfiguration() == 1
        self.setupCheck()
        return self._config_save_status
    

    def blinkDevice(self):
        """Blinks the front panel lamp on the currently selected signal conditioner for 10 seconds.
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return
        if(self.__checkIsInitCheck()):
            return
        self._amti_dll.fmSetBlink()
        
    def __del_handle(self):
        """attempts to save config if config is not saved after instance is garbage collected.
                         *CALLED WHEN INSTANCE IS GARBAGE COLLECTED* 

        Raises:
            OSError: if an OSError is raised from closing DLL handle.
        """
        self.setupCheck()
        if(self.checkDataAcquisitionStatus() and not AMTIUSBDevice._dll_is_shutdown):
            # data = self.getData()
            self.broadcastStop()

        if((not self._config_save_status) and self.auto_save):
            self.saveConfig() # attempt to save the current config file if it's been changed
        if(self._amti_dll is not None):
            try:
                if(AMTIUSBDevice._os == "Windows"):
                    _ct.FreeLibrary(self._amti_dll._handle)
                else:
                    _ct.dlclose(self._amti_dll._handle)
            except OSError:
                raise OSError("Unable to close the DLL handle.")
        
    # DLL get methods, associated instance variables continuously updated to values returned from DLL.
    # Methods return -1 if DLL configuration is not initialized.
       
    def getDeviceCount(self):
        """Wrapper call for fmDLLGetDeviceCount(), gets number of devices connected to DLL
        following DLL initialization.

        Returns:
            int: number of connected devices.
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return self.devices
        if(self.__checkIsInitCheck()):
            return -1
        self.devices = self._amti_dll.fmDLLGetDeviceCount()
        return self.devices

    def getDeviceIndex(self):
        """Wrapper call for fmDLLGetDeviceIndex.

        Returns:
            int: currently selected device. *Zero Indexed*
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return self._sel_device
        if(self.__checkIsInitCheck()):
            return -1
        self._sel_device = self._amti_dll.fmDLLGetDeviceIndex()
        return self._sel_device
    
    def getGenlock(self):
        """Wrapper call for fmDLLGetGenlock.

        Returns:
            int: current genlock mode on DLL configuration settings.
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return self.genlock_mode
        if(self.__checkIsInitCheck()):
            return -1
        
        self.genlock_mode = self._amti_dll.fmDLLGetGenlock()
        return self.genlock_mode
    
    def getRunMode(self):
        """Wrapper call for fmDLLGetRunMode, returns 
        Returns:
            int: current run mode on DLL configuration settings.
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return self.run_mode
        if(self.__checkIsInitCheck()):
            return -1
        
        self.run_mode = self._amti_dll.fmDLLGetRunMode()
        return self.run_mode
    
    def getAcquisitionRate(self):
        """Wrapper call for fmDLLGetAcquisitionRate.

        Returns:
            int: current acquisition rate of selected signal conditioner.
        """
        self.__assertIsDLLShutDown()
        if(self.checkDataAcquisitionStatus()):
            return self.rate
        if(self.__checkIsInitCheck()):
            return -1
        
        self.rate = self._amti_dll.fmDLLGetAcquisitionRate()
        return self.rate
    
    def getDataBufferSize(self):
        """Calculates and returns size of buffer given known parameters.

        Returns:
            int: buffer_size = #channels_per_dataset * #devices * #datasets_per_device
        """
        if(not (self.data_format or self.devices)):
            return -1
        
        return int(self.data_format[1] * self.devices * self.DLL_PACKET_SET_NUM)

    # Data acquisition functions, return empty numpy array on failure instead of -1.

    def getData(self, opt:int=1, format_mode=1):
        """Acquires data chunks from AMTI API. User has the choice to either allocate buffers externally on the API (opt=0) or internally 
        through the wrapper (opt=1 -> default). Furthermore, the user can choose to either get a formatted data chunk or the raw data 
        in a one dimensional array. Sample: singular data packet.

        Args:
            opt (int, optional): 0 -> external memory allocation on C++ compiled API, 1 -> internal memory within wrapper. Defaults to 1.
            format_mode (int, optional): 0 -> raw data (shape = #channels_per_dataset*#samples*#datasets_per_device*#devices, 1), 
            1 -> formatted data (shape = #samples*#datasets_per_device, #channels_per_dataset*#devices), 
            data = {{Frame0_0, Frame1_0, Frame2_0},{Frame0_1, Frame1_1, Frame2_1}, ...}. Defaults to 1.

        Raises:
            ValueError: _description_

        Returns:
            numpy array: data chunk consisting of available data packets across synchronized devices.
        """
        if(opt > 1 or opt < 0):
            raise ValueError(f"opt must either be a 0 or a 1! Received: {format_mode}")
        if(not AMTIUSBDevice._data_acquisition_status or self.__checkIsInitCheck()):
            return np.empty(0)
        
        data_func = self._getDataInt if opt == 1 else self._getDataExt
        
        return data_func(format_mode)
        
    def _getDataExt(self,format_mode=1):
        """Data buffers are allocated on the DLL's end; thus, this version of the transfer float data function does not allocate memory.
        Instead, it returns a pointer to the data buffer. The DLL is responsible for freeing allocated buffers.

        Args:
            format_mode (int, optional): either get raw data as received from DLL or in user-friendly format. Defaults to 1 -> user-friendly.

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            numpy array: data chunk consisting of available data packets across synchronized devices.
        """
        self.__assertIsDLLShutDown()
        if(type(format_mode) is not int and type(format_mode) is not bool):
            raise ValueError(f"get_raw_data must be an int or bool! Received: {format_mode}")
        
        format_mode = int(format_mode)
        
        if(format_mode > 1 or format_mode < 0):
            raise ValueError(f"opt must either be a 0 or a 1! Received: {format_mode}")
        if(not AMTIUSBDevice._data_acquisition_status or self.__checkIsInitCheck()):
            return np.empty(0), 0
                    
        data_buffer_size = self.getDataBufferSize()
        
        sample_ref = ct.c_float()
        
        data_ptr = ct.pointer(sample_ref)
        data = list()
        sample_num = 0

        # Send float pointer by ref.
        while self._amti_dll.fmDLLTransferFloatData(ct.byref(data_ptr)) > 0:
            
            samples = list([data_ptr[i] for i in range(data_buffer_size)])
            
            data.extend(samples)
            sample_num+=1

        del data_ptr

        data = np.array(data)
        
        if(format_mode == 0):
            return data
        
        dim = (sample_num*self.DLL_PACKET_SET_NUM, self.devices*self.data_format[1])
        
        data = np.reshape(data, dim)
        
        return data, sample_num
    
    def _getDataInt(self, get_raw_data=1):
        """Data buffers are allocated internally; thus, this version of the transfer float data function allocates memory within the wrapper.

        Args:
            get_raw_data (int, optional): either get raw data as received from DLL or in user-friendly format. Defaults to 1 -> user-friendly.


        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            numpy array: data chunk consisting of available data packets across synchronized devices.
        """
        self.__assertIsDLLShutDown()
        if(type(get_raw_data) is not int and type(get_raw_data) is not bool):
            raise ValueError(f"get_raw_data must be an int or bool! Received: {get_raw_data}")
        
        get_raw_data = int(get_raw_data)
        
        if(get_raw_data > 1 or get_raw_data < 0):
            raise ValueError(f"opt must either be a 0 or a 1! Received: {get_raw_data}")
        if(not AMTIUSBDevice._data_acquisition_status or self.__checkIsInitCheck()):
            return np.empty(0), 0
        
        
        data_buffer_size = self.getDataBufferSize()

        samples_arr = np.zeros(data_buffer_size,dtype=np.float32) # Make array of size dettermined by buffer_size for floats.

        data_ptr = ct.pointer((ct.c_float*data_buffer_size)(*samples_arr)) # Make float pointer to np array
        data = list()
        sample_num = 0

        buf_byte_size = data_buffer_size*ct.sizeof(ct.c_float)
        
        # Send pointer to array allocated by caller.
        while self._amti_dll.fmDLLGetTheFloatDataLBVStyle(data_ptr, buf_byte_size) > 0:
            if(data_ptr._objects is None or len(data_ptr._objects) < 2):
                continue
            # Get keys to access data
            temp = list(data_ptr._objects.keys())
            # Unit Test this
            samples = list([data_ptr._objects[temp[0]][i] for i in range(data_buffer_size)])

            data.extend(samples)
            sample_num+=1
            
        del data_ptr
        del samples_arr

        data = np.array(data)
        if(get_raw_data == 0):
            return data
        
        dim = (sample_num*self.DLL_PACKET_SET_NUM, self.devices*self.data_format[1])
        
        data = np.reshape(data, dim)
            
        return data, sample_num
        
    # Broadcast methods: set global settings for all interfaced AMTI devices, updates instance vals.

    def broadcastRunMode(self, mode:int):
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        if(self.checkDataAcquisitionStatus()):
            return
        if(mode < 0 or mode > 4):
            raise ValueError(f'Expected mode between 0 and 4, received: {mode}.')
        
        input = ct.c_int(mode)
        self._amti_dll.fmBroadcastRunMode(input)

        self.run_mode = mode
        
        self.setupCheck()
    
    def broadcastGenlock(self, mode:int):
        self.__assertIsDLLShutDown
        self.__assertIsInitCheck()
        if(self.checkDataAcquisitionStatus()):
            return
        if(mode < 0 or mode > 2):
            raise ValueError(f'Expected mode between 0 and 2, received: {mode}.')
        
        input = ct.c_int(mode)
        self._amti_dll.fmBroadcastGenlock(input)
        
        self.genlock_mode = mode

        self.setupCheck()

    def broadcastAcquisitionRate(self, rate:int=DLL_DEF_RATE):
        """Broadcasts the argument rate to all signal conditioners given that the rate is supported by
            the signal conditioners. If the argument rate is not supported, then the rate nearest to the
            argument rate is returned as the second argument of the returned tuple. Does not require a call to reset-software or
            save-device-settings methods. Applied on next broadcast-start command. 

            SUPPORT RATES: [2000, 1800, 1500, 1200, 1000, 900, 800, 600, 500, 450, 400, 360, 300, 250, 240, 225, 200, 180, 150,
                    125, 120, 100, 90, 80, 75, 60, 50, 45, 40, 30, 25, 20, 15, 10] // in Hz

        Args:
            rate (int, optional): acquisition rate to broadcast. Defaults to DLL_DEF_RATE.

        Returns:
            Tuple[:bool:, :int:]: (broadcast successful, nearest rate)
        """
        self.__assertIsDLLShutDown
        self.__assertIsInitCheck()
        if(self.checkDataAcquisitionStatus()):
            return
        if(not rate in self.DLL_VALID_RATES):
            # If param rate is not valid, then inform of unsuccessful rate selection and return closest valid rate.
            closest_rate = min([(val, abs(rate - val)) for val in self.DLL_VALID_RATES], key= lambda v: v[1])
            return False, closest_rate[0]
                
        input = ct.c_int(rate)
        self._amti_dll.fmBroadcastAcquisitionRate(input)
        
        self.rate = rate

        self.setupCheck()
        return True, None   
    
   
    def broadcastStart(self):
        """wrapper call for fmBroadcastStart. Starts data acquisition from all registered signal conditioners. ...
            Any other method called after broadcastStart (except for broadcastZero) will automatically stop acquisition. ... 
            This is to preserve signal conditioner synchronization. The formal stop acquisition function is broadcastStop. ...
            *Note that when genlock mode is active, data will not be sent from a signal conditioner to interface until the...
            genlock pulses start to arrive at the signal conditioner's genlock port.*
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()

        AMTIUSBDevice._data_acquisition_status = True
        self._data_acquisition_status = AMTIUSBDevice._data_acquisition_status
        
        self._amti_dll.fmBroadcastStart()
        
        self.broadcastZero()
    
    def broadcastStop(self):
        """Wrapper call for fmBroadcastStop. Stops data acquisition from all registered signal conditioners.
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        
        AMTIUSBDevice._data_acquisition_status = False
        self._data_acquisition_status = AMTIUSBDevice._data_acquisition_status
        
        self._amti_dll.fmBroadcastStop()
        _time.sleep(0.250)
    
    def broadcastZero(self):
        """Wrapper call for fmBroadcastZero. Signals registered signal conditioners to zero their platforms. ...
                         This method may be called before calling broadcastStart or during data collection. Data collected
                         while platforms are being zeroed will consist of all zeros. 
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()

        self._amti_dll.fmBroadcastZero()
        _time.sleep(0.5) # Wait for zeroing to complete before returning.

    def broadcastSave(self):
        """This function saves the current signal conditioner software settings to non-volatile memory for all attached signal conditioners. 
                The saved settings are restored whenever the signal conditioner is powered on.
                
                *Note: The flash chip in the signal conditioner is rated for 20000 to 50000 writes, to it is best to make 
                all necessary configuration changes and then save.*
            Returns:
                bool: True if save succeeded, else False
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        if(self.checkDataAcquisitionStatus()):
            return

        try:
            self._amti_dll.fmBroadcastSave()
        except:
            return False
        
        _time.sleep(0.5) # wait for new software settings to save.
        return True

    def broadcastResetSoftware(self):
        """Temporarily saves configuration settings (resets software state) on all signal conditioners. 
            When new signal conditioner settings are downloaded, the changes are not implemented until this function is called. 
            First make all the configuration changes (excitations, gains, acquisition rate, etc.), then call this function for the changes to be applied.
        Returns:
            bool: True if save succeeded, else False
        """
        self.__assertIsDLLShutDown()
        self.__assertIsInitCheck()
        if(self.checkDataAcquisitionStatus()):
            return False
        try:
            self._amti_dll.fmBroadcastResetSoftware()
        except:
            return False
        
        _time.sleep(0.5)
        return True
    
    # Assertion functions to prevent calls to dll when undefined behavior is possible.

    def checkDataAcquisitionStatus(self):
        if(AMTIUSBDevice._data_acquisition_status):
            _warnings.warn("Data streaming from force platform is currently active, call 'broadcastStop' to stop data acquistion. Call to DLL did not go through.") 

        return AMTIUSBDevice._data_acquisition_status
    
    def __checkIsInitCheck(self):
        if(self._init_status == self.DLL_INIT_INACTIVE):
            _warnings.warn("DLL has not been initialized, please initialize DLL before using AMTI library. Call to DLL did not go through.") 

        return self._init_status == self.DLL_INIT_INACTIVE
    
    def __assertIsInitCheck(self):
        if(self._init_status == self.DLL_INIT_INACTIVE):
            raise AssertionError("AMTI DLL has not been properly initialized!")

    def __assertIsDLLShutDown(self):
        if(AMTIUSBDevice._dll_is_shutdown):
            raise AssertionError("AMTI DLL has been shut down, can not call DLL functions. Restart the process, to use the DLL once again!")
    