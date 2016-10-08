"""
Graphing requires Matplotlib. Run the 2 statements below in cmd (Assuming Python has already been installed)
py -m pip install -U pip setuptools
py -m pip install matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button #import the button widget
import warnings
warnings.filterwarnings("ignore") 

try:
	x = 2
	
	#looping = True
	x_max = 20
	y_max = 25
	#plt.axis([0, x_max, 0, y_max])
	#plot.ion() #Call plt.ion() in order to enable interactive plotting
	#plt.grid(True)
	global displayingCurrent 
	global displayingVoltage 
	global displayingPower 
	
	displayingCurrent = False
	displayingVoltage = False
	displayingPower = True


	freqs = np.arange(2, 20, 3)
	fig, ax = plt.subplots()
	plt.subplots_adjust(bottom=0.2)
	plt.winter()
	#t = np.arange(0.0, 1.0, 0.001)
	t = list(range(300))
	#s = np.sin(2*np.pi*t)
	#p = np.array(t)**1.5
	p = np.sin(t)
	v = np.array(t)
	a = np.array(t)**2
	
	#l, = plt.plot(t, s, lw=2)
	l, = plt.plot(t, p, lw =3)
	ax.set_xlim(0, 26)
	

	class Index(object):
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
			
		def voltage(self,event):
			l.set_ydata(v)
			ax.set_ylim(0, 16)	
			displayingCurrent = False
			displayingVoltage = True
			displayingPower = False	
		def current(self,event):
			l.set_ydata(a)
			ax.set_ylim(0, 1.5)	
			displayingCurrent = True
			displayingVoltage = False
			displayingPower = False
		def power(self,event):
			l.set_ydata(p)
			ax.set_ylim(0, 10)	
			displayingCurrent = False
			displayingVoltage = False
			displayingPower = True
		def close(self,event):
			plt.ioff()
			plt.close()
						
			
		
	callback = Index()
	
	
	ax25 = plt.axes([0.01, 0.01, 0.12, 0.05])
	ax50 = plt.axes([0.14, 0.01, 0.12, 0.05])
	ax100 = plt.axes([0.27, 0.01, 0.12, 0.05])
	ax200 = plt.axes([0.4, 0.01, 0.12, 0.05])
	ax300 = plt.axes([0.53, 0.01, 0.12, 0.05])
	axclose = plt.axes([0.8, 0.01, 0.12, 0.05])
	
	axvoltage = plt.axes([0.01, 0.08, 0.12, 0.05])
	axcurrent = plt.axes([0.14, 0.08, 0.12, 0.05])
	axpower = plt.axes([0.27, 0.08, 0.12, 0.05])
	
	bclose = Button(axclose, 'Close')
	bclose.on_clicked(callback.close)
	bvoltage = Button(axvoltage, 'Voltage')
	bvoltage.on_clicked(callback.voltage)
	bcurrent = Button(axcurrent, 'Current')
	bcurrent.on_clicked(callback.current)
	bpower = Button(axpower, 'Power')
	bpower.on_clicked(callback.power)
	
	b300 = Button(ax300, '300 Points')
	b300.on_clicked(callback.three_hundred)
	b200 = Button(ax200, '200 Points')
	b200.on_clicked(callback.two_hundred)
	b100 = Button(ax100, '100 Points')
	b100.on_clicked(callback.one_hundred)
	b50 = Button(ax50, '50 Points')
	b50.on_clicked(callback.fifty)
	b25 = Button(ax25, '25 Points')
	b25.on_clicked(callback.twenty_five)

	
	plt.ion() #Call plt.ion() in order to enable interactive plotting
	
	
	
	k = 0
	while True:
		
		k+=1
		#if i==10:
			#s[150:300] = 0
		print(k)
		if displayingCurrent:
			l.set_ydata(a)
		elif displayingVoltage:
			l.set_ydata(v)
		elif displayingPower:
			l.set_ydata(p)
		plt.pause(0.05) #Call plot.pause(0.05) to both draw the new data and it runs the GUI's event loop (allowing for mouse interaction)
		#p[10:300] = 0
		#l.set_ydata(p[0:301])
		#l.set_xdata(t[0:301])
		#plt.draw()
	
except:
	pass
	#print("Graph Closed")	