import pandas as pd
import matplotlib.pyplot as plt
import config

df = pd.read_excel(config.x)

# --- Ensure timestamp column is datetime ---
df['timestamp'] = pd.to_datetime('2000-01-01 ' + df['timestamp'].astype(str), errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp')

# --- Normalize dominant_freq between 0–10 ---
def normalize_column(series):
    min_val = series.min()
    max_val = series.max()
    return (series - min_val) / (max_val - min_val) * 10

df['normalized_freq'] = normalize_column(df['dominant_freq'])

# --- Define thresholds ---
lower_threshold = 2.5
upper_threshold = 5.5

# --- Flag unusual/fault points ---
df['fault'] = (df['normalized_freq'] < lower_threshold) | (df['normalized_freq'] > upper_threshold)

# --- Plotting ---
plt.figure(figsize=(12,6))

batch_size = 100
colors = plt.cm.tab20.colors  # 20 distinct colors from matplotlib

for i, start in enumerate(range(0, len(df), batch_size)):
    end = start + batch_size
    batch = df.iloc[start:end]
    color = colors[i % len(colors)]  # cycle through colors if more than 20 batches
    
    plt.plot(batch['timestamp'], batch['normalized_freq'], color=color, label=f"Batch {start}-{end}")

# Threshold lines
plt.axhline(lower_threshold, color='red', linestyle='--', label="Lower Threshold")
plt.axhline(upper_threshold, color='red', linestyle='--', label="Upper Threshold")

# Highlight faults
fault_points = df[df['fault']]
plt.scatter(fault_points['timestamp'], fault_points['normalized_freq'],
            color='orange', marker='x', s=60, label="Fault / Unusual")

plt.title("Normalized Dominant Frequency with Batch-wise Coloring")
plt.xlabel("Timestamp")
plt.ylabel("Normalized Frequency (0–10)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # move legend outside
plt.grid(True)
plt.tight_layout()
plt.show()
