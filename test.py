import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import SpanSelector, TextBox, RangeSlider



def update(val):
    ax.cla()
    ax.plot(t,signal)
    current_values = slider.val
        # print("Current values:", current_values)
    lc = ax.vlines(current_values[0],0,1)
    lc.set_segments(current_values[0])
    #plt.show()
    #ax.vlines(current_values[1],0,1)

t = np.linspace(0, 5, 1000)
frequency = 3  # Frequency of the oscillation
signal = np.sin(2 * np.pi * frequency * t)+0.8*np.sin(2 * np.pi * frequency*2 * t)
signal = signal + np.random.random(len(signal))*0.3

fig, ax = plt.subplots()

ax.plot(t,signal)

# Create the SpanSelector widget
slider_ax = plt.axes([0.1, 0.01, 0.65, 0.03])
slider = RangeSlider(slider_ax, 'Range',t[0],t[-1])
slider.on_changed(update)  # Call the update function when the slider value changes
plt.show()