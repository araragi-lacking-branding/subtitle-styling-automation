"""ASS (Advanced SubStation Alpha) format support and fansub style templates."""

import pysubs2
from typing import Optional, Dict
from pathlib import Path


# Fansub style templates based on professional groups
# Colors in pysubs2.Color are: Color(r, g, b, a) where a=0 is opaque, a=255 is transparent
FANSUB_STYLES = {
    'gjm': {
        'name': 'GJM',
        'fontname': 'Gandhi Sans',
        'fontsize': 75,
        'primary_colour': pysubs2.Color(255, 255, 255, 0),  # White
        'secondary_colour': pysubs2.Color(0, 0, 255, 0),  # Red (for karaoke)
        'outline_colour': pysubs2.Color(32, 32, 32, 0),  # Dark gray outline
        'back_colour': pysubs2.Color(32, 32, 32, 128),  # Semi-transparent shadow
        'bold': False,
        'italic': False,
        'underline': False,
        'strikeout': False,
        'scale_x': 100.0,
        'scale_y': 100.0,
        'spacing': 0.0,
        'angle': 0.0,
        'border_style': 1,  # Outline + drop shadow
        'outline': 3.5,
        'shadow': 1.5,
        'alignment': 2,  # Bottom center
        'marginl': 150,
        'marginr': 150,
        'marginv': 50,
    },
    'mtbb': {
        'name': 'MTBB',
        'fontname': 'Fontin Sans',
        'fontsize': 68,
        'primary_colour': pysubs2.Color(255, 255, 255, 0),  # White
        'secondary_colour': pysubs2.Color(98, 183, 255, 0),  # Light blue (karaoke)
        'outline_colour': pysubs2.Color(0, 0, 0, 0),  # Black outline
        'back_colour': pysubs2.Color(0, 0, 0, 160),  # Black shadow
        'bold': False,
        'italic': False,
        'underline': False,
        'strikeout': False,
        'scale_x': 100.0,
        'scale_y': 100.0,
        'spacing': 0.0,
        'angle': 0.0,
        'border_style': 1,
        'outline': 3.0,
        'shadow': 2.0,
        'alignment': 2,
        'marginl': 180,
        'marginr': 180,
        'marginv': 55,
    },
    'commie': {
        'name': 'Commie',
        'fontname': 'Cronos Pro',
        'fontsize': 70,
        'primary_colour': pysubs2.Color(255, 255, 255, 0),  # White
        'secondary_colour': pysubs2.Color(247, 255, 98, 0),  # Yellow (karaoke)
        'outline_colour': pysubs2.Color(0, 0, 0, 0),  # Black outline
        'back_colour': pysubs2.Color(0, 0, 0, 160),  # Black shadow
        'bold': True,
        'italic': False,
        'underline': False,
        'strikeout': False,
        'scale_x': 100.0,
        'scale_y': 100.0,
        'spacing': 0.0,
        'angle': 0.0,
        'border_style': 1,
        'outline': 4.0,
        'shadow': 1.5,
        'alignment': 2,
        'marginl': 170,
        'marginr': 170,
        'marginv': 60,
    },
    'subsplus': {
        'name': 'SubsPlus',
        'fontname': 'Arial',
        'fontsize': 72,
        'primary_colour': pysubs2.Color(255, 255, 255, 0),  # White
        'secondary_colour': pysubs2.Color(0, 255, 255, 0),  # Cyan (karaoke)
        'outline_colour': pysubs2.Color(0, 0, 0, 0),  # Black outline
        'back_colour': pysubs2.Color(0, 0, 0, 128),  # Black shadow
        'bold': False,
        'italic': False,
        'underline': False,
        'strikeout': False,
        'scale_x': 100.0,
        'scale_y': 100.0,
        'spacing': 0.0,
        'angle': 0.0,
        'border_style': 1,
        'outline': 3.0,
        'shadow': 2.0,
        'alignment': 2,
        'marginl': 160,
        'marginr': 160,
        'marginv': 50,
    },
    'default': {
        'name': 'Default',
        'fontname': 'Arial',
        'fontsize': 70,
        'primary_colour': pysubs2.Color(255, 255, 255, 0),  # White
        'secondary_colour': pysubs2.Color(0, 255, 255, 0),  # Cyan
        'outline_colour': pysubs2.Color(0, 0, 0, 0),  # Black outline
        'back_colour': pysubs2.Color(0, 0, 0, 128),  # Black shadow
        'bold': False,
        'italic': False,
        'underline': False,
        'strikeout': False,
        'scale_x': 100.0,
        'scale_y': 100.0,
        'spacing': 0.0,
        'angle': 0.0,
        'border_style': 1,
        'outline': 3.0,
        'shadow': 2.0,
        'alignment': 2,
        'marginl': 150,
        'marginr': 150,
        'marginv': 50,
    },
}


def create_ass_style(style_name: str = 'default') -> pysubs2.SSAStyle:
    """Create an ASS style based on fansub template.
    
    Args:
        style_name: Name of the fansub style (gjm, mtbb, commie, subsplus, default)
        
    Returns:
        pysubs2.SSAStyle object with the specified style
    """
    if style_name not in FANSUB_STYLES:
        style_name = 'default'
    
    template = FANSUB_STYLES[style_name]
    
    style = pysubs2.SSAStyle()
    for key, value in template.items():
        if hasattr(style, key):
            setattr(style, key, value)
    
    return style


def convert_srt_to_ass(
    srt_path: str,
    ass_path: str,
    style_name: str = 'default',
    resolution: tuple = (1920, 1080)
) -> None:
    """Convert SRT subtitle file to ASS format with styling.
    
    Args:
        srt_path: Path to input SRT file
        ass_path: Path to output ASS file
        style_name: Fansub style to apply (gjm, mtbb, commie, subsplus, default)
        resolution: Video resolution tuple (width, height)
    """
    # Load SRT file
    subs = pysubs2.load(srt_path, encoding='utf-8')
    
    # Create and set the style
    style = create_ass_style(style_name)
    subs.styles['Default'] = style
    
    # Set resolution info
    subs.info['PlayResX'] = str(resolution[0])
    subs.info['PlayResY'] = str(resolution[1])
    
    # Apply the Default style to all events
    for event in subs.events:
        event.style = 'Default'
    
    # Save as ASS
    subs.save(ass_path, format_='ass')


def apply_fansub_styling_to_ass(
    ass_file: pysubs2.SSAFile,
    style_name: str = 'default'
) -> None:
    """Apply fansub styling to an existing ASS file.
    
    Args:
        ass_file: pysubs2.SSAFile object
        style_name: Fansub style to apply
    """
    style = create_ass_style(style_name)
    ass_file.styles['Default'] = style
    
    # Apply style to all events
    for event in ass_file.events:
        event.style = 'Default'


def get_available_styles() -> list:
    """Get list of available fansub styles.
    
    Returns:
        List of style names
    """
    return list(FANSUB_STYLES.keys())
