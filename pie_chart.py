import matplotlib.pyplot as plt
import matplotlib
import platform
import os

# Set font that supports Chinese characters
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Microsoft YaHei'  # or 'SimHei'
else:
    plt.rcParams['font.family'] = 'Noto Sans CJK SC'

# Team member names mapped to IDs
members = {
    '413540003': '桃公信',
    '413540004': '潘阮明草',
    '313540015': '黎明朋',
    '412551012': '王士銘',
    '313551132': '何承遠'
}

# Flat-friendly color palette
base_colors = ['#f28e8e', '#8ecae6', '#a3d9a5', '#fcd5b4', '#cdb4db']

# Updated contributions
tasks = {
    "LSL Real-Time Data Streaming": [75, 5, 10, 5, 5],
    "Alpha Wave Preprocessing (Bandpass + Filter)": [10, 75, 5, 5, 5],
    "Alpha Ratio & Ensemble Strategy": [5, 5, 75, 10, 5],
    "EEG Control Practice": [25, 15, 35, 15, 10],
    "Report writing": [20, 20, 30, 20, 5]
}

# Create output folder
if not os.path.exists('images'):
    os.makedirs('images')

# Plot each pie chart with bigger text and save with dpi=300
for task, contributions in tasks.items():
    filtered_data = [
        (f"{id} ({members[id]})", contrib, color)
        for (id, contrib, color) in zip(members.keys(), contributions, base_colors)
        if contrib > 0
    ]

    labels = [label for label, _, _ in filtered_data]
    values = [value for _, value, _ in filtered_data]
    colors = [color for _, _, color in filtered_data]

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        colors=colors,
        autopct='%1.0f%%',
        startangle=90,
        shadow=False,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )

    # Set font size of percentage texts
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
        autotext.set_color('black')

    ax.set_title(task, fontsize=18, fontweight='bold')
    ax.axis('equal')
    plt.tight_layout()

    # Save the plot with dpi=300
    image_filename = f"images/{task.replace(' ', '_').replace('(', '').replace(')', '')}.png"
    plt.savefig(image_filename, dpi=300)
    plt.close()  # Close the plot to avoid displaying

# Unified legend chart with larger fonts
fig = plt.figure(figsize=(5, 2))
legend_labels = [f"{id} ({name})" for id, name in members.items()]
handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black') for color in base_colors]

fig.legend(
    handles,
    legend_labels,
    title="Team Members",
    loc='center',
    fontsize=14,
    title_fontsize=16
)
plt.axis('off')
plt.tight_layout()

# Save the legend image with dpi=300
legend_filename = "images/team_members_legend.png"
plt.savefig(legend_filename, dpi=300)
plt.close()  # Close the legend plot to avoid displaying
