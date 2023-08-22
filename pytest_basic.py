# $language = "python"
# $interface = "1.0"

import pytest, sys, time, os, logging ,datetime
import subprocess

import guictl.twamp as guitwamp    
import guictl.radius as guiradius                   
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
import radius.radiusConf as radius
import pm.pmConfig as pmc
import mngConfig.mngConfig as mngc
#######################  PYTEST   ##########################

# TestCase
class TestClass():  

    dut1 = '0.0.0.0'
    dut2 = '0.0.0.0'
    nni = ''
    lagint = ['']
    blockport = ''

    @classmethod
    def setup_class(cls,): # setUP_class(cls) -> unittest
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(sys._getframe(0).f_code.co_name) 
        """ AAA """  
        bc.defaultSetup(cls.dut1,cls.blockport)   
        bc.defaultSetup(cls.dut2,cls.blockport)

    @classmethod       
    def teardown_class(cls):   # tearDown(cls) -> unittest
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(sys._getframe(0).f_code.co_name) 
        """ BBB """ 
    
    def setup_method(self,function):
        logging.info(sys._getframe(0).f_code.co_name)

    def teardown_method(self,function):
        logging.info(sys._getframe(0).f_code.co_name)
  
   ### -----------------------------------------------------
   ### ------- Function Test -------------------------------
   ### -----------------------------------------------------
    
    # def test_001_maximum_number_of_vty(self):
    #     logging.info(sys._getframe(0).f_code.co_name) 
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " maximum number of VTY Session TEST " + "#" * 5
    #     print(Title)
    #     try: 
    #         bc.disTitle(self.dut1,Title)
    #         vty = 39
    #         assert bv.checkVtySsion(self.dut1,vty) == vty
    #         time.sleep(5)
    #     except:                
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(5) 

    # def test_002_vty_configure(self):
    #     logging.info(sys._getframe(0).f_code.co_name)  
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " maximum number of VTY Session Configuration TEST " + "#" * 5
    #     print(Title)
    #     try:     
    #         bc.disTitle(self.dut1,Title) 
    #         vty = 8
    #         bc.confVty(self.dut1,vty)
    #         assert bv.checkVtySsion(self.dut1,vty) == vty 
    #         time.sleep(1)
    #         bc.deftVty(self.dut1)
    #         time.sleep(5)
    #     except:
    #         bc.deftVty(self.dut1)              
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(5)

    # def test_003_user_account(self):
    #     logging.info(sys._getframe(0).f_code.co_name)  
    #     testName =  sys._getframe(0).f_code.co_name 
    #     Title = "#" * 5 + " User Account Configuration TEST " + "#" * 5
    #     print(Title)
    #     try:     
    #         bc.disTitle(self.dut1,Title) 
    #         assert gua.useraccount(self.dut1) == 6
    #         time.sleep(5) 
    #     except:             
    #         assert bv.ExceptionLog(testName) == 'normal'
    #         time.sleep(5)

    def test_04_AAA_RADIUS(self):
        testName =  sys._getframe(0).f_code.co_name 
        Title = "#" * 5 + " AAA with RADIUS Test " + "#" * 5
        print(Title)
        try:         
            bc.disTitle(self.dut1,Title)
            radius.configAaaRadius(self.dut1) 
            guiradius.startRadiusServer() 
            time.sleep(15)      
            assert radius.checklogin(self.dut1) == 6                        
            time.sleep(2)
            guiradius.stopRadiusServer()
            time.sleep(15)               
            assert radius.checklogin(self.dut1) == 0 
            time.sleep(2) 
            radius.removeAaaRadius(self.dut1)  
            time.sleep(2)                             
        except: 
            guiradius.stopRadiusServer()
            time.sleep(10)                
            radius.removeAaaRadius(self.dut1) 
            assert bv.ExceptionLog(testName) == 'normal'
            time.sleep(5)

#     def test_011_static_route(self):
#           logging.info(sys._getframe(0).f_code.co_name)  
#           testName =  sys._getframe(0).f_code.co_name 
#           Title = "#" * 5 + " static route Configuration TEST " + "#" * 5
#           print(Title)
#           try:     
#               bc.disTitle(self.dut1,Title)
#               bc.addiproute(self.dut1)  
#               assert bc.ping(self.dut1) == True
#               time.sleep(1)
#               bc.deliproute(self.dut1)
#               time.sleep(5) 
#           except:             
#               assert bv.ExceptionLog(testName) == 'normal'
#               time.sleep(5)

#     def test_012_trace_route(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " TraceRT Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)
#             bc.addiproute(self.dut1) 
#             time.sleep(1)              
#             assert gmis.traceRT(self.dut1) == "192.168.0.2"
#             time.sleep(1)                
#             bc.deliproute(self.dut1) 
#             time.sleep(5)            
#         except:              
#             bc.deliproute(self.dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_013_tcp_dump(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " TCP_DUMP Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert gmis.tcpdump(self.dut1) >= 10
#             time.sleep(5)                        
#         except:              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_014_mirror_configure(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " Mirror Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert gmis.mirror(self.dut1,self.nni) == True
#             time.sleep(5)                        
#         except:              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_015_service_feature(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " service_feature " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert gmis.feature(self.dut1) == True
#             time.sleep(1)
#             gmis.default_feature(self.dut1) 
#             time.sleep(5)                      
#         except:
#             gmis.default_feature(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_021_max_vlan_4k(self):
#         logging.info(sys._getframe(0).f_code.co_name) 
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " maximum number of VLAN TEST    " + "#" * 5
#         print(Title)
#         try:        
#             vlan = 4095
#             bc.disTitle(self.dut1,Title) 
#             bc.crtVlan(self.dut1,vlan)
#             time.sleep(2)
#             createvlan = bv.checkVlanNum(self.dut1)
#             assert createvlan == str(vlan)       
#             time.sleep(1)        
#             bc.dltDevVlan(self.dut1,vlan)
#             deletevlan = bv.checkVlanNum(self.dut1)
#             assert deletevlan == '1'       
#             time.sleep(5)   
#         except: # This code is added to execute removeLag() function when the test fail.
#             bc.defVlan(self.dut1)
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)                 

#     def test_022_max_service_256(self): 
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " maximum number of of SVCs TEST    " + "#" * 5
#         print(Title)
#         try:  
#             bc.disTitle(self.dut1,Title) 
# #                svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())
# #                while svc == 0 or uni == 0 or svc < uni or svc > 256 or uni > 24:  
# #                    print ('Try agan, the number of UNIs must be larger than EVCs: ')
# #                    svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())    
#             svc = 256
#             uni = 24 
#             mc.crtServi(self.dut1,svc,uni,self.nni)
#             assert mv.checkNmbrSvc(self.dut1) == svc 
#             time.sleep(1)
#             assert mv.checkNmbrUni(self.dut1) == uni 
#             time.sleep(1)
#             assert mv.checkNmbrSep(uni,self.dut1) == svc
#             time.sleep(1) 
#             mc.dltServi(self.dut1,svc,uni)
#             assert mv.checkDflSvc(self.dut1) == 0
#             time.sleep(5)        
#         except:
#             mc.dltServi(self.dut1,svc,uni)                             
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)              

#     def test_031_static_lag(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " Link Aggregation Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(self.dut1,Title)
#             mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1
#             mc.crtServi(self.dut2,1,1,self.nni) 
#             lac.confLag (self.dut2,self.lagint)
#             time.sleep(2)         
#             assert lac.confStaticLag(self.dut1,self.lagint) == 2
#             lac.removeLag(self.dut1,self.lagint) 
#             lac.removeLag(self.dut2,self.lagint) 
#             mc.dltServi(self.dut1,1,1,) # svc = 1, uni = 1
#             mc.dltServi(self.dut2,1,1,) 
#             time.sleep(5)
#         except:
#             lac.removeLag(self.dut1,self.lagint) 
#             lac.removeLag(self.dut2,self.lagint) 
#             mc.dltServi(self.dut1,1,1,) # svc = 1, uni = 1
#             mc.dltServi(self.dut2,1,1,)
#             time.sleep(1)            
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_032_basic_lacp(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " LACP Basic Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(self.dut1,Title)
#             mc.crtServi(self.dut2,1,1,self.nni) # svc = 1, uni = 1        
#             lac.confLacp(self.dut2,self.lagint)
#             mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1             
#             assert lac.confBasicLacp(self.dut1,self.lagint) == 10
#             mc.dltServi(self.dut1,1,1)
#             lac.removeLacp(self.dut2,self.lagint)
#             mc.dltServi(self.dut2,1,1)
#             time.sleep(5) 
#         except: 
#             lac.removeLacp(self.dut2,self.lagint)
#             mc.dltServi(self.dut2,1,1)         
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_033_basic_eoam(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " EOAM Basic Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(self.dut1,Title)
#             mc.crtServi(self.dut2,1,1,self.nni) # svc = 1, uni = 1              
#             eoc.confEoam(self.dut2,self.nni)
#             mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1 
#             time.sleep(3)    
#             assert eoc.confBasicEoam(self.dut1,self.dut2,self.nni) == 8
#             mc.dltServi(self.dut1,1,1)# svc = 1, uni = 1              
#             eoc.removeEoam(self.dut2,self.nni)
#             mc.dltServi(self.dut2,1,1)# svc = 1, uni = 1 
#             time.sleep(5)                 
#         except: 
#             eoc.removeEoam(self.dut1,self.nni)
#             mc.dltServi(self.dut1,1,1)# svc = 1, uni = 1   
#             eoc.removeEoam(self.dut2,self.nni)
#             mc.dltServi(self.dut2,1,1)# svc = 1, uni = 1                   
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_041_basic_lldp(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " LLDP Basic Test " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(self.dut1,Title)
#             mc.crtServi(self.dut1,2,1,self.nni) # svc = 2, uni = 1  
#             mc.crtServi(self.dut2,2,1,self.nni) # svc = 2, uni = 1 
#             time.sleep(1)             
#             assert llc.confBasicLldp(self.dut1,self.dut2,self.nni) == 7
#             mc.dltServi(self.dut1,2,1)# svc = 2, uni = 1  
#             mc.dltServi(self.dut2,2,1)# svc = 2, uni = 1  
#             time.sleep(5)
#         except: 
#             mc.dltServi(self.dut1,2,1)# svc = 2, uni = 1  
#             mc.dltServi(self.dut2,2,1)# svc = 2, uni = 1                 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     @pytest.mark.skip() #Because the feature hase a bug, this test item is skipped.
#     def test_042_basic_twamp(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " TWAMP Basic Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)
#             mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1  
#             twc.conftwamp(self.dut1)
#             guitwamp.twampclient()        
#             assert twv.checkTwampResult(self.dut1) == 20                        
#             time.sleep(1)
#             twc.removetwamp(self.dut1)
#             time.sleep(5)                
#         except:              
#             twc.removetwamp(self.dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_043_basic_ntp_time_zone(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " NTP Basic & TIME ZONE Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)
#             bc.addiproute(self.dut1)
#             time.sleep(1)             
#             gntpc.ntpConf(self.dut1)
#             time.sleep(10)                
#             assert gntpc.checkntpconf(self.dut1) == True 
#             #timestamp = datetime.datetime.now().strftime("%H:%M  KST %a %b %d %Y") 
#             timestamp = datetime.datetime.now().strftime("%H  KST %a %b %d %Y") 
#             assert gntpc.checktime(self.dut1) == timestamp                
#             time.sleep(1)
#             bc.deliproute(self.dut1)
#             gntpc.delntpconfe(self.dut1)
#             time.sleep(5)                  
#         except:              
#             bc.deliproute(self.dut1) 
#             gntpc.delntpconfe(self.dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_044_max_ntp_server(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " Maximum NTP Server Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)
#             bc.addiproute(self.dut1) 
#             time.sleep(1) 
#             gntpc.maxntpserver(self.dut1)
#             time.sleep(1)                
#             assert gntpc.checkmaxntpserver(self.dut1) == 4 
#             time.sleep(1)                
#             assert gntpc.overmaxntpserver(self.dut1) == True           
#             time.sleep(1)
#             bc.deliproute(self.dut1)
#             gntpc.delmaxntpserver(self.dut1) 
#             time.sleep(5)                 
#         except:              
#             bc.deliproute(self.dut1) 
#             gntpc.delmaxntpserver(self.dut1) 
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_051_basic_pm_configure(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " basic PM Config Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert pmc.pmConf(self.dut1) == True
#             time.sleep(1)
#             pmc.default_pm(self.dut1) 
#             time.sleep(5)                       
#         except:
#             pmc.default_pm(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_052_basic_pm_csv(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " basic PM CSV Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert pmc.csvConf(self.dut1) == True
#             time.sleep(1)
#             pmc.default_csv(self.dut1)
#             time.sleep(5)                        
#         except:
#             pmc.default_csv(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_053_mng_gw_config(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " basic MNG Gateway Configuration Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert mngc.mngGwConf(self.dut1) == True
#             time.sleep(1)
#             mngc.default_mng_gw_config(self.dut1) 
#             time.sleep(5)                
#         except:
#             mngc.default_mng_gw_config(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_054_mng_process_config(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " basic MNG Process Configuration Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert mngc.mngProcessConf(self.dut1) == True
#             time.sleep(1)
#             mngc.default_mng_process_config(self.dut1) 
#             time.sleep(5)              
#         except:
#             mngc.default_mng_process_config(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_055_mng_mem_config_(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " basic MNG Memory Configuration Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert mngc.mngMemoryConf(self.dut1) == True
#             time.sleep(1)
#             mngc.default_mng_mem_config(self.dut1) 
#             time.sleep(5)              
#         except:
#             mngc.default_mng_mem_config(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     @pytest.mark.skip() #Because the feature hase a bug, this test item is skipped.
#     def test_056_mng_evm_config_(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " basic MNG EVM Configuration Test " + "#" * 5
#         print(Title)
#         try:         
#             bc.disTitle(self.dut1,Title)            
#             assert mngc.mngEvmConf(self.dut1) == True
#             time.sleep(1)
#             mngc.default_mng_gw_config(self.dut1)
#             mngc.default_mng_evm_config(self.dut1) 
#             time.sleep(5)              
#         except:
#             mngc.default_mng_gw_config(self.dut1)
#             mngc.default_mng_evm_config(self.dut1)              
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

#     def test_099_check_plog(self):
#         testName =  sys._getframe(0).f_code.co_name 
#         Title = "#" * 5 + " check plog " + "#" * 5
#         print(Title)
#         try: 
#             bc.disTitle(self.dut1,Title)
#             assert bv.checkPlog(Title,self.dut1) == 'OK'
#             time.sleep(5)                
#         except:            
#             assert bv.ExceptionLog(testName) == 'normal'
#             time.sleep(5)

class MyPlugin:
    def pytest_sessionfinish(self):
        pass


if __name__ == "__main__":
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    # Create the file name with the timestamp
    file_name = f"report_{timestamp}.html"

    # Construct the arguments string
    args_str = '--html=report/report.html --self-contained-html '+ __file__
    args_str = ' --capture=tee-sys '+ __file__
    args_str = f"--html=report/{file_name} {__file__}"

    args = args_str.split(" ")
    pytest.main(args, plugins=[MyPlugin()])


