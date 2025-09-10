from flask import Flask, Response
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# Load real sensor data
def load_real_data(csv_path=r"C:\VibraGuard\data\data.csv"):
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['motion_raw', 'vibration_raw'])  # Drop rows with missing values
    return df

# Extract features and labels
def extract_features_and_labels(df, window_size=10, step_size=5):
    motion = df['motion_raw']
    vibration = df['vibration_raw']
    motion_norm = (motion - motion.min()) / (motion.max() - motion.min())
    vibration_norm = (vibration - vibration.min()) / (vibration.max() - vibration.min())

    features, labels = [], []

    for start in range(0, len(df) - window_size, step_size):
        m = motion_norm[start:start + window_size].values
        v = vibration_norm[start:start + window_size].values
        feature = [np.mean(m), np.mean(v), np.std(m), np.std(v)]
        label = int((np.sum(m > 0.5) > 0) or (np.mean(v) > 0))
        features.append(feature)
        labels.append(label)

    return np.array(features), np.array(labels)

# Train classifier
def train_model():
    df = load_real_data()
    X, y = extract_features_and_labels(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    return clf, df

# Serve sensor line graph at root
@app.route("/")
def show_sensor_plot():
    _, df = train_model()
    motion = df['motion_raw']
    vibration = df['vibration_raw']
    motion_norm = (motion - motion.min()) / (motion.max() - motion.min())
    vibration_norm = (vibration - vibration.min()) / (vibration.max() - vibration.min())
    timestamps = np.arange(len(df))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(timestamps, motion_norm, label="Motion Sensor", color='blue')
    ax.plot(timestamps, vibration_norm, label="Vibration Sensor", color='orange')
    ax.set_title("Motion and Vibration Sensor Data (Normalized 0–1) Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Normalized Sensor Values")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return Response(buf.getvalue(), mimetype='image/png')

# Serve confusion matrix
@app.route("/confusion_matrix.png")
def stream_confusion_matrix():
    clf, df = train_model()
    X, y_true = extract_features_and_labels(df)
    y_pred = clf.predict(X)

    cm = confusion_matrix(y_true, y_pred, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Event", "Event"])

    fig, ax = plt.subplots()
    disp.plot(ax=ax, cmap='Blues', colorbar=False)
    ax.set_title("Normalized Confusion Matrix")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)