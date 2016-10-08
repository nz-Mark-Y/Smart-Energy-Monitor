"""
Graphing requires Matplotlib. Run the 2 statements below in cmd (Assuming Python has already been installed)
py -m pip install -U pip setuptools
py -m pip install matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

x = 2
i = 0
#looping = True
x_max = 20
y_max = 25
#plt.axis([0, x_max, 0, y_max])
#plot.ion() #Call plt.ion() in order to enable interactive plotting
#plt.grid(True)



#freqs = np.arange(2, 20, 3)
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
#t = np.arange(0.0, 1.0, 0.001)
t = list(range(300))
#s = np.sin(2*np.pi*freqs[0]*t)
s = np.array(t)**1.5
#l, = plt.plot(t, s, lw=2)
l, = plt.plot(t, s)

#while (looping==True):

class Index(object):
	#ind = 0

	def one_hundred(self, event):
        
		
		#plt.axis([0, 100, 0, y_max])
		#l.set_xlim(top = 100)
		#l, = plt.plot(t[0:100], s[0:100])
		l.set_ydata(s[0:101])
		l.set_xdata(t[0:101])
		#plt.autoscale(enable=True, axis='both', tight=True)
		#plt.xlim(0, 100)
		#plt.draw()
		ax.set_xlim(0, 101)
		#l.canvas.draw_idle()
		plt.pause(0.0001)

	def fifty(self, event):
        
		#plt.axis([0, 50, 0, y_max])
		#l.set_xlim(top = 50)
		#l, = plt.plot(t[0:50], s[0:50])
		l.set_ydata(s[0:51])
		l.set_xdata(t[0:51])
		#plt.autoscale(enable=True, axis='both', tight=True)
		#plt.xlim(0, 50)
		#plt.draw()
		ax.set_xlim(0, 51)
		#l.canvas.draw_idle()
		plt.pause(0.0001)

callback = Index()
#ax50 = plt.axes([0.7, 0.05, 0.1, 0.075])
ax50 = plt.axes([0.6, 0.05, 0.15, 0.075])
ax100 = plt.axes([0.81, 0.05, 0.1, 0.075])
b100 = Button(ax100, '100 Points')
b100.on_clicked(callback.one_hundred)
b50 = Button(ax50, '50 Points')
b50.on_clicked(callback.fifty)

#plt.show()

plt.ion()


while True:
	graph1Value = x * 2
	graph2Value = x + 1
		
	#y = 5*np.random.random()
	#plt.scatter(i, graph1Value)
	#plt.draw()
	plt.pause(0.05) #Call plot.pause(0.05) to both draw the new data and it runs the GUI's event loop (allowing for mouse interaction)
	i+=1
	x_max += 1
	y_max +=1
	x += 1
	plt.axis([0, x_max, 0, y_max])
