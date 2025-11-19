#!/usr/bin/env python3
"""
Script to truncate lines in MLIR files to 1000 characters.
Lines longer than 1000 characters will be truncated to exactly 1000 characters.
"""

import argparse
import sys


def truncate_mlir_file(input_file, output_file=None, max_length=1000):
    """
    Truncate lines in an MLIR file to a maximum length.
    
    Args:
        input_file: Path to the input MLIR file
        output_file: Path to the output file (if None, modifies in place)
        max_length: Maximum line length (default: 1000)
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        truncated_lines = []
        truncated_count = 0
        
        for line in lines:
            if len(line) > max_length:
                # Truncate to max_length, preserving the newline if present
                if line.endswith('\n'):
                    truncated_line = line[:max_length-1] + '\n'
                else:
                    truncated_line = line[:max_length]
                truncated_lines.append(truncated_line)
                truncated_count += 1
            else:
                truncated_lines.append(line)
        
        # Determine output file
        output_path = output_file if output_file else input_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(truncated_lines)
        
        print(f"Processed {len(lines)} lines")
        if truncated_count > 0:
            print(f"Truncated {truncated_count} lines to {max_length} characters")
        else:
            print("No lines needed truncation")
        print(f"Output written to: {output_path}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Truncate lines in MLIR files to a maximum length',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.mlir                    # Modify file.mlir in place
  %(prog)s input.mlir -o output.mlir    # Write to output.mlir
  %(prog)s file.mlir --max-length 500   # Use custom max length
        """
    )
    parser.add_argument('input_file', help='Input MLIR file')
    parser.add_argument('-o', '--output', dest='output_file', 
                       help='Output file (default: modify input file in place)')
    parser.add_argument('--max-length', type=int, default=1000,
                       help='Maximum line length (default: 1000)')
    
    args = parser.parse_args()
    
    truncate_mlir_file(args.input_file, args.output_file, args.max_length)


if __name__ == '__main__':
    main()

