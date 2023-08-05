import pyThorlabsTC300.TC300_COMMAND_LIB as TC300_COMMAND_LIB 

class ThorlabsTC300:


    def __init__(self):
        self.connected = False
  
        self.device_handle = None
        self.device_serial = None
     
    def list_devices(self):
        '''
        Scans all potential devices, ask for their identity and check if any of them is a valid device supported by this driver (by comparing their identity with the elements of model_identifiers)

        Returns
        -------
        list_valid_devices, list
            A list of all found valid devices. Each element of the list is a list of three strings, in the format [address,identity,model]

        '''

        self.list_all_devices = TC300_COMMAND_LIB.TC300ListDevices()
        self.list_valid_devices = self.list_all_devices
        # self.list_valid_devices = [] 
        # for addr in self.list_all_devices:
        #     if(not(addr.startswith('ASRL'))):
        #         try:
        #             instrument = self.rm.open_resource(addr)
        #             idn = instrument.query('*IDN?').strip()
        #             for model in self.model_identifiers: #sweep over all supported models
        #                 if model[1] in idn:              #check if idn is one of the supported models
        #                     if self.model_user  and not(self.model_user ==model[0]): #if the user had specified a specific model, we dont consider any other model
        #                         break
        #                     self.list_valid_devices.append([addr,idn,model[0]])
        #             instrument.before_close()
        #             instrument.close()     
        #         except visa.VisaIOError:
        #             pass
        return self.list_valid_devices
    
    def connect_device(self,device_addr):
        self.list_devices()
        device_addresses = [dev[0] for dev in self.list_valid_devices]
        if (device_addr in device_addresses):
            try:         
                hdl = TC300_COMMAND_LIB.TC300Open(device_addr,115200,3)    
                #hdl is less than 0 if something went wrong
                ID = 1
            except:
                Msg = "Error during connection"
                ID = -1 
        else:
            raise ValueError("The specified address is not a valid device address.")
        if(ID>=0):
            self.connected = True
            self.device_handle = hdl
            self.device_serial = device_addr
            Msg = 'Connected'
            #self.read_parameters_upon_connection()
        else:
            self.connected = False
            self.device_handle = None
            self.device_serial = None
            Msg = 'Error during connection'
        return (ID,Msg)

    def read_parameters_upon_connection(self):
        self.wavelength
        self.read_min_max_wavelength()
        self.power
        self.min_power_range
        self.max_power_range
        self.auto_power_range
        self.power_range

    def disconnect_device(self):
        if(self.connected == True):
            try:   
                TC300_COMMAND_LIB.TC300Close(self.device_handle)  
                ID = 1
                Msg = 'Disconnected'
            except Exception as e:
                ID = -1 
                Msg = e
            self.connected = False
            return (ID,Msg)
        else:
            raise RuntimeError("Device is already disconnected.")

    def enable_disable_channel(self,channel,desired_status):
        # desired_status =  0: Disable; 1: Enable
        result = TC300_COMMAND_LIB.TC300EnableChannel(self.device_handle,channel,desired_status)  
        if(result<0):
            raise RuntimeError(f"Error while enabling/disabling channel: {result}")
        else:
            return result
    
    def set_mode_channel(self,channel,mode):
        #mode: 0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)
        result = TC300_COMMAND_LIB.TC300SetMode(self.device_handle, channel,mode) #channel mode: 0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)
        if(result<0):
            raise RuntimeError(f"Error while setting the channel mode: {result}")
        else:
            return result

    def get_mode_channel(self,channel):
        #mode: 0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)
        mode=[0]
        result = TC300_COMMAND_LIB.TC300GetMode(self.device_handle, channel,mode) #channel mode: 0: Heater; 1: Tec; 2: Constant current; 3: Synchronize with Ch1(only for channel 2)
        if(result<0):
            raise RuntimeError(f"Error while reading the channel mode: {result}")
        else:
            return mode[0]

    def get_actual_temperature(self,channel):
        ActualTemperature=[0]
        result = TC300_COMMAND_LIB.TC300GetActualTemperature(self.device_handle,channel,ActualTemperature)
        if(result<0):
            raise RuntimeError(f"Error while reading actual temperature: {result}")
        else:
            return ActualTemperature[0]

    def set_target_temperature(self,channel,T):
        result = TC300_COMMAND_LIB.TC300SetTargetTemperature(self.device_handle,channel,T) 
        if(result<0):
            raise RuntimeError(f"Error while setting target temperature: {result}")
        else:
            return result 
        
    def get_target_temperature(self,channel):
        TargetTemperature=[0]
        result = TC300_COMMAND_LIB.TC300GetTargetTemperature(self.device_handle,channel,TargetTemperature)
        if(result<0):
            raise RuntimeError(f"Error while reading target temperature: {result}")
        else:
            return TargetTemperature[0]  

    def get_actual_current(self,channel):
        ActualCurrent=[0]
        result = TC300_COMMAND_LIB.TC300GetOutputCurrent(self.device_handle,channel,ActualCurrent)
        if(result<0):
            raise RuntimeError(f"Error while reading actual current: {result}")
        else:
            return ActualCurrent[0]

    def set_target_current(self,channel,I):
        result = TC300_COMMAND_LIB.TC300SetOutputCurrent(self.device_handle,channel,I) 
        if(result<0):
            raise RuntimeError(f"Error while setting target current: {result}")
        else:
            return result 
        
    def get_target_current(self,channel):
        TargetCurrent=[0]
        result = TC300_COMMAND_LIB.TC300GetTargetOutputCurrent(self.device_handle,channel,TargetCurrent)
        if(result<0):
            raise RuntimeError(f"Error while reading target current: {result}")
        else:
            return TargetCurrent[0]  
        
    def read_min_max_temperature(self,channel):
        MinTemperature=[0]
        result = TC300_COMMAND_LIB.TC300GetMinTemperature(self.device_handle,channel,MinTemperature)
        if(result<0):
                raise RuntimeError(f"Error while reading min temperature: {result}")
        MaxTemperature=[0]
        result = TC300_COMMAND_LIB.TC300GetMaxTemperature(self.device_handle,channel,MaxTemperature)
        if(result<0):
                raise RuntimeError(f"Error while reading max temperature: {result}")
        return (MinTemperature[0],MaxTemperature[0])

    def set_min_max_temperature(self,channel,mT,MT):
        result = TC300_COMMAND_LIB.TC300SetMinTemperature(self.device_handle, channel, mT) 
        if(result<0):
            raise RuntimeError(f"Error while setting min temperature: {result}")
        result = TC300_COMMAND_LIB.TC300SetMaxTemperature(self.device_handle, channel, MT) 
        if(result<0):
            raise RuntimeError(f"Error while setting max temperature: {result}")
        return True

    def read_PID_parameters(self,channel):
        P=[0]
        result = TC300_COMMAND_LIB.TC300GetPIDParameterP(self.device_handle, channel,P)
        if(result<0):
                raise RuntimeError(f"Error while reading PID parameter P: {result}")
        I=[0]
        result = TC300_COMMAND_LIB.TC300GetPIDParameterI(self.device_handle, channel,I)
        if(result<0):
                raise RuntimeError(f"Error while reading PID parameter I: {result}")
        D=[0]
        result = TC300_COMMAND_LIB.TC300GetPIDParameterD(self.device_handle, channel,D)
        if(result<0):
                raise RuntimeError(f"Error while reading PID parameter D: {result}")
        Period=[0]
        result = TC300_COMMAND_LIB.TC300GetPIDParameterPeriod(self.device_handle, channel,Period)
        if(result<0):
                raise RuntimeError(f"Error while reading PID parameter Period: {result}")
        return (P[0],I[0],D[0],Period[0])
    
    def set_PID_parameter(self,channel,Name,Value):
        PossibleNames = ['P','I','D','Period']
        Functions =[TC300_COMMAND_LIB.TC300SetPIDParameterP,TC300_COMMAND_LIB.TC300SetPIDParameterI,TC300_COMMAND_LIB.TC300SetPIDParameterD,TC300_COMMAND_LIB.TC300SetPIDParameterPeriod]
        if Name in PossibleNames:
            fun = Functions[PossibleNames.index(Name)]
            result = fun(self.device_handle, channel, Value) 
        if(result<0):
            raise RuntimeError(f"Error while setting PID parameter {Name}: {result}")
        return True


    