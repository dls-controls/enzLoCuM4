#!/bin/env python2.4

from pkg_resources import require
require("dls_serial_sim==1.8")
from dls_serial_sim import serial_device
from string import *

class QueryStatus:
	bit = {}

	def __init__(self):
		self.reset()
	
	def reset(self):
		self._val = 0
		self._strVal = "00"
		
	
	def setBit(self, strLED, strLEDState):
		iBit = self.bit[strLED]
		if strLEDState.lower() == "on":
			self._val |= (1 << iBit)
		else:
		    self._val &= ~(1 << iBit)

	def getStr(self):
		iMSB = (self._val >> 4)
		iMSB += 0x30
		iLSB = (self._val & 0x0f)
		iLSB += 0x30
		self._strVal = chr(iMSB)+chr(iLSB)
		return(self._strVal)


class FrontPanelSwitch(QueryStatus):
	bit = {"ExternalRelay":7, "MinusPolarityRelay":6, "BiasONRelay":5, "HVLED":4, "AutoLED":3, "MSBLED":2, "LED":1, "LSBLED":0}

	def setMR(self, iRangeVal):
		""" Set Bit2, Bit1, Bit0 of FP switch  """
		# Clear the lower 3 bits
		self._val &= 0xf8
		# OR in the range bits, allowing only the lower 3 bits
		self._val |= (iRangeVal & 0x07)

class MeasurementRange(QueryStatus):
	bit = {"1mA":7, "100uA":6, "10uA":5, "1uA":4, "100nA":3, "10nA":2, "1nA":1, "100pA":0}

	def setBit(self, strLED, strLEDState):
		self._val = 0
		QueryStatus.setBit(self, strLED, strLEDState)

class AutoRanging(QueryStatus):
	# Terminator is a carriage return
	Terminator = "\n"

	bit = {"CHA>":7, "CHB>":6, "CHC>":5, "CHD>":4, "CHA<":3, "CHB<":2, "CHC<":1, "CHD<":0}
	CH_states = {"CHD:HI":9800, "CHD:LO":410, "CHC:HI":9300, "CHC:LO":250, "CHB:HI":9500, "CHB:LO":400, "CHA:HI":9800, "CHA:LO":300}
	
	def __init__(self, chan_list_objs):
		QueryStatus.__init__(self)
		self._chan_list = chan_list_objs
	
	def getStrChanHi(self, channel_id):
		strRet = "CHA:HI" # default in case of bad key
		key = channel_id+":HI"
		if self.CH_states.has_key(key):
			strRet = "%4.4d" %(self.CH_states[key])
		return(strRet)

	def getStrChanLo(self, channel_id):
		strRet = "CHA:LO" # default in case of bad key
		key = channel_id+":LO"
		if self.CH_states.has_key(key):
			strRet = "%4.4d" %(self.CH_states[key])
		return(strRet)

	def setChanHi(self, channel_id, val):
		key = channel_id+":HI"
		if self.CH_states.has_key(key):
			self.CH_states[key] = val
		
	def setChanLo(self, channel_id, val):
		key = channel_id+":LO"
		if self.CH_states.has_key(key):
			self.CH_states[key] = val
	
	def getString(self):
		""" Compare the four channels (A,B,C,D) in peak_list and return range logic string """
		self.reset()
		if self._chan_list["CHA"].getMillivolts() > self.CH_states["CHA:HI"]:
			self.setBit("CHA>", "ON")
		if self._chan_list["CHB"].getMillivolts() > self.CH_states["CHB:HI"]:
			self.setBit("CHB>", "ON")
		if self._chan_list["CHC"].getMillivolts() > self.CH_states["CHC:HI"]:
			self.setBit("CHC>", "ON")
		if self._chan_list["CHD"].getMillivolts() > self.CH_states["CHD:HI"]:
			self.setBit("CHD>", "ON")
		if self._chan_list["CHA"].getMillivolts() < self.CH_states["CHA:LO"]:
			self.setBit("CHA<", "ON")
		if self._chan_list["CHB"].getMillivolts() < self.CH_states["CHB:LO"]:
			self.setBit("CHB<", "ON")
		if self._chan_list["CHC"].getMillivolts() < self.CH_states["CHC:LO"]:
			self.setBit("CHC<", "ON")
		if self._chan_list["CHD"].getMillivolts() < self.CH_states["CHD:LO"]:
			self.setBit("CHD<", "ON")
			
		return(self.getStr())
			
	def getCompString(self):
		ret = '"ChD ' + "%4.4d"%(self.CH_states['CHD:HI']) + "," + "%4.4d"%(self.CH_states['CHD:LO']) + '"' + self.Terminator + '"ChC ' + "%4.4d"%(self.CH_states['CHC:HI']) + "," + "%4.4d"%(self.CH_states['CHC:LO']) + '"' + self.Terminator + '"ChB ' + "%4.4d"%(self.CH_states['CHB:HI']) + "," + "%4.4d"%(self.CH_states['CHB:LO']) + '"' + self.Terminator + '"ChA ' + "%4.4d"%(self.CH_states['CHA:HI']) + "," + "%4.4d"%(self.CH_states['CHA:LO']) + '"'
		return( ret )


class Measurment:
	""" Channel peak measured current in mv  """
	def __init__(self, channel_id):
		self._chan = channel_id
		self._mv   = 0
		
	def setMillivolts(self, voltage):
		self._mv = voltage
		
	def getMillivolts(self):
		return(self._mv)
	
	def getString(self):
		strRet = "%4.4d" %(self._mv)
		return( strRet )

class enzLoCuM4(serial_device):

	# Terminator is a carriage return
	Terminator = "\n"

	# Options and original settings
	window_list = ['04', '08', '16', '32', '64']
	CH_states = {"CHD:HI":'9800', "CHD:LO":'410', "CHC:HI":'9300', "CHC:LO":'250', "CHB:HI":'9500', "CHB:LO":'400', "CHA:HI":'9800', "CHA:LO":'300'}  
	enz = {}
	
	
	def __init__(self, addresses):
		for address in addresses:
			# Set up dictionary of status for each unit
			vals = {"S1":'Auto', "S2":'0Volt', "HV":'OFF', "Ext":'OFF', "Bias":'OFF', "Auto":'OFF', "Int_Win":'04', "BiasState":'+'}
			# Assign dictionary to each module address setup
			self.enz[address] = vals

		self.fps = FrontPanelSwitch()
		self.mr  = MeasurementRange()

		self._chanA = Measurment("A")
		self._chanB = Measurment("B")
		self._chanC = Measurment("C")
		self._chanD = Measurment("D")

		self._chan_list = {"CHA":self._chanA, "CHB":self._chanB, "CHC":self._chanC, "CHD":self._chanD}

		self.ar  = AutoRanging(self._chan_list)

		self.nDebugLevel = 0


	def setDebugLevel(self, nLevel):
		self.nDebugLevel = nLevel
		
	def diagnostic(self,strDebug):
		if self.nDebugLevel > 0:
			print("enzLoCuM4 sim: "+strDebug)
						
	def reply(self, command):
		# Collect address and command info
		addr = command[1:3]
		operation = command[4:8].strip()   # SYST, CONF
		self.diagnostic("The full command is = " + command)
		#self.diagnostic("The module address = " + addr)
		#self.diagnostic("The command is = " + operation)
	
		# Configuration ettings
		if operation == "CONF":
			request = command[8:10].strip()
			#print "The request is " + request
			# Measuring range options
			if request == ":C":   
				# Check the power and link to the correct option
				self.fps.setBit("AutoLED", "OFF") # Auto OFF by default
				S1_command = command[-2:].strip()
				if S1_command == "10":
					self.diagnostic("Set range: 100pA")
					S1_res = '100pA'
					self.fps.setMR(0)
					self.mr.setBit("100pA", "ON")
				elif S1_command == "09":
					S1_res = '1nA'
					self.fps.setMR(1)
					self.mr.setBit("1nA", "ON")
				elif S1_command == "08":
					S1_res = '10nA'
					self.fps.setMR(2)
					self.mr.setBit("10nA", "ON")
				elif S1_command == "07":
					S1_res = '100nA'
					self.fps.setMR(3)
					self.mr.setBit("100nA", "ON")
				elif S1_command == "06":
					# Chr(181) is the ascii symbol for mu			
					S1_res = '1' + chr(181) + 'A'
					self.fps.setMR(4)
					self.mr.setBit("1uA", "ON")
				elif S1_command == "05":
					S1_res = '10' + chr(181) + 'A'
					self.fps.setMR(5)
					self.mr.setBit("10uA", "ON")
				elif S1_command == "04":
					S1_res = '100' + chr(181) + 'A'
					self.fps.setMR(6)
					self.mr.setBit("100uA", "ON")
				elif S1_command == "03":
					S1_res = '1mA'
					self.fps.setMR(7)
					self.mr.setBit("1mA", "ON")
				elif S1_command == "EF": # last two chars of 'DEF'
					S1_res = 'Auto'		
					self.enz[int(addr)]['Auto'] = 'ON'
					self.fps.setMR(0)
					self.fps.setBit("AutoLED", "ON")
				# Change the status to the new value		
				self.enz[int(addr)]['S1'] = S1_res
				ret = '"S1_' + self.enz[int(addr)]['S1'] 
			# Bias source options
			elif request == ":B":  
				S2_res = command[21:22] + command[22:].strip().lower()
				self.enz[int(addr)]['Ext'] = 'OFF'
				if S2_res == "Def":
					S2_res = "0Volt"
					self.enz[int(addr)]['Bias'] = 'OFF'
					self.fps.setBit("MinusPolarityRelay", "OFF")
					self.fps.setBit("BiasONRelay", "OFF")
					self.fps.setBit("ExternalRelay", "OFF")
					self.fps.setBit("HVLED", "OFF")
				elif S2_res == "Minus":
					self.enz[int(addr)]['BiasState'] = '-'
					self.enz[int(addr)]['Bias'] = 'ON'
					self.fps.setBit("MinusPolarityRelay", "ON")
					self.fps.setBit("BiasONRelay", "ON")
					self.fps.setBit("ExternalRelay", "OFF")
					self.fps.setBit("HVLED", "ON")
				elif S2_res == "Plus":
					self.enz[int(addr)]['BiasState'] = '+'		
					self.enz[int(addr)]['Bias'] = 'ON'
					self.fps.setBit("MinusPolarityRelay", "OFF")
					self.fps.setBit("BiasONRelay", "ON")
					self.fps.setBit("ExternalRelay", "OFF")
					self.fps.setBit("HVLED", "ON")
				elif S2_res == "Ext":
					self.enz[int(addr)]['BiasState'] = '+'		
					self.enz[int(addr)]['Bias'] = 'OFF'
					self.enz[int(addr)]['Ext'] = 'ON'
					self.fps.setBit("MinusPolarityRelay", "OFF")
					self.fps.setBit("BiasONRelay", "OFF")
					self.fps.setBit("ExternalRelay", "ON")
					self.fps.setBit("HVLED", "OFF")
				self.enz[int(addr)]['S2'] = S2_res	
				ret = '"S1_' + self.enz[int(addr)]['S1'] + ',S2_' + self.enz[int(addr)]['S2']
			# Request config status for all values
			elif request == "?": 
				ret = '"S1_' + self.enz[int(addr)]['S1'] + ',S2_' + self.enz[int(addr)]['S2'] + ',HV_' + self.enz[int(addr)]['HV'] + ',Ext_' + self.enz[int(addr)]['Ext'] + ',Bias' + self.enz[int(addr)]['BiasState'] + '_' + self.enz[int(addr)]['Bias'] + ',Auto_' + self.enz[int(addr)]['Auto'] + ',"'

		# System settings
		elif operation == "SYST":
			request = command[9:14].strip()
			#print "The request is " + request
			# Checks error status after every operation
			if request == "ERR?":
				ret = '"No_Error"'
			# Check version of software
			elif request == "VERS?":
		 		ret = '"SCPI_ENZ_1.13"'
			# Check limit values for Hi and Lo of all 4 channels
			elif request == "COMP:":
				Channel = command[17:20]
				HiLo = command[14:16]
				LimitName = Channel + ":" + HiLo
				LimitVal = command[21:].strip()
				if HiLo == "HI":
					self.ar.setChanHi(Channel, atoi(LimitVal))
				else:
					self.ar.setChanLo(Channel, atoi(LimitVal))
					
				self.CH_states[LimitName] = LimitVal
				ret = '"COMP_' + HiLo + "_" + Channel + '"'
			elif request == "COMP?":
				ret = self.ar.getCompString()
				#ret = '"ChD ' + self.CH_states['CHD:HI'] + "," + self.CH_states['CHD:LO'] + '"' + self.Terminator + '"ChC ' + self.CH_states['CHC:HI'] + "," + self.CH_states['CHC:LO'] + '"' + self.Terminator + '"ChB ' + self.CH_states['CHB:HI'] + "," + self.CH_states['CHB:LO'] + '"' + self.Terminator + '"ChA ' + self.CH_states['CHA:HI'] + "," + self.CH_states['CHA:LO'] + '"'
			# Integration window options
			elif request == "INTL":
				Int_Win = command[14:].strip()
				# If only single character, prefix with a zero
				if len(Int_Win) == 1:
					Int_Win = "0" + Int_Win
				# Change the status to the new value
				self.enz[int(addr)]['Int_Win'] = Int_Win
				ret = '"New INTL: ' + Int_Win + '"'
			# Request integration window setting
			elif request == "INTL?":
				ret = '"MVSL: ' + self.enz[int(addr)]['Int_Win'] + '"'

		# Status settings
		elif operation == "CLS":
			if self.enz[int(addr)] == "+":
				BiasState = "p"
			else:
				BiasState = "n"    	

			strFP = self.fps.getStr()
			strMR = self.mr.getStr()
			strAR = self.ar.getString()
			self.diagnostic("strFP = %s  strMR = %s  strAR = %s" %(strFP, strMR, strAR))
 			ret = 'P3_P4_P0:\n' + strFP + strMR + strAR

		# Reset and measurement
		elif operation == "RST":
			ret = '"Reset"'
		# Set the current for a chosen channel
		elif operation == "MEAS":
			Channel = command[9:].strip()
			if self._chan_list.has_key(Channel):
				m = self._chan_list[Channel]
				ret = '"' + Channel + ' ' + m.getString() + '"'
			#ret = '"' + Channel + ' 0012"'

		# Identification of unit
 		elif operation == "IDN?":
			# Check if bias set to positive or negative
			if self.enz[int(addr)] == "+":
				BiasState = "p"
			else:
				BiasState = "n"    	
			
			ret = '\r' + self.Terminator + '"LoCuM4' + BiasState + ',Version 1.13,Address ' + addr + ',#63073"\r'

		# Return the result with a terminator
		ret = ret + self.Terminator
		self.diagnostic("Transmitting: %s" %(ret))
		return ret		

	def getIDN(self):
		pass

	def setFP(self, bit, state):
		pass
	
	def setChanSignal(self, strChan, mv):
		""" Backdoor to set voltage reading for a given channel
		    e.g CHA """
		if (self._chan_list.has_key(strChan)):
			chan = self._chan_list[strChan]
			chan.setMillivolts(mv)

	def setChanLo(self, strChan, mv):
		""" Backdoor to set low range voltage for a given channel
		    e.g CHA """
		self.ar.setChanLo(strChan, mv)

if __name__ == "__main__":
	import os
	myEnz = enzLoCuM4([01,])
	myEnz.start_ip(9004)
	myEnz.start_debug(9006)
	raw_input()


