
import matplotlib.pyplot as plt
import numpy as np
plt.axis([0, 10, 0, 1])
plt.ion() #Call plt.ion() in order to enable interactive plotting

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.05) #Call plt.pause(0.05) to both draw the new data and it runs the GUI's event loop (allowing for mouse interaction)

while True:
    plt.pause(0.05)