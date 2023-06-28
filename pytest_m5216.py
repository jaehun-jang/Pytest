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


# TestCase
class Test_m6424(basic): 

# ##### -----------------------------------------------------
# ##### ------- Flexport Function Test ----------------------
# ##### ----------------------------------------------------- 

    dut1 = '192.168.0.211'
    dut2 = '192.168.0.202' 
    nni = '1/17'
    lagin = ['1/15','1/16']
    blockport = '1/6,1/15-1/16'




    @pytest.mark.skip() #Because the GNMI implementation is not complete, this test item is skipped.
    def test_015_service_feature(self):
        pass

    @pytest.mark.skip() #Because the system is hanging, this test item is skipped.
    def test_021_max_vlan_4k(self):
        pass

    @pytest.mark.skip() #Because the feature hase a bug, this test item is skipped.
    def test_043_basic_ntp_time_zone(self):
        pass

    @pytest.mark.skip() #Because the feature hase a bug, this test item is skipped.
    def test_044_max_ntp_server(self):
        pass


    @pytest.mark.skip()
    def test_201_basic_soam(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " EOAM Basic Test " + "#" * 5
        print(Title)
        try: 
            bc.disTitle(self.dut1,Title)
            eoc.confEoam(self.dut2)
            assert eoc.confBasicEoam(self.dut1,self.dut2) == 8
            time.sleep(1)
            eoc.removeEoam(self.dut2) 
            time.sleep(1)                
        except: 
            eoc.removeEoam(self.dut2)                
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


