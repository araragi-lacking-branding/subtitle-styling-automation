"""Command-line interface for subtitle styling automation."""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

from .parser import SubtitleFile, scan_subtitle_files
from .styler import apply_style_guide


def process_subtitle_file(
    input_path: str,
    output_path: Optional[str] = None,
    style: str = 'clean',
    remove_hi: bool = False,
    verbose: bool = False
) -> None:
    """Process a single subtitle file.
    
    Args:
        input_path: Path to input subtitle file
        output_path: Path to output subtitle file (defaults to input_path with .styled.srt)
        style: Style guide to apply
        remove_hi: Whether to remove hearing impaired annotations
        verbose: Whether to print verbose output
    """
    if verbose:
        print(f"Processing: {input_path}")
    
    # Load subtitle file
    subtitle = SubtitleFile(input_path)
    
    if verbose:
        print(f"  Loaded {len(subtitle)} subtitle entries")
    
    # Apply style guide
    apply_style_guide(subtitle.subtitles, style=style, remove_hi=remove_hi)
    
    # Determine output path
    if output_path is None:
        input_pathobj = Path(input_path)
        output_path = str(input_pathobj.parent / f"{input_pathobj.stem}.styled{input_pathobj.suffix}")
    
    # Save
    subtitle.save(output_path, encoding='utf-8')
    
    if verbose:
        print(f"  Saved to: {output_path}")


def process_directory(
    directory: str,
    output_dir: Optional[str] = None,
    style: str = 'clean',
    remove_hi: bool = False,
    verbose: bool = False,
    extensions: Optional[list] = None
) -> None:
    """Process all subtitle files in a directory.
    
    Args:
        directory: Directory to scan
        output_dir: Output directory (defaults to same as input)
        style: Style guide to apply
        remove_hi: Whether to remove hearing impaired annotations
        verbose: Whether to print verbose output
        extensions: File extensions to process
    """
    # Scan for subtitle files
    subtitle_files = scan_subtitle_files(directory, extensions=extensions)
    
    if verbose:
        print(f"Found {len(subtitle_files)} subtitle files in {directory}")
    
    if not subtitle_files:
        print(f"No subtitle files found in {directory}")
        return
    
    # Process each file
    for input_path in subtitle_files:
        # Determine output path
        if output_dir:
            input_pathobj = Path(input_path)
            rel_path = input_pathobj.relative_to(directory)
            output_path = str(Path(output_dir) / rel_path.parent / f"{rel_path.stem}.styled{rel_path.suffix}")
            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = None
        
        process_subtitle_file(input_path, output_path, style, remove_hi, verbose)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Subtitle Styling Automation - Extract and modify subtitle styling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean a single subtitle file
  subtitle-style input.srt
  
  # Apply uppercase style to a subtitle file
  subtitle-style input.srt --style uppercase
  
  # Process all subtitle files in a directory
  subtitle-style --directory ./subtitles --style clean
  
  # Remove hearing impaired annotations
  subtitle-style input.srt --remove-hi
  
  # Specify output location
  subtitle-style input.srt --output output.srt

Available styles:
  clean      - Just clean up formatting and fix common errors (default)
  uppercase  - Convert all text to UPPERCASE
  lowercase  - Convert all text to lowercase
  title      - Convert All Text To Title Case
  sentence   - Convert text to Sentence case
        """
    )
    
    # Input options
    parser.add_argument(
        'input',
        nargs='?',
        help='Input subtitle file to process'
    )
    parser.add_argument(
        '-d', '--directory',
        help='Process all subtitle files in this directory'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        help='Output file path (for single file mode) or directory (for directory mode)'
    )
    
    # Style options
    parser.add_argument(
        '-s', '--style',
        choices=['clean', 'uppercase', 'lowercase', 'title', 'sentence'],
        default='clean',
        help='Style guide to apply (default: clean)'
    )
    parser.add_argument(
        '--remove-hi',
        action='store_true',
        help='Remove hearing impaired annotations like [sound effects]'
    )
    
    # Extensions
    parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        default=['.srt', '.txt'],
        help='File extensions to process (default: .srt .txt)'
    )
    
    # Other options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not args.input and not args.directory:
        parser.error("Either input file or --directory must be specified")
    
    if args.input and args.directory:
        parser.error("Cannot specify both input file and --directory")
    
    try:
        if args.directory:
            # Directory mode
            process_directory(
                args.directory,
                output_dir=args.output,
                style=args.style,
                remove_hi=args.remove_hi,
                verbose=args.verbose,
                extensions=args.extensions
            )
        else:
            # Single file mode
            if not os.path.exists(args.input):
                print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
                sys.exit(1)
            
            process_subtitle_file(
                args.input,
                output_path=args.output,
                style=args.style,
                remove_hi=args.remove_hi,
                verbose=args.verbose
            )
        
        if args.verbose:
            print("Processing complete!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
