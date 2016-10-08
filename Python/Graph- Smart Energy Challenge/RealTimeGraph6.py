"""
Graphing requires Matplotlib. Run the 2 statements below in cmd (Assuming Python has already been installed)
py -m pip install -U pip setuptools
py -m pip install matplotlib
"""

import matplotlib.pyplot as plt #import the matplotlib library
import numpy as np				#import the numpy extension
from matplotlib.widgets import Button #import the button widget
import warnings
warnings.filterwarnings("ignore") 

try:	
	fig, ax = plt.subplots()	#Create a figure with a set of subplots already made
	plt.subplots_adjust(bottom=0.2) #Adjust the distance from the bottom of the graph to the bottom of the window
		
	ax.patch.set_facecolor('#89CFF0') #set background colour of plot to baby blue
	
	plt.grid(True)
	t = list(range(300))	#x-axis data points
	
	p = np.sin(t) #represents power array
	v = np.array(t)	#represents voltage array
	a = np.array(t)**2 #represents current array
		
	l, = plt.plot(t, p, lw =3)	#plots a line on the axes with a linewidth of 3
	
	#The initial graph on startup will be a Power vs Time graph
	displayingCurrent = False	#These 3 status variables indicate whether power, voltage or current data is being displayed
	displayingVoltage = False	#and are used by the program when updating the graph to ensure that the correct 
	displayingPower = True		#dataset is being drawn
	
	ax.set_xlim(0, 26)			#The x and y limits for the Power vs Time graph is set
	ax.set_ylim(0, 10)
	txt = fig.text(0.4,0.95,' Power vs Time ',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15)	#title of graph
	yaxistxt = fig.text(0.05,0.6,'Power (Watts)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')	#y axis label of graph	
	plt.xlabel('Data Points', fontsize = 15)	#x-axis label of graph
	
	

	class Index(object):
		#The 5 below functions are used to adjust the x-axis limits depending on the button that is pressed
		def three_hundred(self, event):			
			ax.set_xlim(0, 301)
		def two_hundred(self, event):			
			ax.set_xlim(0, 201)
		def one_hundred(self, event):			
			ax.set_xlim(0, 101)
		def fifty(self, event):			
			ax.set_xlim(0, 51)
		def twenty_five(self, event):			
			ax.set_xlim(0, 26)
		
		#The 3 below functions are used to switch between power, voltage or current graphs depending on which button is pressed
		def voltage(self,event):
			l.set_ydata(v)	#sets the plot to display the voltage dataset
			ax.set_ylim(0, 16)	#sets the y-axis limits to the appropriate size for the voltage dataset
			
			for txt in fig.texts: #Makes previously drawn text boxes disappear
				txt.set_visible(False)
			txt = fig.text(0.4,0.95,'Voltage vs Time',bbox=dict(facecolor='none', alpha=10,lw=0),fontsize = 15)
			yaxistxt = fig.text(0.05,0.6,'Voltage (Volts)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')
			
			global displayingCurrent	#sets the status variables to indicate to the program that it should now be plotting voltage data 
			global displayingVoltage 
			global displayingPower 
			displayingCurrent = False
			displayingVoltage = True
			displayingPower = False
		def current(self,event):
			l.set_ydata(a)
			ax.set_ylim(0, 1.5)
			for txt in fig.texts:
				txt.set_visible(False)
			txt = fig.text(0.4,0.95,'Current vs Time',bbox=dict(facecolor='none', alpha=10,lw=0),fontsize = 15)
			yaxistxt = fig.text(0.05,0.6,'Current (Amperes)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')
			global displayingCurrent 
			global displayingVoltage 
			global displayingPower 
			displayingCurrent = True
			displayingVoltage = False
			displayingPower = False
			
		def power(self,event):
			l.set_ydata(p)
			ax.set_ylim(0, 10)
			for txt in fig.texts:
				txt.set_visible(False)
			yaxistxt = fig.text(0.05,0.6,'Power (Watts)',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15,rotation = 'vertical')	
			txt = fig.text(0.4,0.95,' Power vs Time ',bbox=dict(facecolor='none', alpha=10,lw = 0),fontsize = 15)	
			
			global displayingCurrent 
			global displayingVoltage 
			global displayingPower 
			displayingCurrent = False
			displayingVoltage = False
			displayingPower = True
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
		if displayingCurrent:				
			l.set_ydata(a)			
		elif displayingVoltage:
			l.set_ydata(v)			
		elif displayingPower:
			l.set_ydata(p)
					
		plt.pause(0.8) #Call plot.pause(0.8) to both draw the new data and run the GUI's event loop (allowing for mouse interaction)
	
except:
	pass
	