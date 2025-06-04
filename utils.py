from scipy.signal import welch
import numpy as np
from scipy.signal import butter, filtfilt
from pylsl import StreamInlet, resolve_stream

def compute_alpha_ratio(signal, fs, alpha_range=(8, 13), total_range=(3, 30)):
    # Tính phổ bằng Welch
    freqs, psd = welch(signal, fs=fs, nperseg=fs)

    # Tạo mask cho từng dải tần
    alpha_mask = (freqs >= alpha_range[0]) & (freqs <= alpha_range[1])
    total_mask = (freqs >= total_range[0]) & (freqs <= total_range[1])

    # Tính tổng năng lượng
    alpha_power = np.sum(psd[alpha_mask])
    total_power = np.sum(psd[total_mask])

    # Tính tỉ lệ alpha
    alpha_ratio = alpha_power / total_power if total_power > 0 else 0

    # Kết luận
    if alpha_ratio > 0.3:
        conclusion = "✅ Có sóng alpha mạnh (có thể nhắm mắt hoặc thư giãn)"
    else:
        conclusion = "❌ Alpha yếu (có thể mở mắt hoặc đang chú ý)"

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
        weights = [0.134, 0.073, 0.033, 0.0001, 0.0001]  # Δalpha từ top-5
        score = sum(w if r < threshold else 0 for r, w in zip(alpha_ratios, weights))
        return score > 0.1  # tùy bạn chỉnh ngưỡng

def connect_eeg_stream(expected_channels=14):
    print("🔍 Đang tìm EEG stream...")
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    info = inlet.info()
    fs = int(info.nominal_srate())
    print(f"✅ Đã kết nối EEG @ {fs} Hz với {info.channel_count()} kênh")
    if info.channel_count() < expected_channels:
        raise ValueError("❌ Thiết bị không đủ kênh yêu cầu!")
    return inlet, fs


def collect_eeg_data(inlet, fs, duration, n_channels):
    print(f"⏳ Đang thu {duration} giây dữ liệu EEG...")
    samples = []
    for _ in range(fs * duration):
        sample, _ = inlet.pull_sample()
        samples.append(sample[:n_channels])
    raw = np.array(samples).T
    print("✅ Thu xong dữ liệu!")
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
    print("\n🔎 Đánh giá sóng Alpha từng kênh:")
    alpha_ratios = []
    for i in range(filtered_data.shape[0]):
        result = compute_alpha_ratio(filtered_data[i], fs)
        alpha_ratios.append(result["alpha_ratio"])
        print(f"Kênh {i+1:>2}: alpha_ratio = {result['alpha_ratio']:.3f} → {result['conclusion']}")
    return alpha_ratios


def ensemble_open_eye_detection(alpha_ratios, top_k=5, threshold=0.5):
    top_indices = np.argsort(alpha_ratios)[:top_k]
    top_alpha = [alpha_ratios[i] for i in top_indices]
    votes = [1 if val < threshold else 0 for val in top_alpha]

    print(f"\n📊 Top {top_k} alpha_ratio (thấp nhất): {[f'{a:.3f}' for a in top_alpha]}")
    print(f"🗳️ Voting result: {votes} → Tổng phiếu mở mắt = {sum(votes)}")

    if sum(votes) >= (top_k // 2 + 1):
        print("\n🧠 Kết luận cuối cùng: Bạn có thể đang **MỞ MẮT** (alpha yếu)")
        return "open"
    else:
        print("\n🧠 Kết luận cuối cùng: Bạn có thể đang **NHẮM MẮT** (alpha mạnh)")
        return "closed"
