import matplotlib.pyplot as plt
import matplotlib
import platform

# Set font that supports Chinese characters
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Microsoft YaHei'  # or 'SimHei'
else:
    plt.rcParams['font.family'] = 'Noto Sans CJK SC'  # for Linux/macOS if installed

# Team member names mapped to IDs
members = {
    '413540003': '桃公信',
    '413540004': '潘阮明草',
    '313540015': '黎明朋',
    '412551012': '王士銘',
    '313551132': '何承遠'
}

colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

tasks = {
    "LSL Real-Time Data Streaming": [75, 5, 10, 5, 5],
    "Alpha Wave Preprocessing (Bandpass + Filter)": [10, 75, 5, 5, 5],
    "Alpha Ratio & Ensemble Strategy": [5, 5, 75, 10, 5],
    "EEG Control Practice": [25, 15, 35, 15, 10],
    "Report writing": [20, 20, 40, 20, 0]
}

# Plot
for task, contributions in tasks.items():
    plt.figure(figsize=(6, 6))
    plt.pie(
        contributions,
        labels=None,
        colors=colors,
        autopct='%1.0f%%',
        startangle=90
    )
    plt.title(task, fontsize=12)
    plt.legend(
        labels=[f"{id} ({name})" for id, name in members.items()],
        title="Team Members",
        loc='best'
    )
    plt.tight_layout()
    plt.show()
