#!/dls_sw/tools/bin/python2.4

# Test suite to use with pyUnit

import sys
sys.path.insert(0,'/dls_sw/work/common/python/autotestframework/dist/dls.autotestframework-0.0-py2.4.egg')
from pkg_resources import require
#require('dls.autotestframework==1.13')
from dls.autotestframework import *

################################################
# Test suite for the FW102 filter wheel
    
class enzLoCuM4TestSuite(TestSuite):

    def createTests(self):
        # Define the targets for this test suite
        Target("simulation", self,
            iocDirectory="iocs/simulation",
            iocBootCmd="bin/linux-x86/stsimulation.boot",
            runIocInScreenUnderHudson=True,
            epicsDbFiles="db/simulation.db",
            ##simDevices=[SimDevice("locum4", 9016)],
            simDevices=[SimDevice("locum4", 9001, rpc=True)],
            environment=[('EPICS_CA_REPEATER_PORT','6065'),
                ('EPICS_CA_SERVER_PORT','6064')],
            guiCmds=[r'edm -x -eolc -m "P=LOCUM4SIM-01" data/enzLoCuM4.edl'])

        # The tests
        CaseSetRange(self)
        #CaseSetSignal(self)
        #CaseSetLo(self)
        #CaseSetHi(self)
        CaseSetBiasSource(self)
        
################################################
# Intermediate test case class that provides some utility functions
# for this suite

class enzLoCuM4Case(TestCase):
    base_pvname = "LOCUM4SIM-01"
    pv_setrange = base_pvname+":SETRANGE"
    pv_range    = base_pvname+":RANGE"
        
        
################################################
# Test cases
    
class CaseSetRange(enzLoCuM4Case):
    def runTest(self):
        ranges = ["100pA", "1nA", "10nA", "100nA", "1uA", "10uA", "100uA", "1mA", "Auto"]
        expected_fp = {"100pA":0, "1nA":1, "10nA":2, "100nA":3, "1uA":4, "10uA":5, "100uA":6, "1mA":7, "Auto":8}
        print "enzLoCuM4TestSuite - CaseSetRange()"
        '''The SetRange test'''
        if self.simulationDevicePresent("locum4"):
            for rng in ranges:
                #if rng=="100pA":
                #    continue
                self.diagnostic("range=%s" % (rng),1)
                self.putPv(self.pv_setrange, rng)
                self.sleep(2)
                self.diagnostic("range read=%s" % (self.getPv(self.pv_range,datatype=DBR_STRING)),1)
                self.verifyPv(self.pv_range, rng, datatype=DBR_STRING)
                fp = self.getPv(self.base_pvname+":FP")
                self.verify(fp & 0x0f, expected_fp[rng])

class CaseSetSignal(enzLoCuM4Case):
    def runTest(self):
        print "enzLoCuM4TestSuite - CaseSetSignal()"
        '''The Ident test'''
        if self.simulationDevicePresent("locum4"):
            self.simulation('locum4').setChanSignal('CHA', 500)
            self.sleep(1)
            self.verifyPv(self.base_pvname+":CHA:PEAK", 500)
            
class CaseSetLo(enzLoCuM4Case):
    def runTest(self):
        vals = [300, 400, 500, 600]
        chans = ["CHA","CHB","CHC","CHD"]
        print "enzLoCuM4TestSuite - CaseSetLo()"
        if self.simulationDevicePresent("locum4"):
            for ch in chans:
                for v in vals:
                    self.putPv(self.base_pvname+":"+ch+":SETLO", v)
                    self.sleep(5)
                    self.verifyPv(self.base_pvname+":"+ch+":LO", v)
            for ch in chans:
                self.putPv(self.base_pvname+":"+ch+":SETLO", 300)
            
class CaseSetHi(enzLoCuM4Case):
    def runTest(self):
        vals = [9600, 9700, 9800, 9900]
        chans = ["CHA","CHB","CHC","CHD"]
        print "enzLoCuM4TestSuite - CaseSetLo()"
        if self.simulationDevicePresent("locum4"):
            for ch in chans:
                for v in vals:
                    self.putPv(self.base_pvname+":"+ch+":SETHI", v)
                    self.sleep(5)
                    self.verifyPv(self.base_pvname+":"+ch+":HI", v)
            for ch in chans:
                self.putPv(self.base_pvname+":"+ch+":SETHI", 9800)
            
class CaseSetBiasSource(enzLoCuM4Case):
    def runTest(self):
        vals = ['Plus', 'Minus', 'External', 'Ground']
        fpvals = {"Ground":0, "HV":16, "Bias":32, "Neg":64, "External":128}
        expected_fp = {"Plus":fpvals["HV"]|fpvals["Bias"], "Minus":fpvals["HV"]|fpvals["Bias"]|fpvals["Neg"], "External":fpvals["External"], "Ground":fpvals["Ground"]}
        expected_hv = {"Plus":'On'}
        print "enzLoCuM4TestSuite - CaseSetBiasSource()"
        if self.simulationDevicePresent("locum4"):
            for v in vals:
                self.putPv(self.base_pvname+":SETBIASV", v)
                self.sleep(2)
                self.verifyPv(self.base_pvname+":BIASV", v, datatype=DBR_STRING)
                fp = self.getPv(self.base_pvname+":FP")
                self.verify(fp & 0xf0, expected_fp[v])
            
################################################
# Main entry point

if __name__ == "__main__":
    # Create and run the test sequence
    enzLoCuM4TestSuite()

    
