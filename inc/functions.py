import pandas as pd
import numpy as np
import os
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt

def moving_average(signal, window_size):
    return pd.Series(signal).rolling(window=window_size, center=True, min_periods=1).mean().to_numpy()

def fill_nan_with_local_mean(series, window=5):
    filled = series.copy()
    for i in range(len(series)):
        if pd.isna(series[i]):
            left = series[max(0, i - window):i]
            right = series[i + 1:i + 1 + window]
            neighbors = pd.concat([left, right]).dropna()
            if not neighbors.empty:
                filled[i] = neighbors.mean()
    return filled

def process_file (filepath, output_dir):
    try:
        df = pd.read_csv(filepath, sep='\\t', header=1, engine='python')
    except pd.errors.EmptyDataError:
        print(f"Skipped empty file: {filepath}")
        return
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return
    
    df = pd.read_csv(filepath, sep='\\t', header=1, engine='python')
    signal = df["CH4(ppm)"].values
    time = df["time(s)"].values
    fs = 1 / (time[1] - time[0])

    # Filter signal using Butterworth
    lowcut = 0.01
    highcut = 0.15
    fs = 1 / (time[1] - time[0])
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(N=4, Wn=[low, high], btype='band')
    signal_filtered = filtfilt(b, a, signal)

    # Smooth filtered signal
    window = len(signal) // 50
    signal_smoothed = moving_average(signal_filtered, window_size=window)

    # Detect peaks
    peak_indices, _ = find_peaks(signal_smoothed, distance=30, prominence=0.5)
    df["ValidPeak"] = False
    df.loc[peak_indices, "ValidPeak"] = True

    # Manual correction based on peak height
    signal_corrected_manual = signal.copy()
    for i in range(len(peak_indices) - 1):
        start = peak_indices[i] - window
        end = len(signal)
        signal_corrected_manual[start:end] = moving_average(signal_corrected_manual[start:end], window_size=window) - signal[peak_indices[i]] + signal[peak_indices[i] - window]

    # Post-processing smoothing
    manual_smoothed = moving_average(signal_corrected_manual, len(signal) // 50)
    manual_smoothed = fill_nan_with_local_mean(pd.Series(manual_smoothed))
    manual_smoothed = moving_average(manual_smoothed, len(manual_smoothed) // 25)
    manual_smoothed = fill_nan_with_local_mean(pd.Series(manual_smoothed))
    manual_smoothed = moving_average(manual_smoothed, len(manual_smoothed) // 50)
    manual_smoothed = fill_nan_with_local_mean(pd.Series(manual_smoothed))
    manual_smoothed = moving_average(manual_smoothed, len(manual_smoothed) // 100)
    manual_smoothed = fill_nan_with_local_mean(pd.Series(manual_smoothed))
    manual_smoothed[:window] = moving_average(signal[:window], 2)

    # Automatic correction approach
    signal_corrected_auto = signal.copy()
    for i in range(len(peak_indices) - 1):
        start = peak_indices[i] - window
        end = len(signal)
        signal_corrected_auto[start:end] = moving_average(signal_corrected_auto[start:end], window_size=window) - signal[peak_indices[i]] + signal[peak_indices[i] - window]

    auto_smoothed = (signal + signal_corrected_auto) / 2
    auto_smoothed = fill_nan_with_local_mean(pd.Series(auto_smoothed))
    auto_smoothed = moving_average(auto_smoothed, len(auto_smoothed) // 25)

    # Combine both results
    final_signal = (manual_smoothed + auto_smoothed) / 2
    df["CH4_final (ppm)"] = final_signal

    # Preparar paths
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    data_output_dir = os.path.join(output_dir, "data")
    os.makedirs(data_output_dir, exist_ok=True)
    output_csv = os.path.join(data_output_dir, base_name + "_processed.csv")
    plot_dir = os.path.join(output_dir, "plots")
    peaks_dir = os.path.join(output_dir, "peak_plots")
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(peaks_dir, exist_ok=True)

    # Guardar gráfico comparativo final
    plt.figure(figsize=(10, 5))
    plt.plot(time, signal, label="CH4 original", alpha=0.5)
    plt.plot(time, final_signal, label="CH4 final", alpha=0.5)
    plt.xlabel("Tiempo (s)")
    plt.ylabel("CH4 (ppm)")
    plt.title("Correction based on previous peak value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plot_path = os.path.join(plot_dir, base_name + "_final_comparison.png")
    plt.savefig(plot_path)
    plt.close()

   # Guardar gráfico de picos detectados
    # Crear señal escalonada con valores de pico
    step_signal = np.zeros_like(signal)
    peak_indices = df[df['ValidPeak']].index.to_list()
    peak_values = df.loc[peak_indices, "CH4(ppm)"].values

    for i in range(len(peak_indices) - 1):
        start = peak_indices[i]
        end = peak_indices[i + 1]
        step_signal[start:end] = peak_values[i]

    # Rellenar desde el último pico al final (si hay alguno)
    if len(peak_indices) > 0:
        step_signal[peak_indices[-1]:] = peak_values[-1]
        
    plt.figure(figsize=(10, 5))
    plt.plot(time, step_signal, label="Step-like peak response", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("CH4 (ppm)")
    plt.title("Analog-like response of valid peaks")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(peaks_dir, base_name + "_peak_steps.png"))
    plt.close()

    # Guardar CSV
    cols_to_drop = ["CH4_corr", "CH4_filtered", "ValidPeak"]
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"Processed and saved: {output_csv}")