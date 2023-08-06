import warnings
from typing import Union
from typing_extensions import Literal

from edspdf import registry, Pipeline
from edspdf.structures import Page, PDFDoc, TextBox, TextProperties

try:
    from .bindings import Document
except ModuleNotFoundError:
    raise ImportError(
        "Poppler was not correctly built, you won't be able to use the "
        "poppler-extractor component to parse PDFs."
    )

__version__ = "0.1.1"


@registry.factory.register("poppler-extractor")
class PopplerExtractor:
    """
    We provide a PDF line extractor built on top of
    [Poppler](https://poppler.freedesktop.org/).

    The poppler software is more difficult to install than its
    [`pdfminer-extractor`][edspdf.pipes.extractors.pdfminer.PdfMinerExtractor] and
    [`mupdf-extractor`][edspdf_mupdf.MuPdfExtractor] counterparts.
    In particular, the bindings we provide have not been tested on Windows.

    !!! warning "License"

        Beware, Poppler is distributed under the GPL license, therefore so is this
        component, and any model depending on this component must be too.

    Installation
    ------------

    For the licensing reason mentioned above, the `poppler-extractor` component is
    distributed in a separate package `edspdf-poppler`. To install it, use your favorite
    Python package manager :

    ```bash
    poetry add edspdf-poppler
    # or
    pip install edspdf-poppler
    ```

    Example
    -------

    === "API-based"

        ```python
        pipeline.add_pipe(
            "poppler-extractor",
            config=dict(
                extract_style=False,
            ),
        )
        ```

    === "Configuration-based"

        ```toml
        [components.poppler-extractor]
        @factory = "poppler-extractor"
        extract_style = false
        ```

    and use it as follows:

    ```python
    from pathlib import Path

    # Apply on a new document
    pipeline(Path("path/to/your/pdf/document").read_bytes())
    ```

    Parameters
    ----------
    pipeline: Pipeline
        The pipeline object
    name: str
        The name of the component
    extract_style : bool
        Extract style
    raise_on_error: bool
        Whether to raise an error when parsing a corrupted PDF (defaults to False)
    sort_mode: Literal["lines", "none"]
        Box sorting mode

        - "lines": sort by lines, without preserving the order of lines inside blocks
        - "none": do not sort boxes
    """

    def __init__(
        self,
        pipeline: Pipeline = None,
        name: str = "poppler-extractor",
        extract_style: bool = False,
        raise_on_error: bool = False,
        sort_mode: Literal["lines", "none"] = "none",
    ):
        self.extract_style = extract_style
        self.sort_mode = sort_mode
        self.raise_on_error = raise_on_error

    def __call__(self, doc: Union[PDFDoc, bytes]) -> PDFDoc:
        if isinstance(doc, bytes):
            content = doc
            doc = PDFDoc(id=str(hash(content)), content=content)
        else:
            content = doc.content

        try:
            poppler_doc = Document(content, extract_style=self.extract_style)
            pages = doc.pages = []

            content_boxes = []
            for page_num, page in enumerate(poppler_doc):
                page_w, page_h = page.size

                for flow in page:
                    for block in flow:
                        for line in block:
                            if len(line.text) == 0:
                                continue
                            if self.extract_style:
                                styles = [
                                    TextProperties(
                                        fontname=style.font_name,
                                        italic=style.is_italic,
                                        bold=style.is_bold,
                                        begin=style.begin,
                                        end=style.end,
                                    )
                                    for style in line.styles
                                ]
                            else:
                                styles = []
                            if (
                                line.x0 < 0
                                or line.y0 < 0
                                or line.x1 > page_w
                                or line.y1 > page_h
                            ):
                                continue

                            content_boxes.append(
                                TextBox(
                                    doc=doc,
                                    x0=line.x0 / page_w,
                                    y0=line.y0 / page_h,
                                    x1=line.x1 / page_w,
                                    y1=line.y1 / page_h,
                                    text=line.text,
                                    page_num=page_num,
                                    props=styles,
                                )
                            )
                pages.append(
                    Page(
                        doc=doc,
                        page_num=page_num,
                        width=page_w,
                        height=page_h,
                    )
                )

            if self.sort_mode == "lines":
                content_boxes = sorted(content_boxes)
            doc.content_boxes.extend(content_boxes)

        except Exception:
            if self.raise_on_error:
                raise
            doc.pages = []
            doc.error = True
            return doc

        return doc
