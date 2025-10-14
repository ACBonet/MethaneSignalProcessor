from inc.test_functions import process_file
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="CH₄ signal processing from terminal")
    parser.add_argument('--dir', type=str, default='.', help="Root directory (default: current folder)")
    parser.add_argument('--window_peaks', type=int, default=5, help="Window size for analyzing ebullition peaks (default: 5)")
    args = parser.parse_args()

    # Compatible with .py, .pyz and .exe inside /dist
    base_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0])))

    raw_dir = os.path.join(base_path, "Raw data")
    output_dir = os.path.join(base_path, "Processed data")
    os.makedirs(output_dir, exist_ok=True)

    answer = input("Do you want to process a specific file? (y/n): ").strip().lower()

    if answer == 'y':
        file_name = input("Enter the filename inside 'Raw data' (e.g. data): ").strip()
        file_path = os.path.join(raw_dir, file_name + ".txt")

        try:
            window_peaks = int(input("Enter window size for analyzing ebullition peaks (default is 5): ").strip())
        except ValueError:
            window_peaks = 5

        # Validate the file is inside Raw data and exists
        if os.path.commonpath([os.path.abspath(file_path), raw_dir]) == os.path.abspath(raw_dir) \
           and os.path.isfile(file_path):
            process_file(file_path, output_dir, window_peaks=window_peaks)
        else:
            print("Invalid file. Make sure the file exists inside the 'Raw data' folder and has a .txt extension.")
    else:
        try:
            window_peaks = int(input("Enter window size for analyzing ebullition peaks (default is 5): ").strip())
        except ValueError:
            window_peaks = 5

        if not os.path.isdir(raw_dir):
            print(f"Error: Raw data directory not found at {raw_dir}")
            return

        for fname in os.listdir(raw_dir):
            if fname.endswith('.txt'):
                full_path = os.path.join(raw_dir, fname)
                process_file(full_path, output_dir, window_peaks=window_peaks)

if __name__ == "__main__":
    main()