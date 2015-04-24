##
##  filename: demoCore.py
##

import os
import serial
import re
import datetime

CURRENTDIR = os.path.dirname(__file__)
BASEDIR    = os.path.dirname(CURRENTDIR)

last_received = ''

class TempCore():

	def index(self,request):

		json = 0
        	data = ["","",""]
    
		if request.args.get('json', '') == "1":
			json = 1
			ser = serial.Serial('/dev/ttyACM0', 9600)
			data = self.receiving(ser)
		html = self.showDemoHTML(data,json)
		return html

	def receiving(self, ser):
		global last_received
		data = ["","",""]
        
		buffer = ''
		while True:
			buffer = buffer + ser.read()
			if '\r\n' in buffer:
				splitbuffer = buffer.split('\r\n')
 				buffer = splitbuffer[1]
				while True:
					buffer = buffer + ser.read()
					if '\r\n' in buffer:
						data[0] = buffer
					# splitbuffer = buffer.split('\r\n')
					# buffer = splitbuffer[1] 
					#matchTemperature = re.match( r'(.*)Temperature: (.*) \*C', buffer, re.M|re.I)
						#matchTemperature = re.match( r'(.*)Temperature=(.*)', buffer, re.M|re.I)
						#if matchTemperature:
						#	data[1] = matchTemperature.group(2).strip()
						#matchHumidity = re.match( r'(.*)Humidity=(.*)', buffer, re.M|re.I)
						#if matchHumidity:
					#		data[2] = matchHumidity.group(2).strip()
						match = re.match(r'(.*),(.*)', buffer, re.M|re.I)
						if match:
							data[1] = match.group(1).strip()
							data[2] = match.group(2).strip()
						return data
        
	def showDemoHTML(self,data,json):
		## reads an html file and does things with it
		## there are better ways, but they are more complicated

		if json == 1:
			f = open(CURRENTDIR +"/json.html")
			html = f.read()
			html = html.replace("%Debug%",str(data[0]))            
			html = html.replace("%Temperature%",str(data[1]))
			html = html.replace("%Humidity%",str(data[2]))            
			return html        

		else:
			f = open(CURRENTDIR +"/temp_google.html")
			html = f.read()
			return html

if __name__ == "__main__":
    print "Hello World";
