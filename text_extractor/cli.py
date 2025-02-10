import argparse
import os
from text_extractor.extractor import process_directory

def main():
    parser = argparse.ArgumentParser(description="Extract and replace hardcoded texts in source files with a translate function.")
    parser.add_argument("directory", type=str, help="Path to the directory containing source code.")
    parser.add_argument("--outputdir", type=str, default="outputdir", help="Output dir for translated sources.")
    parser.add_argument("--subdir", type=str, default="", help="Subdir for translated srouces.")
    parser.add_argument("--output", type=str, default="translations.json", help="Output file for extracted translations (JSON).")
    # parser.add_argument("--subdirall", type=str, default=".", help="Subdirall for all translated srouces.")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print("Error: Provided path is not a directory.")
        return
    subdir = [item.strip() for item in args.subdir.split(",")]
    # subdirall = [item.strip() for item in args.subdirall.split(",")]

    for sub in subdir:
        process_directory(args.directory, args.output, args.outputdir, sub)

if __name__ == "__main__":
    main()


