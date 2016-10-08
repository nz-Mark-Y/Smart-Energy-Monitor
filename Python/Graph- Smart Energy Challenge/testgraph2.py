import matplotlib.pyplot as plt
import numpy as np
import itertools

fig = plt.figure()
ax = fig.add_subplot(111)
y1 = np.random.rand(10)
y2 = np.random.rand(10)
ys = itertools.cycle((y1,y2))
line, = ax.plot(next(ys))

def onclick(event):
    line.set_ydata(next(ys))
    fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()