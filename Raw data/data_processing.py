from inc.functions import procesar_archivo
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="CH₄ signal processing from terminal")
    parser.add_argument('--dir', type=str, default='.', help="Directory containing .txt files (default: current folder)")
    args = parser.parse_args()

    output_dir = os.path.join(args.dir, "Processed data")
    os.makedirs(output_dir, exist_ok=True)

    # Ask the user if they want to process a specific file
    answer = input("Do you want to process a specific file? (y/n): ").strip().lower()

    if answer == 'y':
        file_path = input("Enter the path to the .txt file: ").strip()
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            procesar_archivo(file_path, output_dir)
        else:
            print("❌ Invalid path or not a .txt file.")
    else:
        for fname in os.listdir(args.dir):
            if fname.endswith('.txt'):
                full_path = os.path.join(args.dir, fname)
                procesar_archivo(full_path, output_dir)

if __name__ == "__main__":
    main()
