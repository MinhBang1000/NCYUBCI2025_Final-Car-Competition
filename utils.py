from scipy.signal import welch
import numpy as np
from scipy.signal import butter, filtfilt
from pylsl import StreamInlet, resolve_stream
import time

def compute_alpha_ratio(signal, fs, alpha_range=(8, 13), total_range=(3, 30)):
    freqs, psd = welch(signal, fs=fs, nperseg=fs)

    alpha_mask = (freqs >= alpha_range[0]) & (freqs <= alpha_range[1])
    total_mask = (freqs >= total_range[0]) & (freqs <= total_range[1])

    alpha_power = np.sum(psd[alpha_mask])
    total_power = np.sum(psd[total_mask])

    alpha_ratio = alpha_power / total_power if total_power > 0 else 0

    if alpha_ratio > 0.3:
        conclusion = "✅ Strong alpha waves detected (possibly eyes closed or relaxed)"
    else:
        conclusion = "❌ Weak alpha (possibly eyes open or focused)"

    return {
        "alpha_power": alpha_power,
        "total_power": total_power,
        "alpha_ratio": alpha_ratio,
        "conclusion": conclusion
    }

def is_eye_open(alpha_ratios, threshold=0.5, vote_method='majority'):
    binary_votes = [1 if r < threshold else 0 for r in alpha_ratios]  # 1 = open
    if vote_method == 'or':
        return any(binary_votes)
    elif vote_method == 'majority':
        return sum(binary_votes) >= (len(alpha_ratios) // 2 + 1)
    elif vote_method == 'weighted':
        weights = [0.134, 0.073, 0.033, 0.0001, 0.0001]  # Δalpha from top-5
        score = sum(w if r < threshold else 0 for r, w in zip(alpha_ratios, weights))
        return score > 0.1

def connect_eeg_stream(expected_channels=14):
    print("🔍 Searching for EEG stream...")
    streams = resolve_stream('type', 'EEG')
    correct_stream = None
    for i, stream in enumerate(streams):
        print(stream.name())
        if stream.name() == "Cygnus-081015-RawEEG":
            correct_stream = stream
    print(correct_stream.name())
    inlet = StreamInlet(correct_stream)
    info = inlet.info()
    fs = int(info.nominal_srate())
    print(f"✅ Connected to EEG @ {fs} Hz with {info.channel_count()} channels")
    if info.channel_count() < expected_channels:
        raise ValueError("❌ Device does not provide enough required channels!")
    return inlet, fs

def collect_eeg_data(inlet, fs, duration, n_channels):
    print(f"⏳ Collecting {duration} seconds of EEG data...")
    samples = []
    for _ in range(fs * duration):
        sample, _ = inlet.pull_sample()
        samples.append(sample[:n_channels])
    raw = np.array(samples).T
    print("✅ Data collection complete!")
    return raw

def bandpass_filter(data, fs, lowcut=8, highcut=30, order=4):
    b, a = butter(order, [lowcut / (0.5 * fs), highcut / (0.5 * fs)], btype='band')
    return filtfilt(b, a, data)

def apply_bandpass(data, fs):
    filtered = np.zeros_like(data)
    for i in range(data.shape[0]):
        filtered[i] = bandpass_filter(data[i], fs)
    return filtered

def analyze_alpha_ratios(filtered_data, fs):
    print("\n🔎 Alpha wave assessment per channel:")
    alpha_ratios = []
    for i in range(filtered_data.shape[0]):
        result = compute_alpha_ratio(filtered_data[i], fs)
        alpha_ratios.append(result["alpha_ratio"])
        print(f"Channel {i+1:>2}: alpha_ratio = {result['alpha_ratio']:.3f} → {result['conclusion']}")
    return alpha_ratios

def ensemble_open_eye_detection(alpha_ratios, top_k=5, threshold=0.5):
    top_indices = np.argsort(alpha_ratios)[:top_k]
    top_alpha = [alpha_ratios[i] for i in top_indices]
    votes = [1 if val < threshold else 0 for val in top_alpha]

    print(f"\n📊 Top {top_k} alpha_ratios (lowest): {[f'{a:.3f}' for a in top_alpha]}")
    print(f"🗳️ Voting result: {votes} → Total open-eye votes = {sum(votes)}")

    if sum(votes) >= (top_k // 2 + 1):
        print("\n🧠 Final Decision: You are likely **EYES OPEN** (weak alpha)")
        return "open"
    else:
        print("\n🧠 Final Decision: You are likely **EYES CLOSED** (strong alpha)")
        return "closed"

# Define control function
def control_car(control_code, ser):
    mapping = {
        '00': b'0',  # Stop
        '01': b'3',  # Left
        '10': b'4',  # Right
        '11': b'1'   # Forward
    }

    degree = {
        '00': 0.5,
        '01': (0.2 * 90) / 32.5,
        '10': (0.2 * 90) / 35,
        '11': 0.5
    }

    command = mapping.get(control_code, b'0')  # Default to stop if unknown
    ser.write(command)
    time.sleep(degree.get(control_code,0.5))
    ser.write(b'0')
    print(f"🚗 Sent to car: {command.decode()} for code {control_code}")


