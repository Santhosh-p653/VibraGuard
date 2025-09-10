import pandas as pd
import matplotlib.pyplot as plt


# Load your data
df = pd.read_csv(r'C:\VibraGuard\data\data.csv')  # Use raw string for Windows path

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Min-Max normalization function
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# Normalize between 0 and 1
df['motion_norm'] = min_max_normalize(df['motion_raw'])
df['vibration_norm'] = min_max_normalize(df['vibration_raw'])

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['motion_norm'], label='Motion Sensor', color='dodgerblue', linewidth=2)
plt.plot(df['timestamp'], df['vibration_norm'], label='Vibration Sensor', color='orange', linewidth=2)

plt.xlabel('Timestamp')
plt.ylabel('Normalized Sensor Values')
plt.title('Motion and Vibration Sensor Data (Normalized 0–1) Over Time')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.ylim(-5, 5)  # Wide y-axis range
plt.tight_layout()
plt.show()