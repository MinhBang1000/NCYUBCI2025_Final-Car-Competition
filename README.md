

---

# 🚗 EEG-Based Eye State Controlled Car

This project implements a brain-computer interface (BCI) system that uses EEG-based eye state detection (open vs. closed) to control a robot car. By analyzing alpha wave activity, the system generates control signals from the user's eye movements and maps them into directional commands.

## 🧠 How It Works

1. **EEG Signal Acquisition**
   The system connects to a 14-channel EEG device using the Lab Streaming Layer (LSL) protocol and collects 8 seconds of brainwave data per trial.

2. **Signal Processing**

   * Applies a bandpass filter (8–30 Hz) to isolate alpha-band frequencies.
   * Computes the alpha ratio (power in alpha band vs. total power) per channel.

3. **Eye State Detection**

   * Uses an ensemble approach: selects the 5 channels with the lowest alpha ratios.
   * If ≥3 of these 5 channels show low alpha → classified as **eyes open**; otherwise, **eyes closed**.

4. **Command Generation**

   * Performs two 8-second trials per cycle.
   * Each trial produces a binary bit: `0` for closed eyes, `1` for open eyes.
   * The combined 2-bit code (e.g., `10`, `01`) is interpreted as a movement command for the car.

5. **Control Loop**

   * A 3-second delay allows the user to change eye state between trials.
   * After generating the control code, the system waits 5 seconds before automatically starting the next cycle.

## 🧰 Folder Structure

```
📁 eeg_car_control/
│
├── main.py               # Main control loop
├── utils.py              # EEG streaming, filtering, alpha analysis, eye state logic
├── requirements.txt      # Python package dependencies
└── README.md             # This documentation
```

## 🛠️ Requirements

* Python 3.8+
* EEG device compatible with Lab Streaming Layer (LSL)
* Python packages:

  * `pylsl`
  * `numpy`
  * `scipy`
  * `matplotlib`

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## ▶️ How to Run

```bash
python main.py
```

### During Execution:

* Relax and either **close or open your eyes** during each 8-second trial.
* The system will generate a control code like `10`, `01`, etc.
* You can use this code to trigger actions on a robot car via serial or Bluetooth.

## 🎯 Example Output

```
📡 Starting 2 measurement phases (each 8 seconds)...

✅ Phase 1 → Eyes Closed (0)
1s
2s
3s
✅ Phase 2 → Eyes Open (1)

🧠 Control Code: 01 → Move Right

⏳ Preparing for next cycle, please wait 5s...
1s
2s
3s
4s
5s
```

## 🔮 Future Work

* Integrate serial or Bluetooth communication for real-time car control.
* Improve eye state accuracy using machine learning.
* Add SSVEP-based or blink-based commands for more control options.
* Visual feedback for alpha signal quality and live predictions.

---
