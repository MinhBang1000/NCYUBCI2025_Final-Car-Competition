from utils import (
    connect_eeg_stream,
    collect_eeg_data,
    apply_bandpass,
    analyze_alpha_ratios,
    ensemble_open_eye_detection,
    control_car,
    ensemble_vote_4ch
)
import time
from serial import Serial
import winsound

# ==== CONFIGURATION ====
DURATION = 8
N_CHANNELS = 14

# ==== CONNECT TO EEG ====
inlet, fs = connect_eeg_stream(expected_channels=N_CHANNELS)

def run_trial():
    raw_data = collect_eeg_data(inlet, fs, DURATION, N_CHANNELS)
    filtered_data = apply_bandpass(raw_data, fs)
    alpha_ratios = analyze_alpha_ratios(filtered_data, fs, channel_indices=[0, 1, 4, 5])
    state = ensemble_vote_4ch(alpha_ratios, 0.5)
    return 0 if state == "closed" else 1

# ==== MAIN LOOP ====
print("🚀 System started. Press Ctrl+C to exit.\n")

ser = Serial("COM4", 9600, timeout=1, write_timeout=1)

try:
    while True:
        print("📡 Starting 2 measurement phases (each 8 seconds)...\n")
        
        result_1 = run_trial()
        print(f"✅ Phase 1 → {'Eyes Closed (0)' if result_1 == 0 else 'Eyes Open (1)'}\n")

        print("Waiting for the next command, please wait 2s...")
        winsound.Beep(1000, 300)
        time.sleep(2)

        result_2 = run_trial()
        print(f"✅ Phase 2 → {'Eyes Closed (0)' if result_2 == 0 else 'Eyes Open (1)'}\n")

        control_code = f"{result_1}{result_2}"
        print(f"🧠 Control Code: {control_code}\n")
        control_car(control_code, ser)  # <<-- Send to car

        # Create the serial then send the control to the car here

        print("Waiting for the next command, please wait 2s (Finish Cycle)...")
        winsound.Beep(400, 700)
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 System stopped.")
