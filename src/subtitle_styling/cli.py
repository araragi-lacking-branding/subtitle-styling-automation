"""Command-line interface for subtitle styling automation."""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, List

from .parser import SubtitleFile, scan_subtitle_files
from .styler import apply_style_guide
from .ass_converter import convert_srt_to_ass, get_available_styles


def process_subtitle_file(
    input_path: str,
    output_path: Optional[str] = None,
    style: str = 'clean',
    remove_hi: bool = False,
    verbose: bool = False,
    output_format: str = 'srt',
    ass_style: str = 'default'
) -> None:
    """Process a single subtitle file.
    
    Args:
        input_path: Path to input subtitle file
        output_path: Path to output subtitle file
        style: Style guide to apply
        remove_hi: Whether to remove hearing impaired annotations
        verbose: Whether to print verbose output
        output_format: Output format (srt, ass, or both)
        ass_style: ASS fansub style template (gjm, mtbb, commie, subsplus, default)
    """
    if verbose:
        print(f"Processing: {input_path}")
    
    # Load subtitle file
    subtitle = SubtitleFile(input_path)
    
    if verbose:
        print(f"  Loaded {len(subtitle)} subtitle entries")
    
    # Apply style guide
    apply_style_guide(subtitle.subtitles, style=style, remove_hi=remove_hi)
    
    # Determine base output path
    input_pathobj = Path(input_path)
    
    # Generate SRT if requested
    if output_format in ['srt', 'both']:
        if output_path is None:
            srt_output_path = str(input_pathobj.parent / f"{input_pathobj.stem}.styled.srt")
        elif output_format == 'both':
            srt_output_path = str(Path(output_path).parent / f"{Path(output_path).stem}.srt")
        else:
            srt_output_path = output_path
        
        subtitle.save(srt_output_path, encoding='utf-8')
        
        if verbose:
            print(f"  Saved SRT to: {srt_output_path}")
    
    # Generate ASS if requested
    if output_format in ['ass', 'both']:
        # First save as SRT temporarily if we haven't already
        if output_format == 'ass':
            temp_srt = str(input_pathobj.parent / f"{input_pathobj.stem}.temp.srt")
            subtitle.save(temp_srt, encoding='utf-8')
            srt_for_conversion = temp_srt
        else:
            srt_for_conversion = srt_output_path
        
        # Determine ASS output path
        if output_path is None:
            ass_output_path = str(input_pathobj.parent / f"{input_pathobj.stem}.styled.ass")
        elif output_format == 'both':
            ass_output_path = str(Path(output_path).parent / f"{Path(output_path).stem}.ass")
        else:
            ass_output_path = output_path
        
        # Convert to ASS with fansub styling
        convert_srt_to_ass(srt_for_conversion, ass_output_path, style_name=ass_style)
        
        # Clean up temp file if created
        if output_format == 'ass' and os.path.exists(temp_srt):
            os.remove(temp_srt)
        
        if verbose:
            print(f"  Saved ASS ({ass_style} style) to: {ass_output_path}")


def process_directory(
    directory: str,
    output_dir: Optional[str] = None,
    style: str = 'clean',
    remove_hi: bool = False,
    verbose: bool = False,
    extensions: Optional[list] = None,
    output_format: str = 'srt',
    ass_style: str = 'default'
) -> None:
    """Process all subtitle files in a directory.
    
    Args:
        directory: Directory to scan
        output_dir: Output directory (defaults to same as input)
        style: Style guide to apply
        remove_hi: Whether to remove hearing impaired annotations
        verbose: Whether to print verbose output
        extensions: File extensions to process
        output_format: Output format (srt, ass, or both)
        ass_style: ASS fansub style template
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
            output_path = str(Path(output_dir) / rel_path.parent / f"{rel_path.stem}.styled")
            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = None
        
        process_subtitle_file(input_path, output_path, style, remove_hi, verbose, 
                            output_format, ass_style)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Subtitle Styling Automation - Extract and modify subtitle styling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean a single subtitle file (SRT output)
  subtitle-style input.srt
  
  # Apply fansub style and generate ASS with GJM styling
  subtitle-style input.srt --style fansub --format ass --ass-style gjm
  
  # Generate both SRT and ASS (MTBB style)
  subtitle-style input.srt --format both --ass-style mtbb
  
  # Process all subtitle files in a directory (Commie ASS style)
  subtitle-style --directory ./subtitles --format ass --ass-style commie
  
  # Remove hearing impaired annotations and output as SubsPlus ASS
  subtitle-style input.srt --remove-hi --format ass --ass-style subsplus
  
  # Specify output location
  subtitle-style input.srt --output output.srt

Available text styles:
  clean      - Just clean up formatting and fix common errors (default)
  fansub     - Anime fansub style (ellipsis, em dash, smart quotes, sentence case)
  uppercase  - Convert all text to UPPERCASE
  lowercase  - Convert all text to lowercase
  title      - Convert All Text To Title Case
  sentence   - Convert text to Sentence case

Available ASS fansub styles (for --format ass or both):
  default    - Standard ASS styling with Arial font
  gjm        - Good Job! Media style (Gandhi Sans, white text, dark outline)
  mtbb       - MTBB style (Fontin Sans, clean minimal styling)
  commie     - Commie style (Cronos Pro, bold, strong outline)
  subsplus   - SubsPlus style (Arial, professional standards)
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
        choices=['clean', 'fansub', 'uppercase', 'lowercase', 'title', 'sentence'],
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
    
    # Format options
    parser.add_argument(
        '-f', '--format',
        choices=['srt', 'ass', 'both'],
        default='srt',
        help='Output format: srt, ass (Advanced SubStation Alpha), or both (default: srt)'
    )
    parser.add_argument(
        '--ass-style',
        choices=['default', 'gjm', 'mtbb', 'commie', 'subsplus'],
        default='default',
        help='ASS fansub style template (only for --format ass or both): gjm (GJM), mtbb (MTBB), commie (Commie), subsplus (SubsPlus), default'
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
                extensions=args.extensions,
                output_format=args.format,
                ass_style=args.ass_style
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
                verbose=args.verbose,
                output_format=args.format,
                ass_style=args.ass_style
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
