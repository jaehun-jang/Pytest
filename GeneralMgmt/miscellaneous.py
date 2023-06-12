# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import unittest
import pexpect
import sys
import time, datetime
import os

import basic.basicConf as bc
import mef.mefConf as mc
import lldp.lldpVef as llv


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

################################################################################### 
### Check LLDP Neighbor ###

def checkntpconf(host): 
    with bc.connect(host) as child:  
        command = child.send_command('show ntp associations')        
        cmd_split = command.splitlines()[1].split()
        # print(cmd_split)       
        readResult = str(cmd_split[0])
        print(f"Server status: {readResult}")
        if readResult == '*~106.247.248.106':
            return True
        else: 
            return False

def checktime(host):
    with bc.connect(host) as child:  
        command = child.send_command('show clock')         
        cmd_split = command.splitlines()[0] 
        #output_string = cmd_split[:5] + cmd_split[8:] # To delete :%S 
        output_string = cmd_split[:2] + cmd_split[8:] # To delete %M:%S 
        print(f"Current time: {output_string}")
        return output_string

def checkmaxntpserver(host):
    with bc.connect(host) as child:  
        command = child.send_command('show ntp associations')        
        cmd_split = command.splitlines()[1:5] 
        output_string = str(cmd_split)
        output_string.split()       
        servercount = output_string.count('~1')
        print(f"server count: {servercount}")
        return servercount

##################################################################################
    
def tcpdump(dut1): 
    with bc.connect(dut1) as child: 
        command = child.send_command('tcpdump -vi eth0', expect_string= 'length')
        time.sleep(1) 
        # print(command)
        child.write_channel('\x03')
        result = command.splitlines() 
        resultlen = len(result) 
        print(f'tcpdump count: {resultlen}')
        return resultlen

def traceRT(dut1): 
    dnsserver = '168.126.63.1'
    with bc.connect(dut1) as child: 
        # command = child.send_command(f'traceroute {dnsserver}', expect_string= 'packets') 
        command = child.send_command(f'traceroute {dnsserver}', expect_string= 'ms')   
        time.sleep(1)
        print(command)
        ctlPC = child.write_channel('\x03')  
        result = command.splitlines()[-2].split()[1]
        print(result)
        return result
