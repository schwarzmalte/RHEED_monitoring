import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector, TextBox, RangeSlider

def read_and_count(video_file):
    # Open the video file
    cap = cv2.VideoCapture(video_file)
    # read the frist frame
    success, image = cap.read()
    # export the first frame into image
    cv2.imwrite("frame%d.jpg" % 0, image)
    # get the total number of frames
    total_frames = get_total_frames(cap)
    # release video
    cap.release()
    return image, total_frames

def get_total_frames(cap):
    return int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

def select_pixel(picture='frame0.jpg'):
    # # Load the image
    # image = cv2.imread(picture)

    # # Function to display the coordinates of the points clicked on the image
    # def click_event(event, x, y, flags, param):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         print(x, y)  # Display the coordinates

    # # Display the image
    # cv2.imshow('Image', image)

    # # Set the mouse callback function
    # cv2.setMouseCallback('Image', click_event)

    # # Wait for a key press and then close the window
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Read the image
    image = cv2.imread(picture)
    # Select a ROI
    # [Top_Left_X, Top_Left_Y, Width, Height]
    r = cv2.selectROI("Select a ROI and then press SPACE or ENTER button! Cancel the selection process by pressing c button!", image, fromCenter=False)

    # Print the selected ROI
    print(r)

    # Crop the selected ROI
    roi_cropped = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # Display the cropped ROI
    # cv2.imshow("Cropped ROI", roi_cropped)
    # cv2.waitKey(0)
    return r

def integrate_video(video):
    image, frames = read_and_count(video)
    #initialize empty arrays to be filled
    time = np.zeros(frames)
    oscillations = np.zeros(frames)
    #launch the pixel selection process as region of interest roi, short r
    r = select_pixel()

    # Open the video file
    cap = cv2.VideoCapture(video)

    # Read frame by frame
    success, image = cap.read()
    count = 0
    while success:
        # crop image
        roi_cropped = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        # integrate all pixel 
        integrated_intensity = np.sum(roi_cropped)
        # get the timestamp of the frame in seconds
        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
        # print intermediate results
        #print(timestamp,integrated_intensity)
        #write both into arrays 
        time[count] = timestamp
        oscillations[count] = integrated_intensity
        #move on to next image
        count += 1
        success, image = cap.read()

    # Release the VideoCapture
    cap.release()
    return time, oscillations

def plot_oscillations(time, intensity):
    fig, ax = plt.subplots()
    ax.set_title('Select the ROI where you expect the oscillations.')
    plt.plot(time, intensity)
    def onselect(xmin, xmax):
        print(f"Selected span: x = [{xmin}, {xmax}]")
        plt.close()

    # Create the SpanSelector widget
    span = SpanSelector(ax, onselect, 'horizontal', useblit=True, props=dict(alpha=0.5, facecolor='red'))
    plt.show()
    return

def smooth_data(y, box_pts=5):
    #smooth
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def run(time, intensity):
    
    fig, ax = plt.subplots()
    ax.set_title('Select ROI')
    plt.plot(time,intensity)

    # # Define the callback function for the SpanSelector
    # def onselect(xmin, xmax):
    #     print(f"Selected span: x = [{xmin}, {xmax}]")

    # # Create the SpanSelector widget
    # span = SpanSelector(ax, onselect, 'horizontal', useblit=True, props=dict(alpha=0.5, facecolor='red'))
    initial_text = "t ** 2"
    l, = plt.plot(time, intensity, lw=2)
    # Define the submit function for the TextBox
    def submit(text):
        ydata = eval(text)
        l.set_ydata(ydata)
        ax.set_ylim(np.min(ydata), np.max(ydata))
        plt.draw()

    # Create the TextBox widget
    axbox = plt.axes([0.1, 0.05, 0.3, 0.075])
    text_box = TextBox(axbox, 'Number of oscillations:', initial=initial_text)
    text_box.on_submit(submit)

    plt.show()
    
    # # Define the onclick event function
    # def onclick(event):
    #     if event.button == 1:  # Check if left mouse button is clicked
    #         plt.plot(time,intensity)
    #         plt.vlines(vline_start,0,np.max(intensity))
    #         plt.vlines(vline_end,0,np.max(intensity))
    #         plt.draw()  # Redraw the plot

    # # Create a plot and connect the onclick event
    # fig, ax = plt.subplots()
    # ax.set_title('Click to add points')
    # fig.canvas.mpl_connect('button_press_event', onclick)
    # plt.show()

    # # initial positions of vlines
    # vline_start = time[0]
    # vline_end = time[-1]

    
    return

def calculate_rate_zeropoint(time, intensity):
    deriv = np.diff(intensity)
    # Get the sign of each element
    signs = np.sign(deriv)

    # Identify the indices where sign changes occur
    sign_changes = np.where(np.diff(signs) != 0)[0] + 1

    #print(sign_changes)

    # the number of periods for the seleccted time frame is calculated by the half the number of the maxima. 2.00001 is used to make it float and force integer round downards
    periods = int(len(sign_changes)/2.00001)+1

    #print(periods)

    #calculate the rate
    rate = periods/(time[-1]-time[0])

    print(rate)
    return rate

def calculate_rate_fft(time, intensity):
    # Compute the FFT
    fft_result = np.fft.fft(intensity)
    frequencies = np.fft.fftfreq(len(time))/(time[1]-time[0])
    #now only positive frequencies
    filtered_frequencies = frequencies[frequencies>0]
    filtered_fft_result = fft_result[frequencies>0]
    #get the dominant frequency
    max_index = np.argmax(np.abs(filtered_fft_result))
    rate = filtered_frequencies[max_index]
    print(rate)
    # Plot the frequency spectrum
    plt.plot(filtered_frequencies, np.abs(filtered_fft_result))
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.title('Frequency Spectrum')
    plt.show()
    return rate 