# |================================================================================================|
# | Group 37                                                                                       |
# |================================================================================================|
# | Have to install pySerial first:                                                                |
# |  1. Go to https://pypi.python.org/pypi/pyserial, download, extract, navigate to pySerial-3.1.1 |
# |  2. Open folder in cmd, run "python setup.py install"                                          | 
# |  3. ???                                                                                        |
# |  4. Profit                                                                                     |
# |================================================================================================|
import serial
import json
import threading
import sys
from firebase import firebase

# Class to store each data value along with a timestamp and which data number it is
class MyData:
    numberCount = 0
    def __init__(self, value):
        self.value = value
        MyData.numberCount += 1
        self.number = MyData.numberCount
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
# Set up serial listening
try:
    ser = serial.Serial(
        port='COM6',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
    print("connected to: " + ser.portstr)
except:
    print("Could not open serial port COM6. Check the COM port listings in Device Manager.")
    sys.exit()

#Set up firebase and clear old data
firebaseObject = firebase.FirebaseApplication('https://electeng209-520f4.firebaseio.com/', authentication=None)
print("Clearing old data")
firebaseObject.delete('/data', None)

dataIn = []

def readData(ser):
    print("Reading data...")
    # Start reading data from serial port
    while True:
        while True:
            try:
                decoded = ser.read().decode("utf-8") # Decode ascii into integers
                break
            except UnicodeDecodeError:
                print("Invalid Start Location. Reattempting.") # Just in case
        if (len(decoded) > 0):
            num = ord(decoded)
            dataIn.append(num)
    return
                
def handleData(dataIn):
    previousEightDigits = [] # Eight digit array for sampling the input
    dataArray = [0,0,0,0] # The four integers which represent the data
    while True:
        if (len(dataIn) >= 8):
            eightDigits = dataIn[len(dataIn)-8:]
            if eightDigits != previousEightDigits: # If we have a change
                largestIndex = findLargestIndex(eightDigits)
                if (largestIndex <= 4) and (eightDigits[largestIndex] not in eightDigits[largestIndex+1:largestIndex+4]):
                    for i in range(largestIndex,largestIndex+4):
                        dataArray[i-largestIndex] = eightDigits[i] # Find the four digits of the data and store in data array
                    value = ololow(dataArray) # Convert the data array back into the data sent
                    dataToSend = MyData(value) # Create a MyData object to upload to firebase as JSON
                    result = firebaseObject.post('/data', dataToSend.toJSON()) # Upload the JSON representation of the data object
                    print(dataToSend.value) # For debugging purposes
                    #===========================
                    # Put graphing in here
                    #===========================
                previousEightDigits = eightDigits
    return

# Finds the largest integer in an array
def findLargestIndex(myArray):
    largestIndex = 0
    largestNum = myArray[largestIndex]
    for i in range(0,len(myArray)):
        if myArray[i] > largestNum:
            largestNum = myArray[i]
            largestIndex = i
    return largestIndex

# Converting the data array back into the float that was measured by the micro
def ololow(myArray):
    value = 0
    decimalPlace = 3
    myArray[0] -= 96
    myArray[1] -= 64
    myArray[2] -= 32
    for i in range(0,4):
        if myArray[i] >= 16:
            myArray[i] -= 16
            decimalPlace = i
    value = 1000*myArray[0] + 100*myArray[1] + 10*myArray[2] + myArray[3]
    value = value / (10**(3-decimalPlace))
    return value

thread = threading.Thread(target=readData, args=(ser,))
thread2 = threading.Thread(target=handleData, args=(dataIn,))
thread.start()
thread2.start()



    
