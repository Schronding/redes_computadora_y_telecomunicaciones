import numpy as np
import matplotlib.pyplot as plt

sampling_rate = 16000  # Hz
duration = 1.0  # s
n_samples = int(sampling_rate * duration)
time_vector = np.linspace(0.0, duration, n_samples, endpoint=False)

freq_0 = 1000
freq_1 = 3000
signal = np.sin(2 * np.pi * freq_0 * time_vector) + 0.5 * np.sin(2 * np.pi * freq_1 * time_vector)

fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(n_samples, 1 / sampling_rate)

positive_mask = frequencies >= 0
positive_freqs = frequencies[positive_mask]
fft_magnitude = np.abs(fft_result[positive_mask])

plt.figure(figsize=(12, 6))
plt.plot(positive_freqs, fft_magnitude)
plt.title('El espectro de la frecuencia de la senial x(t)') 
plt.xlabel('Frecuenia en Hertz')
plt.ylabel('Magnitud')
plt.grid(True)
plt.xlim(0, 4000)
plt.show()