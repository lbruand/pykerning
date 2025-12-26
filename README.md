# PyKerning

Python typesetting using fpdf2 instead of PySide2.

This project is a rewrite of the [python-typesetting](https://github.com/brandon-rhodes/python-typesetting) Steam example to use fpdf2 for PDF generation instead of Qt/PySide2.

## Overview

The original python-typesetting library provides TeX-inspired typesetting algorithms for paragraph formatting and PDF generation. While the original examples use PySide2 (Qt) for PDF rendering, this project demonstrates how to achieve the same professional results using fpdf2, a pure Python PDF library with no GUI framework dependencies.

## Features

- Professional paragraph justification using Knuth-Plass algorithm
- Widow and orphan line prevention
- Multi-page layout with headers and footers
- Support for multiple font styles (regular, italic, bold)
- Pure Python implementation with no Qt dependencies

## Installation

```bash
poetry install
```

## Usage

Generate the typeset PDF:

```bash
poetry run python examples/steam/typeset.py
```

This will create `book.pdf` in the `examples/steam/` directory - a professionally typeset version of the "Steam" essay.

## Running Tests

Run the test suite:

```bash
poetry run pytest tests/ -v
```

## Project Structure

- `pykerning/` - Main package
  - `writer_fpdf.py` - FpdfWriter class that implements the writer interface using fpdf2
- `examples/steam/` - Steam essay example
  - `typeset.py` - Main script that typesets the Steam essay
  - `steam.txt` - The essay text to be typeset
  - `fonts/` - Gentium Basic TrueType fonts (Regular, Italic, Bold)
- `tests/` - Pytest test suite for FpdfWriter

## Key Differences from Original

The main differences from the original python-typesetting examples:

1. **No Qt dependency**: Uses fpdf2 instead of PySide2/Qt
2. **Simpler setup**: No QApplication initialization needed
3. **Pure Python**: Works entirely with Python PDF generation libraries
4. **Same quality**: Maintains all the professional typesetting features

## Implementation Details

### FpdfWriter

The `FpdfWriter` class provides a drop-in replacement for the original `QtWriter`:

- `load_font(path)` - Load TrueType fonts
- `get_fonts(specs)` - Create font objects with proper metrics
- `new_page()` - Add new pages
- `set_font(font)` - Set active font
- `draw_text(x, y, text)` - Render text at coordinates

### Font Handling

Font metrics (ascent, descent, leading, width) are calculated to match the original Qt implementation, ensuring consistent layout and spacing.

## Credits

- Original python-typesetting library by Brandon Rhodes
- Steam essay by J. Elmer Rhodes, Jr. (1920-1995)
- Gentium Basic fonts by SIL International

## License

This project uses code adapted from python-typesetting. Please refer to the original repository for licensing information.