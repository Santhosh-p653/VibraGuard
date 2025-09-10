import serial
import time
import csv
import os
import numpy as np
from collections import deque

# ── Serial configuration ───────────────────────────────
SERIAL_PORT = 'COM5'
BAUD_RATE = 9600

# ── File path setup ─────────────────────────────────────
data_path = r"C:\VibraGuard\data"
os.makedirs(data_path, exist_ok=True)
csv_file = os.path.join(data_path, 'data.csv')

# ── Ensure CSV header once ──────────────────────────────
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp',
            'motion_raw', 'motion_state',
            'vibration_raw', 'vibration_state',
            'status',
            'rawline',
            'motion_mean', 'motion_std', 'motion_3mean', 'motion_3std', 'motion_median', 'motion_domfreq',
            'vibration_mean', 'vibration_std', 'vibration_3mean', 'vibration_3std', 'vibration_median', 'vibration_domfreq',
            'svm_mean', 'svm_std'
        ])

# ── Buffer setup for computation ────────────────────────
BUFFER_SIZE = 100
motion_buffer = deque(maxlen=BUFFER_SIZE)
vibration_buffer = deque(maxlen=BUFFER_SIZE)
svm_buffer = deque(maxlen=BUFFER_SIZE)

def compute_stats(arr):
    mean = np.mean(arr)
    std = np.std(arr)
    median = np.median(arr)
    triple_mean = 3 * mean
    triple_std = 3 * std
    fft_vals = np.fft.fft(arr - np.mean(arr))
    freqs = np.fft.fftfreq(len(arr))
    dominant_freq = abs(freqs[np.argmax(np.abs(fft_vals[1:])) + 1])
    return mean, std, triple_mean, triple_std, median, dominant_freq

# ── Start serial read and log ───────────────────────────
try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)
        print("📡 Receiving data from Arduino...")

        with open(csv_file, 'a', newline='', encoding='utf-8') as cf:
            writer = csv.writer(cf)

            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue

                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"📥 Raw line: {line}")

                motion_raw, vibration_raw = 0, 0
                motion_state, vibration_state = "LOW", "LOW"
                status = "UNKNOWN"

                try:
                    parts = line.split("|")
                    if len(parts) == 2:
                        motion_raw = int(parts[0].split(":")[1].strip())
                        vibration_raw = int(parts[1].split(":")[1].strip())

                        motion_state = "HIGH" if motion_raw == 1 else "LOW"
                        vibration_state = "HIGH" if vibration_raw == 1 else "LOW"

                        # ── Updated Status Logic ─────────────────────
                        if motion_raw == -1 or vibration_raw == -1:
                            status = "SENSOR_FAIL"
                        elif motion_raw == 1 and vibration_raw == 1:
                            status = "SERIOUS"
                        elif motion_raw == 1 or vibration_raw == 1:
                            status = "ALERT"
                        elif motion_raw == 0 and vibration_raw == 0:
                            status = "NORMAL"
                        else:
                            status = "UNKNOWN"
                    else:
                        status = "FORMAT_ERROR"
                        print("⚠ Unexpected format, saved raw only")

                except Exception as e:
                    status = "PARSE_ERROR"
                    print(f"⚠ Parse error: {e}")

                # ── Update buffers ─────────────────────────────
                motion_buffer.append(motion_raw)
                vibration_buffer.append(vibration_raw)
                svm = np.sqrt(motion_raw**2 + vibration_raw**2)
                svm_buffer.append(svm)

                # ── Compute stats if buffer is full ────────────
                if len(motion_buffer) == BUFFER_SIZE:
                    m_arr = np.array(motion_buffer)
                    v_arr = np.array(vibration_buffer)
                    svm_arr = np.array(svm_buffer)

                    m_mean, m_std, m_3mean, m_3std, m_median, m_domfreq = compute_stats(m_arr)
                    v_mean, v_std, v_3mean, v_3std, v_median, v_domfreq = compute_stats(v_arr)
                    svm_mean = np.mean(svm_arr)
                    svm_std = np.std(svm_arr)
                else:
                    # Fill with placeholders until buffer fills
                    m_mean = m_std = m_3mean = m_3std = m_median = m_domfreq = ''
                    v_mean = v_std = v_3mean = v_3std = v_median = v_domfreq = ''
                    svm_mean = svm_std = ''

                # ── Log row ─────────────────────────────────────
                writer.writerow([
                    timestamp,
                    motion_raw, motion_state,
                    vibration_raw, vibration_state,
                    status,
                    line,
                    m_mean, m_std, m_3mean, m_3std, m_median, m_domfreq,
                    v_mean, v_std, v_3mean, v_3std, v_median, v_domfreq,
                    svm_mean, svm_std
                ])
                cf.flush()

                print(f"✅ Logged @ {timestamp} → Motion={motion_state}, Vibration={vibration_state}, Status={status}")

except serial.SerialException as e:
    print("❌ Serial error:", e)
except KeyboardInterrupt:
    print("🛑 Logging stopped by user.")