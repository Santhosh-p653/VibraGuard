import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import config

df = pd.read_excel(config.x)

print(df.head())
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')

plt.figure(figsize=(12, 6))
plt.plot(df['timestamp'], df['dominant_freq'])
plt.xlabel('Timestamp')
plt.ylabel('Dominant Frequency')
plt.title('Dominant Frequency Over Time')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gcf().autofmt_xdate()
plt.show()
