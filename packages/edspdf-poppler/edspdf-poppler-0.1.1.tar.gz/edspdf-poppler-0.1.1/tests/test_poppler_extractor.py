import pytest
from blocks_ground_truth import blank_blocks, pdf_blocks, styles_blocks

from edspdf_poppler import PopplerExtractor


def test_poppler(pdf, styles_pdf, blank_pdf):
    extractor = PopplerExtractor(extract_style=False)

    pytest.nested_approx(extractor(pdf).text_boxes, pdf_blocks, abs=5e-2)
    pytest.nested_approx(extractor(styles_pdf).text_boxes, styles_blocks, abs=5e-2)
    pytest.nested_approx(extractor(blank_pdf).text_boxes, blank_blocks, abs=5e-2)


def test_poppler_error(error_pdf):
    extractor = PopplerExtractor(extract_style=False, raise_on_error=True)

    with pytest.raises(OSError):
        extractor(error_pdf)

    extractor.raise_on_error = False
    result = extractor(error_pdf)
    assert len(result.text_boxes) == 0
    assert result.error is True
