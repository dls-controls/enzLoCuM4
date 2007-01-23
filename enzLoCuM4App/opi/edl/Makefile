TOP = ../../..

ifdef EPICS_HOST_ARCH
include $(TOP)/configure/CONFIG
buildInstall: $(EDL_FROM_V)

DATA += $(patsubst ../%, %, $(wildcard ../*.edl))
DATA += $(patsubst ../%, %, $(wildcard ../*.gif))
DATA += $(patsubst ../%, %, $(wildcard ../*.png))

clean::
	rm -f $(EDL_FROM_V) velocity.log

uninstall:
	$(foreach file,$(EDL_FROM_V),rm -f $(file))

include $(TOP)/configure/RULES

%.edl: %.v
	velocity -a $< > $@

%.edl: ../%.v
	velocity -a $< > ../$@

else
endif
