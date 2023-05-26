# funBaConf.py

# $language = "python"
# $interface = "1.0"

from logging import root
from netmiko import ConnectHandler
import sys
import time
import os

def login(testName):
    child = connect() 
    fout = open('./log/' + testName +'_log.txt', 'wt' )
    child.logfile = fout
    child.logfile_read = sys.stdout
    return child

def connect(host):
    login ={
        'device_type':'cisco_ios',
        'ip': host, 
        'username':'root', 
        'password':'admin',
        'session_timeout': 120,
        'timeout': 120,
        'global_delay_factor': 2,
        }
    device = ConnectHandler(**login)
    # with ConnectHandler(**login) as device:
    device.enable() ## Enable mode ##
    return device
def connectbcm(host):
    login ={
        'device_type':'cisco_ios',
        'ip': host, 
        'username':'root', 
        'password':'admin',
        'session_timeout': 120,
        'timeout': 120,
        'global_delay_factor': 2,
        }
    device = ConnectHandler(**login)
    # with ConnectHandler(**login) as device:
    return device
                      
### Print Title  ###	
def disTitle(host,Title):
    with connect(host) as child:
        child.send_command(Title)
 
### default SetUp  ###	  
def defaultSetup(host):
    with connect(host) as child:
        child.enable()
        default_config = ["logging console", "aaa auth attempts login 0"]
        child.send_config_set(default_config)
        time.sleep(1)
        hostname_config = {"192.168.0.211": "hostname LAB3", "192.168.0.212": "hostname LAB4"} 
        """  Using Dictionary """
        if host in hostname_config:
            child.send_config_set(hostname_config[host])
        time.sleep(1)

### Create maximum numberof VLAN  ###	  
def crtVlan(host,vlans):
    with connect(host) as sub_child:
        result= sub_child.send_config_set('vlan 2-%s' % str(vlans))
        return result 

### Delet maximum numberof VLAN  ###	  
def dltVlan(host,vlans):
    with connect(host) as child:
        if vlans == 1:
            return
        else:
            host.send_config_set("no vlan 2-%s" % str(vlans))    
            time.sleep(1) 


### Delet maximum numberof VLAN  ###	  
def dltDevVlan(host,vlans):
    with connect(host) as sub_child:
        if vlans == 1:
            return
        else:
            groups = []
            quotient, remainder = divmod(vlans, 10)
            start = 1
            for i in range(10):
                if remainder > 0:
                    end = start + quotient
                    remainder -= 1
                    sub_child.send_config_set("no vlan %s-%s" % (str(start), str(end)))
                else:
                    end = start + quotient - 1
                    sub_child.send_config_set("no vlan %s-%s" % (str(start), str(end)))
                groups.append([start, end])
                start = end + 1
        time.sleep(0.5) 

def defVlan(host):
    with connect(host) as sub_child:
        sub_child.send_config_set("no vlan 2-4095" )

### Config maximum numberof vty session  ###	  
def confVty(host,vty):
    with connect(host) as sub_child:
        sub_child.send_config_set("no line vty %s 39" % vty)

### Restore maximum numberof vty session  ###	  
def deftVty(host):
    with connect(host) as child:
        child.send_config_set("line vty 0 39")
       
### Restore maximum numberof vty session  ###	  
def deftSystem(host):
    with connect(host) as child:
        child.send_command('write default',expect_string='[y/n]' )
        child.send_command('y')
        child.send_command('reload',expect_string='(y/n)')
        child.send_command("y")
        time.sleep(180) 
        child.expect(None)
        time.sleep(1)
