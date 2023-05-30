# funBaVef.py

# $language = "python"
# $interface = "1.0"

import pexpect
import sys
import time
import os
import basic.basicConf as bc

### Check port-channel ###
def checkPortChannel(host, state):
    with bc.connect(host) as sub_child:
        results = []
        pass_count = 0
        flexport = sub_child.send_command('show port-channel summary')
        results.extend(flexport.splitlines()[8].split())
    print(results)
    check_lists = {'static': ['po1', '(SU)', 'NONE', '1/24(P)', '1/23(P)*'],
                    'lacp': ['(SU)', 'LACP', '8', '1/24(P)', '1/23(P)'],
                    'hotstandby': ['(SU)', 'LACP', '1', '1/24(D)', '1/23(P)']}
    for i in check_lists[state]:
        pass_count += results.count(i)
    # print(pass_count)
    if state == 'hotstandby':
        return 'Ok' if pass_count == 6 else 'Nok'
    else:
        return 'Ok' if pass_count == 5 else 'Nok'    

def checkLacpInternal(host, state):                  
    with bc.connect(host) as sub_child:
        sub_child.send_command('sh lacp 1 internal ')
        flexport = sub_child.send_command('sh lacp 1 internal ')
        results = flexport.splitlines()[8:10]
        results = str(results).split()
        print(results) 
    check_lists = {'active': ['FA', 'bndl'],
                   'passive': ['FP', 'bndl'],
                   'hotstandby': ['FP', 'standby']}
    pass_count = sum(results.count(i) for i in check_lists[state])
    # print(pass_count)
    if state == 'hotstandby':
            return 'Ok' if pass_count == 3 else 'Nok'
    else:
        return 'Ok' if pass_count == 4 else 'Nok'

def checkBcmPort(host,state):                 
    with bc.connectbcm(host) as sub_child: 
        sub_child.send_command('debug no-auth')
        sub_child.send_command('bcm-shell',expect_string='BCM.0>')
        command = sub_child.send_command('ps',expect_string='BCM.0>')
        cmd_split = command.splitlines()
        read_list = [line for line in cmd_split if line.strip()]    
        readResult = str(read_list[25]).split()
        print(readResult)
    if state == 'hotstandby' and readResult[7] == 'Block': 
        return 'Ok' 
    elif state == 'normal' and readResult[7] == 'Forward': 
        return 'Ok' 
    else:
        return 'Nok'

 