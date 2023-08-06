import argparse
import os

import klembord

def cleanify(args):
    """Strips newlines, tabs from a file and copies it to the clipboard

    Args:
        args (Namespace): parsed CLI flags from argparse
    """
    with open(args.file, 'r') as f:
        fileText = f.read()

    cleanedText = fileText.replace('\n', '').replace('\t', '')

    if args.repQuotes: cleanedText = cleanedText.replace('"', "'") # Replacing quotes if needed

    klembord.set_text(cleanedText) # Adding final str to clipboard

def main():
    """Creates parser and calls cleanify with args
    """
    # Setting up parser
    parser = argparse.ArgumentParser(
        description="Copy a file's contents to your clipboard while removing newlines.")

    parser.add_argument('-file', "-f",
        type = os.path.abspath,
        help = "The file to read.")

    parser.add_argument("--repQuotes", "--rq",
        action="store_true",
        default=False,
        help="Replace double quotes with single ones (helps when storing HTML in .json files)")

    args = parser.parse_args()

    # Calling cleaner
    try:
        cleanify(args)
        print("Cleaned and copied to clipboard!")

    except Exception as e:
        print(f"Error cleaning: {e}")

if __name__ == "__main__":
    main()