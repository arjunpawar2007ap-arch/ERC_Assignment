from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.signal import iirnotch

sample_rate, data = wavfile.read('/Users/arjunsagarpawar/Downloads/Signals_corrupted.wav')

print(f"Sample rate: {sample_rate} Hz")
print(f"Data shape: {data.shape}")
print(f"Data type: {data.dtype}")
print(f"Duration: {len(data) / sample_rate:.2f} seconds")

time = np.arange(len(data)) / sample_rate
plt.figure(figsize=(10, 4))
plt.plot(time, data)
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.title("Stage 1 - Time Domain")
plt.savefig("stage1_time_domain.png")
plt.show()

fft_vals = np.fft.fft(data)
fft_magnitude = np.abs(fft_vals)
frequencies = np.fft.fftfreq(len(data), d=1/sample_rate)


plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], fft_magnitude[:len(fft_magnitude)//2])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Stage 1 - FFT")
plt.savefig("stage1_fft.png")
plt.show()

t = np.arange(len(data)) / sample_rate
carrier = np.cos(2 * np.pi * 7300.1953 * t)

demodulated = data.astype(np.float64) * carrier

def lowpass_filter(signal, cutoff, fs, order=5):
    nyq = fs / 2
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low')
    return filtfilt(b, a, signal)

recovered = lowpass_filter(demodulated, 4000, sample_rate)

fft_vals2 = np.fft.fft(recovered)
fft_magnitude2 = np.abs(fft_vals2)

plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], fft_magnitude2[:len(fft_magnitude2)//2])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Stage 2 - FFT after demodulation")
plt.savefig("stage2_fft.png")
plt.show()

def notch_filter(signal, freq, fs, quality=30):
    b, a = iirnotch(freq, quality, fs)
    return filtfilt(b, a, signal)

def highpass_filter(signal, cutoff, fs, order=5):
    nyq = fs / 2
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high')
    return filtfilt(b, a, signal)

cleaned = highpass_filter(recovered, 80, sample_rate)
cleaned = notch_filter(cleaned, 1200.1, sample_rate)
cleaned = notch_filter(cleaned, 2199.9, sample_rate)
cleaned = notch_filter(cleaned, 4100.1, sample_rate)

fft_vals3 = np.fft.fft(cleaned)
fft_magnitude3 = np.abs(fft_vals3)

plt.figure(figsize=(10, 4))
plt.plot(frequencies[:len(frequencies)//2], fft_magnitude3[:len(fft_magnitude3)//2])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Stage 3 - FFT after notch filtering")
plt.xlim(0, 5000)
plt.savefig("stage3_fft.png")
plt.show()

final_normalized = np.int16(cleaned / np.max(np.abs(cleaned)) * 32767)
wavfile.write('/Users/arjunsagarpawar/Downloads/recovered.wav', sample_rate, final_normalized)

