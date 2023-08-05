import ctypes
import enum
import os
import sys
import logging
import time
from pkg_resources import resource_stream
from collections import deque
import threading
from re import search
from enum import IntEnum

########################################################################################################
#               ENUMERATIONS                                                                           #
########################################################################################################
#enumeration list for known registers for Sentio products
class StateMachineStates(IntEnum):
    INITIALIZE = 0
    CONNECTING = 1
    CONNECTED = 2

    GET_DEVICE_LIST = 10
    WAITING_DEVICE_LIST = 11

    START_UPDATE = 20
    UPDATING = 21

    DISCONNECT = 98
    ERROR = 99
    DONE = 100
    

#Enumeration
class RAPI_WKD_STATUS(enum.IntEnum):
	RAPI_WDK_STATUS_FINDING_SERVER = 0
	RAPI_WDK_STATUS_485BUS_CONNECTING = 1
	RAPI_WDK_STATUS_YTUN_CONNECTING_SERVER = 2
	RAPI_WDK_STATUS_YTUN_CONNECTING_DEVICE = 3
	RAPI_WDK_STATUS_YTUN_AUTHENTICATING = 4
	RAPI_WDK_STATUS_YTUN_BAD_KEY = 5
	RAPI_WDK_STATUS_OPENING_ROXI_SESSION = 6
	RAPI_WDK_STATUS_READY = 7
	RAPI_WDK_STATUS_FAULT_BOOTLOADER = 8
	RAPI_WDK_STATUS_FAULT_GENERAL = 9
	RAPI_WDK_STATUS_CLOSED = 10

class RAPI_WKD_DIRECT_UPDATE_STATUS(enum.IntEnum):
    RAPI_DUS_FAIL = 0                    #Error occured. 
    RAPI_DUS_SUCCESFULL_FINISHED = 1     #Update finished succesfully
    RAPI_DUS_TIMEOUT = 2                 #Reconnect to CCU after reboot timed out
    RAPI_DUS_ERROR = 3                   #Device rejected update and returns result code
    RAPI_DUS_CONNECTING = 4              #Trying to connect to device
    RAPI_DUS_SWITCHING_BOOTLOADER = 5    #Device is switching to bootloader mode
    RAPI_DUS_UPDATING = 6                #Device is busy with updating procedure
    RAPI_DUS_SWITCHING_APPLICATION = 7   #Device is switching to aplication after update

firmware_update_status = {
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_FAIL                     : "RAPI_DUS_FAIL",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_SUCCESFULL_FINISHED      : "RAPI_DUS_SUCCESFULL_FINISHED",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_TIMEOUT                  : "RAPI_DUS_TIMEOUT",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_ERROR                    : "RAPI_DUS_ERROR",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_CONNECTING               : "RAPI_DUS_CONNECTING",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_SWITCHING_BOOTLOADER     : "RAPI_DUS_SWITCHING_BOOTLOADER",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_UPDATING                 : "RAPI_DUS_UPDATING",
    RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_SWITCHING_APPLICATION    : "RAPI_DUS_SWITCHING_APPLICATION"
}
	
########################################################################################################
#                     STRUCTURES                                                                       #
########################################################################################################
#Global structure definitions
class Struct_roxi_api_wdk_direct_update_device_list(ctypes.Structure):
    _fields_ = [
        ("dIndex", ctypes.c_uint32),
        ("serial_number", (ctypes.c_char * 19)),
        ("room", ctypes.c_int),
        ("connection_status", ctypes.c_int),
        ("curent_version", (ctypes.c_char * 128)),
        ("available_version", (ctypes.c_char * 128)),
        ("firmware_status", ctypes.c_int)]

########################################################################################################
#               Global Functions                                                                       #
########################################################################################################
#Global definitions
MAX_TIME_NO_UPDATE_DEFAULT = 10 #10 seconds since no update is critical error!


#global variables
mState = 0
mDeviceList = []
mLastTick = 0
mWatchdogTimeout = MAX_TIME_NO_UPDATE_DEFAULT


#Global state machine functions
def getMState():
    global mState
    return mState

def setMState(state, init=False):
    global mState
    if not init: #all messages transfered in init state should not be logged yet due to initalization of the library not yet complete
        logging.info("Update state to {0}".format(StateMachineStates(state).name))
    mState = state

def mStateEquals(state):
    global mState
    return mState == state

def setDeviceList(deviceList):
    global mDeviceList
    mDeviceList = deviceList

def getDeviceList():
    global mDeviceList
    return mDeviceList

#
# Convert serial number / device address to device type
#
def getDeviceType(deviceAddress):
    if int(deviceAddress)>= int(0) and int(deviceAddress) <= int(65535):
        return "DHW-201"
    elif int(deviceAddress)> int(65535) and int(deviceAddress) <= int(131071):
        return "TH-201B"
    elif int(deviceAddress)> int(131071) and int(deviceAddress) <= int(196607):
        return "TH-201B"
    elif int(deviceAddress)> int(196607) and int(deviceAddress) <= int(262143):
        return  "TH-201R"
    elif int(deviceAddress)> int(262143) and int(deviceAddress) <= int(327679):
        return "LCD-200"
    elif int(deviceAddress)> int(327679) and int(deviceAddress) <= int(393215):
        return "RT-210"
    elif int(deviceAddress)> int(393215) and int(deviceAddress) <= int(458751):
        return "RT-250"
    elif int(deviceAddress)> int(458751) and int(deviceAddress) <= int(524287):
        return "RT-211"
    elif int(deviceAddress)> int(524287) and int(deviceAddress) <= int(589823):
        return "RT-251"
    elif int(deviceAddress)> int(589823) and int(deviceAddress) <= int(655359):
        return "RT-250IR"
    elif int(deviceAddress)> int(655359) and int(deviceAddress) <= int(720895):
        return "EU-208-A"
    elif int(deviceAddress)> int(720895) and int(deviceAddress) <= int(786431):
        return "EU-206-VFR"
    elif int(deviceAddress)> int(786431) and int(deviceAddress) <= int(851967):
        return "ET-250"
    elif int(deviceAddress)> int(851967) and int(deviceAddress) <= int(917503):
        return "ET-210"
    elif int(deviceAddress)> int(917503) and int(deviceAddress) <= int(983039):
        return "VH-250"
    elif int(deviceAddress)> int(983039) and int(deviceAddress) <= int(1048575):
        return "VH-210"
    elif int(deviceAddress)> int(16711679) and int(deviceAddress)<= int(16777215):
        return "Applications"
    elif int(deviceAddress)> int(299892735) and int(deviceAddress)<= int(299958271):
        return "CCU-208"

def kickWatchdog():
    global mLastTick
    global mWatchdogTimeout
    logging.debug("Kicking Watchdog {0} -> {1} [Max = {2}]".format(mLastTick, time.time(), mWatchdogTimeout))
    mLastTick = time.time()

########################################################################################################
#               CLASS   RoxiStateHandler                                                               #
########################################################################################################
class RoxiStateHandler(object):
    #CLASS Variables
    hDll = None
    mTaskList = deque()
    mFirmwareDirectory = b''
    mWatchdogIdle = False

    #Class definitions
    SCHEDULER_TIME_UPDATE_TASK = 60 #Update every minute
    
    ### Callback Function for Status callbacks from Roxi DLL
    @ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int)
    def status_callback(rapi_wkd_status):
        kickWatchdog()
        logging.debug("status_callback called Status ={0} : State = {1}".format(rapi_wkd_status, getMState()))
        if rapi_wkd_status == RAPI_WKD_STATUS.RAPI_WDK_STATUS_READY:
            setMState( StateMachineStates.CONNECTED)
            logging.info("Status is Connected!")
        elif rapi_wkd_status == RAPI_WKD_STATUS.RAPI_WDK_STATUS_CLOSED:
            setMState( StateMachineStates.DONE)
            logging.info ("Disconnected")
        #ToDo; handle other returns from RAPI_WKD_STATUS
        return None

    ### Callback Function for get device list callback from DLL
    @ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(Struct_roxi_api_wdk_direct_update_device_list), ctypes.c_uint32)
    def roxi_api_wdk_direct_update_get_device_list_callback(_result, _device_list_ptr, _device_cnt):
        kickWatchdog()
        logging.debug("Device list Callback")
        _deviceList = []
        for i in range(_device_cnt):
            d = _device_list_ptr[i]
            logging.debug("Device: Index:{0:3} - Room:{1:3} - {2} [{3} {4}] - {5}".format(d.dIndex, d.room, d.serial_number, d.connection_status, d.curent_version, d.available_version, d.firmware_status))
            regexMatch = search(r"^(\d*)-(\d*)-(\d*)-(\d*)", d.serial_number.decode("utf-8"))
            if regexMatch:
                #print (regexMatch)
                deviceId = str("{0}{1}{2}".format(regexMatch[2], regexMatch[3],regexMatch[4]))
                #logging.info("Device ID: {:d} 0x{:X}".format(int(deviceId), int(deviceId)))
                device = {"Index": d.dIndex, "Room": d.room, "Serial": d.serial_number, "ConnectionStatus": d.connection_status, 
                                "CurrentFW": d.curent_version, "AvailableFW": d.available_version, "StatusFW": d.firmware_status,
                                "DeviceOID": int(regexMatch[1]), "DeviceAddress": int(deviceId), "DeviceType": getDeviceType(deviceId)}
            else:
                logging.error("Unmatching OID Device found which was not matched!!!!")
                device = {"Index": d.dIndex, "Room": d.room, "Serial": d.serial_number, "ConnectionStatus": d.connection_status, 
                                "CurrentFW": d.curent_version, "AvailableFW": d.available_version, "StatusFW": d.firmware_status,
                                "DeviceOID": -1, "DeviceAddress": -1, "DeviceType": -1}
            _deviceList.append(device)
            logging.info("Device {0}".format(device))
        setMState( StateMachineStates.CONNECTED ) 
        setDeviceList(_deviceList)
        return None

    @ctypes.WINFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32)
    def roxi_api_wdk_direct_update_update_device_callback(_result, _data_sent, _fw_size, _rc_error, _reboot_time):
        global mUpdateStep
        global mWatchdogTimeout
        global MAX_TIME_NO_UPDATE_DEFAULT

        mWatchdogTimeout = MAX_TIME_NO_UPDATE_DEFAULT # Reset to default!

        kickWatchdog()
        updateStep = _result
        logging.debug("roxi_api_wdk_direct_update_update_device_callback => {0}, {1}, {2}, {3}, {4}".format(firmware_update_status[_result], _data_sent, _fw_size, _rc_error, _reboot_time))
        if _result == RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_SUCCESFULL_FINISHED:
            logging.info("Update device completed")
            setMState(StateMachineStates.CONNECTED)
        elif _result == RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_FAIL or _result == RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_ERROR:
            logging.error("Error occured during upgrade procedure {0}".format(_result))
            setMState(StateMachineStates.ERROR)
        elif _result == RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_UPDATING:
            logging.info("Update Device {0}/{1} {2}%".format(_data_sent, _fw_size, round((_data_sent * 100) / _fw_size, 1)))
        elif _result == RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_SWITCHING_APPLICATION or RAPI_WKD_DIRECT_UPDATE_STATUS.RAPI_DUS_SWITCHING_BOOTLOADER:
            mWatchdogTimeout = MAX_TIME_NO_UPDATE_DEFAULT + _reboot_time
            logging.info("Rebooting device into {0} --> {1} seconds max -> Reset watchdog to {2}".format(_result, _reboot_time, mWatchdogTimeout))
        return None

    ##
    ## Global Roxi State machine
    ## 
    def __init__(self):
        setMState ( StateMachineStates.INITIALIZE, init=True)
        _dir = os.path.dirname(sys.modules["RoxiLib"].__file__)
        _path = os.path.join(_dir, "libRoxi.dll")

        self.hDll = ctypes.WinDLL(_path)
        self.mDllLock = threading.Lock()
        pass
    
    #append task to waiting task lists
    def appendTask(self, task):
        if task in self.mTaskList:
            logging.debug("Skipping adding of task {0} since it is already queued.".format(task))
        else:
            logging.debug("-----------> Adding task to tasklist: {0}".format(task))
            self.mTaskList.append(task)
        
       
    def getNextTask(self):
        _task = 0
        try:
            _task = self.mTaskList.popleft()
        except IndexError:
            logging.debug("Next task list is empty")
        return _task

    def GetValue(self):
        return self.value

    ## Recursive scheduler task to schedule recurring tasks into the scheduler
    def appendTaskScheduled(self, task):
        global mWatchdogTimeout
        logging.debug("======= [Append Task scheduled] ({0}) in {1} seconds ======= ".format(task, self.SCHEDULER_TIME_UPDATE_TASK))
        self.mTimerTask = threading.Timer(self.SCHEDULER_TIME_UPDATE_TASK, self.appendTaskScheduled, [StateMachineStates.GET_DEVICE_LIST],{} )
        self.mTimerTask.start()
        self.appendTask(task)
        pass

    def __initializeState(self):
        self.mDllLock.acquire()
        try:
            logging.debug("---> Trying to connect <----")
            val = 0
            val = self.hDll.roxi_api_wdk_connect_ccu_via_bus(self.status_callback)
            if val:
                logging.error("Failed to start connecting")
                setMState ( StateMachineStates.ERROR )
            else:
                setMState ( StateMachineStates.CONNECTING )
                logging.debug("Connecting.")
                self.appendTask(StateMachineStates.GET_DEVICE_LIST) #append get Device list to task queue, and also set it repeatingly using scheduled tasks
                self.mTimerTask = threading.Timer(self.SCHEDULER_TIME_UPDATE_TASK, self.appendTaskScheduled, [StateMachineStates.GET_DEVICE_LIST],{} )
                self.mTimerTask.start()
        except Exception as exception:
            logging.error("ERROR!!! {0}".format(exception))
        self.mDllLock.release()
        pass

    def __connecting(self):
        logging.debug(".") #Waiting State
        pass

    def __running(self):
        logging.debug(".") #Waiting State
        _nextTask = self.getNextTask()
        if(_nextTask != StateMachineStates.INITIALIZE):
            logging.debug("Task Manager set state: {0}".format(_nextTask)) #Waiting State
            setMState(_nextTask)
        pass

    def __updating(self):
        logging.debug("Processing Update.")

    def __getDeviceList(self):
        global mDeviceList
        
        #acquire the dll lock
        self.mDllLock.acquire()
        mDeviceList = None #Clear device list

        if(getMState() == StateMachineStates.GET_DEVICE_LIST): #sometimes this function get's called to soon wich results in error and apparantly the DLL cannot handle it.
            logging.info("Obtaining device list with firmware dir {0}".format(self.mFirmwareDirectory))
            _retVal = self.hDll.roxi_api_wdk_direct_update_get_device_list(self.roxi_api_wdk_direct_update_get_device_list_callback, self.mFirmwareDirectory)
            kickWatchdog()
            if(_retVal != 0):
                logging.error("Failure to get device list {0}".format(_retVal))
                setMState(StateMachineStates.ERROR)
            else:
                setMState ( StateMachineStates.WAITING_DEVICE_LIST )
        else:
            logging.error("Invalid query of get device list issued!! {0}".format(StateMachineStates(getMState()).name))
        
        #release the dll lock    
        self.mDllLock.release()
        pass
        

    def __disconnect(self):
        self.mDllLock.acquire()
        val = self.hDll.roxi_api_wdk_disconnect()
        logging.info("Disconnect result = {0}".format(val))
        setMState ( StateMachineStates.DONE )
        self.mDllLock.release()
        pass

    def __done(self):
        logging.debug("Done.. ")
        pass

    def __error(self):
        logging.error("Error State")
        pass

    def Running(self):
        return not (mStateEquals(StateMachineStates.ERROR) or mStateEquals(StateMachineStates.DONE))
         
    def __waitDeviceList(self):
        logging.debug("Waiting device list callback")
        pass

    def __watchDogCheck(self):
        global mLastTick
        global mWatchdogTimeout

        currTime = time.time()
        lastTimeStamp = mLastTick
        logging.debug("Check watchdog Last Tick: {0}, Now: {1}. Diff = {2} < {3} (Max) === Watchdog Idle={4}".format(lastTimeStamp, currTime, (currTime-lastTimeStamp), mWatchdogTimeout, self.mWatchdogIdle))
        if ((self.mWatchdogIdle == False) and ((currTime - lastTimeStamp) > mWatchdogTimeout) and (lastTimeStamp != 0)):
            logging.error("Error occured, no update received for {0} seconds, which exceeds the limit of {1} seconds".format(currTime - lastTimeStamp, mWatchdogTimeout))
            setMState(StateMachineStates.ERROR)

    stateHandler = {
        StateMachineStates.INITIALIZE: __initializeState,
        StateMachineStates.CONNECTING: __connecting,
        StateMachineStates.CONNECTED: __running,
        StateMachineStates.GET_DEVICE_LIST: __getDeviceList,
        StateMachineStates.WAITING_DEVICE_LIST: __waitDeviceList,
        StateMachineStates.UPDATING: __updating,
        StateMachineStates.DISCONNECT: __disconnect,
        StateMachineStates.ERROR: __error,
        StateMachineStates.DONE: __done,
    }

    def ExecuteState(self):
        if(mState != StateMachineStates.ERROR and mState != StateMachineStates.DONE):
            self.__watchDogCheck()
        _statePre = getMState()
        try:
            self.stateHandler.get(_statePre)(self) #execute function from stateHandler
            logging.debug("Executed state {0} -> {1}".format(StateMachineStates(_statePre).name, StateMachineStates(getMState()).name))
        except:
            logging.error("No function available for state {0} or failed elsewise".format(_statePre))
        if  (mStateEquals(StateMachineStates.ERROR) or mStateEquals(StateMachineStates.DONE)):
            return False #means we are done
        else:
            return True #everything OK, continuing
    
    def Shutdown(self):
        setMState(StateMachineStates.DISCONNECT)
        logging.info("Disconnecting the Roxibus")
        return True


    def isConnected(self):
        _state = getMState()
        if(_state >= StateMachineStates.CONNECTED and _state < StateMachineStates.DISCONNECT):
            return True
        else:
            return False
    
    def GetDeviceList(self):
        return getDeviceList()
    
    def ClearDeviceList(self):
        global mDeviceList
        mDeviceList = None
        self.appendTask(StateMachineStates.GET_DEVICE_LIST)
        pass

    def UpdateDevice(self, _deviceIndex):
        kickWatchdog()
        returnValue = False
        self.mDllLock.acquire()
        logging.debug("Initiate update device index: {0}".format(_deviceIndex))
        _retVal = self.hDll.roxi_api_wdk_direct_update_update_device(self.roxi_api_wdk_direct_update_update_device_callback, _deviceIndex)
        if(_retVal != 0):
            logging.error("Failure to initiate update device  {0}".format(_retVal))
            setMState(StateMachineStates.ERROR)
        else:
            logging.info("Succeeded update device list.")
            setMState(StateMachineStates.UPDATING ) 
            returnValue = True
        self.mDllLock.release()
        return returnValue

    def UpdateDeviceStatusBusy(self):
        if mStateEquals(StateMachineStates.UPDATING):
            return True
        else:
            return False

    def setFirmwareDirectory(self, _firmwareDirectory):
        self.mFirmwareDirectory = bytes(_firmwareDirectory, encoding='utf8')
        logging.info("Update firmware directory to {0} -> {1}".format(_firmwareDirectory, self.mFirmwareDirectory))
        return True

    def SetIdleMode(self, idlemode):
        self.mWatchdogIdle = idlemode
        return True