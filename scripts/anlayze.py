import pandas as pd
import matplotlib.pyplot as plt
file_path = '/content/drive/My Drive/Colab Notebooks/geophone.csv.xlsx'
df = pd.read_excel(file_path)
print(df.head())
# --- Ensure timestamp column is datetime ---
# Combine the time with a dummy date before converting to datetime
df['timestamp'] = pd.to_datetime('2000-01-01 ' + df['timestamp'].astype(str), errors='coerce')
df = df.dropna(subset=['timestamp']) # Drop rows where timestamp conversion failed
df = df.sort_values('timestamp')

# --- Define thresholds ---
lower_threshold = 250
upper_threshold = 550

# Flag unusual/fault points
df['fault'] = (df['dominant_freq'] < lower_threshold) | (df['dominant_freq'] > upper_threshold)

# --- Plot ---
plt.figure(figsize=(12,6))
plt.plot(df['timestamp'], df['dominant_freq'], label="Dominant Frequency", color="blue")

# Add threshold lines
plt.axhline(lower_threshold, color='red', linestyle='--', label="Lower Threshold")
plt.axhline(upper_threshold, color='red', linestyle='--', label="Upper Threshold")

# Highlight faults
fault_points = df[df['fault']]
plt.scatter(fault_points['timestamp'], fault_points['dominant_freq'],
            color='orange', marker='x', s=60, label="Fault / Unusual")

plt.title("Dominant Frequency with Threshold-based Fault Detection")
plt.xlabel("Timestamp")
plt.ylabel("Dominant Frequency (Hz)")
plt.legend()
plt.grid(True)
plt.show()
