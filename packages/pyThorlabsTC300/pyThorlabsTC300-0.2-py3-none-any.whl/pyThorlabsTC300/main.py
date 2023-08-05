from genericpath import samefile
import os
import PyQt5
dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
import PyQt5.QtWidgets as Qt# QApplication, QWidget, QMainWindow, QPushButton, QHBoxLayout
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import logging
import sys
import argparse

import abstract_instrument_interface
#import pyThorlabsTC300.driver_virtual
import pyThorlabsTC300.driver

graphics_dir = os.path.join(os.path.dirname(__file__), 'graphics')

##This application follows the model-view-controller paradigm, but with the view and controller defined inside the same object (the GUI)
##The model is defined by the class 'interface', and the view+controller is defined by the class 'gui'. 

class interface(abstract_instrument_interface.abstract_interface):
    """
    Create a high-level interface with the device, validates input data and perform high-level tasks such as periodically reading data from the instrument.
    It uses signals (i.e. QtCore.pyqtSignal objects) to notify whenever relevant data has changes. These signals are typically received by the GUI
    Several general-purpose attributes and methods are defined in the class abstract_interface defined in abstract_instrument_interface
    ...

    Attributes specific for this class (see the abstract class abstract_instrument_interface.abstract_interface for general attributes)
    [LIST TO FINISH]
    ----------
    instrument
        Instance of pyThorlabsTC300.driver.ThorlabsTC300
    connected_device_name : str
        Name of the physical device currently connected to this interface 
    continuous_read : bool 
        When this is set to True, the data from device are acquired continuosly at the rate set by refresh_time       
        settings = {
                'refresh_time': float,      The time interval (in seconds) between consecutive reeading from the device driver (default = 0.2)
                }
    ramp 
        Instance of abstract_instrument_interface.ramp class


    Methods defined in this class (see the abstract class abstract_instrument_interface.abstract_interface for general methods)
    [LIST TO FINISH]
    -------
    refresh_list_devices()
        Get a list of compatible devices from the driver. Store them in self.list_devices, send signal to populate the combobox in the GUI.
    connect_device(device_full_name)
        Connect to the device identified by device_full_name
    disconnect_device()
        Disconnect the currently connected device
    close()
        Closes this interface and calls the close() method of the parent class, which typically calls the disconnect_device method
   
    set_connected_state()
        This method also calls the set_connected_state() method defined in abstract_instrument_interface.abstract_interface
    
        
    update()
        This method also calls the update() method defined in abstract_instrument_interface.abstract_interface

    """

    output = {'Power':0}  #We define this also as class variable. This makes it possible to see which data is produced by this interface without having to create an object

    ## SIGNALS THAT WILL BE USED TO COMMUNICATE WITH THE GUI
    #                                                               | Triggered when ...                                        | Parameter(s) Sent     
    #                                                           #   -----------------------------------------------------------------------------------------------------------------------         
    sig_list_devices_updated = QtCore.pyqtSignal(list)          #   | List of devices is updated                                | List of devices   
    sig_channel_mode_changed = QtCore.pyqtSignal(int,int)       #   | The mode of one channel changed (or was read)             | Channel number, Channel mode [0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)]
    sig_temperature_read = QtCore.pyqtSignal(int,float)         #   | The actual tempereature of a channel was read             | Channel number, Actual Temperature
    sig_current_read = QtCore.pyqtSignal(int,float)             #   | The actual current of a channel was read                  | Channel number, Actual Current
    sig_target_temperature_read = QtCore.pyqtSignal(int,float)  #   | The target temperature of a channel was read              | Channel number, Target Temperature
    sig_target_current_read = QtCore.pyqtSignal(int,float)      #   | The target current of a channel was read                  | Channel number, Target Current
    sig_channel_enabled = QtCore.pyqtSignal(int)                #   | A channel has been enabled                                | Channel number
    sig_enabled_state_change = QtCore.pyqtSignal(int,int)
    sig_change_moving_status = QtCore.pyqtSignal(int)           #   | A step (either of temperature or current) initiated by ramp has started or ended | self.interface.SIG_MOVEMENT_STARTED, self.interface.SIG_MOVEMENT_ENDED
    
    sig_reading = QtCore.pyqtSignal(int)                    #   | Reading status changes                                    | 1 = Started Reading, 2 = Paused Reading, 3 Stopped Reading
    sig_updated_data = QtCore.pyqtSignal(object)            #   | Data is read from instrument                              | Acquired data 
    sig_wavelength = QtCore.pyqtSignal(int)                 #   | Wavelength is changed                                     | Current Wavelength
    sig_min_max_wavelength = QtCore.pyqtSignal(int,int)     #   | Min and max wavelengths supported by this device are read | Current Min and max wavelengths
    sig_refreshtime = QtCore.pyqtSignal(float)              #   | Refresh time is changed                                   | Current Refresh time 
    sig_power_range = QtCore.pyqtSignal(float)              #   | Power range is changed                                    | Current Power range
    sig_auto_power_range = QtCore.pyqtSignal(bool)          #   | Auto power range setting is changed                       | Current Status of auto power range (true/false)
    ##
    # Identifier codes used for view-model communication. Other general-purpose codes are specified in abstract_instrument_interface
    SIG_READING_START = 1
    SIG_READING_PAUSE = 2
    SIG_READING_STOP = 3

    SIG_MOVEMENT_STARTED = 1
    SIG_MOVEMENT_ENDED = 2

    def __init__(self, **kwargs):
        self.output = {'T1':0, 'T2':0, 'i1':0, 'i2':0} 
        ### Default values of settings (might be overwritten by settings saved in .json files later)
        self.settings = {   'refresh_time': 1,
                            'ramp' : {  
                                        'ramp_step_size': 1,            #Increment value of each ramp step
                                        'ramp_wait_1': 1,               #Wait time (in s) after each ramp step
                                        'ramp_send_trigger' : True,     #If true, the function self.func_trigger is called after each 'movement'
                                        'ramp_wait_2': 1,               #Wait time (in s) after each (potential) call to trigger, before doing the new ramp step
                                        'ramp_numb_steps': 10,          #Number of steps in the ramp
                                        'ramp_repeat': 1,               #How many times the ramp is repeated
                                        'ramp_reverse': 1,              #If True (or 1), it repeates the ramp in reverse
                                        'ramp_send_initial_trigger': 1, #If True (or 1), it calls self.func_trigger before starting the ramp
                                        'ramp_reset' : 1                #If True (or 1), it resets the value of the instrument to the initial one after the ramp is done
                                        }
                            }
        self.list_devices = []          #list of devices found 
        self.connected_device_name = ''
        self.continuous_read = False    # When this is set to True, the data from device are acquired continuosly at the rate set by self.refresh_time
        self.channels = [1,2]
        self.mode = [0,0,0] #Stores the mode of each channel [0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)]
                    #The element self.mode[0] is dummy
        self.channel_controlled_by_ramp = 1
        self.modality_names = {0: "Heater", 1: "Tec", 2: "Constant current", 3: "Synchronize with Ch1(only for channel 2)"}
        self.is_enabled = [0,0,0] #Stores whether a channel is enabled (1) or disabled (0)
        self.actual_temperature = [0,0,0] #Stores the latest read temperature of each channel. The element self.actual_temperature[0] is dummy
        self.actual_current = [0,0,0] #Stores the latest read current of each channel. The element self.actual_current[0] is dummy
        self.target_temperature = [0,0,0] #Stores the latest read target temperature of each channel. The element self.target_temperature[0] is dummy
        self.target_current = [0,0,0] #Stores the latest read target current of each channel. The element self.target_current[0] is dummy

        ###
        if ('virtual' in kwargs.keys()) and (kwargs['virtual'] == True):
            pass
            #self.instrument = pyThorlabsPM100x.driver_virtual.ThorlabsPM100x() 
        else:    
            self.instrument = pyThorlabsTC300.driver.ThorlabsTC300() 
        ###
        super().__init__(**kwargs)

        # Setting up the ramp object, which is defined in the package abstract_instrument_interface
        self.ramp = abstract_instrument_interface.ramp(interface=self)  
        self.ramp.set_ramp_settings(self.settings['ramp'])
        self.ramp.set_ramp_functions(func_move = self.increase_target_by,
                                     func_check_step_has_ended = self.step_has_ended, 
                                     func_trigger = super().update(), 
                                     func_trigger_continue_ramp = None,
                                     func_set_value = self.set_target_value, 
                                     func_read_current_value = self.get_target_value, 
                                     list_functions_step_not_ended = [],  
                                     list_functions_step_has_ended = [self.read_output_channel],#lambda:self.end_movement(send_signal=False)],  
                                     list_functions_ramp_started = [self.pause_reading],
                                     list_functions_ramp_ended = [self.start_reading])
        self.ramp.sig_ramp.connect(self.on_ramp_state_changed)

        self.refresh_list_devices()   
        
    def refresh_list_devices(self):
        '''
        Get a list of all devices connected, by using the method list_devices() of the driver. For each device obtain its identity and its address.
        '''     
        self.logger.info(f"Looking for devices...") 
        list_valid_devices = self.instrument.list_devices() #Then we read the list of devices
        self.logger.info(f"Found {len(list_valid_devices)} devices.") 
        self.list_devices = list_valid_devices
        self.send_list_devices()

    def send_list_devices(self):
        if(len(self.list_devices)>0):
            list_IDNs_and_devices = [dev[0] + " --> " + dev[1] for dev in self.list_devices] 
        else:
            list_IDNs_and_devices = []
        self.sig_list_devices_updated.emit(list_IDNs_and_devices)

    def connect_device(self,device_full_name):
        if(device_full_name==''): 
            self.logger.error("No valid device has been selected.")
            return
        self.set_connecting_state()
        device_addr = device_full_name.split(' --> ')[0].lstrip()   # We extract the device address from the device name
        self.logger.info(f"Connecting to device {device_addr}...")
        try:
            (ID, Msg) = self.instrument.connect_device(device_addr)      # Try to connect by using the method connect_device of the device driver
            if(ID==1):  #If connection was successful
                self.logger.info(f"Connected to device {device_addr}.")
                self.connected_device_name = device_addr
                self.set_connected_state()
            else: #If connection was not successful
                self.logger.error(f"Error: {Msg}")
                self.set_disconnected_state()
        except Exception as e:
            self.logger.error(f"Error: {e}")
            self.set_disconnected_state()

    def disconnect_device(self):
        self.logger.info(f"Disconnecting from device {self.connected_device_name}...")
        (ID, Msg) = self.instrument.disconnect_device()
        if(ID==1): # If disconnection was successful
            self.logger.info(f"Disconnected from device {self.connected_device_name}.")
            self.continuous_read = 0 # We set this variable to 0 so that the continuous reading from the powermeter will stop
            self.set_disconnected_state()
        else: #If disconnection was not successful
            self.logger.error(f"Error: {Msg}")
            self.set_disconnected_state() #When disconnection is not succeful, it is typically because the device alredy lost connection
                                          #for some reason. In this case, it is still useful to have all widgets reset to disconnected state      
    def close(self,**kwargs):
        super().close(**kwargs) 
        self.settings['ramp'] = self.ramp.settings

    def on_ramp_state_changed(self,status):
        '''
        Slot for signals coming from the ramp object
        '''
        if status == self.ramp.SIG_RAMP_STARTED:
            #self.set_moving_state()
            self.settings['ramp'] = self.ramp.settings
        if status == self.ramp.SIG_RAMP_ENDED:
            pass
            #self.set_non_moving_state()
        
    def toggle_enable_disable(self,channel):
        if self.is_enabled[channel]:
            self.disable_channel(channel)
        else:
            self.enable_channel(channel)

    def set_connected_state(self):
        super().set_connected_state()
        self.read_status_channels()
        
        #self.read_min_max_wavelength()
        #self.read_wavelength()
        #self.read_status_power_autorange()
        #self.set_auto_power_range(self.settings['auto_power_range'])
        #self.read_power_range()
        self.start_reading()

    def read_status_channels(self,channels=None):
        #This is typically called after connection, to check different properties of the channels and fire the corresponding signals
        # if channels is not specified, it does everything for all channels in channels, otherwise it only does it for the channel specified by channels, which must be a valid integer or a list of integers
        if channels == None : channels = self.channels
        if not(isinstance(channels, list)): channels = [channels]
        self.check_if_channel_is_enabled(channels)
        self.read_mode_channel(channels)
        self.read_output_channel(channels)
        self.read_target_channel(channels)

        return

    def check_if_channel_is_enabled(self,channels=None):
        # if channels is not specified, it does everything for all channels in channels, otherwise it only does it for the channel specified by channels, which must be a valid integer or a list of integers
        if channels == None : channels = self.channels
        if not(isinstance(channels, list)): channels = [channels]
        for channel in channels:
            self.is_enabled[channel] = self.is_enabled[channel] #This is just a placeholder
            self.sig_enabled_state_change.emit(channel,self.is_enabled[channel])
        return

    def read_mode_channel(self,channels=None):
        # if channels is not specified, it does everything for all channels in channels, otherwise it only does it for the channel specified by channels, which must be a valid integer or a list of integers
        #[0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)]
        if channels == None : channels = self.channels
        if not(isinstance(channels, list)): channels = [channels]
        
        for channel in channels:
            self.mode[channel] = self.instrument.get_mode_channel(channel)
            self.sig_channel_mode_changed.emit(channel,self.mode[channel])
            self.logger.info(f"Channel {channel} is in modality: {self.modality_names[self.mode[channel]]}.")

    def set_mode_channel(self,channel,mode):
        #[0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)]
        try:
            self.instrument.set_mode_channel(channel,mode)
        except Exception as e:
            self.logger.error(f"An error occurred while setting the mode of channel {channel}: {e}")
        self.read_mode_channel(channel)
        self.read_target_channel() #This will update the target quantity displayed in the GUI, which depends on the channel modality

    def read_output_channel(self,channels=None):
        # if channels is not specified, it does everything for all channels in channels, otherwise it only does it for the channel specified by channels, which must be a valid integer or a list of integers
        
        if channels == None : channels = self.channels
        if not(isinstance(channels, list)): channels = [channels]
        for channel in channels:
            if self.mode[channel] == 0:
                T = self.instrument.get_actual_temperature(channel)
                self.actual_temperature[channel] = T
                self.sig_temperature_read.emit(channel,T)
                self.output['T'+str(channel)] = T
            elif self.mode[channel] == 2:
                I = self.instrument.get_actual_current(channel)
                self.actual_current[channel] = I
                self.sig_current_read.emit(channel,I)
                self.output['T'+str(channel)] = I

    def read_target_channel(self,channels=None):
        # if channels is not specified, it does everything for all channels in channels, otherwise it only does it for the channel specified by channels, which must be a valid integer or a list of integers
        
        if channels == None : channels = self.channels
        if not(isinstance(channels, list)): channels = [channels]
        for channel in channels:
            if self.mode[channel] == 0:
                T = self.instrument.get_target_temperature(channel)
                self.target_temperature[channel] = T
                self.sig_target_temperature_read.emit(channel,T)
            elif self.mode[channel] == 2:
                I = self.instrument.get_target_current(channel)
                self.target_current[channel] = I
                self.sig_target_current_read.emit(channel,I)

    def set_target_channel(self,channel,target):
        try: 
            target = float(target)
        except ValueError:
            self.logger.error(f"The target time must be a valid number.")
            self.read_target_channel(channel)
            return False
        
        if self.mode[channel] == 0:
            self.logger.info(f"Setting the target of channel {channel} to {target} C")
            try:
                self.instrument.set_target_temperature(channel,target)
            except Exception as e:
                self.logger.error(f"An error occurred while setting target temperature for channel {channel}: {e}")
        elif self.mode[channel] == 2:
            self.logger.info(f"Setting the target of channel {channel} to {target} mA")
            try:
                self.instrument.set_target_current(channel,target)
            except Exception as e:
                self.logger.error(f"An error occurred while setting target current for channel {channel}: {e}")
        self.read_target_channel(channel)

    def enable_channel(self,channel):
        self.logger.info(f"Enabling channel {channel}...")
        try:
            self.instrument.enable_disable_channel(channel,1)
        except Exception as e:
            self.logger.error(f"An error occurred while enabling channel {channel}: {e}")
        self.logger.info(f"Channel {channel} enabled")
        self.is_enabled[channel] = 1
        self.sig_enabled_state_change.emit(channel,1)

    def disable_channel(self,channel):
        self.logger.info(f"Disabling channel {channel}...")
        try:
            self.instrument.enable_disable_channel(channel,0)
        except Exception as e:
            self.logger.error(f"An error occurred while disabling channel {channel}: {e}")
        self.logger.info(f"Channel {channel} disabled")
        self.is_enabled[channel] = 0
        self.sig_enabled_state_change.emit(channel,0)

    def set_refresh_time(self, refresh_time):
        try: 
            refresh_time = float(refresh_time)
            if self.settings['refresh_time'] == refresh_time: #in this case the number in the refresh time edit box is the same as the refresh time currently stored
                return True
        except ValueError:
            self.logger.error(f"The refresh time must be a valid number.")
            self.sig_refreshtime.emit(self.settings['refresh_time'])
            return False
        if refresh_time < 0.001:
            self.logger.error(f"The refresh time must be positive and >= 1ms.")
            self.sig_refreshtime.emit(self.settings['refresh_time'])
            return False
        self.logger.info(f"The refresh time is now {refresh_time} s.")
        self.settings['refresh_time'] = refresh_time
        self.sig_refreshtime.emit(self.settings['refresh_time'])
        return True

    ### Functions mainly used for interface with ramp

    def increase_target_by(self,step,channel = None):
        if channel == None: channel = self.channel_controlled_by_ramp
        if self.mode[channel] == 0:
            current_target = self.target_temperature[channel]
        elif self.mode[channel] == 2:
            current_target = self.target_current[channel]
             
        next_target = current_target + step
        self.set_target_channel(channel,next_target)

    def get_target_value(self,channel = None):
        if channel == None: channel = self.channel_controlled_by_ramp
        self.read_target_channel(channel)
        current_target = self.target_current[channel]
        return current_target

    def set_target_value(self,target,channel = None):
        if channel == None: channel = self.channel_controlled_by_ramp
        self.set_target_channel(channel,target)

    def step_has_ended(self):
        # This function is used by the ramp to check if a step has ended. For now it is a placeholder and always returns True
        return True


    ###

    #def set_wavelength(self, wl):
    #    try:
    #        if int(self.instrument.wavelength) == int(float(wl)): #in this case the number in the refresh time edit box is the same as the wavelength currently set
    #                return True
    #        self.logger.info(f"Setting the wavelength to {wl} for the device {self.connected_device_name}...")
    #    except ValueError as e:
    #        self.logger.error(f"The wavelength must be a valid number.")
    #        self.sig_wavelength.emit(self.instrument.wavelength)
    #        return False
    #    try: 
    #        self.instrument.wavelength = int(float(wl))
    #        self.logger.info(f"Wavelength set correctly.")
    #    except Exception as e:
    #        self.logger.error(f"An error occurred while setting the wavelength: {e}")
    #        self.sig_wavelength.emit(self.instrument.wavelength)
    #        return False
    #    self.read_power_range() #The boundaries of the power ranges might change when the wavelength is changed, so we need to update it after changing the wavelength
    #    return True
  
    #def read_wavelength(self):
    #    self.logger.info(f"Reading current wavelength from device {self.connected_device_name}...") 
    #    self.wavelength = int(self.instrument.wavelength)
    #    if self.wavelength == None:
    #        self.logger.error(f"An error occurred while reading the wavelength from this device.")
    #        return
    #    self.sig_wavelength.emit(self.instrument.wavelength)
    #    self.logger.info(f"Current wavelength is {self.wavelength}.") 
    #    return
      
    #def read_min_max_wavelength(self):
    #    self.logger.info(f"Reading min and max wavelength supported by device {self.connected_device_name}...") 
    #    self.min_max_wls =  (self.instrument.min_wavelength,self.instrument.max_wavelength)
    #    self.sig_min_max_wavelength.emit(self.min_max_wls[0],self.min_max_wls[1])
    #    self.logger.info(f"Wavelength range: {self.min_max_wls[0]}-{self.min_max_wls[1]} nm") 

    #def change_power_range(self,direction):
    #    if direction == +1:
    #        string = 'increase'
    #    else: 
    #        string = 'decrease'
    #    self.logger.info(f"Trying to {string} the power range...")
    #    self.instrument.move_to_next_power_range(direction)
    #    self.read_power_range()
    #    return

    #def read_power_range(self):
    #    self.logger.info(f"Reading current power range from device {self.connected_device_name}...") 
    #    self.power_range = self.instrument.power_range
    #    if self.power_range == None:
    #        self.logger.error(f"An error occurred while reading the power range from this device.")
    #        return
    #    self.sig_power_range.emit(self.power_range)
    #    self.logger.info(f"Current power range is {self.power_range}.") 

    #def set_auto_power_range(self,auto_power_range):
    #    auto_power_range = bool(auto_power_range)
    #    status_string = 'ON' if auto_power_range else 'OFF'
    #    self.logger.info(f"Setting the auto-ranging function to {status_string} for the device {self.connected_device_name}...")    
    #    try:
    #        self.instrument.auto_power_range  = auto_power_range
    #        self.sig_auto_power_range.emit(auto_power_range)
    #        self.logger.info(f"Setting changed succesfully.")
    #        self.settings['auto_power_range'] = auto_power_range
    #    except Exception as e:
    #        self.logger.error(f"An error occurred while setting the auto-ranging status: {e}")
    #    #self.read_auto_power_range()
    #    self.read_power_range()

    #def read_auto_power_range(self):
    #    self.logger.info(f"Reading the status of the auto-ranging function for the device {self.connected_device_name}...")   
    #    try:
    #        auto_power_range = self.instrument.auto_power_range
    #        status_string = 'ON' if auto_power_range else 'OFF'
    #        self.sig_auto_power_range.emit(auto_power_range)
    #        self.logger.info(f"The auto-ranging function is currently set to {status_string}.")
    #        self.settings['auto_power_range'] = auto_power_range
    #        return auto_power_range
    #    except Exception as e:
    #        self.logger.error(f"An error occurred while reading the auto-ranging status: {e}")

    #def set_zero_powermeter(self):
    #    try: 
    #        ID = self.instrument.set_zero()
    #        self.logger.info(f"Zero-ing the device {self.connected_device_name}...")
    #        if ID == 1:
    #            self.logger.info(f"Device was succesfully zeroed.")
    #        else:
    #            self.logger.error(f"An error occurred while zero-ing this device.")
    #    except Exception as e:
    #        self.logger.error(f"An error occurred while zero-ing this device: {e}")
    #    return

    def start_reading(self):
        if(self.instrument.connected == False):
            self.logger.error(f"No device is connected.")
            return
        #self.logger.info(f"Updating wavelength and refresh time before starting reading...")       
        self.sig_reading.emit(self.SIG_READING_START) # This signal will be caught by the GUI
        self.continuous_read = True #Until this variable is set to True, the function UpdatePower will be repeated continuosly 
        self.logger.info(f"Starting reading from device {self.connected_device_name}...")
        # Call the function self.update(), which will do stome suff (read power and store it in a global variable) and then call itself continuosly until the variable self.continuous_read is set to False
        self.update()
        return
 
    def pause_reading(self):
        #Sets self.continuous_read to False (this will force the function update() to stop calling itself)
        self.continuous_read = False
        self.logger.info(f"Paused reading from device {self.connected_device_name}.")
        self.sig_reading.emit(self.SIG_READING_PAUSE) # This signal will be caught by the GUI
        return

    def stop_reading(self):
        #Sets self.continuous_read to False (this will force the function update() to stop calling itself) and delete all accumulated data
        self.continuous_read = False
        self.stored_data = []
        self.logger.info(f"Stopped reading from device {self.connected_device_name}. All stored data have been deleted.")
        self.sig_reading.emit(self.SIG_READING_PAUSE) # This signal will be caught by the GUI
        # ...
        return
        
    def update(self):
        '''

        '''
        if(self.continuous_read == True):
            self.read_output_channel()
            #(currentPower,power_units) = self.instrument.power
            #self.output['Power'] = currentPower
            #self.power_units = power_units
            #self.stored_data.append(currentPower)
            #self.output['PowerUnits'] = power_units

            super().update()    

            #self.sig_updated_data.emit([currentPower, power_units])
            QtCore.QTimer.singleShot(int(self.settings['refresh_time']*1e3), self.update)
           
        return
    
    
class gui(abstract_instrument_interface.abstract_gui):
     
    def __init__(self,interface,parent):
        """
        Attributes specific for this class (see the abstract class abstract_instrument_interface.abstract_gui for general attributes)
        ----------

        """
        super().__init__(interface,parent)

        self.initialize()

    def initialize(self):
        self.create_widgets()
        self.connect_widgets_events_to_functions()

        ### Call the initialize method of the super class. 
        super().initialize()

        ### Connect signals from model to event slots of this GUI
        self.interface.sig_list_devices_updated.connect(self.on_list_devices_updated)
        self.interface.sig_connected.connect(self.on_connection_status_change) 
        self.interface.sig_channel_mode_changed.connect(self.on_channel_mode_changed)
        self.interface.sig_temperature_read.connect(self.on_actual_temperature_changed)
        self.interface.sig_current_read.connect(self.on_actual_current_changed)
        self.interface.sig_target_temperature_read.connect(self.on_target_temperature_changed)
        self.interface.sig_target_current_read.connect(self.on_target_current_changed)
        self.interface.sig_enabled_state_change.connect(self.on_enabled_state_change)
        #self.interface.sig_reading.connect(self.on_reading_status_change) 
        #self.interface.sig_updated_data.connect(self.on_data_change) 
        #self.interface.sig_refreshtime.connect(self.on_refreshtime_change)
        #self.interface.sig_wavelength.connect(self.on_wavelength_change)
        #self.interface.sig_min_max_wavelength.connect(self.on_min_max_wavelength_update)
        #self.interface.sig_auto_power_range.connect(self.on_auto_power_range_change)
        #self.interface.sig_power_range.connect(self.on_power_range_change)
        #self.interface.sig_close.connect(self.on_close)

        ### SET INITIAL STATE OF WIDGETS
        #self.edit_RefreshTime.setText(f"{self.interface.settings['refresh_time']:.3f}")
        self.interface.send_list_devices()  
        #self.on_connection_status_change(self.interface.SIG_DISCONNECTED) #When GUI is created, all widgets are set to the "Disconnected" state              
        ###

    def create_panel_channel(self,channel_name = 'CH'):

        QGroupBoxStyle = """ {
            font: bold;
            border: 1px solid silver;
            border-radius: 6px;
            margin-top: 6px;
        }"""

        QGroupBoxTitleStyle = """::title {
                                subcontrol-origin: margin;
                                left: 17px;
                                padding: -5px 5px 0px 5px;
                            }"""

        groupbox_main = Qt.QGroupBox(channel_name)
        groupbox_main.setObjectName(channel_name)

        string = "QGroupBox"
        groupbox_main.setStyleSheet(string + QGroupBoxStyle + string + QGroupBoxTitleStyle) #This line changes the style of ONLY this QWdiget

        vbox_main = Qt.QVBoxLayout()

        hbox_row1 = Qt.QHBoxLayout()
        button_onoff = Qt.QPushButton("OFF")
        button_onoff.setCheckable(True)
        button_onoff.setStyleSheet("background-color: red; font: bold;")
        label_mode = Qt.QLabel('Mode:')
        combo_mode = Qt.QComboBox()
        combo_mode.addItems([self.interface.modality_names[0],self.interface.modality_names[2]]) 
        widgets_row1 = {'button_onoff':button_onoff,'label_mode':label_mode,'combo_mode':combo_mode}
        widgets_row1_stretches = [0]*len(widgets_row1)
        for w,s in zip(widgets_row1.values(),widgets_row1_stretches):
            hbox_row1.addWidget(w,stretch=s)
        hbox_row1.addStretch(1)

        hbox_row2 = Qt.QHBoxLayout()
        label_value = Qt.QLabel('0')
        label_value.setAlignment(QtCore.Qt.AlignCenter)
        label_value.setStyleSheet("font-weight: bold")
        label_value.setFont(QtGui.QFont('Arial', 10))
        widgets_row2 = {'label_value':label_value}
        widgets_row2_stretches = [1]*len(widgets_row2)
        for w,s in zip(widgets_row2.values(),widgets_row2_stretches):
            hbox_row2.addWidget(w,stretch=s)

        hbox_row3 = Qt.QHBoxLayout()
        label_target = Qt.QLabel('Target')
        edit_target = Qt.QLineEdit(' ')
        label_target_units = Qt.QLabel('')
        widgets_row3 = {'label_target':label_target,'edit_target':edit_target,'label_target_units':label_target_units}
        widgets_row3_stretches = [0]*len(widgets_row3)
        for w,s in zip(widgets_row3.values(),widgets_row3_stretches):
            hbox_row3.addWidget(w,stretch=s)

        box_stretches = [0,1,0]
        boxes = [hbox_row1,hbox_row2,hbox_row3]
        for box,s in zip(boxes,box_stretches):
            vbox_main.addLayout(box,stretch=s)  
        #vbox_main.addStretch(1)

        groupbox_main.setLayout(vbox_main)
        widgets = {**widgets_row1, **widgets_row2, **widgets_row3}

        return groupbox_main,widgets

    def create_widgets(self):
        """
        Creates all widgets and layout for the GUI. Any Widget and Layout must assigned to self.containter, which is a pyqt Layout object
        """ 
        self.container = Qt.QVBoxLayout()

        self.widgets_channels =[0,0,0]

        hbox1, widgets_dict = self.create_panel_connection_listdevices()
        for key, val in widgets_dict.items(): 
            setattr(self,key,val) 

        hbox2 = Qt.QHBoxLayout()

        box_CH1,widgets_CH1 = self.create_panel_channel(channel_name = 'CH1')
        box_CH2,widgets_CH2 = self.create_panel_channel(channel_name = 'CH2')

        self.widgets_channels[1] = widgets_CH1 
        self.widgets_channels[2] = widgets_CH2 
  
        for box in [box_CH1,box_CH2]:
            hbox2.addWidget(box,stretch=1) 
        #hbox2.addStretch(1)

        self.ramp_groupbox = abstract_instrument_interface.ramp_gui(ramp_object=self.interface.ramp)     

        for box in [hbox1,hbox2]:
            self.container.addLayout(box) 
        self.container.addWidget(self.ramp_groupbox)
        #self.container.addStretch(1)

        ## Widgets for which we want to constraint the width by using sizeHint()
        #widget_list = [self.button_StopReading,self.label_RefreshTime,self.label_Power,self.button_SetZeroPowermeter,self.label_WavelengthUnits,self.label_PowerRange,self.box_PowerRangeAuto]
        #for w in widget_list:
        #    w.setMaximumSize(w.sizeHint())
        self.widgets_enabled_when_connected =[]
        #self.widgets_enabled_when_connected = [self.button_SetZeroPowermeter,self.edit_Wavelength,self.edit_PowerRange,self.box_PowerRangeAuto, 
        #                                       self.button_IncreasePowerRange,self.button_DecreasePowerRange,self.button_StartPauseReading,self.button_StopReading]
        self.widgets_enabled_when_disconnected = []
        #self.widgets_enabled_when_disconnected = [self.combo_Devices,self.button_RefreshDeviceList]

    def connect_widgets_events_to_functions(self):
        self.button_RefreshDeviceList.clicked.connect(self.click_button_refresh_list_devices)
        self.button_ConnectDevice.clicked.connect(self.click_button_connect_disconnect)
        for channel in [1,2]:
            self.widgets_channels[channel]['button_onoff'].clicked.connect(lambda x,y=channel:self.click_button_on_off(y))
            self.widgets_channels[channel]['combo_mode'].activated.connect(lambda x,y=channel:self.click_combo_mode(y))
            self.widgets_channels[channel]['edit_target'].returnPressed.connect(lambda y=channel: self.press_enter_edit_target(y))
        #self.edit_RefreshTime.returnPressed.connect(self.press_enter_refresh_time)


###########################################################################################################
### Event Slots. They are normally triggered by signals from the model, and change the GUI accordingly  ###
###########################################################################################################

    def on_connection_status_change(self,status):
        if status == self.interface.SIG_DISCONNECTED:
            self.disable_widget(self.widgets_enabled_when_connected)
            self.enable_widget(self.widgets_enabled_when_disconnected)
            #self.edit_PowerRange.setText('')
            #self.edit_Wavelength.setText('')
            #self.label_Wavelength.setText(f"Wavelength: ")
            self.button_ConnectDevice.setText("Connect")
            #self.edit_Power.setText('')
        if status == self.interface.SIG_DISCONNECTING:
            self.disable_widget(self.widgets_enabled_when_connected)
            self.enable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Disconnecting...")
        if status == self.interface.SIG_CONNECTING:
            self.disable_widget(self.widgets_enabled_when_connected)
            self.enable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Connecting...")
        if status == self.interface.SIG_CONNECTED:
            self.enable_widget(self.widgets_enabled_when_connected)
            self.disable_widget(self.widgets_enabled_when_disconnected)
            self.button_ConnectDevice.setText("Disconnect")

    def on_enabled_state_change(self,channel,status):
        if status == 1:
            if not(self.widgets_channels[channel]['button_onoff'].isChecked()):
                self.widgets_channels[channel]['button_onoff'].toggle()
            self.widgets_channels[channel]['button_onoff'].setText('ON')
            self.widgets_channels[channel]['button_onoff'].setStyleSheet("background-color: green; font: bold;")
        if status == 0:
            if self.widgets_channels[channel]['button_onoff'].isChecked():
                self.widgets_channels[channel]['button_onoff'].toggle()
            self.widgets_channels[channel]['button_onoff'].setText('OFF')
            self.widgets_channels[channel]['button_onoff'].setStyleSheet("background-color: red; font: bold;")

    def on_channel_mode_changed(self,channel,mode):
        #{0: "Heater", 1: "Tec", 2: "Constant current", 3: "Synchronize with Ch1(only for channel 2)"}
        if mode in [0,2]:
            self.widgets_channels[channel]['combo_mode'].setCurrentText(self.interface.modality_names[mode])

    def on_actual_temperature_changed(self,channel,T):
        if self.interface.mode[channel] == 0:
            self.widgets_channels[channel]['label_value'].setText(f'{T:.2f} C')
        return

    def on_actual_current_changed(self,channel,I):
        if self.interface.mode[channel] == 2:
            self.widgets_channels[channel]['label_value'].setText(f'{I:.2f} mA')
        return

    def on_target_temperature_changed(self,channel,T):
        if self.interface.mode[channel] == 0:
            self.widgets_channels[channel]['edit_target'].setText(f'{T:.2f}')
            self.widgets_channels[channel]['label_target_units'].setText(f'C')
        return

    def on_target_current_changed(self,channel,I):
        if self.interface.mode[channel] == 2:
            self.widgets_channels[channel]['edit_target'].setText(f'{I:.2f}')
            self.widgets_channels[channel]['label_target_units'].setText(f'mA')
        return

    def on_reading_status_change(self,status):
        if status == self.interface.SIG_READING_PAUSE:
            self.button_StartPauseReading.setIcon(QtGui.QIcon(os.path.join(graphics_dir,'play.png')))
        if status == self.interface.SIG_READING_START:
            self.button_StartPauseReading.setIcon(QtGui.QIcon(os.path.join(graphics_dir,'pause.png')))
        if status == self.interface.SIG_READING_STOP: 
            self.button_StartPauseReading.setIcon(QtGui.QIcon(os.path.join(graphics_dir,'play.png')))

    def on_list_devices_updated(self,list_devices):
        self.combo_Devices.clear()  #First we empty the combobox  
        self.combo_Devices.addItems(list_devices) 

    #def on_data_change(self,data):
    #    #Data is (in this case) a string
    #    current_power_string = f"{data[0]:.2e}" + ' ' +  data[1]
    #    self.edit_Power.setText(current_power_string)

    #def on_refreshtime_change(self,value):
    #    self.edit_RefreshTime.setText(f"{value:.3f}")

    #def on_wavelength_change(self,value):
    #    self.edit_Wavelength.setText(str(int(value)))

    #def on_min_max_wavelength_update(self,min,max):
    #    self.label_Wavelength.setText(f"Wavelength<br>(<b>{min}-{max}</b>): ")
    
    #def on_power_range_change(self,value):
    #    self.edit_PowerRange.setText(f"{value:.2e}")
    #    self.edit_PowerRange.setCursorPosition(1)

    #def on_auto_power_range_change(self,value):
    #    self.set_auto_power_range_state(value)
    #    self.box_PowerRangeAuto.setChecked(value)

    #def on_close(self):
    #    return

    #def set_auto_power_range_state(self,auto_power_range):
    #    if auto_power_range:
    #        self.disable_widget([self.edit_PowerRange,self.button_IncreasePowerRange, self.button_DecreasePowerRange])
    #    else:
    #        self.enable_widget([self.edit_PowerRange,self.button_IncreasePowerRange, self.button_DecreasePowerRange])

#######################
### END Event Slots ###
#######################

            
###################################################################################################################################################
### GUI Events Functions. They are triggered by direct interaction with the GUI, and they call methods of the interface (i.e. the model) object.###
###################################################################################################################################################

    def click_button_refresh_list_devices(self):
        self.interface.refresh_list_devices()

    def click_button_connect_disconnect(self):
        if(self.interface.instrument.connected == False): # We attempt connection   
            device_full_name = self.combo_Devices.currentText() # Get the device name from the combobox
            self.interface.connect_device(device_full_name)
        elif(self.interface.instrument.connected == True): # We attempt disconnection
            self.interface.disconnect_device()

    def click_button_on_off(self,channel):
        self.interface.toggle_enable_disable(channel)

    def click_combo_mode(self,channel):
        text = self.widgets_channels[channel]['combo_mode'].currentText()
        keys = [k for k, v in self.interface.modality_names.items() if v == text]
        mode = keys[0]
        self.interface.set_mode_channel(channel,mode)

    def press_enter_edit_target(self,channel):
        target = self.widgets_channels[channel]['edit_target'].text()
        self.interface.set_target_channel(channel,target)

    #def click_box_PowerRangeAuto(self, state):
    #    if state == QtCore.Qt.Checked:
    #        status_bool = True
    #    else:
    #        status_bool = False
    #    self.interface.set_auto_power_range(status_bool)

    #def click_button_set_zero_powermeter(self):
    #    self.interface.set_zero_powermeter()

    #def press_enter_wavelength(self):
    #    return self.interface.set_wavelength(self.edit_Wavelength.text())
        
    #def click_button_change_power_range(self,direction):
    #    self.interface.change_power_range(direction)
       
    #def click_button_StartPauseReading(self): 
    #    if(self.interface.continuous_read == False):
    #        if not(self.press_enter_refresh_time()): #read the current value in the refresh_time textbox, and validates it. The function returns True/False if refresh_time was valid
    #            return
    #        if not(self.press_enter_wavelength()): #read the current value in the wavelength textbox, and validates it. The function returns True/False if refresh_time was valid
    #            return
    #        self.interface.start_reading()
    #    elif (self.interface.continuous_read == True):
    #        self.interface.pause_reading()
    #    return

    #def click_button_StopReading(self):
    #    self.interface.stop_reading()

    #def press_enter_refresh_time(self):
    #    return self.interface.set_refresh_time(self.edit_RefreshTime.text())


#################################
### END GUI Events Functions ####
#################################


            
#################################################################################################

class MainWindow(Qt.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(__package__)

    def closeEvent(self, event):
        #if self.child:
        pass#self.child.close()

#################################################################################################

def main():
    parser = argparse.ArgumentParser(description = "",epilog = "")
    parser.add_argument("-s", "--decrease_verbose", help="Decrease verbosity.", action="store_true")
    parser.add_argument('-virtual', help=f"Initialize the virtual driver", action="store_true")
    args = parser.parse_args()
    virtual = args.virtual
    
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    Interface = interface(app=app,virtual=virtual) 
    Interface.verbose = not(args.decrease_verbose)
    app.aboutToQuit.connect(Interface.close) 
    view = gui(interface = Interface, parent=window) #In this case window is the parent of the gui
    window.show()
    app.exec()# Start the event loop.

if __name__ == '__main__':
    main()

#################################################################################################
