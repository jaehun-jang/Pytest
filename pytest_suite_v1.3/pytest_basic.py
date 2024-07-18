# $language = "python"
# $interface = "1.0"

import pytest, sys, time, os, logging ,datetime
import pandas as pd 
from logging import root
from netmiko import ConnectHandler

# ###  TEST MODULE ###                
import basic.basicConf as bc
import basic.basicVef as bv
import GeneralMgmt.userAccount as gua
import GeneralMgmt.ntpConf as gntpc
import GeneralMgmt.timeZoneConf as gtzc
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
import spanningTree.stpConfig as stpc

# ###  GUI MODULE ###    
import guictl.twamp as guitwamp    
import guictl.radius as guiradius  

#######################  PYTEST   ##########################

# TestCase
class TestClass():  
   
    dut1 = '192.168.0.201'
    dut2 = '192.168.0.202'
    dut3 = '192.168.0.203'
    dut1and2 = ['192.168.0.201','192.168.0.202']
    devAll = ['192.168.0.201','192.168.0.202','192.168.0.203']
    nni = '1/25'
    lagint = ['1/15','1/16']
    blockport = '1/6,1/10-1/16'
    stpblockport = '1/25'

    # # Fixture 정의
    # @pytest.fixture
    # def setup_teardown(self):
    #     testName = sys._getframe(0).f_code.co_name
    #     Title = "#" * 5 + " " + testName + " " + "#" * 5
    #     yield testName, Title
    #     time.sleep(1)
    #     assert bv.checkPlog(self.devAll,self.Title) == 'OK'

    ###    -----------------------------------------------------
    # setup_class: 클래스 레벨에서 한 번 실행         
    @classmethod
    def setup_class(cls,): # setUP_class(cls) -> unittest
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(sys._getframe(0).f_code.co_name) 
        """ AAA """  
        # bc.defaultSetup(cls.devAll,cls.blockport)   
    
    # setup_class: 클래스 레벨에서 한 번 실행
    @classmethod       
    def teardown_class(cls):   # tearDown(cls) -> unittest
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(sys._getframe(0).f_code.co_name) 
        """ BBB """ 

    # setup_method: 각 테스트 메서드 실행 전마다 실행
    def setup_method(self, method):
        logging.info(sys._getframe(0).f_code.co_name)
        self.testName = method.__name__
        self.Title = "#" * 5 + " " + self.testName + " " +"TEST START " + "#" * 5

    # teardown_method: 각 테스트 메서드 실행 후마다 실행
    def teardown_method(self, method):
        logging.info(sys._getframe(0).f_code.co_name)
        self.testName = method.__name__
        self.Title = "#" * 5 + " " + self.testName + " " +"TEST END " + "#" * 5
        bc.disTitle(self.devAll,self.Title) 
        bv.checkPlog(self.devAll,self.Title)

    ###    -----------------------------------------------------
    ###    ------- Function Test -------------------------------
    ###    -----------------------------------------------------
    
    # def test_001_maximum_number_of_vty(self,setup_teardown):
    #     testName, Title = setup_teardown

    #     try: 
    #         bc.disTitle(self.devAll,self.Title)
    #         vty = 39
    #         assert bv.checkVtySsion(self.dut1,vty) == vty
    #         time.sleep(5)
    #     except:                
    #         assert bv.ExceptionLog(self.testName) == 'normal'
    #         time.sleep(5) 

    def test_001_maximum_number_of_vty(self):
        try: 
            bc.disTitle(self.devAll,self.Title)
            vty = 39
            assert bv.checkVtySsion(self.dut1,vty) == vty
            time.sleep(5)
        except:                
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5) 

    def test_002_vty_configure(self):
        try:     
            bc.disTitle(self.devAll,self.Title) 
            vty = 8
            bc.confVty(self.dut1,vty)
            assert bv.checkVtySsion(self.dut1,vty) == vty 
            time.sleep(1)
            bc.deftVty(self.dut1)
            time.sleep(5)
        except:
            bc.deftVty(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_003_user_account(self):
        try:     
            bc.disTitle(self.devAll,self.Title) 
            assert gua.useraccount(self.dut1) == 6
            time.sleep(5) 
        except:             
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    @pytest.mark.skip() 
    def test_04_AAA_RADIUS(self):
        try:         
            bc.disTitle(self.devAll,self.Title)
            radius.configAaaRadius(self.dut1) 
            guiradius.startRadiusServer() 
            time.sleep(5)      
            assert radius.checklogin(self.dut1) == 6                        
            time.sleep(2)
            guiradius.stopRadiusServer()
            time.sleep(5)               
            assert radius.checklogin(self.dut1) == 2 
            time.sleep(2) 
            radius.removeAaaRadius(self.dut1)  
            time.sleep(2)                             
        except: 
            guiradius.stopRadiusServer()
            time.sleep(2)                
            radius.removeAaaRadius(self.dut1) 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_011_static_route(self):
        try:     
            bc.disTitle(self.devAll,self.Title)
            bc.addiproute(self.dut1)  
            assert bc.ping(self.dut1) == True
            time.sleep(1)
            bc.deliproute(self.dut1)
            time.sleep(5) 
        except:             
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_012_trace_route(self):
        try:         
            bc.disTitle(self.devAll,self.Title)
            bc.addiproute(self.dut1) 
            time.sleep(1)              
            assert gmis.traceRT(self.dut1) == "192.168.0.2"
            time.sleep(1)                
            bc.deliproute(self.dut1) 
            time.sleep(5)            
        except:              
            bc.deliproute(self.dut1) 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_013_tcp_dump(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert gmis.tcpdump(self.dut1) == True
            time.sleep(5)                        
        except:              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_014_mirror_configure(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert gmis.mirror(self.dut1,self.nni) == True
            time.sleep(5)                        
        except:              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_015_service_feature(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert gmis.feature(self.dut1) == True
            time.sleep(1)
            gmis.default_feature(self.dut1) 
            time.sleep(5)                      
        except:
            gmis.default_feature(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_021_max_vlan_4k(self):
        try:        
            vlan = 4095
            bc.disTitle(self.devAll,self.Title) 
            bc.crtVlan(self.dut1,vlan)
            time.sleep(2)
            createvlan = bv.checkVlanNum(self.dut1)
            assert createvlan == str(vlan)       
            time.sleep(1)        
            bc.dltDevVlan(self.dut1,vlan)
            deletevlan = bv.checkVlanNum(self.dut1)
            assert deletevlan == '1'       
            time.sleep(5)   
        except: # This code is added to execute removeLag() function when the test fail.
            bc.defVlan(self.dut1)
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)                 

    def test_022_max_service_256(self): 
        try:  
            bc.disTitle(self.devAll,self.Title) 
#                svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())
#                while svc == 0 or uni == 0 or svc < uni or svc > 256 or uni > 24:  
#                    print ('Try agan, the number of UNIs must be larger than EVCs: ')
#                    svc, uni = map(int, input('Enter the maximum numbers of SVCs and UNIs: ').split())    
            svc = 256
            uni = 24 
            mc.crtServi(self.dut1,svc,uni,self.nni)
            assert mv.checkNmbrSvc(self.dut1) == svc 
            time.sleep(1)
            assert mv.checkNmbrUni(self.dut1) == uni 
            time.sleep(1)
            assert mv.checkNmbrSep(uni,self.dut1) == svc
            time.sleep(1) 
            mc.dltServi(self.dut1,svc,uni)
            assert mv.checkDflSvc(self.dut1) == 0
            time.sleep(5)        
        except:
            mc.dltServi(self.dut1,svc,uni)                             
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)              

    def test_031_static_lag(self):
        try: 
            bc.disTitle(self.devAll,self.Title)
            mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1
            mc.crtServi(self.dut2,1,1,self.nni) 
            lac.confLag (self.dut2,self.lagint)
            time.sleep(2)         
            assert lac.confStaticLag(self.dut1,self.lagint) == 2
            lac.removeLag(self.dut1,self.lagint) 
            lac.removeLag(self.dut2,self.lagint) 
            mc.dltServi(self.dut1,1,1,) # svc = 1, uni = 1
            mc.dltServi(self.dut2,1,1,) 
            time.sleep(5)
        except:
            lac.removeLag(self.dut1,self.lagint) 
            lac.removeLag(self.dut2,self.lagint) 
            mc.dltServi(self.dut1,1,1,) # svc = 1, uni = 1
            mc.dltServi(self.dut2,1,1,)
            time.sleep(1)            
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_032_basic_lacp(self):
        try: 
            bc.disTitle(self.devAll,self.Title)
            mc.crtServi(self.dut2,1,1,self.nni) # svc = 1, uni = 1        
            lac.confLacp(self.dut2,self.lagint)
            mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1             
            assert lac.confBasicLacp(self.dut1,self.lagint) == 10
            mc.dltServi(self.dut1,1,1)
            lac.removeLacp(self.dut2,self.lagint)
            mc.dltServi(self.dut2,1,1)
            time.sleep(5) 
        except: 
            lac.removeLacp(self.dut2,self.lagint)
            mc.dltServi(self.dut2,1,1)         
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_033_basic_eoam(self):
        try: 
            bc.disTitle(self.devAll,self.Title)
            mc.crtServi(self.dut2,1,1,self.nni) # svc = 1, uni = 1              
            eoc.confEoam(self.dut2,self.nni)
            mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1 
            time.sleep(3)    
            assert eoc.confBasicEoam(self.dut1,self.dut2,self.nni) == 8
            mc.dltServi(self.dut1,1,1)# svc = 1, uni = 1              
            eoc.removeEoam(self.dut2,self.nni)
            mc.dltServi(self.dut2,1,1)# svc = 1, uni = 1 
            time.sleep(5)                 
        except: 
            eoc.removeEoam(self.dut1,self.nni)
            mc.dltServi(self.dut1,1,1)# svc = 1, uni = 1   
            eoc.removeEoam(self.dut2,self.nni)
            mc.dltServi(self.dut2,1,1)# svc = 1, uni = 1                   
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_041_basic_lldp(self):
        try: 
            bc.disTitle(self.devAll,self.Title)
            mc.crtServi(self.dut1,2,1,self.nni) # svc = 2, uni = 1  
            mc.crtServi(self.dut2,2,1,self.nni) # svc = 2, uni = 1 
            time.sleep(1)             
            assert llc.confBasicLldp(self.dut1,self.dut2,self.nni) == 7
            mc.dltServi(self.dut1,2,1)# svc = 2, uni = 1  
            mc.dltServi(self.dut2,2,1)# svc = 2, uni = 1  
            time.sleep(5)
        except: 
            mc.dltServi(self.dut1,2,1)# svc = 2, uni = 1  
            mc.dltServi(self.dut2,2,1)# svc = 2, uni = 1                 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    @pytest.mark.skip() #Because the feature hase a bug, this test item is skipped.
    def test_042_basic_twamp_light(self):
        try:         
            bc.disTitle(self.devAll,self.Title)
            mc.crtServi(self.dut1,1,1,self.nni) # svc = 1, uni = 1  
            twc.conftwamp(self.dut1)
            guitwamp.twampclient()        
            assert twv.checkTwampResult(self.dut1) == 20                        
            time.sleep(1)
            twc.removetwamp(self.dut1)
            time.sleep(5)                
        except:              
            twc.removetwamp(self.dut1) 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_043_basic_ntp_and_time_zone(self):
        try:         
            bc.disTitle(self.devAll,self.Title)
            bc.addiproute(self.dut1)
            time.sleep(2)             
            gntpc.ntpConf(self.dut1)
            time.sleep(15)                
            assert gntpc.checkntpconf(self.dut1) == True 
            #timestamp = datetime.datetime.now().strftime("%H:%M  KST %a %b %d %Y") 
            timestamp = datetime.datetime.now().strftime("%H  KST %a %b %d %Y") 
            assert gntpc.checktime(self.dut1) == timestamp                
            time.sleep(2)
            bc.deliproute(self.dut1)
            gntpc.delntpconfe(self.dut1)
            time.sleep(5)                  
        except:              
            bc.deliproute(self.dut1) 
            gntpc.delntpconfe(self.dut1) 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_044_max_ntp_server(self):
        try:         
            bc.disTitle(self.devAll,self.Title)
            bc.addiproute(self.dut1) 
            time.sleep(1) 
            gntpc.maxntpserver(self.dut1)
            time.sleep(1)                
            assert gntpc.checkmaxntpserver(self.dut1) == 4 
            time.sleep(1)                
            assert gntpc.overmaxntpserver(self.dut1) == True           
            time.sleep(1)
            bc.deliproute(self.dut1)
            gntpc.delmaxntpserver(self.dut1) 
            time.sleep(5)                 
        except:              
            bc.deliproute(self.dut1) 
            gntpc.delmaxntpserver(self.dut1) 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_045_time_zone_user_profile(self):
        try:         
            bc.disTitle(self.devAll,self.Title)
            time.sleep(1)            
            assert gtzc.timeZone(self.dut1) == True           
            time.sleep(10)                 
        except:              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(10)
            
    def test_051_xstp_portRole(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            ### To start the STP test, block ports or unblock them ###
            bc.noshutblockport(self.devAll,self.blockport)
            bc.shutStpBlockPort(self.devAll,self.stpblockport) 
            time.sleep(10)
            ##########################################################              
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(3)                  
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            stpc.stpSystemPri(self.dut1,mode,4096)
            time.sleep(10)  
            assert stpc.check_stp_PortRole(self.dut2,mode) == True   
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            stpc.stpSystemPri(self.dut1,mode,4096)
            time.sleep(10)  
            assert stpc.check_stp_PortRole(self.dut2,mode) == True
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            stpc.stpSystemPri(self.dut1,mode,4096)
            time.sleep(10)  
            assert stpc.check_stp_PortRole(self.dut2,'mstp') == True
            mode = 'disable'       
            stpc.stpEnaDisConf(self.devAll,mode)
            assert stpc.check_stp_PortRole(self.dut2,mode) == False            
            time.sleep(2)
            ### To clear the STP test, block ports or unblock them ###
            # bc.shutblockport(self.devAll,self.blockport)
            # bc.noshutStpBlockPort(self.devAll,self.stpblockport)
            ##########################################################
        except:
            # bc.shutblockport(self.devAll,self.blockport)
            # bc.noshutStpBlockPort(self.devAll,self.stpblockport)
            stpc.stpEnaDisConf(self.devAll,'disable')            
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
            
    def test_052_xstp_portState(self):
        ###  Only config at DUT2  ###
        try:         
            bc.disTitle(self.devAll,self.Title)   
            mode = 'stp'
            assert stpc.check_stp_PortState(self.dut2,mode) == True         
            mode = 'rstp'
            assert stpc.check_stp_PortState(self.dut2,mode) == True
            mode = 'mst' 
            assert stpc.check_stp_PortState(self.dut2,mode) == True           
            time.sleep(2)
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')             
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5) 
    
    def test_053_xstp_RooteBridge(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(5)  
            assert stpc.check_stp_RouteBridge(self.dut2,mode) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(5) 
            assert stpc.check_stp_RouteBridge(self.dut2,mode) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(5) 
            assert stpc.check_stp_RouteBridge(self.dut2,mode) == True            
            time.sleep(2)
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)   
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')               
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5) 

    def test_054_xstp_system_path_cost_config(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10)  
            assert stpc.check_stp_system_config(self.dut3) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_system_config(self.dut3) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_system_config(self.dut3) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)    
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5) 
            
    def test_055_xstp_timer_config(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)       
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(15)  
            assert stpc.check_stp_timer_config(self.devAll) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(15) 
            assert stpc.check_stp_timer_config(self.devAll) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(15) 
            assert stpc.check_stp_timer_config(self.devAll) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)    
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5) 
                                              
    def test_056_xstp_interface_RootGuard(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10)  
            assert stpc.check_stp_RootGuard(self.devAll,mode) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_RootGuard(self.devAll,mode) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_RootGuard(self.devAll,mode) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)    
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')
            bc.sendConfigSet(self.dut1,['interface 1/14','no shutdown'])                             
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_057_xstp_interface_BpduGuard(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10)  
            assert stpc.check_stp_BpduGuard(self.devAll) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_BpduGuard(self.devAll) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_BpduGuard(self.devAll) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)    
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable') 
            stpc.noStpBpduGuardConf(self.dut3)                 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
            
    def test_058_xstp_interface_BpduFilter(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10)  
            assert stpc.check_stp_BpduFilter(self.dut3,mode) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_BpduFilter(self.dut3,mode) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_stp_BpduFilter(self.dut3,mode) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)    
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')
            stpc.noStpBpduFilterConf(self.dut2)                 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
  
    def test_059_xstp_interface_EdgePort(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.dut1and2,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10)  
            assert stpc.check_stp_EdgePort(self.devAll,mode) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10) 
            assert stpc.check_stp_EdgePort(self.devAll,mode) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10) 
            assert stpc.check_stp_EdgePort(self.devAll,mode) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')
            stpc.noStpEdgePortConf(self.dut2,['1/10','1/13'])                 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
  
    def test_060_xstp_interface_PortPri(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10)  
            assert stpc.check_stp_PortPri(self.devAll) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10) 
            assert stpc.check_stp_PortPri(self.devAll) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10) 
            assert stpc.check_stp_PortPri(self.devAll) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable') 
            stpc.noStpPortPridConf(self.dut1,'1/16')                 
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_061_xstp_interface_PortCost(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'stp'
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10)  
            assert stpc.check_stp_PortCost(self.devAll) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10) 
            assert stpc.check_stp_PortCost(self.devAll) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.dut1and2,mode)
            time.sleep(10) 
            assert stpc.check_stp_PortCost(self.devAll) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable') 
            stpc.noStpPortCostConf(self.dut1,'1/16')               
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_062_mstp_multi_instance(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
             ### Configure MSTP multi instance ###
            stpc.mstpMultiInstance(self.devAll) 
            time.sleep(5) 
            ######################################
            assert stpc.check_mstp_MultiInstance(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_063_mstp_Priority_of_instance(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
            # stpc.mstpMultiInstance(self.devAll) 
            # time.sleep(5)  
            assert stpc.check_mstp_priority_of_instance(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')          
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_064_mstp_interface_cost_per_instance(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
            # stpc.mstpMultiInstance(self.devAll) 
            # time.sleep(5)  
            assert stpc.check_mstp_interface_cost(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')          
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
  
    def test_065_mstp_interface_priority_per_instance(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
            # stpc.mstpMultiInstance(self.devAll) 
            # time.sleep(5)  
            assert stpc.check_mstp_interface_pri(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')          
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
  
    def test_066_mstp_region_vlan(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
            stpc.mstpMultiInstance(self.devAll) 
            time.sleep(5)  
            assert stpc.check_mstp_region_vlan(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')          
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_067_mstp_region_name(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
            # stpc.mstpMultiInstance(self.devAll) 
            # time.sleep(5)  
            assert stpc.check_mstp_region_name(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')           
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_068_mstp_region_revision(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(2)
            # stpc.mstpMultiInstance(self.devAll) 
            # time.sleep(5)  
            assert stpc.check_mstp_region_revision(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')          
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)  

    def test_069_mstp_portRole_master(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)      
            mode = 'mst'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(3)
            # stpc.mstpMultiInstance(self.devAll) 
            # time.sleep(3)  
            assert stpc.check_mstp_portRole_master(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
            ### Remove MSTP Multi INstances ####
            stpc.noMstpMultiInstance(self.devAll)
            ####################################
            time.sleep(2)                      
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')
            time.sleep(2)
            ### Remove MSTP Multi INstances ####
            stpc.noMstpMultiInstance(self.devAll)
            ####################################
            time.sleep(2)        
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)  
                                                                                                       
    def test_070_STP_compatibility_with_xSTP(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2)  
            assert stpc.check_STP_compatibility_with_xSTP(self.devAll) == True       
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)     
            time.sleep(2)
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')                          
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
            
    def test_071_xstp_with_LACP(self):
        try:         
            bc.disTitle(self.devAll,self.Title) 
            mode = 'enable' 
            stpc.stpEnaDisConf(self.devAll,mode) 
            time.sleep(2) 
            mode = 'stp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10)  
            assert stpc.check_xstp_with_LACP(self.devAll) == True       
            mode = 'rstp'
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_xstp_with_LACP(self.devAll) == True 
            mode = 'mst' 
            stpc.stpModeConf(self.devAll,mode)
            time.sleep(10) 
            assert stpc.check_xstp_with_LACP(self.devAll) == True 
            mode = 'disable' 
            stpc.stpEnaDisConf(self.devAll,mode)    
            time.sleep(2)
            ### To clear the STP test, block ports or unblock them ###
            bc.shutblockport(self.devAll,self.blockport)
            bc.noshutStpBlockPort(self.devAll,self.stpblockport) 
            ########################################################## 
        except:
            stpc.stpEnaDisConf(self.devAll,'disable')
            ### To clear the STP test, block ports or unblock them ###
            bc.shutblockport(self.devAll,self.blockport)
            bc.noshutStpBlockPort(self.devAll,self.stpblockport) 
            ##########################################################                             
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
    
    def test_091_basic_pm_configure(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert pmc.pmConf(self.dut1) == True
            time.sleep(1)
            pmc.default_pm(self.dut1) 
            time.sleep(5)                       
        except:
            pmc.default_pm(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_092_basic_pm_csv(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert pmc.csvConf(self.dut1) == True
            time.sleep(1)
            pmc.default_csv(self.dut1)
            time.sleep(5)                        
        except:
            pmc.default_csv(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_093_mng_gw_config(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert mngc.mngGwConf(self.dut1) == True
            time.sleep(1)
            mngc.default_mng_gw_config(self.dut1) 
            time.sleep(5)                
        except:
            mngc.default_mng_gw_config(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    # @pytest.mark.skip() #For STP test
    def test_094_mng_process_config(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert mngc.mngProcessConf(self.dut1) == True
            time.sleep(1)
            mngc.default_mng_process_config(self.dut1) 
            time.sleep(5)              
        except:
            mngc.default_mng_process_config(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    def test_095_mng_mem_config(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert mngc.mngMemoryConf(self.dut1) == True
            time.sleep(1)
            mngc.default_mng_mem_config(self.dut1) 
            time.sleep(5)              
        except:
            mngc.default_mng_mem_config(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

    @pytest.mark.skip() #Because the feature hase a bug, this test item is skipped.
    def test_096_mng_evm_config(self):
        try:         
            bc.disTitle(self.devAll,self.Title)            
            assert mngc.mngEvmConf(self.dut1) == True
            time.sleep(1)
            mngc.default_mng_gw_config(self.dut1)
            mngc.default_mng_evm_config(self.dut1) 
            time.sleep(5)              
        except:
            mngc.default_mng_gw_config(self.dut1)
            mngc.default_mng_evm_config(self.dut1)              
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)
                        
    def test_0100_check_plog(self):
        try: 
            bc.disTitle(self.devAll,self.Title)
            assert bv.checkPlog(self.dut1,self.Title) == 'OK'
            time.sleep(5)                
        except:            
            assert bv.ExceptionLog(self.testName) == 'normal'
            time.sleep(5)

class MyPlugin:
    def pytest_sessionfinish(self,session, exitstatus):
        print("Test session finished!")


if __name__ == "__main__":
    
    # Get the current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    # Create the file name with the timestamp
    file_name = f"report_{timestamp}.html"

    # Construct the arguments string
    args_str = '--html=report/report.html --self-contained-html '+ __file__
    args_str = '--capture=tee-sys '+ __file__
    args_str = f"--html=report/{file_name} {__file__}"

    args = args_str.split(" ")
       
    pytest.main(args, plugins=[MyPlugin()])


