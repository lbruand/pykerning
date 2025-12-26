"""Tests for FpdfWriter and FpdfFont classes."""

import pytest
from pathlib import Path
import tempfile
import os
from fpdf import FPDF

from writer_fpdf import FpdfWriter, FpdfFont


class TestFpdfFont:
    """Tests for the FpdfFont class."""

    @pytest.fixture
    def pdf(self):
        """Create a basic PDF instance for testing."""
        return FPDF(unit='pt', format=(612, 792))

    @pytest.fixture
    def font(self, pdf):
        """Create a basic FpdfFont instance for testing."""
        return FpdfFont(pdf, 'Helvetica', '', 12)

    def test_init(self, pdf):
        """Test FpdfFont initialization."""
        font = FpdfFont(pdf, 'Helvetica', '', 12)
        assert font.pdf is pdf
        assert font.font_family == 'Helvetica'
        assert font.font_style == ''
        assert font.font_size == 12
        assert font.height == 12

    def test_font_metrics(self, font):
        """Test that font metrics are calculated correctly."""
        assert font.height == 12
        assert font.ascent == 12 * 0.8
        assert font.descent == 12 * 0.2
        assert font.leading == 12 * 0.2

    def test_font_metrics_different_size(self, pdf):
        """Test font metrics with different font size."""
        font = FpdfFont(pdf, 'Helvetica', '', 24)
        assert font.height == 24
        assert font.ascent == 24 * 0.8
        assert font.descent == 24 * 0.2
        assert font.leading == 24 * 0.2

    def test_width_of_text(self, pdf):
        """Test width_of method returns a numeric value."""
        # Need to set up the font properly in the PDF
        pdf.add_page()
        font = FpdfFont(pdf, 'Helvetica', '', 12)

        width = font.width_of('Hello')
        assert isinstance(width, (int, float))
        assert width > 0

    def test_width_of_empty_string(self, pdf):
        """Test width_of with empty string."""
        pdf.add_page()
        font = FpdfFont(pdf, 'Helvetica', '', 12)

        width = font.width_of('')
        assert width == 0

    def test_width_of_longer_text_is_larger(self, pdf):
        """Test that longer text has larger width."""
        pdf.add_page()
        font = FpdfFont(pdf, 'Helvetica', '', 12)

        width_short = font.width_of('Hi')
        width_long = font.width_of('Hello World')
        assert width_long > width_short

    def test_width_of_preserves_pdf_font(self, pdf):
        """Test that width_of preserves the PDF's current font."""
        pdf.add_page()
        pdf.set_font('Helvetica', '', 10)

        font = FpdfFont(pdf, 'Times', 'B', 12)
        font.width_of('Test')

        # PDF should still have the original font (fpdf2 uses lowercase)
        assert pdf.font_family == 'helvetica'
        assert pdf.font_size_pt == 10


class TestFpdfWriter:
    """Tests for the FpdfWriter class."""

    @pytest.fixture
    def temp_pdf_path(self):
        """Create a temporary file path for PDF output."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            path = f.name
        yield path
        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    @pytest.fixture
    def writer(self, temp_pdf_path):
        """Create a FpdfWriter instance for testing."""
        return FpdfWriter(temp_pdf_path, 612, 792)

    def test_init(self, temp_pdf_path):
        """Test FpdfWriter initialization."""
        writer = FpdfWriter(temp_pdf_path, 612, 792)

        assert writer.path == temp_pdf_path
        assert writer.width_pt == 612
        assert writer.height_pt == 792
        assert isinstance(writer.pdf, FPDF)
        assert writer.loaded_fonts == {}
        assert writer.fonts == {}
        assert writer.current_font is None

    def test_init_width_height_conversion(self, temp_pdf_path):
        """Test that width and height are converted to mm correctly."""
        writer = FpdfWriter(temp_pdf_path, 72, 72)

        # 1 point = 1/72 inch, 1 inch = 25.4 mm
        # 72 points = 1 inch = 25.4 mm
        assert abs(writer.width_mm - 25.4) < 0.01
        assert abs(writer.height_mm - 25.4) < 0.01

    def test_close_creates_file(self, temp_pdf_path):
        """Test that close() creates the PDF file."""
        writer = FpdfWriter(temp_pdf_path, 612, 792)
        writer.close()

        assert os.path.exists(temp_pdf_path)
        assert os.path.getsize(temp_pdf_path) > 0

    def test_load_font_nonexistent_file(self, writer):
        """Test that load_font raises FileNotFoundError for nonexistent file."""
        with pytest.raises(FileNotFoundError, match="Font file not found"):
            writer.load_font('nonexistent_font.ttf')

    def test_load_font_with_existing_file(self, writer):
        """Test loading an existing font file."""
        # This test assumes the fonts directory exists
        font_path = 'fonts/GenBasR.ttf'
        if os.path.exists(font_path):
            writer.load_font(font_path)
            assert str(Path(font_path)) in writer.loaded_fonts
            family, style = writer.loaded_fonts[str(Path(font_path))]
            assert family == 'GentiumBasic'
            assert style == ''
        else:
            pytest.skip("Font file not available for testing")

    def test_load_font_italic(self, writer):
        """Test loading an italic font."""
        font_path = 'fonts/GenBasI.ttf'
        if os.path.exists(font_path):
            writer.load_font(font_path)
            family, style = writer.loaded_fonts[str(Path(font_path))]
            assert family == 'GentiumBasic'
            assert style == 'I'
        else:
            pytest.skip("Font file not available for testing")

    def test_load_font_bold(self, writer):
        """Test loading a bold font."""
        font_path = 'fonts/GenBasB.ttf'
        if os.path.exists(font_path):
            writer.load_font(font_path)
            family, style = writer.loaded_fonts[str(Path(font_path))]
            assert family == 'GentiumBasic'
            assert style == 'B'
        else:
            pytest.skip("Font file not available for testing")

    def test_get_fonts(self, writer):
        """Test get_fonts method."""
        font_specs = [
            ('roman', 'Gentium Basic', 'Regular', 12),
            ('italic', 'Gentium Basic', 'Italic', 12),
            ('title', 'Gentium Basic', 'Regular', 24),
        ]

        fonts = writer.get_fonts(font_specs)

        assert len(fonts) == 3
        assert 'roman' in fonts
        assert 'italic' in fonts
        assert 'title' in fonts

        assert isinstance(fonts['roman'], FpdfFont)
        assert fonts['roman'].font_size == 12
        assert fonts['title'].font_size == 24

    def test_get_fonts_stores_fonts(self, writer):
        """Test that get_fonts stores fonts in the writer."""
        font_specs = [('roman', 'Gentium Basic', 'Regular', 12)]
        fonts = writer.get_fonts(font_specs)

        assert writer.fonts == fonts

    def test_get_fonts_style_mapping(self, writer):
        """Test that font styles are mapped correctly."""
        font_specs = [
            ('regular', 'Gentium Basic', 'Regular', 12),
            ('italic', 'Gentium Basic', 'Italic', 12),
            ('bold', 'Gentium Basic', 'Bold', 12),
        ]

        fonts = writer.get_fonts(font_specs)

        assert fonts['regular'].font_style == ''
        assert fonts['italic'].font_style == 'I'
        assert fonts['bold'].font_style == 'B'

    def test_new_page(self, writer):
        """Test new_page method."""
        initial_page_count = writer.pdf.page
        writer.new_page()
        assert writer.pdf.page == initial_page_count + 1

    def test_set_font(self, writer):
        """Test set_font method."""
        font = FpdfFont(writer.pdf, 'Helvetica', '', 12)
        writer.set_font(font)

        assert writer.current_font is font
        assert writer.pdf.font_family == 'helvetica'
        assert writer.pdf.font_size_pt == 12

    def test_draw_text(self, writer):
        """Test draw_text method."""
        # Set up a font first
        writer.pdf.set_font('Helvetica', '', 12)

        # This should not raise an exception
        writer.draw_text(100, 100, 'Test text')

    def test_integration_create_simple_pdf(self, temp_pdf_path):
        """Integration test: Create a simple PDF with text."""
        writer = FpdfWriter(temp_pdf_path, 612, 792)

        # Create a font and draw some text
        font = FpdfFont(writer.pdf, 'Helvetica', '', 12)
        writer.set_font(font)
        writer.draw_text(100, 100, 'Hello, World!')

        # Save the PDF
        writer.close()

        # Verify the file was created and has content
        assert os.path.exists(temp_pdf_path)
        assert os.path.getsize(temp_pdf_path) > 0

    def test_integration_multiple_pages(self, temp_pdf_path):
        """Integration test: Create a PDF with multiple pages."""
        writer = FpdfWriter(temp_pdf_path, 612, 792)

        font = FpdfFont(writer.pdf, 'Helvetica', '', 12)
        writer.set_font(font)

        # First page
        writer.draw_text(100, 100, 'Page 1')

        # Second page
        writer.new_page()
        writer.draw_text(100, 100, 'Page 2')

        writer.close()

        assert os.path.exists(temp_pdf_path)
        assert os.path.getsize(temp_pdf_path) > 0
