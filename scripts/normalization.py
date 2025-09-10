import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay

# Load your data

df = pd.read_csv(r'C:\VibraGuard\data\data.csv')

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter rows:
# Keep rows that are either:
# 1. Fully complete (no NaNs)
# 2. OR have status == 'alert' (even if they have NaNs)
df_filtered = df[df.notna().all(axis=1) | (df['status'] == 'alert')]

# Min-Max normalization
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df_filtered['motion_norm'] = min_max_normalize(df_filtered['motion_raw'])
df_filtered['vibration_norm'] = min_max_normalize(df_filtered['vibration_raw'])

# Simulate binary labels (replace with actual labels if available)
df_filtered['label'] = (df_filtered['motion_norm'] > 0.5).astype(int)

# Features and target
X = df_filtered[['motion_norm', 'vibration_norm']]
y = df_filtered['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Confusion Matrix
ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)
plt.title("Confusion Matrix - Random Forest")
plt.show()

# Plot normalized sensor data with wide y-axis
plt.figure(figsize=(12, 6))
plt.plot(df_filtered['timestamp'], df_filtered['motion_norm'], label='Motion Sensor', color='dodgerblue', linewidth=2)
plt.plot(df_filtered['timestamp'], df_filtered['vibration_norm'], label='Vibration Sensor', color='orange', linewidth=2)

plt.xlabel('Timestamp')
plt.ylabel('Normalized Sensor Values')
plt.title('Motion and Vibration Sensor Data (Normalized 0–1)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.ylim(-5, 5)  # Wide y-axis range
plt.tight_layout()
plt.show()