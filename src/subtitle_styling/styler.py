"""Subtitle text cleaning and styling utilities."""

import re
from typing import List, Callable


class SubtitleCleaner:
    """Cleans and normalizes subtitle text."""
    
    @staticmethod
    def remove_formatting_tags(text: str) -> str:
        """Remove HTML-like formatting tags from subtitle text.
        
        Args:
            text: Subtitle text with potential tags
            
        Returns:
            Cleaned text without formatting tags
        """
        # Remove common subtitle formatting tags
        patterns = [
            r'<[^>]+>',  # HTML-like tags
            r'\{[^}]+\}',  # Curly brace tags (SubStation Alpha)
            r'\\[nN]',  # Line breaks in some formats
        ]
        
        cleaned = text
        for pattern in patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        return cleaned
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in subtitle text.
        
        Args:
            text: Subtitle text
            
        Returns:
            Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    @staticmethod
    def fix_common_errors(text: str) -> str:
        """Fix common subtitle errors.
        
        Args:
            text: Subtitle text
            
        Returns:
            Text with common errors fixed
        """
        # Fix missing space after punctuation
        text = re.sub(r'([.!?,;:])([A-Za-z])', r'\1 \2', text)
        # Fix spacing around quotes
        text = re.sub(r'\s+"', '"', text)
        text = re.sub(r'"\s+', '"', text)
        return text
    
    @staticmethod
    def remove_hearing_impaired(text: str) -> str:
        """Remove hearing impaired annotations.
        
        Args:
            text: Subtitle text
            
        Returns:
            Text without hearing impaired annotations
        """
        # Remove [sound effects] and (descriptions)
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\(.*?\)', '', text)
        # Clean up extra whitespace left after removal
        text = re.sub(r'^\s+', '', text)  # Remove leading whitespace
        text = re.sub(r'\s+$', '', text)  # Remove trailing whitespace
        return text
    
    @classmethod
    def clean_all(cls, text: str, remove_hi: bool = False) -> str:
        """Apply all cleaning operations.
        
        Args:
            text: Subtitle text to clean
            remove_hi: Whether to remove hearing impaired annotations
            
        Returns:
            Fully cleaned text
        """
        cleaned = text
        cleaned = cls.remove_formatting_tags(cleaned)
        if remove_hi:
            cleaned = cls.remove_hearing_impaired(cleaned)
        cleaned = cls.fix_common_errors(cleaned)
        cleaned = cls.normalize_whitespace(cleaned)
        return cleaned


class SubtitleStyler:
    """Applies styling to subtitle text."""
    
    @staticmethod
    def apply_uppercase(text: str) -> str:
        """Convert text to uppercase.
        
        Args:
            text: Subtitle text
            
        Returns:
            Uppercase text
        """
        return text.upper()
    
    @staticmethod
    def apply_lowercase(text: str) -> str:
        """Convert text to lowercase.
        
        Args:
            text: Subtitle text
            
        Returns:
            Lowercase text
        """
        return text.lower()
    
    @staticmethod
    def apply_title_case(text: str) -> str:
        """Convert text to title case.
        
        Args:
            text: Subtitle text
            
        Returns:
            Title case text
        """
        return text.title()
    
    @staticmethod
    def apply_sentence_case(text: str) -> str:
        """Convert text to sentence case.
        
        Args:
            text: Subtitle text
            
        Returns:
            Sentence case text
        """
        # Split into sentences
        sentences = re.split(r'([.!?]+\s*)', text)
        result = []
        
        for i, part in enumerate(sentences):
            if i % 2 == 0 and part:  # Text parts
                # Capitalize first letter, lowercase rest
                if len(part) > 0:
                    part = part[0].upper() + part[1:].lower()
            result.append(part)
        
        return ''.join(result)
    
    @staticmethod
    def apply_fansub_style(text: str) -> str:
        """Apply anime fansub styling guidelines.
        
        Based on standards from groups like Good Job! Media, MTBB, Commie, and SubsPlus.
        Includes its own cleaning to preserve quote spacing.
        
        Args:
            text: Subtitle text
            
        Returns:
            Text styled according to anime fansub guidelines
        """
        styled = text
        
        # Remove formatting tags first
        styled = SubtitleCleaner.remove_formatting_tags(styled)
        
        # Fix missing space after punctuation (but not quotes)
        styled = re.sub(r'([.!?,;:])([A-Za-z])', r'\1 \2', styled)
        
        # Replace three periods with proper ellipsis (…)
        styled = re.sub(r'\.\.\.', '…', styled)
        
        # Replace double/triple hyphens with em dash (—)
        styled = re.sub(r'--+', '—', styled)
        
        # Replace straight quotes with smart quotes for dialogue
        # Opening double quote (at start or after whitespace/punctuation)
        styled = re.sub(r'(^|[\s(\[])"', r'\1"', styled)
        # Closing double quote (before whitespace/punctuation or at end)
        styled = re.sub(r'"([\s.,!?;:\])]|$)', r'"\1', styled)
        # Handle remaining quotes (likely closing if not caught above)
        styled = styled.replace('"', '"')
        
        # Opening single quote
        styled = re.sub(r"(^|[\s(\[])\'", r"\1'", styled)
        # Closing single quote
        styled = re.sub(r"\'([\s.,!?;:\])]|$)", r"'\1", styled)
        # Handle remaining single quotes
        styled = styled.replace("'", "'")
        
        # Ensure proper spacing around em dashes (no spaces)
        styled = re.sub(r'\s*—\s*', '—', styled)
        
        # Ensure proper spacing after ellipsis (space if followed by uppercase letter)
        styled = re.sub(r'…([A-Z])', r'… \1', styled)
        # Remove extra spaces after ellipsis
        styled = re.sub(r'…\s+', '… ', styled)
        
        # Normalize multiple spaces to single space
        styled = re.sub(r' +', ' ', styled)
        # Remove leading/trailing whitespace
        styled = styled.strip()
        
        # Apply sentence case (capitalize first letter of sentences)
        sentences = re.split(r'([.!?…]+\s*)', styled)
        result = []
        
        for i, part in enumerate(sentences):
            if i % 2 == 0 and part:  # Text parts (not punctuation)
                # Capitalize first letter, keep rest as-is (to preserve honorifics, names)
                if len(part) > 0:
                    # Only capitalize if not already capitalized (preserves proper nouns)
                    first_char_idx = 0
                    # Skip opening quotes (including smart quotes)
                    while first_char_idx < len(part) and part[first_char_idx] in '"\'""''':
                        first_char_idx += 1
                    if first_char_idx < len(part):
                        part = part[:first_char_idx] + part[first_char_idx].upper() + part[first_char_idx+1:]
            result.append(part)
        
        styled = ''.join(result)
        
        return styled


def apply_style_guide(subtitles, style: str = 'clean', remove_hi: bool = False) -> None:
    """Apply a style guide to subtitles in-place.
    
    Args:
        subtitles: SubRipFile or list of subtitle items
        style: Style to apply ('clean', 'fansub', 'uppercase', 'lowercase', 'title', 'sentence')
        remove_hi: Whether to remove hearing impaired annotations
    """
    for sub in subtitles:
        # Fansub style does its own cleaning
        if style == 'fansub':
            if remove_hi:
                sub.text = SubtitleCleaner.remove_hearing_impaired(sub.text)
            sub.text = SubtitleStyler.apply_fansub_style(sub.text)
        else:
            # Clean the text for other styles
            cleaned_text = SubtitleCleaner.clean_all(sub.text, remove_hi=remove_hi)
            
            # Apply style
            if style == 'uppercase':
                cleaned_text = SubtitleStyler.apply_uppercase(cleaned_text)
            elif style == 'lowercase':
                cleaned_text = SubtitleStyler.apply_lowercase(cleaned_text)
            elif style == 'title':
                cleaned_text = SubtitleStyler.apply_title_case(cleaned_text)
            elif style == 'sentence':
                cleaned_text = SubtitleStyler.apply_sentence_case(cleaned_text)
            # 'clean' just applies cleaning, no additional styling
            
            sub.text = cleaned_text
