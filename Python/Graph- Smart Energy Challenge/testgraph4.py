import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
sin_l, = ax.plot(np.sin(0))
cos_l, = ax.plot(np.cos(0))
ax.set_ylim(-1, 1)
ax.set_xlim(0, 5)
dx = 0.1

def update(i):
    # i is a counter for each frame.
    # We'll increment x by dx each frame.
    x = np.arange(0, i) * dx
    sin_l.set_data(x, np.sin(x))
    cos_l.set_data(x, np.cos(x))
    return sin_l, cos_l

ani = animation.FuncAnimation(fig, update, frames=51, interval=50)
plt.show()