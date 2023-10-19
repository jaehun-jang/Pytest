# funBaConf.py

# $language = "python"
# $interface = "1.0"
import pytest, sys, time, os, logging ,datetime
from logging import root
import time, paramiko
import basic.basicConf as bc


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

################################################################################### 

def stpModeCheck(dut):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        # print(command_output)
        lines = command_output.splitlines()
        for line in lines:
            columns = line.split()           
            # Check spanning-tree Mode
            if columns and columns[0] == 'spanning-tree': 
                xstp = columns[3] 
                print(f"## The Spanning mode is {xstp} ##") 
 
def stpPortStateCheck(child,interface):
    # To reduce process time, this method uses child processes.
    command_output = child.send_command('show spanning-tree')
    lines = command_output.splitlines()
    for line in lines:
        columns = line.split()           
        if columns and columns[0] == interface: 
            state = columns[2] 
            print(f"The Spanning port state is {state}")
            return state

def get_stp_addrAndPri(dut):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()

        root_address = None
        bridge_address = None
        reading_root = False
        reading_bridge = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[0] == 'ROOT':
                reading_root = True
                reading_bridge = False
                rootPri = columns[3] 
            elif columns[0] == 'BRIDGE':
                reading_bridge = True
                reading_root = False
                bridgePri = columns[3] 
            if reading_root and columns[0] == 'address':
                root_address = columns[1]
            elif reading_bridge and columns[0] == 'address':
                bridge_address = columns[1]
                
        print('root_address: ', root_address, 'bridge_address: ', bridge_address)
        print('root_pri: ', rootPri, 'bridge_Pri: ', bridgePri)
        return root_address, bridge_address, rootPri, bridgePri

def get_stp_timer(dut,bridge):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()

        root_timer = None
        bridge_timer = None
        reading_root = False
        reading_bridge = False

        for line in lines:
            columns = line.split()
            if not columns:
                continue

            if columns[0] == 'ROOT':
                reading_root = True
                reading_bridge = False
            elif columns[0] == 'BRIDGE':
                reading_bridge = True
                reading_root = False
            if reading_root and columns[0] == 'Hello':
                root_timer = [columns[2], columns[5], columns[8]]
            elif reading_bridge and columns[0] == 'Hello':
                bridge_timer = [columns[2], columns[5], columns[8]]        

        if bridge == 'root':
            print(f'Root Bridge Hello_Time: {root_timer[0]}, Max_age: {root_timer[1]}, Forward_Delay: {root_timer[2]}')
            return root_timer
        elif bridge == 'bridge':
            print(f'Bridge Hello_Time: {bridge_timer[0]}, Max_age: {bridge_timer[1]}, Forward_Delay: {bridge_timer[2]}')
            return bridge_timer
        
def get_stp_cli_result(dut,string,cloum):
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()
        print(command_output)
        for line in lines:
            columns = line.split()         
            # Check spanning-tree Mode
            if columns and columns[0] == string : 
                result = columns[cloum] 
                print(f"The result of reding spanning CLI is {result} ")
                return result 
        
def get_cli_result(dut,command,string,cloum):
    with bc.connect(dut) as child:
        command_output = child.send_command(command)
        lines = command_output.splitlines()
        print(command_output)
        for line in lines:
            columns = line.split()        
            # Check spanning-tree Mode
            if columns and columns[0] == string : 
                result = columns[cloum] 
                print(f'The result of reding spanning CLI is "{result}" ')
                return result
         
### check_stp_[PORT ROLE]............                                                                 
def check_stp_PortRole(dut,mode):
    # Define the list of interfaces you want to check
    intList = ['1/11', '1/12', '1/13', '1/15', '1/16']  

    # Define the expected result as a dictionary
    expectResult = {
        '1/11': 'Desg',
        '1/12': 'Bakp',
        '1/13': 'Desg',
        '1/15': 'Root',
        '1/16': 'Altn',
    }

    # Initialize the portRoles dictionary with default values
    readResult = {
        '1/11': 'Unknown',
        '1/12': 'Unknown',
        '1/13': 'Unknown',
        '1/15': 'Unknown',
        '1/16': 'Unknown',
    }
    with bc.connect(dut) as child:
        command_output = child.send_command('show spanning-tree')
        lines = command_output.splitlines()

        for line in lines:
            columns = line.split()
            
            # Check if the line starts with the spanning-tree 
            if columns and columns[0] == 'spanning-tree': 
                xstp = columns[3] 
                print(f"The Spanning mode is {xstp}")   
                                                   
        for interface in intList:
            for index, line in enumerate(lines):
                columns = line.split()

                # Check if the line starts with the interface name
                if columns and columns[0] == interface:
                    # print(f"The index, including the interface {interface}, is {index}.")              
                    # Store the readResult in the dictionary
                    readResult[interface] = columns[1]
                
    # Print the port roles for the specified interfaces
    # for interface, role in readResult.items():
    #     print(f"Interface {interface}: Port Role is {role}")

    print("Read Roles:", readResult)
    print("Expected Result:", expectResult)
    
    # Compare readResult with expectResult
    if readResult == expectResult and xstp == mode:
        return True
    else:
        return False

### check_stp_[PORT STATE]............                                                      
def check_stp_PortState(dut,mode):
    normalport = '1/10'
    blockport = '1/12'
       
    with bc.connect(dut) as child:
        stp_mode_config =[
        f'spanning mode {mode}'       
        ]
        child.send_config_set(stp_mode_config)     
                         
        if mode == 'stp': 
            expectResult = ['LSN','LRN','FWD','BLK']
            readResult = []
            # Check the STP state of the interface.
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(15) 
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(15)            
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(2)            
            readResult.append(stpPortStateCheck(child,blockport)) 
            
            print("Read Roles:", readResult) 
             
            stpModeCheck(dut) 
            time.sleep(2)  
                            
            # Compare readResult with expectResult
            if readResult == expectResult:
                return True
            else:
                return False  

        else: 
            expectResult = ['DSC','FWD','DSC']
            readResult = []
            # Check the STP state of the interface.
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(5)            
            readResult.append(stpPortStateCheck(child,normalport))
            time.sleep(1)             
            readResult.append(stpPortStateCheck(child,blockport))  
                        
            print("Read Roles:", readResult)  
            # Compare readResult with expectResult
            if readResult == expectResult:
                return True
            else:
                return False    

### check_stp_[ROOT BRIDGE ELECTION]............
def check_stp_RouteBridge(dut,mode):     
    result =[] 
    syspri = 4096
    bridge = 32768 

    stpModeCheck(dut) 
    time.sleep(2)
                
    # Check the bridge which has higher MAC address is elected as root bridge.
    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(dut)
    if root_address ==  bridge_address:
        result.append('True')
    else:
        result.append('False') 

    # Configure STP system priority                    
    stpSystemPri(dut,mode,syspri)
    time.sleep(3) 
    
    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(dut)
    
    if root_address == bridge_address and (root_pri == '4096' or root_pri == '4097'):
        result.append('True')
    else:
        result.append('False') 
                        
    # Configure STP system priority   
    stpSystemPri(dut,mode,bridge)
    time.sleep(3) 
                                    
    print(result)
    if result == ['False', 'True']:
        return True
    else:
        return False

### check_stp_[PATH-COST]............  
def check_stp_system_config(dut):     
    result =[]
    cloum = 0
    string = 'Cost'
    
    stpModeCheck(dut) 
    time.sleep(2)
                  
    # Check the bridge which has higher MAC address is elected as root bridge.        
    # cloum = 1  # Get Port role of the interface      
    # Portrole = get_stp_cli_result(dut,string,cloum)
    # # Costvalue = get_stp_cli_result(dut,string,cloum)
    # print(Portrole)     
    # time.sleep(2)
    
    cloum = 1  # cost value of the interface            
    Costvalue = get_stp_cli_result(dut,string,cloum)
    # Costvalue = get_stp_cli_result(dut,string,cloum)
    print(Costvalue)  
    time.sleep(2)  
        
    if Costvalue == '2000':
    # if Portrole ==  'Altn' and Costvalue == '2000':
        result.append('True')
    else:
        result.append('False') 
    
    # Configure STP Path-Cost as Shot                    
    stpPathCost(dut,'short')
    time.sleep(3) 
    
    # cloum = 1  # Get Port role of the interface      
    # Portrole = get_stp_cli_result(dut,string,cloum)
    # # Costvalue = get_stp_cli_result(dut,string,cloum)
    # print(Portrole)     
    # time.sleep(2)
    
    cloum = 1  # cost value of the interface            
    Costvalue = get_stp_cli_result(dut,string,cloum)
    # Costvalue = get_stp_cli_result(dut,string,cloum)
    print(Costvalue)  
    time.sleep(2)  
    
    if Costvalue == '2':
    # if Portrole ==  'Desg' and Costvalue == '2':
        result.append('True')
    else:
        result.append('False') 

    # Configure STP Path-Cost as Shot                    
    stpPathCost(dut,'long')
    time.sleep(5) 
        
    print(result)                                            
    if result == ['True','True']:
        return True
    else:
        return False

### check_stp_[TIMER]............    
def check_stp_timer_config(devs): 
        
    stpModeCheck(devs[0]) 
    time.sleep(2)
    
    with bc.connect(devs[0]) as child:  # Connect to DUT1                      
        # Configure STP Path-Cost as Shot  
        hello = 4
        forwardDelaty = 30
        maxage = 40                  
        stpTimerConf(devs[0],hello,forwardDelaty,maxage)
        time.sleep(5) 

        #Check the bridge which has higher MAC address is elected as root bridge.        
        bridge = 'bridge'  # Get Port role of the interface      
        rootTimer = get_stp_timer(devs[0],bridge)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(rootTimer)     
        time.sleep(5)
                
    with bc.connect(devs[1]) as child:  # Connect to DUT1               
        # Check the bridge which has higher MAC address is elected as root bridge.        
        bridge = 'root'  # Get Port role of the interface      
        bridgeTimer = get_stp_timer(devs[1],bridge)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(bridgeTimer)     
        time.sleep(5)

    with bc.connect(devs[0]) as child:  # Connect to DUT1                      
        # Configure STP Path-Cost as Shot  
        hello = 2
        forwardDelaty = 15
        maxage = 20                    
        stpTimerConf(devs[0],hello,forwardDelaty,maxage)
        time.sleep(5) 
                                                  
    if rootTimer == bridgeTimer:
        return True
    else:
        return False

### check_stp_[RootGuard]............ 
def check_stp_RootGuard(devs,mode):
    result = []  
    command =['interface 1/14','shutdown'] 
    bc.sendConfigSet(devs[0],command)  
    
    syspri = 8192        
    stpRootGuardConf(devs[0])
    time.sleep(1)    
    stpSystemPri(devs[0],mode,syspri) 
    time.sleep(1) 
            
    syspri = 4096    
    stpSystemPri(devs[1],mode,syspri) 
    
    # Check if the root bridge is protected..            
    with bc.connect(devs[0]) as child:  # Connect to DUT1               
        startString = '1/15'
        cloum = 6
        
    reString = get_stp_cli_result(devs[0],startString,cloum)
        
    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(devs[0])    
    
    if reString == 'Root-Inc' and root_address == bridge_address:
        result.append('True')
    else:
        result.append('False')

    # Check if the root bridge is changed.      
    noStpRootGuardConf(devs[0]) # Disable Root Guard in the interface
    time.sleep(10) 

    root_address, bridge_address, root_pri, bridge_pri = get_stp_addrAndPri(devs[0])  
    
    if  root_address != bridge_address:
        result.append('True')
    else:
        result.append('False')

    syspri = 32768    
    stpSystemPri(devs[1],mode,syspri) 
    
    command =['interface 1/14','no shutdown'] 
    bc.sendConfigSet(devs[0],command)
                                                                    
    if  result.count('True') == 2:
        return True
    else:
        False

### check_stp_BpduGuard............ 
def check_stp_BpduGuard(devs):
    result = []

    stpModeCheck(devs[2]) 
    time.sleep(2)
                                      
    stpBpduGuardConf(devs[2])
    time.sleep(2)    
    errdisBpduGuar(devs[2])
    time.sleep(5) 
        
    # Check if the bpduguard is detected..                         
    command = 'sh errdisable recovery'
    startString = 'bpduguard(1/16)'
    cloum = 0        
    reString = get_cli_result(devs[2],command,startString,cloum)
    
    time.sleep(2) 
    noStpBpduGuardConf(devs[2])
    time.sleep(2) 
        
    if reString == 'bpduguard(1/16)':
        return True
    else:
        return False


### check_stp_BpduFilter............ 
def check_stp_BpduFilter(dut,mode):
    result = []

    stpModeCheck(dut) 
    time.sleep(1)
                                      
    # Check if the bpduguard is detected..                         
    command = 'sh spanning-tree'
    startString = '1/16'
    cloum = 1        
    reString = get_cli_result(dut,command,startString,cloum)
    
    if reString == 'Root':
        result.append('True')
    else:
        result.append('False')
        
    # Config BPDU filter on the interface. #         
    stpBpduFilterConf(dut)
    # stpBpduFilterConf(dut)
    time.sleep(1)    
        
    # Wait until the MAX-Age time has elapsed. # 
    if mode == 'stp':
        time.sleep(25) 
    else:
        time.sleep(7)       

    reString = get_cli_result(dut,command,startString,cloum)
    
    if reString == 'Desg':
        result.append('True')
    else:
        result.append('False')

    noStpBpduFilterConf(dut)
    time.sleep(2) 
        
    time.sleep(2) 

    print(result)            
    if  result.count('True') == 2:
        return True
    else:
        False
       
### check_stp_EdgePort............ 
def check_stp_EdgePort(devs,mode):
    result = []

    stpModeCheck(devs[1]) 
    time.sleep(2)
                                              
    # Check if the edgeport is configured.                         
    command = 'sh spanning-tree'
    startString = '1/13'
    cloum = 5   

    stpEdgePortConf(devs[1],startString)
    time.sleep(5)         
         
    reString = get_cli_result(devs[1],command,startString,cloum)

    print('reString :', reString)    
    
    if reString == 'Edge':
        result.append('True')
    else:
        result.append('False')
    
    # Enable STP on dut#3 
    dut = ['192.168.0.203']
    stpModeConf(dut,mode)

    # Check if the edgeport is released.
    reString = get_cli_result(devs[1],command,startString,cloum)
    
    if reString == 'point-to-point':
        result.append('True')
    else:
        result.append('False')
        
    time.sleep(2)
    noStpEdgePortConf(devs[1],startString)     

    # Disable STP on dut#3 
    dut = ['192.168.0.203']
    # dut = ['192.168.0.203']
    stpModeConf(dut,'disable')
    
    print(result)            
    if  result.count('True') == 2:
        return True
    else:
        False
       
        
        
##############################################################################
        
def stpSystemPri(dut,mode,syspri):
    with bc.connect(dut) as child:
        if mode == 'mst':            
            stp_mode_config =[
            f'spanning-tree mst 0 priority {syspri}'
            ]
            child.send_config_set(stp_mode_config)
            time.sleep(1)                            
        else:                
            stp_mode_config =[
            f'spanning-tree priority {syspri}'
            ]
            child.send_config_set(stp_mode_config) 
            time.sleep(1)     
                                                                                                       
def stpModeConf(devs,mode):
    for dev in devs:    
        with bc.connect(dev) as child:
            # stp_mode_disable = f'spanning mode disable'
            # child.send_config_set(stp_mode_disable)  
            # time.sleep(2) 
            stp_mode_config = f'spanning mode {mode}'
            child.send_config_set(stp_mode_config)
            time.sleep(1)               
                       
def stpEdgePortConf(dev,int):
    with bc.connect(dev) as child:
        stp_edgeport_config =[
            f'interface {int}',
            'spanning port type edge'
        ]
        child.send_config_set(stp_edgeport_config)  
        time.sleep(1)
            
def noStpEdgePortConf(dev,int):
    with bc.connect(dev) as child:
        stp_edgeport_config =[
            f'interface {int}',
            'no spanning port type'
        ]
        child.send_config_set(stp_edgeport_config)  
        time.sleep(1)
            
def stpPathCost(dut, mode):
    with bc.connect(dut) as child:
        stp_edgeport_config =[
            f'spanning-tree pathcost method {mode}',
        ]
        child.send_config_set(stp_edgeport_config)  
        time.sleep(1)
                                           

def stpTimerConf(dut,hello,forwardDelaty,maxage):
    with bc.connect(dut) as child:
        stp_timer_config =[
            f'spanning-tree hello-time {hello}',
            f'spanning-tree forward-time {forwardDelaty}',
            f'spanning-tree max-age {maxage}',
        ]
        child.send_config_set(stp_timer_config)  
        time.sleep(1)

def stpRootGuardConf(dut):
    with bc.connect(dut) as child:
        stp_rootguard_config =[
            'interface range 1/15-1/16',
            'spanning-tree guard root'                
        ]
        child.send_config_set(stp_rootguard_config)  
        time.sleep(1)

def noStpRootGuardConf(dut):
    with bc.connect(dut) as child:
        stp_rootguard_config =[
            'interface range 1/15-1/16',
            'no spanning-tree guard root'
        ]
        child.send_config_set(stp_rootguard_config)  
        time.sleep(1)                                    

def stpBpduGuardConf(dut):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            'interface range 1/16',
            'spanning-tree bpduguard enable'                
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)

def noStpBpduGuardConf(dut):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            'interface range 1/16',
            'no spanning-tree bpduguard'
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)  
                
def errdisBpduGuar(dut):
    with bc.connect(dut) as child:
        stp_bpduguard_config =[
            'errdisable recovery reason bpduguard'            
        ]
        child.send_config_set(stp_bpduguard_config)  
        time.sleep(1)        
                
def stpBpduFilterConf(dut):
    with bc.connect(dut) as child:
        stp_bpdufilter_config =[
            'interface 1/16',
            'spanning-tree bpdufilter enable'                
        ]
        child.send_config_set(stp_bpdufilter_config)  
        time.sleep(1)          
        
def noStpBpduFilterConf(dut):
    with bc.connect(dut) as child:
        stp_bpdufilter_config =[
            'interface 1/16',
            'no spanning-tree bpdufilter'             
        ]
        child.send_config_set(stp_bpdufilter_config)  
        time.sleep(1)       
               