# $language = "python"
# $interface = "1.0"

import pytest, sys, time, os, logging ,datetime
import subprocess

import guictl.twamp as guitwp               
import basic.basicConf as bc
import basic.basicVef as bv
import GeneralMgmt.userAccount as gua
import GeneralMgmt.ntpConf as gntpc
import GeneralMgmt.miscellaneous as gmis
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
import twamp.twampConf as twc
import twamp.twampVef as twv
#######################  PYTEST   ##########################

dut1 = '192.168.0.201'
dut2 = '192.168.0.202'

# TestCase
class TestClass():   
    @classmethod
    def setup_class(cls): # setUP_class(cls) -> unittest
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(sys._getframe(0).f_code.co_name) 
        """ AAA """  
        bc.defaultSetup(dut1)   
        bc.defaultSetup(dut2)

    @classmethod       
    def teardown_class(cls):   # tearDown(cls) -> unittest
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(sys._getframe(0).f_code.co_name) 
        """ BBB """ 
    
    def setup_method(self,function):
        logging.info(sys._getframe(0).f_code.co_name)
        test_method_name = function.__name__ 
        assert bv.checkPlog(test_method_name,dut1) == 'OK'
        time.sleep(2)  
    
    def teardown_method(self,function):
        logging.info(sys._getframe(0).f_code.co_name)
  

# #### -----------------------------------------------------
# #### ------- Function Test -------------------------------
# #### -----------------------------------------------------
   
#     def test_001_max_vty(self):
#         logging.info(sys._getframe(0).f_code.co_name) 
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " maximum number of VTY Session TEST " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(dut1,Title)
#             vty = 39
#             assert bv.checkVtySsion(dut1,vty) == vty
#             time.sleep(1)
#         except:                
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2) 

#     def test_002_conf_vty(self):
#         logging.info(sys._getframe(0).f_code.co_name)  
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " maximum number of VTY Session Configuration TEST " + "#" * 5
#         print(Title)
#         try:     
#             bc.disTitle(dut1,Title) 
#             vty = 8
#             bc.confVty(dut1,vty)
#             assert bv.checkVtySsion(dut1,vty) == vty 
#             time.sleep(1)
#             bc.deftVty(dut1)
#             time.sleep(1)
#         except:
#             bc.deftVty(dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

#     def test_003_user_account(self):
#         logging.info(sys._getframe(0).f_code.co_name)  
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " User Account Configuration TEST " + "#" * 5
#         print(Title)
#         try:     
#             bc.disTitle(dut1,Title) 
#             assert gua.useraccount(dut1) == 6
#             time.sleep(1)
#         except:             
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

#     def test_011_static_route(self):
#           logging.info(sys._getframe(0).f_code.co_name)  
#           testName =  sys._getframe(0).f_code.co_name 
#           Title = "#" * 5 + " static route Configuration TEST " + "#" * 5
#           print(Title)
#           try:     
#               bc.disTitle(dut1,Title)
#               bc.addiproute(dut1)  
#               assert bc.ping(dut1) == "icmp_seq=10"
#               time.sleep(1)
#           except:             
#               assert bv.ExceptionLog(testName) == 'normal'
#               time.sleep(2)

#     def test_012_basic_ntp_time_zone(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " NTP Basic & TIME ZONE Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(dut1,Title)
#             bc.addiproute(dut1) 
#             gntpc.ntpConf(dut1)
#             time.sleep(10)                
#             #assert gntpc.checkntpconf(dut1) == True 
#             #timestamp = datetime.datetime.now().strftime("%H:%M  KST %a %b %d %Y") 
#             timestamp = datetime.datetime.now().strftime("%H  KST %a %b %d %Y") 
#             assert gntpc.checktime(dut1) == timestamp                
#             time.sleep(1)
#             bc.deliproute(dut1)
#             gntpc.delntpconfe(dut1)                  
#         except:              
#             bc.deliproute(dut1) 
#             gntpc.delntpconfe(dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

#     def test_013_max_ntp_server(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " Maximum NTP Server Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(dut1,Title)
#             bc.addiproute(dut1) 
#             time.sleep(1) 
#             gntpc.maxntpserver(dut1)
#             time.sleep(1)                
#             assert gntpc.checkmaxntpserver(dut1) == 4 
#             time.sleep(1)                
#             assert gntpc.overmaxntpserver(dut1) == True           
#             time.sleep(1)
#             bc.deliproute(dut1)
#             gntpc.delmaxntpserver(dut1)                  
#         except:              
#             bc.deliproute(dut1) 
#             gntpc.delmaxntpserver(dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

#     def test_014_trace_route(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " TraceRT Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(dut1,Title)
#             bc.addiproute(dut1) 
#             time.sleep(1)              
#             assert gmis.traceRT(dut1) == "192.168.0.2"
#             time.sleep(1)                
#             bc.deliproute(dut1)             
#         except:              
#             bc.deliproute(dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

    # def test_015_tcp_dump(self):
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " TCP_DUMP Test " + "#" * 5
    #     print(Title)
    #     try:         
    #         bc.disTitle(dut1,Title)            
    #         assert gmis.tcpdump(dut1) >= 10
    #         time.sleep(1)                        
    #     except:              
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(2)

    # def test_016_mirror(self):
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " Mirror Test " + "#" * 5
    #     print(Title)
    #     try:         
    #         bc.disTitle(dut1,Title)            
    #         assert gmis.mirror(dut1) == True
    #         time.sleep(1)                        
    #     except:              
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(2)

    def test_017_service_feature(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " service_feature " + "#" * 5
        print(Title)
        try:         
            bc.disTitle(dut1,Title)            
            assert gmis.feature(dut1) == True
            time.sleep(1)
            gmis.default_feature(dut1)                        
        except:
            gmis.default_feature(dut1)              
            assert bv.ExceptionLog(testName) == 'normal'
            time.sleep(2)

#     def test_021_max_vlan(self):
#         logging.info(sys._getframe(0).f_code.co_name) 
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " maximum number of VLAN TEST    " + "#" * 5
#         print(Title)
#         try:        
#             vlan = 4095
#             bc.disTitle(dut1,Title) 
#             bc.crtVlan(dut1,vlan)
#             time.sleep(2)
#             createvlan = bv.checkVlanNum(dut1)
#             assert createvlan == str(vlan)       
#             time.sleep(1)        
#             bc.dltDevVlan(dut1,vlan)
#             deletevlan = bv.checkVlanNum(dut1)
#             assert deletevlan == '1'       
#             time.sleep(1)   
#         except: # This code is added to execute removeLag() function when the test fail.
#             bc.defVlan(dut1)
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)                 

#     def test_022_max_svc(self): 
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " maximum number of of SVCs TEST    " + "#" * 5
#         print(Title)
#         try:  
#             bc.disTitle(dut1,Title) 
# #                svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())
# #                while svc == 0 or uni == 0 or svc < uni or svc > 256 or uni > 24:  
# #                    print ('Try agan, the number of UNIs must be larger than EVCs: ')
# #                    svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())    
#             svc = 256
#             uni = 24 
#             mc.crtServi(dut1,svc,uni)
#             assert mv.checkNmbrSvc(dut1) == svc 
#             time.sleep(1)
#             assert mv.checkNmbrUni(dut1) == uni 
#             time.sleep(1)
#             assert mv.checkNmbrSep(uni,dut1) == svc
#             time.sleep(1) 
#             mc.dltServi(dut1,svc,uni)
#             assert mv.checkDflSvc(dut1) == 0
#             time.sleep(1)        
#         except:
#             mc.dltServi(dut1,svc,uni)                             
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)              

#     def test_031_static_lag(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " Link Aggregation Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(dut1,Title)
#             lac.confLag (dut2) 
#             assert lac.confStaticLag(dut1) == 2
#             time.sleep(1)
#             lac.removeLag(dut2)
#             time.sleep(1)
#         except:
#             lac.removeLag(dut2)
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)                

#     def test_032_basic_lacp(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " LACP Basic Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(dut1,Title)
#             lac.confLacp(dut2)
#             assert lac.confBasicLacp(dut1) == 10
#             time.sleep(1)
#             lac.removeLacp(dut2) 
#             time.sleep(1)
#         except: 
#             lac.removeLacp(dut2)             
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

#     def test_041_basic_lldp(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " LLDP Basic Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(dut1,Title)
#             llc.confEthService(dut2)
#             assert llc.confBasicLldp(dut1,dut2) == 7
#             time.sleep(1)
#             llc.removeEthService(dut2) 
#             time.sleep(1)
#         except: 
#             llc.removeEthService(dut2)                
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

#     def test_051_basic_eoam(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " EOAM Basic Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(dut1,Title)
#             eoc.confEoam(dut2)
#             assert eoc.confBasicEoam(dut1,dut2) == 8
#             time.sleep(1)
#             eoc.removeEoam(dut2) 
#             time.sleep(1)                
#         except: 
#             eoc.removeEoam(dut2)                
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(2)

    # def test_061_basic_twamp(self):
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " TWAMP Basic Test " + "#" * 5
    #     print(Title)
    #     try:         
    #         bc.disTitle(dut1,Title)
    #         twc.conftwamp(dut1)
    #         guitwp.twampclient()        
    #         assert twv.checkTwampResult(dut1) == 20                        
    #         time.sleep(1)
    #         twc.removetwamp(dut1)                
    #     except:              
    #         twc.removetwamp(dut1) 
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(2)

    # def test_099_plog(self):
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " check plog " + "#" * 5
    #     print(Title)
    #     try: 
    #         bc.disTitle(dut1,Title)
    #         assert bv.checkPlog(Title,dut1) == 'OK'
    #         time.sleep(2)                
    #     except:            
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(2)

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


