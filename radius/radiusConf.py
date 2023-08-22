
import pytest, sys, time, os, logging ,datetime
from netmiko import ConnectHandler
import basic.basicConf as bc


def configAaaRadius(host):
    with bc.connect(host) as child:
        child.enable()
        config_commands = [
            "radius-server host 192.168.0.157 key radius auth-port 1812",
            "aaa auth login default group radius",
            "aaa auth login default fallback error local" 
        ]
        output = child.send_config_set(config_commands)
        print(output)

def removeAaaRadius(host):
    with bc.connect(host) as child:
        child.enable()
        config_commands = [
            "no aaa auth login default group radius",
            "no aaa auth login default fallback error local", 
            "no radius-server host 192.168.0.157"
        ]
        output = child.send_config_set(config_commands)
        print(output)

def privilige(net_connect,role):
        print('# Check user privilige #')
        if role == 'network-admin':
            net_connect.enable()
            config_commands = [
                " username radius password radius123" 
            ]
            output = net_connect.send_config_set(config_commands)
            print(output)
            if "%" in output:
                return False
            else:
                return True

        elif role == 'network-operator':
            net_connect.enable()
            config_commands = [
                "username" 
            ]
            output = net_connect.send_config_set(config_commands)
            print(output)
            if "%" in output:
                return True 
            else:
                return True

        elif role == 'network-viewer':
            output = net_connect.send_command("config terminal")
            print(output)
            if "%" in output:
                return True
            else:
                return True

def login_with_credentials(device, username, password,role):
    try:
        temp_device = device.copy()
        temp_device['username'] = username
        temp_device['password'] = password        
        net_connect = ConnectHandler(**temp_device)  
        command1 = net_connect.send_command('show users')
        print(command1) 
        checkPriv = privilige(net_connect,role)
        print(f"Successful login - Username: {username}, Password: {password}")      
        net_connect.disconnect()
        if checkPriv == True:
            return True 
    except Exception as e:
        print(f"Failed login - Username: {username}, Password: {password}")
        print(e)
        return False

def checklogin(host):
    ssh_device = {
        'device_type': 'cisco_ios',
        'ip': host,
        'username': 'root',
        'password': 'admin',
        'port': 22
    }
    telnet_device = {
        'device_type': 'cisco_ios_telnet',
        'ip': host,
        'username': 'root',
        'password': 'admin',
        'port': 23
    }
    new_users = [
        ('admin', 'hfrn','network-admin'),
        ('operator', 'hfrn','network-operator'),
        ('viewer', 'hfrn','network-viewer')
    ]
    okcount = [] 

    '// For SSH Connection //'
    for new_username, new_password, role in new_users:  
        print('# For RADIUS authentication with SSH #')
        result = login_with_credentials(ssh_device, new_username, new_password, role)
        print(result)
        if result == True:
            okcount.append('Ok')
        else:
            okcount.append('Nok')
        time.sleep(1.5) 

    '// For Telnet Connection //'
    for new_username, new_password, role in new_users:  
        print('# For RADIUS authentication with Telnet #')
        result = login_with_credentials(telnet_device, new_username, new_password, role)
        print(result)
        if result == True:
            okcount.append('Ok')
        else:
            okcount.append('Nok')
        time.sleep(1.5) 

    print(okcount)
    return okcount.count('Ok')

