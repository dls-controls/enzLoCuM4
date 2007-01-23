TOP=../..
                                                                                
ifdef EPICS_HOST_ARCH
# R3.14 Makefile
                                                                                
include $(TOP)/configure/CONFIG
                                                                                
USR_CFLAGS += -DABOVE_EPICS_R3_13

# enzLoCuM4.dbd will be installed into <top>/dbd
DBD += enzLoCuM4.dbd
                                                                                
enzLoCuM4_DBD += base.dbd

include $(TOP)/configure/RULES
                                                                                
else
endif

