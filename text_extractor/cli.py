import argparse
import os
from text_extractor.extractor import process_directory

def main():
    parser = argparse.ArgumentParser(description="Extract and replace hardcoded texts in source files with a translate function.")
    parser.add_argument("directory", type=str, help="Path to the directory containing source code.")
    parser.add_argument("--outputdir", type=str, default="outputdir", help="Output dir for translated sources.")
    parser.add_argument("--output", type=str, default="translations.json", help="Output file for extracted translations (JSON).")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a directory.")
        return

    process_directory(args.directory, args.output, args.outputdir)

if __name__ == "__main__":
    main()


