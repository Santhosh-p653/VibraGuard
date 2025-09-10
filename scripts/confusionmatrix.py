import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from imblearn.over_sampling import SMOTE


df = pd.read_csv(r'C:\VibraGuard\data\data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Normalize raw sensor values
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

df['motion_norm'] = min_max_normalize(df['motion_raw'])
df['vibration_norm'] = min_max_normalize(df['vibration_raw'])

# Sliding window parameters
window_size = 10
step_size = 5

features = []
labels = []
timestamps = []

# Sliding window computation
for start in range(0, len(df) - window_size, step_size):
    window = df.iloc[start:start + window_size]
    motion_series = window['motion_norm'].values
    vibration_series = window['vibration_norm'].values

    # Feature extraction
    motion_mean = np.mean(motion_series)
    vibration_mean = np.mean(vibration_series)
    motion_std = np.std(motion_series)
    vibration_std = np.std(vibration_series)

    # Modified Labeling Logic: Label as 'Alert' if any motion_norm > 0.5 OR if vibration_mean > 0
    label = int((np.sum(motion_series > 0.5) > 0) or (vibration_mean > 0))


    features.append([motion_mean, vibration_mean, motion_std, vibration_std])
    labels.append(label)
    timestamps.append(window['timestamp'].iloc[-1])  # end of window

# Convert to DataFrame
X = pd.DataFrame(features, columns=['motion_mean', 'vibration_mean', 'motion_std', 'vibration_std'])
y = np.array(labels)

# Train-test split
# Use stratify to ensure both classes are present in train and test sets if possible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y if len(np.unique(y)) > 1 else None)

# Apply SMOTE to the training data to handle class imbalance
if len(np.unique(y_train)) > 1:
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print(f"Shape of training data before SMOTE: {X_train.shape}")
    print(f"Shape of training data after SMOTE: {X_train_resampled.shape}")
else:
    X_train_resampled, y_train_resampled = X_train, y_train
    print("SMOTE not applied: Only one class present in training data.")


# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_resampled, y_train_resampled) # Train on resampled data
y_pred = clf.predict(X_test)

# Confusion matrix (normalized)
# Check if both classes are present in y_test and y_pred before plotting
unique_labels = np.unique(np.concatenate((y_test, y_pred)))
if len(unique_labels) > 1:
    cm = confusion_matrix(y_test, y_pred, normalize='true', labels=[0, 1]) # Explicitly define labels
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal', 'Alert'])
    disp.plot(cmap='Blues')
    plt.title("Normalized Confusion Matrix - Random Forest")
    plt.show()
else:
    print("Cannot plot confusion matrix: Only one class present in test set or predictions.")
    # You could optionally print a simplified report here if needed

# Classification report
# Check if both classes are present in y_test and y_pred before generating report
if len(unique_labels) > 1:
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Alert']))
else:
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred)) # Use default labels if only one class


# Plot normalized sensor data
plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['motion_norm'], label='Motion Sensor', color='dodgerblue', linewidth=2)
plt.plot(df['timestamp'], df['vibration_norm'], label='Vibration Sensor', color='orange', linewidth=2)
plt.xlabel('Timestamp')
plt.ylabel('Normalized Sensor Values')
plt.title('Motion and Vibration Sensor Data (Normalized 0–1)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.ylim(-5, 5)  # Wide y-axis range
plt.tight_layout()
plt.show()