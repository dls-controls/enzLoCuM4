TOP=../..

ifdef EPICS_HOST_ARCH
# R3.14 Makefile
                                                                                
include $(TOP)/configure/CONFIG
                                                                                
USR_CFLAGS += -DABOVE_EPICS_R3_13
                                                                                
# -------------------------------
# Build an Diamond Support Module
# -------------------------------
                                                                                
LIBRARY_IOC_vxWorks += enzLoCuM4Test

# DLS8512.dbd will be installed into <top>/dbd

# The following are compiled and added to the support library
enzLoCuM4Test_SRCS += test_enzLoCuM4.c

# We need to link against the EPICS Base libraries
enzLoCuM4Test_LIBS += $(EPICS_BASE_IOC_LIBS)

include $(TOP)/configure/RULES
                                                                                
else
# R3.13 Makefile
                                                                                
include $(TOP)/config/CONFIG_APP
include $(TOP)/config/RULES_ARCHS
                                                                                
endif
