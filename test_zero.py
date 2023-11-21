from rheed_analyzer import *


# Generate a sample signal
t = np.linspace(0, 5, 1000)
frequency = 3  # Frequency of the oscillation
signal = np.sin(2 * np.pi * frequency * t)+0.8*np.sin(2 * np.pi * frequency*2 * t)
signal = signal + np.random.random(len(signal))*0.3
# signal = smooth_data(signal)
# signal = smooth_data(signal)

#calculate_rate_zeropoint(t,signal)

calculate_rate_fft(t,signal)

plt.plot(t,signal)
plt.show()