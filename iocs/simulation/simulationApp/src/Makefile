TOP=../..

include $(TOP)/configure/CONFIG

# ------------------------
# Build an IOC Application
# ------------------------

PROD_IOC = simulation

# simulation.dbd will be installed into <top>/dbd
DBD += simulation.dbd

# simulation.dbd will be created from these files
simulation_DBD += base.dbd
#simulation_DBD += pyDrv.dbd
simulation_DBD += stdSupport.dbd
simulation_DBD += asyn.dbd
simulation_DBD += drvAsynIPPort.dbd
simulation_DBD += drvAsynSerialPort.dbd
simulation_DBD += stream.dbd
simulation_DBD += calcSupport.dbd

# simulation_registerRecordDeviceDriver.cpp will be created
# simulation.dbd
simulation_SRCS += simulation_registerRecordDeviceDriver.cpp

# These two lines are needed for non-vxWorks builds, such as Linux
simulation_SRCS_DEFAULT += simulationMain.cpp
simulation_SRCS_vxWorks += -nil-

# Add locally compiled object code
#simulation_SRCS +=

# The following adds object code from base/src/vxWorks
simulation_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# This line says that this IOC Application depends on the
# xxx Support Module
simulation_LIBS += calc
simulation_LIBS += std
simulation_LIBS += stream
simulation_LIBS += asyn
simulation_LIBS += pcre
#simulation_LIBS += pyDrv

# We need to link this IOC Application against the EPICS Base libraries
simulation_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
