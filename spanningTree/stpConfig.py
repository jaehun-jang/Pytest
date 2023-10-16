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
        
# def check_mng_gw(child,state):
#     successExpect = ['enable','10','1','192.168.0.2','success','normal']
#     failureExpect = ['enable','11','2','10.1.1.1','failure','fail']
#     result = []  
#     command = child.send_command('show mng ping') 
#     cmd_split = (command.splitlines())
#     command_list = [line for line in cmd_split if line.strip()] 
#     # print(type(command_list),command_list )               
#     result.append(command_list[2].split()[2]) 
#     result.append(command_list[3].split()[2])
#     result.append(command_list[4].split()[2])  
#     result.append(command_list[5].split()[3]) 
#     result.append(command_list[10].split()[3]) 
#     result.append(command_list[11].split()[3])         
#     print(result)            
#     if state == 'normal':           
#         if successExpect == result:
#             return True
#         else:
#             return False
#     if state == 'failure':           
#         if failureExpect == result:
#             return True
#         else:
#             return False

# def check_mng_evm(child,state):
#     command = child.send_command('show mng evm') 
#     cmd_split = (command.splitlines())
#     command_list = [line for line in cmd_split if line.strip()]                        
#     print(len(command_list))
#     if len(command_list) >= 15:
#         if state == 'gw':
#             process = command_list[15].split(':')[1].strip()  
#             action = command_list[16].split(':')[1].strip()     
#             print(f'Reserved Actions: {process} & {action}')        
#             if 'gate mon' == process and 'reboot' == action:
#                 return True
#             else:
#                 return False
#         elif state == 'process':
#             process = command_list[15].split(':')[1].strip() 
#             action = command_list[16].split(':')[1].strip()    
#             print(f'Reserved Actions: {process} & {action}')        
#             if 'mstpd' == process and 'restart' == action:
#                 return True
#             else:
#                 return False
#         elif state == 'memory':
#             process = command_list[15].split(':')[1].strip() 
#             action = command_list[16].split(':')[1].strip()    
#             print(f'Reserved Actions: {process} & {action}')        
#             if 'memory mon' == process and 'reboot' == action:
#                 return True
#             else:
#                 return False
#         elif state == 'watchdog':
#             result1 = command_list[10].split(':')[1].strip()   
#             result2 = command_list[11].split(':')[1].strip()     
#             print(result1,result2)        
#             if 'Normal' == result1 and '1' == result2:
#                 return True
#             else:
#                 return False
#     else:
#         return False

def stpModeCheck(child):
    # To reduce process time, this method uses child processes.
    command_output = child.send_command('show spanning-tree')
    # print(command_output)
    lines = command_output.splitlines()
    for line in lines:
        columns = line.split()           
        # Check spanning-tree Mode
        if columns and columns[0] == 'spanning-tree': 
            xstp = columns[3] 
            print(f"The Spanning mode is {xstp}") 
 
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

def get_stp_cli_result(child,string,cloum):
    command_output = child.send_command('show spanning-tree')
    lines = command_output.splitlines()
    for line in lines:
        columns = line.split() 
        # print(columns)          
        # Check spanning-tree Mode
        if columns and columns[0] == string : 
            result = columns[cloum] 
            print(f"The result reding spanning CLI is {result} ")
            return result 
                                 
# def get_stp_cli_result(dut,string,cloum):
#     with bc.connect(dut) as child:
#         # To reduce process time, this method uses child processes.
#         command_output = child.send_command('show spanning-tree')
#         lines = command_output.splitlines()
#         for line in lines:
#             columns = line.split()           
#             # Check spanning-tree Mode
#             if columns and columns[0] == string : 
#                 result = columns[1] 
#                 print(f"The result reding spanning CLI is {result} ")
#                 return result 
                                                                  
def check_stp_PortRole(dut2,mode):
    # Define the list of interfaces you want to check
    intList = ['1/10','1/11', '1/12', '1/13', '1/15', '1/16']  

    # Define the expected result as a dictionary
    expectResult = {
        '1/10': 'Edge',
        '1/11': 'Desg',
        '1/12': 'Bakp',
        '1/13': 'Desg',
        '1/15': 'Root',
        '1/16': 'Altn',
    }

    # Initialize the portRoles dictionary with default values
    readResult = {
        '1/10': 'Unknown',
        '1/11': 'Unknown',
        '1/12': 'Unknown',
        '1/13': 'Unknown',
        '1/15': 'Unknown',
        '1/16': 'Unknown',
    }
    with bc.connect(dut2) as child:
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

                    if  intList[0] == interface:  
                        # Check edge-port 
                        readResult[interface] = columns[5] 
                    else:                  
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
                                                      
def check_stp_PortState(dut,mode):
    normalport = '1/10'
    blockport = '1/12'
       
    with bc.connect(dut) as child:
        stp_mode_config =[
        f'spanning mode {mode}'
        ]
        child.send_config_set(stp_mode_config) 
        
        # Check spanning-tree Mode
        stpModeCheck(child) 
                 
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

def check_stp_RouteBridge(dut,mode):     
    result =[] 
    syspri = 4096
    bridge = 32768 
    with bc.connect(dut) as child:  
        # Check spanning-tree Mode
        stpModeCheck(child) 
        # Check current root bridge
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

def check_stp_system_config(devices):     
    result =[]
    cloum = 0
    string = '1/15'
    
    dut = devices[2]
    with bc.connect(dut) as child:  # Connect to DUT3 
        # Check spanning-tree Mode
        stpModeCheck(child) 
        time.sleep(2) 
                  
        # Check the bridge which has higher MAC address is elected as root bridge.        
        cloum = 1  # Get Port role of the interface      
        Portrole = get_stp_cli_result(child,string,cloum)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(Portrole)     
        time.sleep(2)
        
        cloum = 3  # cost value of the interface            
        Costvalue = get_stp_cli_result(child,string,cloum)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(Costvalue)  
        time.sleep(2)  
           
        if Portrole ==  'Altn' and Costvalue == '2000':
            result.append('True')
        else:
            result.append('False') 
        
        # Configure STP Path-Cost as Shot                    
        stpPathCost(dut,'short')
        time.sleep(3) 
        
        cloum = 1  # Get Port role of the interface      
        Portrole = get_stp_cli_result(child,string,cloum)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(Portrole)     
        time.sleep(2)
        
        cloum = 3  # cost value of the interface            
        Costvalue = get_stp_cli_result(child,string,cloum)
        # Costvalue = get_stp_cli_result(dut,string,cloum)
        print(Costvalue)  
        time.sleep(2)  
        
        if Portrole ==  'Desg' and Costvalue == '2':
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
    

def stpSystemPri(dut,mode,syspri):
    with bc.connect(dut) as child:
        if mode == 'mst':            
            stp_mode_config =[
            f'spanning-tree mst 0 priority {syspri}'
            ]
            child.send_config_set(stp_mode_config)  
            
        else:                
            stp_mode_config =[
            f'spanning-tree priority {syspri}'
            ]
            child.send_config_set(stp_mode_config)  
                                                                                                       
def stpModeConf(devices,mode):
    for device in devices:    
        with bc.connect(device) as child:
            stp_mode_disable = f'spanning mode disable'
            child.send_config_set(stp_mode_disable)  
            time.sleep(2) 
            stp_mode_config = f'spanning mode {mode}'
            child.send_config_set(stp_mode_config)  
                       
def stpEdgePortConf(devices):
    for device in devices:  
        with bc.connect(device) as child:
            stp_edgeport_config =[
                'interface 1/10',
                'spanning port type edge'
            ]
            child.send_config_set(stp_edgeport_config)  
            time.sleep(1)
            
def noStpEdgePortConf(devices):
    for device in devices:  
        with bc.connect(device) as child:
            stp_edgeport_config =[
                'interface 1/10',
                'no spanning port type edge'
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
                                           

