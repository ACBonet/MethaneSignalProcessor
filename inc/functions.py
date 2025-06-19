import pandas as pd
import numpy as np
import os
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt
from scipy.stats import linregress
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

def plot_signal_with_slopes_and_r2(x, y, valid_peaks, window=10):
    x = np.array(x)
    y = np.array(y)
    segments = []

    if len(valid_peaks) == 0:
        segments = [(0, len(x) - 1)]
    else:
        if valid_peaks[0] > window:
            segments.append((0, valid_peaks[0] - window))

        for i in range(len(valid_peaks) - 1):
            start = valid_peaks[i] + window
            end = valid_peaks[i + 1] - window
            if end > start:
                segments.append((start, end))

        if valid_peaks[-1] + window < len(x) - 1:
            segments.append((valid_peaks[-1] + window, len(x) - 1))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, label="Original signal", color="blue", alpha=0.6)

    for i, (start, end) in enumerate(segments):
        x_seg = x[start:end]
        y_seg = y[start:end]
        if len(x_seg) < 2:
            continue
        slope, intercept, r_value, _, _ = linregress(x_seg, y_seg)
        y_fit = slope * x_seg + intercept

        if r_value**2 > 0.7:
            plt.plot(x_seg, y_fit, color='red', linewidth=2, label='Fitted slope' if i == 0 else "")
            mid_x = (x_seg[0] + x_seg[-1]) / 2
            mid_y = (slope * mid_x + intercept) + 0.02 * (max(y) - min(y))  # small offset above the line
            plt.text(mid_x, mid_y, f"Slope: {slope:.2f}\n$r^2$: {r_value**2:.2f}",
                     fontsize=8, color='darkred', ha='center', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CH₄ Concentration (ppm)")
    ax.set_title("Slopes & $r^2$ of Signal Segments")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

def get_describe(dataframe, valid_peaks, window):
    total_adjusted_concentration = 0
    time_of_bubbles = 0

    for peak in valid_peaks:
        start = max(peak - window, 0)
        end = min(peak + window, len(dataframe) - 1)

        baseline = dataframe.loc[start, 'CH4(ppm)']
        peak_max = dataframe.loc[start:end, 'CH4(ppm)'].max()

        adjusted_concentration = peak_max - baseline
        if adjusted_concentration > 0:
            total_adjusted_concentration += adjusted_concentration

        # Calcular duración del evento en segundos
        t_start = dataframe.loc[start, 'time(s)']
        t_end = dataframe.loc[end, 'time(s)']
        time_of_bubbles += max(t_end - t_start, 0)

    n_bubbles = len(valid_peaks)
    time_of_bubbles_h = time_of_bubbles / 3600
    bubbles_per_hour = n_bubbles / time_of_bubbles_h if time_of_bubbles_h > 0 else 0

    # Valor final de CH₄
    total_concentration = dataframe['CH4(ppm)'].max()
    percent_bubbling = (total_adjusted_concentration / total_concentration) * 100 if total_concentration > 0 else 0

    return {
        "Peak Analysis Interval": window*2,
        "Total Adjusted CH₄ Concentration (ppm)": round(total_adjusted_concentration, 2),
        "Final CH₄ Concentration (ppm)": round(total_concentration, 2),
        "Contribution of boiling to the total (%)": round(percent_bubbling, 2),
        "Number of Bubbles": n_bubbles,
        "Index of Bubbles": valid_peaks.tolist(),
        "Total Bubble Time (h)": round(time_of_bubbles_h, 3),
        "Bubbles per Hour": round(bubbles_per_hour, 2)
    }

def print_summary(stats_dict):
    df_summary = pd.DataFrame.from_dict(stats_dict, orient='index', columns=["Value"])
    df_summary.index.name = "Metric"
    pd.options.display.float_format = '{:,.2f}'.format  # Formato con dos decimales
    # print("\n--- Summary of Ebullitive Events ---\n")
    # print(df_summary)
    
def ppm_per_s_to_umol_per_m2h(pressure_mmHg, concentration_ppm_per_s, volume_m3, temperature_C, area_m2):
    R = 8.314  # J/(mol·K)
    T_K = temperature_C + 273.15
    P_Pa = pressure_mmHg * 133.322
    mol_total = (P_Pa * volume_m3) / (R * T_K)
    mol_per_s = (concentration_ppm_per_s / 1e6) * mol_total
    umol_per_m2h = (mol_per_s * 1e6 * 3600) / area_m2
    return umol_per_m2h

def calculate_slopes_and_difusive_flux(
    x, y, valid_peaks, temperatures_C, pressures_mmHg, 
    volume_m3, area_m2, window=10, only_positive=True, return_series=False
):
    x = np.array(x)
    y = np.array(y)
    temperatures_C = np.array(temperatures_C)
    pressures_mmHg = np.array(pressures_mmHg)

    slopes = []
    umol_fluxes = []
    flux_lines = []

    segments = []

    if len(valid_peaks) == 0:
        # No peaks, use entire signal as one segment
        segments = [(0, len(x) - 1)]
    else:
        if valid_peaks[0] > window:
            segments.append((0, valid_peaks[0] - window))
        for i in range(len(valid_peaks) - 1):
            start = valid_peaks[i] + window
            end = valid_peaks[i + 1] - window
            if end > start:
                segments.append((start, end))
        if valid_peaks[-1] + window < len(x) - 1:
            segments.append((valid_peaks[-1] + window, len(x) - 1))

    # print(f"Valid segments with R² > 0.7{' & slope > 0' if only_positive else ''}:")

    for start, end in segments:
        x_seg = x[start:end]
        y_seg = y[start:end]
        temp_seg = temperatures_C[start:end]
        pres_seg = pressures_mmHg[start:end]

        if len(x_seg) < 2:
            continue

        slope, intercept, r_value, _, _ = linregress(x_seg, y_seg)

        if r_value**2 > 0.7 and (slope > 0 if only_positive else True):
            avg_temp = np.mean(temp_seg)
            avg_pres = np.mean(pres_seg)
            flux = ppm_per_s_to_umol_per_m2h(avg_pres, slope, volume_m3, avg_temp, area_m2)

            line = f"- Slope: {slope:.4f} ppm/s | r²: {r_value**2:.3f} | T: {avg_temp:.1f}°C | P: {avg_pres:.1f} mmHg | Diffusive Flux: {flux:.2f} µmol/m²·h"
            # print(line)

            slopes.append(slope)
            umol_fluxes.append(flux)
            flux_lines.append(line)

    if not umol_fluxes:
        # print("No valid segments were found.")
        if return_series:
            return flux_lines, pd.Series(dtype=float)
        else:
            return None

    flux_series = pd.Series(umol_fluxes)
    # print("\nSummary Statistics of Diffusive Fluxes (µmol/m²·h):")
    # print(flux_series.describe().round(2))
    if return_series:
        return flux_lines, flux_series

def process_file (filepath, output_dir, window_peaks=5):
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
    all_peaks, _ = find_peaks(signal_smoothed)
    all_peak_values = signal_smoothed[all_peaks]

    # Theshold calculation
    mean_val = np.mean(all_peak_values)
    std_val = np.std(all_peak_values)
    threshold = mean_val + std_val / 3

    # Peak prominence evaluation
    peaks_above_threshold = [i for i in all_peaks if signal_smoothed[i] > threshold]

    # Calculate minimum distance between peaks
    if len(peaks_above_threshold) > 1:
        intervals = np.diff(peaks_above_threshold)
        mean_distance = np.mean(intervals)
        std_distance = np.std(intervals)
        min_distance = int(mean_distance - std_distance)
        if min_distance < 1:
            min_distance = 1
    else:
        min_distance = 1 

    # Detect valid peaks based on threshold and minimum distance
    valid_peaks, _ = find_peaks(signal_smoothed, height=threshold, distance=min_distance)

    # Create variable to store valid peaks in the DataFrame
    df["ValidPeak"] = False
    df.loc[valid_peaks, "ValidPeak"] = True

    # Manual correction based on peak height
    signal_corrected_manual = signal.copy()
    for i in range(len(valid_peaks) - 1):
        start = valid_peaks[i] - window
        end = len(signal)
        signal_corrected_manual[start:end] = moving_average(signal_corrected_manual[start:end], window_size=window) - signal[valid_peaks[i]] + signal[valid_peaks[i] - window]

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
    for i in range(len(valid_peaks) - 1):
        start = valid_peaks[i] - window
        end = len(signal)
        signal_corrected_auto[start:end] = moving_average(signal_corrected_auto[start:end], window_size=window) - signal[valid_peaks[i]] + signal[valid_peaks[i] - window]

    auto_smoothed = (signal + signal_corrected_auto) / 2
    auto_smoothed = fill_nan_with_local_mean(pd.Series(auto_smoothed))
    auto_smoothed = moving_average(auto_smoothed, len(auto_smoothed) // 25)

    final_signal = (manual_smoothed + auto_smoothed) / 2
    df["CH4_final (ppm)"] = final_signal

    # Preparar paths
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    data_output_dir = os.path.join(output_dir, "data")
    plot_dir = os.path.join(output_dir, "plots")
    results_dir = os.path.join(output_dir, "results")
    os.makedirs(data_output_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    output_csv = os.path.join(data_output_dir, base_name + "_processed.csv")

    # ------------------ Gráfica comparativa Original vs Final con picos detectados ------------------
    peaks_subdir = os.path.join(plot_dir, "with_peaks")
    os.makedirs(peaks_subdir, exist_ok=True)
    detected_peaks_path = os.path.join(peaks_subdir, base_name + "_peaks_comparison.png")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(time, signal, label="Original Signal")
    ax.plot(time, final_signal, label="Processed Signal")
    ax.scatter(time[valid_peaks], signal[valid_peaks], color='red', marker='o', label="Detected Peaks")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CH₄ (ppm)")
    ax.set_title("Original vs Processed Signals with Peaks")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(detected_peaks_path)
    plt.close(fig)

    # ------------------ Gráfica con pendientes ------------------
    slopes_subdir = os.path.join(plot_dir, "slopes")
    os.makedirs(slopes_subdir, exist_ok=True)
    slopes_plot_path = os.path.join(slopes_subdir, base_name + "_slopes_on_signal.png")
    fig = plot_signal_with_slopes_and_r2(df['time(s)'], final_signal, valid_peaks, window=10)
    fig.savefig(slopes_plot_path)
    plt.close(fig)

    # ------------------ Cálculo del flujo difusivo ------------------
    flux_lines, flux_series = calculate_slopes_and_difusive_flux(
        x=df['time(s)'],
        y=final_signal,
        valid_peaks=valid_peaks,
        temperatures_C=df['Temp'] if 'Temp' in df.columns else df['temp'],
        pressures_mmHg=df['Pressure(Hg_mm)'],
        volume_m3=0.35 * 0.25 * 0.20,
        area_m2=0.35 * 0.25,
        window=10,
        only_positive=True,
        return_series=True
    )

    # ------------------ Resumen de eventos ebullicionantes ------------------
    results = get_describe(df, valid_peaks=valid_peaks, window=window_peaks)
    print_summary(results)

    # ------------------ Guardar informe numérico ------------------
    txt_path = os.path.join(results_dir, base_name + "_results.txt")
    with open(txt_path, "w") as f:
        f.write(f"# Source File: {base_name}\n\n")
        f.write("--- Diffusive Flux Segments ---\n")
        for line in flux_lines:
            f.write(line + "\n")
        f.write("\n--- Summary Statistics of Diffusive Fluxes (µmol/m²·h) ---\n")
        f.write(str(flux_series.describe().round(2)))
        f.write("\n\n--- Summary of Ebullitive Events ---\n")
        for key, value in results.items():
            f.write(f"{key}: {value}\n")

    # ------------------ Señal escalonada de picos ------------------
    steps_subdir = os.path.join(plot_dir, "steps")
    os.makedirs(steps_subdir, exist_ok=True)
    step_plot_path = os.path.join(steps_subdir, base_name + "_peak_steps.png")
    step_signal = np.zeros_like(signal)
    peak_values = df.loc[valid_peaks, "CH4(ppm)"].values
    for i in range(len(valid_peaks) - 1):
        start = valid_peaks[i]
        end = valid_peaks[i + 1]
        step_signal[start:end] = peak_values[i]
    if len(valid_peaks) > 0:
        step_signal[valid_peaks[-1]:] = peak_values[-1]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time, step_signal, label="Step-like peak response", color='orange')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("CH₄ (ppm)")
    ax.set_title("Analog-like response of valid peaks")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(step_plot_path)
    plt.close(fig)

    # ------------------ Guardar CSV ------------------
    cols_to_drop = ["CH4_corr", "CH4_filtered", "ValidPeak"]
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
    df.to_csv(output_csv, index=False)
    
    print("--------------------")
    print(f"Processed and saved: {base_name}")
    print(f"All plots saved to: {base_name}")
    print(f"Results saved to: {base_name}")