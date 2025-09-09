import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

# --- Load and prepare data ---
file_path = r'c:\vibraguard\data\geophone-sensor-data.xlsx'
df = pd.read_excel(file_path)

df['timestamp'] = pd.to_datetime('2000-01-01 ' + df['timestamp'].astype(str), errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp')

# Normalize dominant_freq
df['normalized_freq'] = (df['dominant_freq'] - df['dominant_freq'].min()) / \
                        (df['dominant_freq'].max() - df['dominant_freq'].min()) * 10

# Threshold-based fault labels
lower_threshold = 2.5
upper_threshold = 5.5
df['fault'] = (df['normalized_freq'] < lower_threshold) | (df['normalized_freq'] > upper_threshold)

# --- Train Random Forest ---
X = df[['normalized_freq']]
y = df['fault'].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Predict faults for all data
df['predicted_fault'] = clf.predict(X)

# --- Confusion Matrix ---
cm = confusion_matrix(y_test, clf.predict(X_test))
print("Classification Report:\n")
print(classification_report(y_test, clf.predict(X_test)))

plt.figure(figsize=(12,6))

# --- Plot batch-wise data ---
batch_size = 100
colors = plt.cm.tab20.colors

for i, start in enumerate(range(0, len(df), batch_size)):
    end = start + batch_size
    batch = df.iloc[start:end]
    color = colors[i % len(colors)]
    plt.plot(batch['timestamp'], batch['normalized_freq'], color=color)

# Overlay predicted faults
predicted_fault_points = df[df['predicted_fault'] == 1]
plt.scatter(predicted_fault_points['timestamp'], predicted_fault_points['normalized_freq'],
            color='black', marker='x', s=60, label="Predicted Faults")

# Threshold lines
plt.axhline(lower_threshold, color='red', linestyle='--', label="Lower Threshold")
plt.axhline(upper_threshold, color='red', linestyle='--', label="Upper Threshold")

plt.title("Normalized Frequency with Random Forest Predicted Faults")
plt.xlabel("Timestamp")
plt.ylabel("Normalized Frequency (0–10)")
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Plot confusion matrix ---
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Normal','Fault'], yticklabels=['Normal','Fault'])
plt.title("Confusion Matrix for Random Forest Fault Prediction")
plt.ylabel("Actual")
plt.xlabel("Predicted")
plt.show()
