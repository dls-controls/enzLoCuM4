INTRODUCTION
------------
This is the EPICS support module for the
FMB (ENZ) LoCuM-4 low current monitor.

The conroller utilises a RS232 interface for serial communications.

The specification is based on FMB document:
http://www.beamline.net/
http://www.enz-de.de/beamline/pr-locurr.html
"4-Channel Low-Current Monitor LoCuM-4" V1.1

USAGE
-----


One template is provided here:

1) enzLoCuM4.template
    This instatiates all the records associated with the unit's control via the
serial interface

2) enzLoCuM4Readback.template
    This defines the records required to read the four analogue signals output
from the controller, each
associated with the four blades within the XBPM module. It's within the LoCuM4
support module as a supplementary template to perform appropriate data reduction
on the blade signals in order to derive beam position.

   
The user interface is presently available via EDM screens. 
enzLoCuM4.edl         - Configuration and status monitoring of the controller
enzLoCuM4Readback.edl - Displays the four blade analogue signals and derived
beam position.

MAINTAINERS
-----------

Current maintainers:
* Ian Gillingham (Diamond Light Source) - ian.gillingham@diamond.ac.uk

First created March 2006.


