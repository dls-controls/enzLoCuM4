TOP = ../..

ifdef EPICS_HOST_ARCH

include $(TOP)/configure/CONFIG
DATA += $(patsubst ../%, %, $(wildcard ../*.protocol))
include $(TOP)/configure/RULES

else
endif

