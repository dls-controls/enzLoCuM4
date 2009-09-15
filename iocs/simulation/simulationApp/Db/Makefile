TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
#  Optimization of db files using dbst (DEFAULT: NO)
#DB_OPT = YES

#----------------------------------------------------
# In a Diamond Support Module, install
# templates like this
#
#DB += motor.template
#DB += basic_motor.template

#----------------------------------------------------
# In a Diamond IOC Application, build db files from
# template files like this
#
DB += simulation.db

USES_TEMPLATE += $(LOCUM4)/db/enzLoCuM4.template

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
