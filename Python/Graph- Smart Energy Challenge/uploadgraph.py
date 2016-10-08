import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

t = list(range(300))

s = np.array(t)**1.5

l, = plt.plot(t, s)

class Index(object):

	def one_hundred(self, event):
     		
		l.set_ydata(s[0:100])
		l.set_xdata(t[0:100])
		
		ax.xlim(0,100)
		ax.canvas.draw_idle()
		ax.xlim(0,50)
		plt.pause(0.0001)

	def fifty(self, event):
    		
		l.set_ydata(s[0:50])
		l.set_xdata(t[0:50])
		
		ax.xlim(0,50)
		ax.canvas.draw_idle()
		ax.xlim(0,50)
		plt.pause(0.0001)

callback = Index()

ax50 = plt.axes([0.6, 0.05, 0.12, 0.075])
ax100 = plt.axes([0.81, 0.05, 0.12, 0.075])
b100 = Button(ax100, '100 Points')
b100.on_clicked(callback.one_hundred)
b50 = Button(ax50, '50 Points')
b50.on_clicked(callback.fifty)

plt.ion()

while True:
	plt.pause(0.05) 
	
