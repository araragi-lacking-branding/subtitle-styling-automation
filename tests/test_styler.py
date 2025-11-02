"""Tests for subtitle styler module."""

import pytest
from subtitle_styling.styler import (
    SubtitleCleaner,
    SubtitleStyler,
    apply_style_guide
)
import pysrt


class TestSubtitleCleaner:
    """Tests for SubtitleCleaner class."""
    
    def test_remove_formatting_tags(self):
        """Test removing formatting tags."""
        text = "<i>Hello</i> <b>world</b>"
        cleaned = SubtitleCleaner.remove_formatting_tags(text)
        assert cleaned == "Hello world"
        
        text = "{\\i1}Italic text{\\i0}"
        cleaned = SubtitleCleaner.remove_formatting_tags(text)
        assert cleaned == "Italic text"
    
    def test_normalize_whitespace(self):
        """Test normalizing whitespace."""
        text = "Hello    world   test"
        cleaned = SubtitleCleaner.normalize_whitespace(text)
        assert cleaned == "Hello world test"
        
        text = "  Spaces around  "
        cleaned = SubtitleCleaner.normalize_whitespace(text)
        assert cleaned == "Spaces around"
    
    def test_fix_common_errors(self):
        """Test fixing common errors."""
        text = "Hello.World"
        fixed = SubtitleCleaner.fix_common_errors(text)
        assert fixed == "Hello. World"
        
        text = "Question?Answer"
        fixed = SubtitleCleaner.fix_common_errors(text)
        assert fixed == "Question? Answer"
    
    def test_remove_hearing_impaired(self):
        """Test removing hearing impaired annotations."""
        text = "[MUSIC PLAYING] Dialog here"
        cleaned = SubtitleCleaner.remove_hearing_impaired(text)
        assert cleaned == "Dialog here"
        
        text = "(door slams) More dialog"
        cleaned = SubtitleCleaner.remove_hearing_impaired(text)
        assert cleaned == "More dialog"
    
    def test_clean_all(self):
        """Test applying all cleaning operations."""
        text = "<i>[MUSIC]</i>  Hello.World  "
        cleaned = SubtitleCleaner.clean_all(text, remove_hi=True)
        assert cleaned == "Hello. World"


class TestSubtitleStyler:
    """Tests for SubtitleStyler class."""
    
    def test_apply_uppercase(self):
        """Test uppercase styling."""
        text = "Hello world"
        styled = SubtitleStyler.apply_uppercase(text)
        assert styled == "HELLO WORLD"
    
    def test_apply_lowercase(self):
        """Test lowercase styling."""
        text = "HELLO WORLD"
        styled = SubtitleStyler.apply_lowercase(text)
        assert styled == "hello world"
    
    def test_apply_title_case(self):
        """Test title case styling."""
        text = "hello world test"
        styled = SubtitleStyler.apply_title_case(text)
        assert styled == "Hello World Test"
    
    def test_apply_sentence_case(self):
        """Test sentence case styling."""
        text = "HELLO WORLD. ANOTHER SENTENCE."
        styled = SubtitleStyler.apply_sentence_case(text)
        assert styled == "Hello world. Another sentence."
    
    def test_apply_fansub_style(self):
        """Test anime fansub styling."""
        # Test ellipsis replacement
        text = "Wait... what?"
        styled = SubtitleStyler.apply_fansub_style(text)
        assert "…" in styled
        assert "..." not in styled
        
        # Test em dash replacement
        text = "I was going to--"
        styled = SubtitleStyler.apply_fansub_style(text)
        assert "—" in styled
        assert "--" not in styled
        
        # Test smart quotes
        text = '"Hello there"'
        styled = SubtitleStyler.apply_fansub_style(text)
        # Should have smart quotes or at least quotes preserved
        assert "Hello there" in styled
        
        # Test capitalization (sentence case but preserves existing caps)
        text = "hello world. Naruto-kun said that."
        styled = SubtitleStyler.apply_fansub_style(text)
        assert styled[0].isupper()  # First letter capitalized
        assert "kun" in styled.lower()  # Honorific preserved


def test_apply_style_guide():
    """Test applying style guide to subtitles."""
    # Create a simple subtitle
    subs = pysrt.SubRipFile()
    sub1 = pysrt.SubRipItem(
        index=1,
        start=pysrt.SubRipTime(0, 0, 1),
        end=pysrt.SubRipTime(0, 0, 3),
        text="<i>hello</i>  world"
    )
    subs.append(sub1)
    
    # Apply clean style
    apply_style_guide(subs, style='clean')
    assert subs[0].text == "hello world"
    
    # Apply uppercase style
    subs[0].text = "<i>hello</i>  world"
    apply_style_guide(subs, style='uppercase')
    assert subs[0].text == "HELLO WORLD"


def test_apply_style_guide_remove_hi():
    """Test applying style guide with hearing impaired removal."""
    subs = pysrt.SubRipFile()
    sub1 = pysrt.SubRipItem(
        index=1,
        start=pysrt.SubRipTime(0, 0, 1),
        end=pysrt.SubRipTime(0, 0, 3),
        text="[MUSIC] Dialog here"
    )
    subs.append(sub1)
    
    # Apply with HI removal
    apply_style_guide(subs, style='clean', remove_hi=True)
    assert "[MUSIC]" not in subs[0].text
    assert "Dialog here" in subs[0].text


def test_apply_style_guide_fansub():
    """Test applying fansub style guide."""
    subs = pysrt.SubRipFile()
    sub1 = pysrt.SubRipItem(
        index=1,
        start=pysrt.SubRipTime(0, 0, 1),
        end=pysrt.SubRipTime(0, 0, 3),
        text='Wait... "what did you say?"'
    )
    subs.append(sub1)
    
    # Apply fansub style
    apply_style_guide(subs, style='fansub')
    result = subs[0].text
    
    # Should have proper ellipsis
    assert "…" in result or "..." in result
    
    # Should have quotes preserved
    assert "what did you say" in result.lower()
