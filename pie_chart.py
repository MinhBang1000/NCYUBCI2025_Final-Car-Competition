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

# Original flat-friendly color palette (for max 5 members)
base_colors = ['#f28e8e', '#8ecae6', '#a3d9a5', '#fcd5b4', '#cdb4db']

# Task contributions
tasks = {
    "LSL Real-Time Data Streaming": [75, 5, 10, 5, 5],
    "Alpha Wave Preprocessing (Bandpass + Filter)": [10, 75, 5, 5, 5],
    "Alpha Ratio & Ensemble Strategy": [5, 5, 75, 10, 5],
    "EEG Control Practice": [25, 15, 35, 15, 10],
    "Report writing": [20, 20, 40, 20, 0]
}

# Create an 'images' folder if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Plot each pie chart WITHOUT individual legends
for task, contributions in tasks.items():
    # Filter out members with 0% contribution
    filtered_data = [
        (f"{id} ({members[id]})", contrib, color)
        for (id, contrib, color) in zip(members.keys(), contributions, base_colors)
        if contrib > 0
    ]
    
    # Unpack filtered data
    labels = [label for label, _, _ in filtered_data]
    values = [value for _, value, _ in filtered_data]
    colors = [color for _, _, color in filtered_data]

    # Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=None,
        colors=colors,
        autopct='%1.0f%%',
        startangle=90,
        shadow=False,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1}
    )
    plt.title(task, fontsize=13, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()

    # Save the plot
    image_filename = f"images/{task.replace(' ', '_').replace('(', '').replace(')', '')}.png"
    plt.savefig(image_filename)
    plt.show()

# Create a separate figure for the unified legend only
fig = plt.figure(figsize=(5, 2))
legend_labels = [f"{id} ({name})" for id, name in members.items()]
handles = [plt.Rectangle((0, 0), 1, 1, color=color, edgecolor='black') for color in base_colors]

fig.legend(
    handles,
    legend_labels,
    title="Team Members",
    loc='center',
    fontsize=10,
    title_fontsize=12
)
plt.axis('off')
plt.tight_layout()

# Save the legend image
legend_filename = "images/team_members_legend.png"
plt.savefig(legend_filename)
plt.show()
