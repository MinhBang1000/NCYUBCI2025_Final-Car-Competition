import numpy as np
from pylsl import StreamInlet, resolve_stream
from scipy.signal import butter, filtfilt, welch
import time

# === 1. Bandpass filter ===
def bandpass_filter(data, fs, lowcut=8, highcut=13, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if not (0 < low < high < 1):
        raise ValueError(f"Invalid filter: low={low:.3f}, high={high:.3f}, fs={fs}")
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# === 2. PSD computation ===
def compute_psd(data, fs, nperseg=None):
    if nperseg is None:
        nperseg = fs
    freqs, psd = welch(data, fs, nperseg=nperseg)
    return freqs, psd

# === 3. Connect to EEG ===
print("🔍 Searching for EEG stream...")
streams = resolve_stream('type', 'EEG')
correct_stream = None
for i, stream in enumerate(streams):
    print(stream.name())
    if stream.name() == "Cygnus-081015-RawEEG":
        correct_stream = stream
print(correct_stream.name())
inlet = StreamInlet(correct_stream)
fs = 1000
n_channels = 14
print(f"✅ Connected to EEG @ {fs} Hz with {n_channels} channels")

# === 4. Monitor PSD in target band ===
def monitor_band_psd(channel_idx=0, band=(2, 4), window_sec=2.5):
    buffer = []
    samples_needed = int(window_sec * fs)
    print(f"📡 Monitoring PSD on channel {channel_idx}, band {band[0]}–{band[1]} Hz")

    while True:
        sample, _ = inlet.pull_sample(timeout=1.0)
        if sample:
            buffer.append(sample)
            if len(buffer) >= samples_needed:
                data = np.array(buffer)[-samples_needed:]
                signal = data[:, channel_idx]

                try:
                    filtered = bandpass_filter(signal, fs, band[0], band[1])
                    freqs, psd = compute_psd(filtered, fs)

                    # Extract power in band
                    band_power = np.mean([p for f, p in zip(freqs, psd) if band[0] <= f <= band[1]])
                    print(f"🔍 Band {band[0]}–{band[1]} Hz Power: {band_power:.4f} μV²/Hz")
                    time.sleep(1)
                except ValueError as e:
                    print(f"[⚠️ Filter Error] {e}")

                buffer = buffer[-samples_needed:]

# === 5. Run main ===
if __name__ == "__main__":
    try:
        monitor_band_psd(channel_idx=0, band=(2, 4), window_sec=2.5)
    except KeyboardInterrupt:
        print("\n🛑 Stopped monitoring.")
