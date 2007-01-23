TOP=../..

include $(TOP)/configure/CONFIG

# -------------------------------
# Build an Diamond Support Module
# -------------------------------

#LIBRARY_IOC += xxx

# xxxRecord.h will be created from xxxRecord.dbd
#DBDINC += xxx.h

# xxxRecord.dbd will be installed into <top>/dbd
#DBD += xxx.dbd

# The following are compiled and added to the support library
#xxx_SRCS += xxxCodeA.c
#xxx_SRCS += xxxCodeB.c

# We need to link against the EPICS Base libraries
#xxx_LIBS += $(EPICS_BASE_IOC_LIBS)


# ------------------------
# Build an IOC Application
# ------------------------

PROD_IOC_vxWorks = enzLoCuM4Example
#PROD_IOC = enzLoCuM4Example

# enzLoCuM4Example.dbd will be installed into <top>/dbd
DBD += enzLoCuM4Example.dbd

# enzLoCuM4Example.dbd will be created from these files
enzLoCuM4Example_DBD += base.dbd
enzLoCuM4Example_DBD += stream.dbd
enzLoCuM4Example_DBD += drvAsynSerialPort.dbd
enzLoCuM4Example_DBD += drvAsynIPPort.dbd
enzLoCuM4Example_DBD += drvIpac.dbd
enzLoCuM4Example_DBD += Hy8515.dbd
enzLoCuM4Example_DBD += Hy8401ip.dbd

#enzLoCuM4Example_DBD += xxx.dbd

# enzLoCuM4Example_registerRecordDeviceDriver.cpp will be created
# enzLoCuM4Example.dbd
enzLoCuM4Example_SRCS += enzLoCuM4Example_registerRecordDeviceDriver.cpp

# These two lines are needed for non-vxWorks builds, such as Linux
enzLoCuM4Example_SRCS_DEFAULT += enzLoCuM4ExampleMain.cpp
enzLoCuM4Example_SRCS_vxWorks += -nil-

# Add locally compiled object code
#enzLoCuM4Example_SRCS +=

# The following adds object code from base/src/vxWorks
enzLoCuM4Example_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# This line says that this IOC Application depends on the
# xxx Support Module
enzLoCuM4Example_LIBS += stream
enzLoCuM4Example_LIBS += asyn
enzLoCuM4Example_LIBS += Hy8401ip
enzLoCuM4Example_LIBS += drvHy8515
enzLoCuM4Example_LIBS += Ipac

# We need to link this IOC Application against the EPICS Base libraries
enzLoCuM4Example_LIBS += $(EPICS_BASE_IOC_LIBS)

# ---------------------------------------------------

# NOTE: To build SNL programs, SNCSEQ must be defined
# in the <top>/configure/RELEASE file
#
# The difference between a file with an "st" extension
# and one with an "stt" extension is:
# The "st" extension files get passed through the C preprocessor
# whereas the "stt" files do not.

#ifneq ($(SNCSEQ),)
    # This builds sncExample as a component of enzLoCuM4Example
#    enzLoCuM4Example_SNCFLAGS += +r
#    enzLoCuM4Example_DBD      += sncExample.dbd
#    enzLoCuM4Example_SRCS     += sncExample.stt
#    enzLoCuM4Example_LIBS     += seq pv

    # The following builds sncExample as a standalone application
#    PROD_HOST           += sncExample
#    sncExample_SNCFLAGS += +m
#    sncExample_SRCS     += sncExample.stt
#    sncExample_LIBS     += seq pv
    # Here, we need to specify the dependency on EPICS Base libraries
    # again because this is a standalone application and
    # not part of enzLoCuM4Example
#    sncExample_LIBS     += $(EPICS_BASE_HOST_LIBS)
#endif

include $(TOP)/configure/RULES
