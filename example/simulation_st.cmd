###########################################################
# Pete Owens 2/9/04 vxWorks/EPICS startup file, 
# Example to simulate ENZ LoCuM-4 stream device application
#

#enzTop = "/home/pho76/diamond/enzLoCuM4"
enzTop  = "/home/diamond/R3.13.9/work/support/enzLoCuM4/Rx-y"
diamondTop = "/home/diamond/R3.13.9/work/support/superTop/Rx-y"

###########################################################

cd diamondTop
cd "bin/ppc604" 
ld < iocCore
ld < baseLib   
ld < utilityLib

###########################################################

cd diamondTop
cd "dbd" 
dbLoadDatabase "baseApp.dbd"

###########################################################
# Load the databses & start the IOC
#
cd enzTop
cd "example"

dbLoadTemplate "simulation_enzLoCuM4.substitutions"
iocInit

###########################################################
