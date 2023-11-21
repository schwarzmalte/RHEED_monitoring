import numpy as np
import matplotlib.pyplot as plt

# Generate a sample signal
t = np.linspace(0, 1, 1000)
frequency = 5  # Frequency of the oscillation
signal = np.sin(2 * np.pi * frequency * t)

# Compute the FFT
fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(t))

# Plot the frequency spectrum
plt.plot(frequencies, np.abs(fft_result))
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title('Frequency Spectrum')
plt.show()