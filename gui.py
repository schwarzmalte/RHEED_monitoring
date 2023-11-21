import tkinter as tk
from tkinter import filedialog, messagebox
from rheed_analyzer import *

class RHEED_measurement:
    video_path = ""
    time = []
    intensity = []
    fig_osc, ax_osc = plt.subplots()
    fig_freq, ax_freq = plt.subplots()
    freq = []
    freq_amplitude = []
    time_roi = []
    intensity_roi = []
    fig_roi, ax_roi = plt.subplots()
    manual_start = 0
    manual_end = 0.1
    manual_rate = 10000

def integrate_button_action():
    messagebox.showinfo("Message from Code","Select a ROI and then press SPACE or ENTER button! Cancel the selection process by pressing c button!")
    measurement.time, measurement.intensity = integrate_video(measurement.video_path)
    messagebox.showinfo("Message from Code","The video is successfully integrated!")
    # Define the action for the first button
    pass

def smooth_button_action():
    measurement.intensity = smooth_data(measurement.intensity)
    plot_oscillations_button_action()

def close_all_fig():
    plt.close(measurement.fig_freq)
    plt.close(measurement.fig_osc)
    plt.close(measurement.fig_roi)

def reininitalize_figure_osc():
    plt.close(measurement.fig_osc)
    measurement.fig_osc, measurement.ax_osc = plt.subplots()

def reininitalize_figure_osc_roi():
    plt.close(measurement.fig_roi)
    measurement.fig_roi, measurement.ax_rpo = plt.subplots()

def plot_oscillations_button_action():
    reininitalize_figure_osc()
    plt.plot(measurement.time,measurement.intensity)
    plt.show(block=False)

def plot_oscillations_roi_button_action():
    reininitalize_figure_osc_roi()
    plt.plot(measurement.time_roi,measurement.intensity_roi)
    plt.show(block=False)

def select_ROI_button_action():
    reininitalize_figure_osc()
    # measurement.ax.set_title('Select the ROI where you expect the oscillations.')
    plt.plot(measurement.time,measurement.intensity)
    def onselect(xmin, xmax):
        plt.close()
        print(f"Selected span: x = [{xmin}, {xmax}]")
        #modify the data range based on selected ROI
        measurement.intensity_roi = measurement.intensity[(xmin<measurement.time) & (measurement.time<xmax)]
        measurement.time_roi = measurement.time[(xmin<measurement.time) & (measurement.time<xmax)]
        plot_oscillations_roi_button_action()

    # Create the SpanSelector widget
    span = SpanSelector(measurement.ax_osc, onselect, 'horizontal', useblit=True, props=dict(alpha=0.5, facecolor='red'))
    plt.show()

def fft_button_action():
    # Compute the FFT
    fft_result = np.fft.fft(measurement.intensity_roi)
    frequencies = np.fft.fftfreq(len(measurement.time_roi))/(measurement.time_roi[1]-measurement.time_roi[0])
    #now only positive frequencies
    filtered_frequencies = frequencies[frequencies>0]
    filtered_fft_result = fft_result[frequencies>0]
    #get the dominant frequency
    max_index = np.argmax(np.abs(filtered_fft_result))
    rate = filtered_frequencies[max_index]
    messagebox.showinfo("The dominant freuqency is: ", str(rate)+" ML/s")
    #save into object
    measurement.freq = filtered_frequencies
    measurement.freq_amplitude = np.abs(filtered_fft_result)
    messagebox.showinfo("Message from Code","You can plot the results now.")

def reininitalize_figure_freq():
    plt.close(measurement.fig_freq)
    measurement.fig_freq, measurement.ax_freq = plt.subplots()

def fft_plot_button_action():
    reininitalize_figure_freq()
    plt.plot(measurement.freq,measurement.freq_amplitude)
    plt.show(block=False)


def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        #filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    if file_path:
        messagebox.showinfo("Message from Code", "You have selected the file: "+file_path)
        measurement.video_path = file_path


def manual_select_button_action():
    reininitalize_figure_osc()
    # measurement.ax.set_title('Select the ROI where you expect the oscillations.')
    measurement.ax_osc.plot(measurement.time,measurement.intensity)
    def update(val):
    # Update the plot based on the RangeSlider values
        #plt.plot(measurement.time,measurement.intensity)
        measurement.ax_osc.cla()
        measurement.ax_osc.plot(measurement.time,measurement.intensity)
        current_values = slider.val
        # print("Current values:", current_values)
        vlines = measurement.ax_osc.vlines([current_values[0], current_values[1]],[np.min(measurement.intensity),np.min(measurement.intensity)],[np.max(measurement.intensity),np.max(measurement.intensity)],colors=['r','g'])
        #vlines.set_segments([current_values[0], current_values[1]])
        measurement.manual_start = current_values[0]
        measurement.manual_end = current_values[1]
        print(measurement.manual_start,measurement.manual_end)

    # Create the SpanSelector widget
    slider_ax = plt.axes([0.1, 0.01, 0.65, 0.03])
    slider = RangeSlider(slider_ax, 'Range', measurement.time[0],measurement.time[-1])
    slider.on_changed(update)  # Call the update function when the slider value changes
    plt.show()


root = tk.Tk()
root.title("RHEED Oscillations Video Analyzer")
root.geometry("1200x100")

measurement = RHEED_measurement()
close_all_fig()


select_button = tk.Button(root, text="Select File", command=select_file)
select_button.pack(pady=20)

integrate_button = tk.Button(root, text="Integrate Video", command=integrate_button_action)
integrate_button.pack(side=tk.LEFT)

plot_oscillations_button = tk.Button(root, text="Plot Oscialltions", command=plot_oscillations_button_action)
plot_oscillations_button.pack(side=tk.LEFT)

smooth_button = tk.Button(root, text="Smooth", command=smooth_button_action)
smooth_button.pack(side=tk.LEFT)

select_ROI_button = tk.Button(root, text="Select ROI", command=select_ROI_button_action)
select_ROI_button.pack(side=tk.LEFT)

plot_oscillations_roi = tk.Button(root, text="Plot ROI", command=plot_oscillations_roi_button_action)
plot_oscillations_roi.pack(side=tk.LEFT)

fft_button = tk.Button(root, text="Perfrom FT", command=fft_button_action)
fft_button.pack(side=tk.LEFT)

fft_plot_button = tk.Button(root, text="Plot FFT", command=fft_plot_button_action)
fft_plot_button.pack(side=tk.LEFT)

manual_select_button = tk.Button(root, text="Select Manually", command=manual_select_button_action)
manual_select_button.pack(side=tk.LEFT)

def print_input():
    input_period = input_field.get()
    periods = int(input_period)
    print(str(periods))
    measurement.manual_rate = np.round(periods / (measurement.manual_end-measurement.manual_start),3)
    print(measurement.manual_rate)
    output_entry.delete(0, tk.END)  # Clear the output Entry widget
    output_entry.insert(0, str(measurement.manual_rate)+" ML/s")  # Set the content of the output Entry widget

input_field = tk.Entry(root)
input_field.pack(side=tk.LEFT)

submit_button = tk.Button(root, text="<-Period|Rate->", command=print_input)
submit_button.pack(side=tk.LEFT)

output_entry = tk.Entry(root)  # Create an output Entry widget
output_entry.pack(side=tk.LEFT)


root.mainloop()