"""FPDF2-based writer for python-typesetting library.

This module provides an alternative to QtWriter that uses fpdf2 instead of PySide2.
"""

from fpdf import FPDF
from pathlib import Path

# Unit conversion constants
POINTS_PER_INCH = 72
MM_PER_INCH = 25.4

# Font metric ratios (typical values for matching Qt's metrics)
FONT_ASCENT_RATIO = 0.8
FONT_DESCENT_RATIO = 0.2
FONT_LEADING_RATIO = 0.2

# Font family constants
DEFAULT_FONT_FAMILY = "GentiumBasic"

# Font style codes for fpdf2
STYLE_REGULAR = ''
STYLE_ITALIC = 'I'
STYLE_BOLD = 'B'
STYLE_BOLD_ITALIC = 'BI'


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
        self.ascent = font_size * FONT_ASCENT_RATIO
        self.descent = font_size * FONT_DESCENT_RATIO
        self.leading = font_size * FONT_LEADING_RATIO

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
            path: Output PDF file path, or None to return PDF as bytes in close()
            width_pt: Page width in points
            height_pt: Page height in points
        """
        self.path = path
        self.width_pt = width_pt
        self.height_pt = height_pt

        # Convert points to mm for fpdf2
        self.width_mm = width_pt * MM_PER_INCH / POINTS_PER_INCH
        self.height_mm = height_pt * MM_PER_INCH / POINTS_PER_INCH

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
        """Save and close the PDF.

        Returns:
            bytearray or None: PDF content as bytearray if path was None, otherwise None
        """
        if self.path is None:
            return self.pdf.output()
        else:
            self.pdf.output(self.path)
            return None

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
        style = STYLE_REGULAR
        if filename.endswith('I'):
            style = STYLE_ITALIC
        elif filename.endswith('B'):
            style = STYLE_BOLD
        elif filename.endswith('BI') or filename.endswith('IB'):
            style = STYLE_BOLD_ITALIC

        # For Gentium Basic fonts, use a consistent family name
        family_name = DEFAULT_FONT_FAMILY

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
            fpdf_family = DEFAULT_FONT_FAMILY

            # Map style names to fpdf2 style codes
            fpdf_style = STYLE_REGULAR
            if 'Italic' in style:
                fpdf_style = STYLE_ITALIC
            elif 'Bold' in style:
                fpdf_style = STYLE_BOLD

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