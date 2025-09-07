import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Load and prepare data ---
file_path = '/content/drive/My Drive/Colab Notebooks/geophone.csv.xlsx'
df = pd.read_excel(file_path)

df['timestamp'] = pd.to_datetime('2000-01-01 ' + df['timestamp'].astype(str), errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp')

# Normalize dominant_freq
df['normalized_freq'] = (df['dominant_freq'] - df['dominant_freq'].min()) / \
                        (df['dominant_freq'].max() - df['dominant_freq'].min()) * 10

# Threshold-based faults
lower_threshold = 2.5
upper_threshold = 5.5
df['fault'] = (df['normalized_freq'] < lower_threshold) | (df['normalized_freq'] > upper_threshold)

# --- Focus only on faults ---
fault_df = df[df['fault']]

# Classify fault type
def classify_fault(row):
    if row['normalized_freq'] <= lower_threshold:
        return 'Machine Failure (Low)'
    elif row['normalized_freq'] >= upper_threshold:
        return 'Unusual Vibration / High'
    else:
        return 'Other Fault'

fault_df['fault_type'] = fault_df.apply(classify_fault, axis=1)

# --- Train Random Forest only on fault data ---
X_fault = fault_df[['normalized_freq']]  # Can add more features if available
y_fault = fault_df['fault_type']

# Encode fault_type as integers for classifier
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y_fault)

X_train, X_test, y_train, y_test = train_test_split(X_fault, y_encoded, test_size=0.2, random_state=42)
clf_fault = RandomForestClassifier(n_estimators=100, random_state=42)
clf_fault.fit(X_train, y_train)

# Predict fault types
fault_df['predicted_fault_type'] = le.inverse_transform(clf_fault.predict(X_fault))

# --- Plot fault points with classification ---
plt.figure(figsize=(12,6))

colors = {'Machine Failure (Low)':'green', 'Unusual Vibration / High':'red', 'Other Fault':'orange'}
for ftype, group in fault_df.groupby('predicted_fault_type'):
    plt.scatter(group['timestamp'], group['normalized_freq'],
                color=colors[ftype], s=60, label=ftype, marker='x')

plt.axhline(lower_threshold, color='black', linestyle='--', label="Lower Threshold")
plt.axhline(upper_threshold, color='black', linestyle='--', label="Upper Threshold")

plt.title("Classified Faults Based on Random Forest")
plt.xlabel("Timestamp")
plt.ylabel("Normalized Frequency (0–10)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
