#================================================================================================
# Group 37
#================================================================================================
# Have to install pySerial first:
#   1. Go to https://pypi.python.org/pypi/pyserial, download, extract, navigate to pySerial-3.1.1
#   2. Open folder in cmd, run "python setup.py install"
#   3. ???
#   4. Profit
#================================================================================================
import serial

def main():
    ser = serial.Serial(
        port='COM6',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)

    print("connected to: " + ser.portstr)

    previousEightDigits = []
    dataArray = [0,0,0,0]

    while True:
        eightDigits = []
        while len(eightDigits) < 8:
            decoded = ser.read().decode("utf-8")
            if (len(decoded) > 0):
                num = ord(decoded)
                eightDigits.append(num)

        if eightDigits != previousEightDigits:
            largestIndex = findLargestIndex(eightDigits)
            for i in range(largestIndex,largestIndex+4):
                dataArray[i-largestIndex] = eightDigits[i]
            print(dataArray)
            previousEightDigits = eightDigits
        
    ser.close()
    return

def findLargestIndex(myArray):
    largestIndex = 0
    largestNum = myArray[largestIndex]
    for i in range(0,len(myArray)):
        if myArray[i] > largestNum:
            largestNum = myArray[i]
            largestIndex = i
    return largestIndex
  
main()
    
