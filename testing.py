from rheed_analyzer import *

# image, frames = read_and_count("Ga988.AVI")
# print(frames)
# print(image)
# select_pixel()

time, intensity = integrate_video("Ga988.AVI")
intensity = intensity + np.random.random(len(intensity)) * 1
plot_oscillations(time, intensity)
# smoothed = smooth_data(intensity)
# plot_oscillations(time, smoothed)
# smoothed2 = smooth_data(smoothed)
# plot_oscillations(time, smoothed2)

# calculate_rate_fft(time, intensity)

FLOW: Sleect ROI, GUI smooth/select reduced region, get frequencies with calculate_rate_fft
