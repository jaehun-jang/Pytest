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
class Test_m5216(basic):   

    def test_201_basic_soam(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " EOAM Basic Test " + "#" * 5
        print(Title)
        try: 
            bc.disTitle(dut1,Title)
            eoc.confEoam(dut2)
            assert eoc.confBasicEoam(dut1,dut2) == 8
            time.sleep(1)
            eoc.removeEoam(dut2) 
            time.sleep(1)                
        except: 
            eoc.removeEoam(dut2)                
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


