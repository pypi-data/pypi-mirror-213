import time as _time
import numpy as np
from AMTIUSBDeviceWrapper import AMTIUSBDevice as amti
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import atexit as _atexit

matplotlib.use('TKAgg')

def onExit():
    global a
    a.broadcastStop()
    plt.close()

_atexit.register(onExit)

amti.AMTIUSBDevice.InitializeLibrary(dll_path="./tests/bin/AMTIUSBDevice - 64.dll")
a = amti.AMTIUSBDevice(platform="gen5", auto_save=False)
LC = 1

# Matplot lib live plot info
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

a.init()
a.broadcastAcquisitionRate(rate=500) # A data sample every 2ms
a.broadcastStart()

col = 8*(LC-1) + 3 # column for LC Forces in Z
samples = 0

def animate(i, xs, ys):
    global samples, col

    # get Data from devices
    data, samp_num = a.getData(opt=1)
    if(samp_num == 0):
        return
    data = np.round(data, 4)

    data_z = data[:,col]

    # Add x and y to lists
    xs.append(samples)
    ys.append(np.average(data_z))

    samples += 1

    # # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('AMTI LC1')
    plt.ylabel('Force in Z (N)')

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=20) # updates every 10ms
plt.show()

a.broadcastStop()