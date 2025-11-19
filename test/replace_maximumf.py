#!/usr/bin/env python3
"""
Replace 'maximumf' with 'maxf' in a file.
Usage: python replace_maximumf.py <input_file> [output_file]
If output_file is not specified, modifies input_file in place.
"""

import sys
import argparse


def replace_maximumf(content):
    """Replace all occurrences of 'maximumf' with 'maxf'."""
    return content.replace('maximumf', 'maxf')


def main():
    parser = argparse.ArgumentParser(
        description='Replace maximumf with maxf in a file'
    )
    parser.add_argument(
        'input_file',
        help='Input file to process'
    )
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Output file (if not specified, modifies input_file in place)'
    )
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Perform replacement
    new_content = replace_maximumf(content)
    
    # Write output
    output_file = args.output_file if args.output_file else args.input_file
    try:
        with open(output_file, 'w') as f:
            f.write(new_content)
        if output_file == args.input_file:
            print(f"Modified '{args.input_file}' in place.")
        else:
            print(f"Wrote output to '{output_file}'.")
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

