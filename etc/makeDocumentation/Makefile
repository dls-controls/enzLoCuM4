TOP = ../..
include $(TOP)/configure/CONFIG

# set to -d to get debugging
DEBUG :=

# add the documentation files to the install target
install: $(TOP)/documentation/build_instructions $(TOP)/documentation/index.html

# rule for documentation
$(TOP)/documentation/index.html: config.src manual.src $(TOP)/documentation/build_instructions
	mkdir -p $(TOP)/documentation
	/dls_sw/work/common/python/documentation/src/documentation.py -o $(TOP)/documentation config.src manual.src

# rule for generating build instructions from example.xml file
$(TOP)/documentation/build_instructions: $(TOP)/etc/makeIocs/example.xml
	mkdir -p $(TOP)/documentation
	/dls_sw/work/common/python/xmlbuilder/src/xmlbuilder.py --doc=$@ $(DEBUG) $^

# Remove entire documentation dir on clean
clean:
	rm -rf $(TOP)/documentation
