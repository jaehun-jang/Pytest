# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
import unittest
import pexpect
import sys
import time
import os

import basic.basicConf as bc
import mef.mefConf as mc
import eoam.eoamVef as eov


###################################################################################
def disSubTitle(child,Title):
    child.send_config(Title )

###################################################################################

def disbEoam(child):
    config_set = [
                'interface 1/25',
                'ethernet oam disable'
                ]
    child.send_config_set(config_set)

def enbEoamAct(child):
    config_set = [
                'interface 1/25',
                'ethernet oam enable',
                'ethernet oam mode active'
                ]
    child.send_config_set(config_set)

def enbEoamPsv(child):
    config_set = [
                'interface 1/25',
                'ethernet oam enable',
                'ethernet oam mode passive'
                ]
    child.send_config_set(config_set)

def confDyingGasp(child):
    config_set = [
                'interface 1/25',
                'no ethernet oam link-event dying-gasp enable'
                ]
    child.send_config_set(config_set) 

def confLinkFault(child):
    config_set = [
                'interface 1/25',
                'no ethernet oam link-event link-fault enable'
                ]
    child.send_config_set(config_set) 

def confMonitor(child):
    config_set = [
                'interface 1/25',
                'ethernet oam link-monitor on', 
                'ethernet oam link-monitor supported' 
                ]
    child.send_config_set(config_set) 

def confRemoteLB(child):
    config_set = [
                'interface 1/25',
                'ethernet oam remote-loopback supported', 
                'ethernet oam remote-loopback timeout 5' 
                ]
    child.send_config_set(config_set) 

def startRemoteLB(child):
    config_set = [
                'ethernet oam remote-loopback test packet-count 15',
                'ethernet oam remote-loopback test packet-size 1500', 
                'ethernet oam remote-loopback start interface 1/25',
                'ethernet oam remote-loopback test start'
                ]
    for i in config_set:
        child.send_command(i)

def stopRemoteLB(child):
    child.send_command('ethernet oam remote-loopback stop interface 1/25 ') 

###################################################################################

def confEoam(host):
    svc = 1
    uni = 1
    with bc.connect(host) as child: 
        mc.crtServi(host,svc,uni)
        time.sleep(1)
        enbEoamAct(child)
        time.sleep(1)

def removeEoam(host):
    svc = 1
    uni = 1
    with bc.connect(host) as child: 
        mc.dltServi(host,svc,uni)
        time.sleep(1)
        disbEoam(child)
        time.sleep(1)

def confBasicEoam(dut1,dut2):
    with bc.connect(dut1) as child: 
        result = []
        confEoam(dut1)
        time.sleep(2) 
        enbEoamPsv(child)
        time.sleep(2) 
        print('#'*3 + ' Ethernet OAM Passive Mode ' + '#'*3 )
        result.append(eov.checkEoamNeighborDisc(dut2,'passive'))
        print(result)
        time.sleep(2)
        enbEoamAct(child)
        time.sleep(2) 
        print('#'*3 + ' Ethernet OAM Active Mode ' + '#'*3 )                 
        result.append(eov.checkEoamNeighborDisc(dut2,'active'))
        print(result)
        time.sleep(2)
        confDyingGasp(child)
    #    input("Enter!") 
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM dying-gasp ' + '#'*3 )                    
        result.append(eov.checkEoamStatus(dut1,'dying-gasp'))
        print(result)
        time.sleep(2)
        confLinkFault(child)
    #    input("Enter!") 
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM link-fault ' + '#'*3 )                      
        result.append(eov.checkEoamStatus(dut1,'link-fault'))
        print(result)
        time.sleep(2)
        confMonitor(child)
    #    input("Enter!") 
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM link-monitor ' + '#'*3 )                
        result.append(eov.checkEoamStatus(dut1,'link-monitor'))
        print(result)
        time.sleep(2) 
        startRemoteLB(child)
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM Loopback Test(start) ' + '#'*3 )  
        result.append(eov.checkEoamNeighborDisc(dut2,'startLBTest'))  
        print(result)
        time.sleep(15) 
        stopRemoteLB(child)
        time.sleep(2)
        print('#'*3 + ' Ethernet OAM Loopback Test(stop) ' + '#'*3 )  
        result.append(eov.checkEoamNeighborDisc(dut2,'stopLBTest'))  
        print(result)
        result.append(eov.RLBTestResult(dut1))  
        time.sleep(2)    
        print(result)
        removeEoam(dut1)
        time.sleep(5)
        return result.count('Ok')
