###########################################################
# Pete Owens 2/9/04 vxWorks/EPICS startup file, 
# Example to test ENZ LoCuM-4 stream device application
# This IOC is configured for :
#       Hytec IP Carrier 8002 card in slot 7 - 
#       Hytec 8515 Octal serial module in slot A
#	ENZ LoCuM-4 low current monitor on port 0
#

#enzTop = "/home/pho76/diamond/enzLoCuM4"
enzTop  = "/home/diamond/R3.13.9/work/support/enzLoCuM4/Rx-y"
diamondTop = "/home/diamond/R3.13.9/work/support/superTop/Rx-y"

IPSLOTA = 0
IPSLOTB = 1
IPSLOTC = 2
IPSLOTD = 3

###########################################################
# Configure serial port numbers here
#  
VMESLOT = 7
IPSLOT  = IPSLOTB
PORTNUM = 3
TSTPNUM = 4
CARDNUM = (10 * VMESLOT) + IPSLOT

###########################################################

cd diamondTop
cd "bin/ppc604" 
ld < iocCore
ld < baseLib   
ld < utilityLib
ld < streamLib
ld < streamTty.o
ld < ipacLib
ld < drvHy8515.o

###########################################################

cd diamondTop
cd "dbd" 
dbLoadDatabase "baseApp.dbd"
dbLoadDatabase "drvIpac.dbd" 
dbLoadDatabase "stream.dbd" 

###########################################################
# Configure a Hytec 8002 carrier VME slot 7
#
#                        vmeslotnum, IPintlevel, HSintnum
ARGS = malloc (20)
IVEC = newInterruptVector ()
sprintf (ARGS, "%d %d %d", VMESLOT, 2, IVEC)
CARRIER = ipacEXTAddCarrier (&EXTHy8002, ARGS)

###########################################################
# Hytec 8515 IPOctal serial module in slot C on the IP carrier card. 
#
# Configure module on carrier 7, slot 3
# Params are : 
#	cardnum, 
#	vmeslotnum, 
#	ipslotnum, 
#	vectornum, 
#	intdelay (-ve => FIFO interrupt), 
#	halfduplexmode, 
#	delay845
#
IVEC = newInterruptVector ()
MODNUM = Hy8515Configure (CARDNUM, CARRIER, IPSLOT, IVEC, -32, 0, 0)

# Create devices
# Params are :
#	name
#	card number
#	port number
#	read buffer size
#	write buffer size
#
ENZPORT = tyHYOctalDevCreate("/ty/enz/3", MODNUM, PORTNUM, 2500, 250)

tyHYOctalConfig (ENZPORT, 9600, 'N', 1, 8, 'N')

###########################################################
# Configure stream device
#
STREAM_PROTOCOL_DIR = malloc (100)
strcpy (STREAM_PROTOCOL_DIR, enzTop)
strcat (STREAM_PROTOCOL_DIR, "/enzLoCuM4App/protocol")

ty_enz_3_streamBus = "Tty"

streamTtyDebug = 1

###########################################################
# Load the databases & start the IOC
#
cd enzTop
cd "example"

dbLoadTemplate "enzLoCuM4.substitutions"
iocInit

###########################################################
