# funBaVef.py

# $language = "python"
# $interface = "1.0"

import pytest, sys, time, os, logging ,datetime
import sys
import time
import os
import basic.basicConf as bc
import paramiko
from netmiko import ConnectHandler

### Check VLAN Number ###

def checkVlanNum(host):                 
    with bc.connect(host) as child:
        command = "show vlan summary"
        print(command)
        cmdResult = child.send_command(command)
        numOfVlan = cmdResult.splitlines()[1].split()[5]
        print('Number of VLAN: {}'.format(numOfVlan))
        return numOfVlan


### Check MAX VTY SESSION  NETMIKO ###        
def checkVtySsion(host, vty):
    try:
        child_list = []
        for i in range(vty):
            child = bc.connect(host)
            child_list.append(child) # Child append a list To disconnect() the sesseions
        cmdResult = child.send_command('show users')
        cmdResult_list = cmdResult.splitlines()
        readResult = str(cmdResult_list)
        numOfVty = readResult.count('pts/')
        for child in child_list:
            child.disconnect()
        print('Number of sessions: {}'.format(numOfVty))
        return numOfVty
    except Exception as e:
        print('Error connecting: {}'.format(str(e)))
        return numOfVty
    
### Check Process plog ###
def checkPlog(testName,host):                  
    with bc.connect(host) as child:
        Command = "show process plog"
        cmdResult = child.send_command(Command)
        result_split = cmdResult.splitlines()[0]
        print(result_split)     
        result_split = result_split.split(':')[0]
        print(result_split)
        if result_split == 'ls':
            return 'OK'
        else:
            print (f'##### {testName} occur proecee log {result_split}  #####')
            return 'nok'

### Exception log ###
def ExceptionLog(testName):                 
    with open('./log/Exception_log.txt', 'at') as fw:

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

        fw.writelines(f'Exception occurs while performing_{testName} + {timestamp}' )
        return('exception')


     
 ### function to check the product type, which is either m6424 or not ### 
def checkProcuctType(host):
    with bc.connect(host) as child:
        showproduct = child.send_command ("sh fruinfo system ")
        checkproduct = showproduct.split()
        search_string = 'M6424'
        if search_string in checkproduct:
            return '6424'
        else:
            return 'other'
                
