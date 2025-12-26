"""PyKerning - Python typesetting using fpdf2.

This package includes:
- FpdfWriter and FpdfFont for PDF generation using fpdf2
- Typesetting algorithms from python-typesetting (composing, knuth, skeleton)
- TeX line breaking and hyphenation algorithms
"""

from pykerning.writer_fpdf import FpdfWriter, FpdfFont

# Typesetting modules are available as submodules:
# from pykerning.composing import ...
# from pykerning.knuth import ...
# from pykerning.skeleton import ...

__all__ = ['FpdfWriter', 'FpdfFont']