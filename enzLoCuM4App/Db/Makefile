TOP=../..
ifdef EPICS_HOST_ARCH
                                                                                
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
                                                                                
#----------------------------------------------------
#  Optimization of db files using dbst (DEFAULT: NO)
#DB_OPT = YES
                                                                                
#----------------------------------------------------
# In a Diamond Support Module, install
# templates like this
DB += enzLoCuM4.template
                                                                                
include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
                                                                                
else
                                                                                
include $(TOP)/config/CONFIG_APP
include $(TOP)/config/RULES_ARCHS
                                                                                
endif
