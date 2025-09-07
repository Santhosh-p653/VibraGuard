import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# --- Load and prepare data ---
file_path = '/content/drive/My Drive/Colab Notebooks/geophone.csv.xlsx'
df = pd.read_excel(file_path)

df['timestamp'] = pd.to_datetime('2000-01-01 ' + df['timestamp'].astype(str), errors='coerce')
df = df.dropna(subset=['timestamp'])
df = df.sort_values('timestamp')

# Normalize dominant_freq
df['normalized_freq'] = (df['dominant_freq'] - df['dominant_freq'].min()) / \
                        (df['dominant_freq'].max() - df['dominant_freq'].min()) * 10

# Threshold-based faults
lower_threshold = 2.5
upper_threshold = 5.5
df['fault'] = (df['normalized_freq'] < lower_threshold) | (df['normalized_freq'] > upper_threshold)

# --- Use only fault data for clustering ---
fault_df = df[df['fault']].copy()

# --- Apply K-Means ---
X = fault_df[['normalized_freq']]  # Feature for clustering, can add more
kmeans = KMeans(n_clusters=2, random_state=42)  # 2 clusters: low vs high faults
fault_df['cluster'] = kmeans.fit_predict(X)

# Map clusters to labels for visualization
cluster_colors = {0:'green', 1:'red'}
cluster_labels = {0:'Cluster 0', 1:'Cluster 1'}

# --- Plot ---
plt.figure(figsize=(12,6))
for cluster_id, group in fault_df.groupby('cluster'):
    plt.scatter(group['timestamp'], group['normalized_freq'], 
                color=cluster_colors[cluster_id], s=60, label=cluster_labels[cluster_id], marker='x')

plt.axhline(lower_threshold, color='black', linestyle='--', label="Lower Threshold")
plt.axhline(upper_threshold, color='black', linestyle='--', label="Upper Threshold")

plt.title("Unsupervised Clustering of Faults (K-Means)")
plt.xlabel("Timestamp")
plt.ylabel("Normalized Frequency (0–10)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
