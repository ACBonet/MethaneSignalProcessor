from inc.functions import process_file
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="CH₄ signal processing from terminal")
    parser.add_argument('--dir', type=str, default='.', help="Root directory (default: current folder)")
    args = parser.parse_args()

    # Compatible with .py, .pyz and .exe inside /dist
    base_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0])))

    raw_dir = os.path.join(base_path, "Raw data")
    output_dir = os.path.join(base_path, "Processed data")
    os.makedirs(output_dir, exist_ok=True)

    answer = input("Do you want to process a specific file? (y/n): ").strip().lower()

    if answer == 'y':
        file_path = input("Enter the path to the .txt file: ").strip()
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            process_file(file_path, output_dir)
        else:
            print("Invalid path or not a .txt file.")
    else:
        if not os.path.isdir(raw_dir):
            print(f"Error: Raw data directory not found at {raw_dir}")
            return

        for fname in os.listdir(raw_dir):
            if fname.endswith('.txt'):
                full_path = os.path.join(raw_dir, fname)
                process_file(full_path, output_dir)

if __name__ == "__main__":
    main()