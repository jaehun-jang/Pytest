# $language = "python"
# $interface = "1.0"

import pytest, sys, time, os, logging ,datetime
                
import basic.basicConf as bc
import basic.basicVef as bv
import mef.mefConf as mc
import mef.mefVef as mv
import flexport.flexConf as fc
import flexport.flexVef as fv
import flexport.flexConfExam as fce
import flexport.flexBreakoutConf as fbc
import lag.lagConf as lac
import lag.lagVef as lav
import lldp.lldpConf as llc
import lldp.lldpVef as llv
import eoam.eoamConf as eoc
import eoam.eoamVef as eov
from pytest_basic import TestClass as basic
#######################  PYTEST   ##########################

dut1 = '192.168.0.201'
dut2 = '192.168.0.202'

# TestCase
class Test_m6424(basic):   

# ##### -----------------------------------------------------
# ##### ------- Flexport Function Test ----------------------
# ##### -----------------------------------------------------
   

    def test_101_basic_flexport(self): 
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Flexport Basic configuration Test " + "#" * 5
        print(Title)
        try:  
            bc.disTitle(dut1,Title) 
            assert bv.checkPlog(testName,dut1) == 'OK'
            time.sleep(2) 
        except: 
            bc.deftSystem(dut1)
            bc.defaultSetup(dut1) 
            time.sleep(1)   
            assert bv.ExceptionLog(testName) == 'normal'
            time.sleep(2)                 

    def test_102_flexport_example(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Flexport Example configuration Test " + "#" * 5
        print(Title)
        try: 
            bc.disTitle(dut1,Title) 
            assert fce.confFlexPortExam(dut1) == 7 
            time.sleep(1)
        except:
            bc.deftSystem(dut1)
            bc.defaultSetup(dut1) 
            time.sleep(1) 
            assert bv.ExceptionLog(testName) == 'normal'
            time.sleep(2)                 

    def test_103_flexport_breakout(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " Flexport Breakout configuration Test " + "#" * 5
        print(Title)
        try: 
            bc.disTitle(dut1,Title) 
            assert fbc.flexPortBreakout(dut1) == 3
            time.sleep(1)
        except:
            bc.deftSystem(dut1)
            bc.defaultSetup(dut1) 
            time.sleep(1) 
            assert bv.ExceptionLog(testName) == 'normal'
            time.sleep(2)                


class MyPlugin:
    def pytest_sessionfinish(self):
        pass


if __name__ == "__main__":
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    # Create the file name with the timestamp
    file_name = f"report_{timestamp}.html"

    # Construct the arguments string
    args_str = f"--html=report/{file_name} {__file__}"

    args = args_str.split(" ")
    pytest.main(args, plugins=[MyPlugin()])


