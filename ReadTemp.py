import os
import serial
import re
import datetime
import requests, json

CURRENTDIR = os.path.dirname(__file__)
BASEDIR    = os.path.dirname(CURRENTDIR)

class ReadTemp():
    def receiving(self):
        ser = serial.Serial('/dev/ttyACM0', 9600)
        data = ["","","",""]

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
                        match = re.match(r'(.*),(.*),(.*)', buffer, re.M|re.I)
                        if match:
                            data[1] = match.group(1).strip()
                            data[2] = match.group(2).strip()
                            data[3] = match.group(3).strip()
                        print data
                        return data

    def send_data(self):
        data = self.receiving()
        thData = {'humidity': float(data[1]), 'temperature': float(data[2]), 'heatIndex': float(data[3])}

        url = 'https://ZKO8dy1AE8bESiGKEtoV2WzayMX023OpCabQ3ijl:javascript-key=fgKvOnZvBjqIfbWL10I3ZRHILpujZURKnnoYZaeS@api.parse.com/1/classes/THObject'
        headers = {'Content-Type':'application/json'}
        r = requests.post(url, data=json.dumps(thData), headers=headers)
        print(r.text)


if __name__ == "__main__":
    readTemp = ReadTemp()
    readTemp.send_data()
