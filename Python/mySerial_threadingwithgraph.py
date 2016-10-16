# |================================================================================================|
# | Group 37                                                                                       |
# |================================================================================================|
# | Have to install pySerial first:                                                                |
# |  1. Go to https://pypi.python.org/pypi/pyserial, download, extract, navigate to pySerial-3.1.1 |
# |  2. Open folder in cmd, run "python setup.py install"                                          | 
# |  3. ???                                                                                        |
# |  4. Profit                                                                                     |
# |================================================================================================|                                                                |
# | Graphing requires Matplotlib. Run the 2 statements below in cmd  							   |
# |  (Assuming Python has already been installed)                                     			   | 
# |  py -m pip install -U pip setuptools                                                           |
# |  py -m pip install matplotlib                                                                  |
# |================================================================================================|

import serial
import json
import threading
import sys
from firebase import firebase

import matplotlib.pyplot as plt #import the matplotlib library
import numpy as np				#import the numpy extension
from matplotlib.widgets import Button #import the button widget
import warnings
warnings.filterwarnings("ignore") 

# Class to store each data value along with a timestamp and which data number it is
class MyData:
    numberCount = 0
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit
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
    print("Could not open serial port COM7. Check the COM port listings in Device Manager.")
    sys.exit()

#Set up firebase and clear old data
firebaseObject = firebase.FirebaseApplication('https://electeng209-520f4.firebaseio.com/', authentication=None)
print("Clearing old data")
firebaseObject.delete('/data', None)

dataIn = []
p = [0]*300
v = [0]*300
a = [0]*300
displaying = 0;

def readData(ser):
    print("Reading data...")
    print("Graphing loading...")
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
    global p
    global v
    global a
    previousEightDigits = [] # Eight digit array for sampling the input
    dataArray = [0,0,0,0] # The four integers which represent the data
    while True:
        try:
            if (len(dataIn) >= 8):
                eightDigits = dataIn[len(dataIn)-8:]
                if eightDigits != previousEightDigits: # If we have a change
                    largestIndex = findLargestIndex(eightDigits)
                    if (largestIndex <= 4) and (eightDigits[largestIndex] not in eightDigits[largestIndex+1:largestIndex+4]):
                        for i in range(largestIndex,largestIndex+4):
                            dataArray[i-largestIndex] = eightDigits[i] # Find the four digits of the data and store in data array
                        value = ololow(dataArray) # Convert the data array back into the data sent
                        if dataArray[3] == 15:
                            unit = 'W'
                            p.insert(0, value)
                            p = p[0:300]
                        elif dataArray[3] == 14:
                            unit = 'V'
                            v.insert(0, value)
                            v = v[0:300]
                        else:
                            if value > 10 or value < 0:
                                continue
                            unit = 'A'
                            a.insert(0, value)
                            a = a[0:300]
                        dataToSend = MyData(value, unit) # Create a MyData object to upload to firebase as JSON
                        result = firebaseObject.post('/data', dataToSend.toJSON()) # Upload the JSON representation of the data object
                        print(dataToSend.value, dataToSend.unit) # For debugging purposes
                    previousEightDigits = eightDigits
        except:
            print("Firebase Connection Failed")
            continue
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
    value = 100*myArray[0] + 10*myArray[1] + myArray[2]
    value = value / (10**(2-decimalPlace))
    return value

def realtimegraph():
    global p
    global v
    global a
    while True:
        if (p[0] != 0) and (v[0] != 0) and (a[0] != 0):
            print("Graphing loaded.")
            break
                
    try:
        fig, ax = plt.subplots()	#Create a figure with a set of subplots already made
        plt.subplots_adjust(bottom=0.2) #Adjust the distance from the bottom of the graph to the bottom of the window
			
        ax.patch.set_facecolor('#89CFF0') #set background colour of plot to baby blue
		
        plt.grid(True)
        t = list(range(300))	#x-axis data points
	
        l, = plt.plot(t, p, lw =3)	#plots a line on the axes with a linewidth of 3
        #ax = plt.gca()#
        #ax.invert_yaxis()#
        #The initial graph on startup will be a Power vs Time graph
        global displaying
        displaying = 0;
        print("Graph displaying power")
        
        #The x and y limits for the Power vs Time graph is set
        ax.set_xlim(25,0)
        ax.set_ylim(0, 10)
        txt = fig.text(0.4,0.95,' Power vs Time ',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15)	#title of graph
        yaxistxt = fig.text(0.05,0.6,'Power (Watts)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')	#y axis label of graph	
        plt.xlabel('Data Points', fontsize = 15)	#x-axis label of graph
        
        class Index(object):
            #The 5 below functions are used to adjust the x-axis limits depending on the button that is pressed
            def three_hundred(self, event):			
                ax.set_xlim(300,0)
            def two_hundred(self, event):			
                ax.set_xlim(200,0)
            def one_hundred(self, event):			
                ax.set_xlim(100,0)
            def fifty(self, event):			
                ax.set_xlim(50, 0)
            def twenty_five(self, event):			
                ax.set_xlim(25, 0)
            
            #The 3 below functions are used to switch between power, voltage or current graphs depending on which button is pressed
            def voltage(self,event):
                print("Graph displaying voltage")
                l.set_ydata(v)	#sets the plot to display the voltage dataset
                ax.set_ylim(0, 16)	#sets the y-axis limits to the appropriate size for the voltage dataset
                
                for txt in fig.texts: #Makes previously drawn text boxes disappear
                    txt.set_visible(False)
                txt = fig.text(0.4,0.95,'Voltage vs Time',bbox=dict(facecolor='none', alpha=10,lw=0),fontsize = 15)
                yaxistxt = fig.text(0.05,0.6,'Voltage (Volts)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')            
                global displaying
                displaying = 1
                
            def current(self,event):
                print("Graph displaying current")
                l.set_ydata(a)
                ax.set_ylim(0, 1.5)
                for txt in fig.texts:
                    txt.set_visible(False)
                txt = fig.text(0.4,0.95,'Current vs Time',bbox=dict(facecolor='none', alpha=10,lw=0),fontsize = 15)
                yaxistxt = fig.text(0.05,0.6,'Current (Amperes)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')
                global displaying
                displaying = 2
                
            def power(self,event):
                print("Graph displaying power")
                l.set_ydata(p)
                ax.set_ylim(0, 10)
                for txt in fig.texts:
                    txt.set_visible(False)
                yaxistxt = fig.text(0.05,0.6,'Power (Watts)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')	
                txt = fig.text(0.4,0.95,' Power vs Time ',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15)	         
                global displaying
                displaying = 0
                
            def close(self,event): #Pressing the close button closes the graphing window
                plt.ioff()
                plt.close()
                
        callback = Index()
        
        #sizes of the buttons
        ax25 = plt.axes([0.01, 0.01, 0.12, 0.05])
        ax50 = plt.axes([0.14, 0.01, 0.12, 0.05])
        ax100 = plt.axes([0.27, 0.01, 0.12, 0.05])
        ax200 = plt.axes([0.4, 0.01, 0.12, 0.05])
        ax300 = plt.axes([0.53, 0.01, 0.12, 0.05])
        axclose = plt.axes([0.8, 0.01, 0.12, 0.05])	
        axvoltage = plt.axes([0.01, 0.08, 0.12, 0.05])
        axcurrent = plt.axes([0.14, 0.08, 0.12, 0.05])
        axpower = plt.axes([0.27, 0.08, 0.12, 0.05])
        
        #initialise the buttons
        bclose = Button(axclose, 'Close',color='green',hovercolor='#E97451') #hover colour: Burnt Sienna colour:
        bclose.on_clicked(callback.close)
        bvoltage = Button(axvoltage, 'Voltage',color='cyan',hovercolor='#E97451')
        bvoltage.on_clicked(callback.voltage)
        bcurrent = Button(axcurrent, 'Current',color='cyan',hovercolor='#E97451')
        bcurrent.on_clicked(callback.current)
        bpower = Button(axpower, 'Power',color='cyan',hovercolor='#E97451')
        bpower.on_clicked(callback.power)	
        b300 = Button(ax300, '300 Points',color='#EFDECD',hovercolor='#E97451')#color:almond
        b300.on_clicked(callback.three_hundred)
        b200 = Button(ax200, '200 Points',color='#EFDECD',hovercolor='#E97451')
        b200.on_clicked(callback.two_hundred)
        b100 = Button(ax100, '100 Points',color='#EFDECD',hovercolor='#E97451')
        b100.on_clicked(callback.one_hundred)
        b50 = Button(ax50, '50 Points',color='#EFDECD',hovercolor='#E97451')
        b50.on_clicked(callback.fifty)
        b25 = Button(ax25, '25 Points',color='#EFDECD',hovercolor='#E97451')
        b25.on_clicked(callback.twenty_five)
        
        plt.ion() #Call plt.ion() in order to enable interactive plotting
                
        while True:
            #Continously update the graph
            if displaying == 2:				
                l.set_ydata(a)
            elif displaying == 1:
                l.set_ydata(v)			
            elif displaying == 0:
                l.set_ydata(p)
                                    
            plt.pause(0.8) #Call plot.pause(0.8) to both draw the new data and run the GUI's event loop (allowing for mouse interaction)
    
    except:
        print("Graphing failed")
        pass
 
thread = threading.Thread(target=readData, args=(ser,))
thread2 = threading.Thread(target=handleData, args=(dataIn,))
thread3 = threading.Thread(target=realtimegraph, args=())
thread.start()
thread2.start()
thread3.start()



    
