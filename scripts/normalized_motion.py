import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import config  

# Load dataset using y from config
df = pd.read_excel(config.y)

# Normalize the columns
scaler = MinMaxScaler()
normalized_values = scaler.fit_transform(df[['svm_mean', 'step_count']])

# Create a new DataFrame with normalized values
df_normalized = pd.DataFrame(
    normalized_values,
    columns=['svm_mean_norm', 'step_count_norm']
)

# Plot the normalized data
plt.figure(figsize=(8, 5))
plt.scatter(
    df_normalized['svm_mean_norm'],
    df_normalized['step_count_norm'],
    color='purple', alpha=0.6
)
plt.title('Normalized Motion Intensity vs Step Count')
plt.xlabel('Normalized SVM Mean')
plt.ylabel('Normalized Step Count')
plt.grid(True)
plt.tight_layout()
plt.show()