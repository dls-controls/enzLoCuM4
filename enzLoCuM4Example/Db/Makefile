TOP=../..
include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE

#----------------------------------------------------
#  Optimization of db files using dbst (DEFAULT: NO)
#DB_OPT = YES

#----------------------------------------------------
# In a Diamond IOC Application, build db files from
# template files like this
#
DB += enzLoCuM4Example.db
DB += simulation_enzLoCuM4Example.db

USES_TEMPLATE += $(TOP)/enzLoCuM4/db/enzLoCuM4.template
USES_TEMPLATE += $(TOP)/enzLoCuM4/db/enzLoCuM4Readback.template
USES_TEMPLATE += $(TOP)/enzLoCuM4/db/simulation_enzLoCuM4.template

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE
