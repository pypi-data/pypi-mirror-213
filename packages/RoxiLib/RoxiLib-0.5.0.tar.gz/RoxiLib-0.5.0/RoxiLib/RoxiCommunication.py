from .RoxiStateHandler import RoxiStateHandler, StateMachineStates
import time
import threading
import logging


########################################################################################################
#               CLASS   RoxiCommunication                                                              #
########################################################################################################
class RoxiCommunication():
    mStateHandler = RoxiStateHandler()
    mRunning = True

    def __init__(self):
        self.mRunning = True
        pass

    def __startHandler(self):
        while self.mRunning == True:
            self.mRunning = self.mStateHandler.ExecuteState()
            time.sleep(0.2) #Provide some time for other tasks as well.

    def Connect(self):
        self.thread = threading.Thread(target=self.__startHandler)
        self.thread.daemon = True
        self.thread.start()
        self.mStateHandler.SetIdleMode(False)
        pass

    def Shutdown(self):
        self.mStateHandler.Shutdown()
        logging.info("Shutdown issued .. ")
        self.thread.join()
        logging.info(" Join completed")

    def IsConnected(self):
        return self.mStateHandler.isConnected()

    def GetConnectedDevices(self):
        self.mStateHandler.SetIdleMode(False)
        return self.mStateHandler.GetDeviceList()

    def ClearConnectedDevices(self):
        self.mStateHandler.ClearDeviceList()
        self.mStateHandler.appendTask(StateMachineStates.GET_DEVICE_LIST)
        pass

    def UpdateDevice(self, deviceIndex):
        self.mStateHandler.SetIdleMode(False)
        return self.mStateHandler.UpdateDevice(deviceIndex)
    
    def UpdateDeviceStatusBusy(self):
        return self.mStateHandler.UpdateDeviceStatusBusy()

    def IsRunning(self):
        return self.mStateHandler.Running()

    def SetIdleMode(self):
        return self.mStateHandler.SetIdleMode(True)