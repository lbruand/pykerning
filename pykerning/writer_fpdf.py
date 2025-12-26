"""FPDF2-based writer for python-typesetting library.

This module provides an alternative to QtWriter that uses fpdf2 instead of PySide2.
"""

from fpdf import FPDF
from pathlib import Path


class FpdfFont:
    """Font wrapper that matches the QtFont interface."""

    def __init__(self, pdf, font_family, font_style, font_size):
        self.pdf = pdf
        self.font_family = font_family
        self.font_style = font_style
        self.font_size = font_size

        # Calculate font metrics
        # fpdf2 uses points, and we need to match Qt's metrics
        self.height = font_size
        # Typical font metrics ratios
        self.ascent = font_size * 0.8
        self.descent = font_size * 0.2
        self.leading = font_size * 0.2

    def width_of(self, text):
        """Returns the width of text in points."""
        # Temporarily set the font to measure text
        current_family = self.pdf.font_family
        current_style = self.pdf.font_style
        current_size = self.pdf.font_size_pt

        self.pdf.set_font(self.font_family, self.font_style, self.font_size)
        width = self.pdf.get_string_width(text)

        # Restore previous font
        if current_family:
            self.pdf.set_font(current_family, current_style, current_size)

        return width


class FpdfWriter:
    """PDF writer using fpdf2 that matches the QtWriter interface."""

    def __init__(self, path, width_pt, height_pt):
        """Initialize the PDF writer.

        Args:
            path: Output PDF file path
            width_pt: Page width in points
            height_pt: Page height in points
        """
        self.path = path
        self.width_pt = width_pt
        self.height_pt = height_pt

        # Convert points to mm for fpdf2
        # 1 point = 1/72 inch, 1 inch = 25.4 mm
        self.width_mm = width_pt * 25.4 / 72
        self.height_mm = height_pt * 25.4 / 72

        # Create PDF with custom page size
        self.pdf = FPDF(unit='pt', format=(width_pt, height_pt))
        self.pdf.set_auto_page_break(False)
        self.pdf.add_page()

        # Track loaded fonts: path -> (family_name, style)
        self.loaded_fonts = {}
        # Track font specifications: name -> FpdfFont
        self.fonts = {}

        self.current_font = None

    def close(self):
        """Save and close the PDF."""
        self.pdf.output(self.path)

    def load_font(self, path):
        """Load a TrueType font file.

        Args:
            path: Path to the .ttf font file
        """
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Font file not found: {path}")

        # Extract font info from filename
        # GenBasR.ttf -> Gentium Basic Regular
        # GenBasI.ttf -> Gentium Basic Italic
        # GenBasB.ttf -> Gentium Basic Bold
        filename = path_obj.stem

        # Determine style from filename
        style = ''
        if filename.endswith('I'):
            style = 'I'  # Italic
        elif filename.endswith('B'):
            style = 'B'  # Bold
        elif filename.endswith('BI') or filename.endswith('IB'):
            style = 'BI'  # Bold Italic

        # For Gentium Basic fonts, use a consistent family name
        family_name = "GentiumBasic"

        # Add font to PDF
        self.pdf.add_font(family_name, style, str(path_obj))
        self.loaded_fonts[str(path_obj)] = (family_name, style)

    def get_fonts(self, font_specs):
        """Get font objects from specifications.

        Args:
            font_specs: List of tuples (name, family, style, size)
                       e.g., ('roman', 'Gentium Basic', 'Regular', 12)

        Returns:
            Dictionary mapping font names to FpdfFont objects
        """
        fonts = {}

        for name, family, style, size in font_specs:
            # Map family and style to the loaded font
            fpdf_family = "GentiumBasic"  # We use a consistent name

            # Map style names to fpdf2 style codes
            fpdf_style = ''
            if 'Italic' in style:
                fpdf_style = 'I'
            elif 'Bold' in style:
                fpdf_style = 'B'

            fonts[name] = FpdfFont(self.pdf, fpdf_family, fpdf_style, size)

        self.fonts = fonts
        return fonts

    def new_page(self):
        """Create a new page."""
        self.pdf.add_page()

    def set_font(self, font):
        """Set the current font.

        Args:
            font: An FpdfFont object
        """
        self.current_font = font
        self.pdf.set_font(font.font_family, font.font_style, font.font_size)

    def draw_text(self, x_pt, y_pt, text):
        """Draw text at specified coordinates.

        Args:
            x_pt: X coordinate in points
            y_pt: Y coordinate in points
            text: Text string to draw
        """
        # fpdf2 uses top-left origin, same as Qt
        # The y coordinate in the typesetting system appears to be baseline
        # We need to draw at the position
        self.pdf.text(x_pt, y_pt, text)