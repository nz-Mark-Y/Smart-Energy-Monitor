#================================================================================================
# Group 37 
#================================================================================================
# Have to install pySerial first:
#   1. Go to https://pypi.python.org/pypi/pyserial, download, extract, navigate to pySerial-3.1.1
#   2. Open folder in cmd, run "python setup.py install"
#   3. ???
#   4. Profit
#
# Additionally we have to set pin36 "as input tri-stated", and do some jumpers on the board.
#================================================================================================
import serial

ser = serial.Serial(
    port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)

#this will store the line
line = []

while True:
    for c in ser.read():
        line.append(c)
        if c == '\n':
            print("Line: " + line)
            line = []
            break

ser.close()
