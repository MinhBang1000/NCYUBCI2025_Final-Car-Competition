from utils import (
    connect_eeg_stream,
    collect_eeg_data,
    apply_bandpass,
    analyze_alpha_ratios,
    ensemble_open_eye_detection
)
import time

# ==== CONFIGURATION ====
DURATION = 8
N_CHANNELS = 14

# ==== CONNECT TO EEG ====
inlet, fs = connect_eeg_stream(expected_channels=N_CHANNELS)

def run_trial():
    raw_data = collect_eeg_data(inlet, fs, DURATION, N_CHANNELS)
    filtered_data = apply_bandpass(raw_data, fs)
    alpha_ratios = analyze_alpha_ratios(filtered_data, fs)
    state = ensemble_open_eye_detection(alpha_ratios)
    return 0 if state == "closed" else 1

# ==== MAIN LOOP ====
print("🚀 System started. Press Ctrl+C to exit.\n")

try:
    while True:
        print("📡 Starting 2 measurement phases (each 8 seconds)...\n")
        
        result_1 = run_trial()
        print(f"✅ Phase 1 → {'Eyes Closed (0)' if result_1 == 0 else 'Eyes Open (1)'}\n")

        for i in range(1, 4):
            print(f"{i}s")
            time.sleep(1)

        result_2 = run_trial()
        print(f"✅ Phase 2 → {'Eyes Closed (0)' if result_2 == 0 else 'Eyes Open (1)'}\n")

        control_code = f"{result_1}{result_2}"
        print(f"🧠 Control Code: {control_code}\n")

        # Create the serial then send the control to the car here

        print("Waiting for the next command, please wait 5s...")
        for i in range(1, 5):
            print(f"{i}s")
            time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 System stopped.")
