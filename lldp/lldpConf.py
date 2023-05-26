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
import lldp.lldpVef as llv


def disTitle(child,Title):
    child.sendline('\n') 
    child.sendline(Title )
    child.sendline('\n')

###################################################################################

def disblldp(child):
    config_set = ['interface 1/25', 'lldp disable']
    child.send_config_set(config_set)

def enblldp(child):
    config_set = ['interface 1/25', 'lldp enable txrx']
    child.send_config_set(config_set)

def changLldpTlv(child,stateI,tlvI):
    state = ['','no']
    tlv = ['8021-org-spec','8023-org-spec','basic']
    config_set = ['interface 1/25', state[stateI] + ' lldp tlv-select ' + tlv[tlvI] + ' all']
    child.send_config_set(config_set) 
    
def changLldpTlvall(child,dut2):
    result = []
    sucCount = 0
    state = ['no','']
    org = ['8021-org-spec','8023-org-spec','basic']
    tlv = ['port-protocol-vid', 'port-vid', 'protocol-identity', 'vlan-name', 'link-aggregation', 'mac-phy-cfg', 'max-frame-size', 'power', 'preemption-capability', 'management-address', 'port-description', 'system-capabilities', 'system-description ', 'system-name']
    time.sleep(1)
    for stateI in state:
        for orgI in org:
            if orgI == '8021-org-spec':
                print('#'*3 + ' ' + stateI +' 8021-org-spec ' + '#'*3  )
                for tlvI in tlv[0:4]:
                    config_set = ['interface 1/25', stateI+' lldp tlv-select '+ orgI +' '+ tlvI ]
                    child.send_config_set(config_set) 
                    time.sleep(1.5)
                    result.append(llv.checkLldpNeighborTlvCF(dut2,sucCount))
                    time.sleep(1.5)
                    sucCount += 1
            elif orgI == '8023-org-spec':
                print('#'*3 + ' ' +  stateI +' 8023-org-spec ' + '#'*3  )
                for tlvI in tlv[4:9]:
                    config_set = ['interface 1/25', stateI+' lldp tlv-select '+ orgI +' '+ tlvI ]
                    child.send_config_set(config_set)
                    time.sleep(1.5)
                    result.append(llv.checkLldpNeighborTlvCF(dut2,sucCount))
                    time.sleep(1.5)
                    sucCount += 1
            elif orgI == 'basic':
                print('#'*3 + ' ' +  stateI +' basic ' + '#'*3  )
                for tlvI in tlv[9::]:
                    config_set = ['interface 1/25', stateI+' lldp tlv-select '+ orgI +' '+ tlvI ]
                    child.send_config_set(config_set)
                    time.sleep(1.5)
                    result.append(llv.checkLldpNeighborTlvCF(dut2,sucCount))
                    time.sleep(1.5)
                    sucCount += 1 
#    print(result)   
    if result.count('Ok') == 28:
        return ['Ok']
    else:
        return ['Nok']
    
    
def setMgmtTlv(child):
    child.send_config_set('lldp tlv-set management-address-tlv mac-address')

def setLldpTimer(child):
    config_set = ['lldp holdtime-multiplier 4', 'lldp tx-interval 10']
    child.send_config_set(config_set)

def chgMgmtTlv(child):
    child.send_config_set('system management-address vlan 1 v6')


    
###################################################################################

### Static Link Aggregation ###	  
def confEthService(host):
    svc = 2
    uni = 1
    mc.crtServi(host,svc,uni)
    time.sleep(1)

### Pure Static Link Aggregation ###	  
def removeEthService(host):
    svc = 2
    uni = 1  
    mc.dltServi(host,svc,uni)
    time.sleep(1)

def confBasicLldp(dut1,dut2): 
    with bc.connect(dut1) as child: 
        result = []
        confEthService(dut1)
        time.sleep(3)
        print('#' * 3 + ' check lacp default tlv ' + '#' * 3)
        result.append(llv.checkLldpNeighborTlvC(dut2,'default'))
        time.sleep(1)               
        disblldp(child)
        time.sleep(3)
        print('#' * 3 + ' check lldp disable all tlv ' + '#' * 3)
        result.append(llv.checkLldpNeighborTlvC(dut2,'disable'))
        time.sleep(1)
        enblldp(child)
        time.sleep(3)
        print('#' * 3 + ' check lldp enable all tlv' + '#' * 3)
        result.append(llv.checkLldpNeighborTlvC(dut2,'enable'))
        time.sleep(3)
        print('#' * 3 + ' change lldp TLV to enable/disable for each tlv' + '#' * 3)
        result.extend(changLldpTlvall(child,dut2))
        time.sleep(3)
        setMgmtTlv(child)
        time.sleep(3)
        print('#' * 3 + ' check lldp setMgmtTlv ' + '#' * 3)
        result.append(llv.checkLldpNeighborTlvD(dut2,'mgmt-subtype'))
        time.sleep(1)
        setLldpTimer(child)
        time.sleep(3)
        print('#' * 3 + ' check lldp setLldpTimer ' + '#' * 3)
        result.append(llv.checkLldpNeighborTlvD(dut2,'lldp-timer'))
        time.sleep(1)
        chgMgmtTlv(child) 
        time.sleep(3)
        print('#' * 3 + ' check lldp chgMgmtTlv ' + '#' * 3)
        result.append(llv.checkLldpNeighborTlvD(dut2,'sys-mgmt'))
        time.sleep(1)
        print(result)
        removeEthService(dut1) 
        return result.count('Ok')

