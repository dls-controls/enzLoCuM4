#Makefile at top of application tree
TOP = .
ifdef EPICS_HOST_ARCH

include $(TOP)/configure/CONFIG
DIRS := $(DIRS) $(filter-out $(DIRS), configure)
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard *App))
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard *app))
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard iocBoot))
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard iocboot))
# Uncomment the next line to build examples
#DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard *Example))
DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard etc))
# Comment out the following line to disable building of example iocs
#DIRS := $(DIRS) $(filter-out $(DIRS), $(wildcard iocs))
include $(TOP)/configure/RULES_TOP

else

include $(TOP)/config/CONFIG_APP
DIRS += config
DIRS += $(wildcard *App)
DIRS += $(wildcard *app)
DIRS += $(wildcard iocBoot)
DIRS += $(wildcard iocboot)
include $(TOP)/config/RULES_TOP

endif

