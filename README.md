# PyKerning

A self-contained Python typesetting library using fpdf2 for PDF generation.

PyKerning includes professional TeX-inspired typesetting algorithms (from Brandon Rhodes' python-typesetting) combined with fpdf2 for PDF generation, providing a pure Python solution with no Qt/PySide2 dependencies.

## Overview

This library combines:
- **Typesetting algorithms**: Knuth-Plass line breaking, widow/orphan prevention, and paragraph composition
- **PDF generation**: fpdf2-based writer for creating professional PDFs
- **Pure Python**: No GUI framework dependencies, works entirely with Python libraries

## Features

- **TeX-Quality Typesetting**: Knuth-Plass paragraph breaking algorithm for optimal line breaks
- **Widow/Orphan Prevention**: Automatic adjustment to prevent isolated lines
- **Hyphenation**: Frank Liang's hyphenation algorithm for professional text flow
- **Multi-page Layouts**: Single and multi-column layouts with headers and footers
- **Font Support**: Multiple font styles (regular, italic, bold) with accurate metrics
- **Pure Python**: No Qt/PySide2 dependencies, fully self-contained
- **fpdf2 Integration**: Modern PDF generation without external dependencies

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
  - `writer_fpdf.py` - PDF writer using fpdf2
  - `composing.py` - Composition and layout algorithms
  - `knuth.py` - Knuth-Plass paragraph breaking
  - `skeleton.py` - Layout data structures (Page, Column, Line, Font)
  - `vendored/` - TeX algorithms
    - `texlib_wrap.py` - TeX line breaking implementation
    - `hyphenate.py` - Hyphenation algorithm
- `examples/steam/` - Steam essay example
  - `typeset.py` - Example script demonstrating typesetting
  - `steam.txt` - The essay text to be typeset
  - `fonts/` - Gentium Basic TrueType fonts (Regular, Italic, Bold)
- `tests/` - Comprehensive pytest test suite
  - `test_writer_fpdf.py` - Tests for PDF writer (22 tests)
  - `test_typesetting.py` - Tests for typesetting algorithms (18 tests)

## Key Differences from python-typesetting

This project differs from the original python-typesetting library:

1. **Self-contained**: All typesetting algorithms are included in the package (no external git dependency)
2. **fpdf2 Integration**: Uses fpdf2 instead of Qt/PySide2 for PDF generation
3. **Simpler setup**: No QApplication initialization or GUI framework needed
4. **Full test coverage**: Includes 40 tests covering both PDF generation and typesetting algorithms

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

This project incorporates code and algorithms from several sources:

- **Typesetting algorithms**: From [python-typesetting](https://github.com/brandon-rhodes/python-typesetting) by Brandon Rhodes
- **Line breaking algorithm**: Based on "Breaking Paragraphs into Lines" by Knuth and Plass (1981)
- **Hyphenation algorithm**: Frank Liang's algorithm for TeX
- **Steam essay**: By J. Elmer Rhodes, Jr. (1920-1995)
- **Gentium Basic fonts**: By SIL International

## License

This project includes code from python-typesetting by Brandon Rhodes. The typesetting algorithms (`composing.py`, `knuth.py`, `skeleton.py`, and `vendored/`) are adapted from that project. Please refer to the [original repository](https://github.com/brandon-rhodes/python-typesetting) for licensing information.