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
import lag.lagVef as lav


def disSubTitle(child,Title):
    child.send_command(Title )


def staticLag(child):
    config_set = [
                'interface 1/23',  
                'channel-group 1 mode on working',
                'interface 1/24',
                'channel-group 1 mode on protection'
    ]
    child.send_config_set(config_set)

def activeLacp(child):
    config_set = [
                'interface 1/23',  
                'channel-group 1 mode active',
                'lacp timeout short',
                'interface 1/24',
                'channel-group 1 mode active',
                'lacp timeout short'
    ]
    child.send_config_set(config_set)

def passiveLacp(child):
    config_set = [
                'interface 1/23',  
                'channel-group 1 mode passive',
                'lacp timeout short',
                'interface 1/24',
                'channel-group 1 mode passive',
                'lacp timeout short'
    ]
    child.send_config_set(config_set)

def changeMaxMember(child,maxmember):
    child.send_config_set(f'port-channel 1 max-member {maxmember}')

def delNniInt(child):
    config_set = ['ethernet nni nni1', 'no map interface']
    child.send_config_set(config_set)    

def addNniInt(child):
    config_set = ['ethernet nni nni1', 'map interface po1']
    child.send_config_set(config_set)     

def delPortCh(child):    
    config_set = ['interface range 1/23-1/24', 'no channel-group']
    child.send_config_set(config_set)

def deflacpTime(child):    
    config_set = ['interface range 1/23-1/24', 'lacp timeout long']
    child.send_config_set(config_set)

def noshutLagInt(child):    
    config_set = ['interface po1', 'no shutdown']
    child.send_config_set(config_set)

def shutLagInt(child):    
    config_set = ['interface po1', 'shutdown']
    child.send_config_set(config_set)

###################################################################################

### Static Link Aggregation ###	  
def confLag(host):
    with bc.connect(host) as child:
        svc = 1
        uni = 1
        mc.crtServi(host,svc,uni)
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        staticLag(child)
        time.sleep(1)
        addNniInt(child)
        time.sleep(1)
        noshutLagInt(child)
        time.sleep(1)

### Static Link Aggregation ###	  
def confLacp(host):
    with bc.connect(host) as child:
        svc = 1
        uni = 1
        mc.crtServi(host,svc,uni)
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        activeLacp(child)
        time.sleep(1)
        addNniInt(child)
        time.sleep(1)


### Pure Static Link Aggregation ###	  
def removeLag(host):
    with bc.connect(host) as child:
        svc = 1
        uni = 1
        delNniInt(child)
        time.sleep(1)
        delPortCh(child)
        time.sleep(1)   
        mc.dltServi(host,svc,uni)
        time.sleep(1)
        shutLagInt(child)
        time.sleep(1)

### Pure Static Link Aggregation ###	  
def removeLacp(host):
    with bc.connect(host) as child:
        svc = 1
        uni = 1
        delNniInt(child)
        time.sleep(1)
        deflacpTime(child)
        time.sleep(1)
        delPortCh(child)
        time.sleep(1)   
        mc.dltServi(host,svc,uni)
        time.sleep(1)
        shutLagInt(child)
        time.sleep(1)

### Redundant Static Link Aggregation ###	  

def confStaticLag(host):
        result = []
        confLag(host)
        print('#' * 3 + ' check static channel-group ' + '#' * 3)
        result.append(lav.checkPortChannel(host,'static'))
        time.sleep(1)
        print('#' * 3 + ' check BCM Port state ' + '#' * 3)
        result.append(lav.checkBcmPort(host,'hotstandby'))
        time.sleep(1)
        removeLag(host)
        print(result)
        return result.count('Ok')

def confBasicLacp(host): 
    with bc.connect(host) as child: 
        result = []
        confLacp(host)
        time.sleep(10)
        print('#' * 3 + ' check lacp active Mode ' + '#' * 3)
        result.append(lav.checkPortChannel(host,'lacp'))
        result.append(lav.checkLacpInternal(host,'active')) 
        time.sleep(1)
        delNniInt(child)
        time.sleep(1)
        passiveLacp(child)
        time.sleep(1)    
        addNniInt(child)
        time.sleep(5)
        print('#' * 3 + ' check lacp passive Mode ' + '#' * 3)    
        result.append(lav.checkPortChannel(host,'lacp'))
        result.append(lav.checkLacpInternal(host,'passive'))
        time.sleep(1)
        changeMaxMember(child,1)
        time.sleep(5)
        print('#' * 3 + ' check lacp MaxMember 1 ' + '#' * 3) 
        result.append(lav.checkPortChannel(host,'hotstandby'))
        result.append(lav.checkLacpInternal(host,'hotstandby'))
        time.sleep(1)
        print('#' * 3 + ' check BCM Port state ' + '#' * 3)            
        result.append(lav.checkBcmPort(host,'hotstandby'))
        changeMaxMember(child,8)
        time.sleep(5)
        print('#' * 3 + ' check lacp MaxMember 8 ' + '#' * 3) 
        result.append(lav.checkPortChannel(host,'lacp'))
        result.append(lav.checkLacpInternal(host,'passive'))
        time.sleep(1)  
        result.append(lav.checkBcmPort(host,'normal'))
        time.sleep(1)
        removeLacp(host)  
        print(result)  
        return result.count('Ok')

