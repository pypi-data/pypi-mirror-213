![Tests](https://img.shields.io/github/actions/workflow/status/aphp/edspdf-poppler/tests.yml?branch=main&label=tests&style=flat-square)
[![Documentation](https://img.shields.io/github/actions/workflow/status/aphp/edspdf-poppler/documentation.yml?branch=main&label=docs&style=flat-square)](https://aphp.github.io/edspdf-poppler/latest/)
[![PyPI](https://img.shields.io/pypi/v/edspdf-poppler?color=blue&style=flat-square)](https://pypi.org/project/edspdf-poppler/)
[![Codecov](https://img.shields.io/codecov/c/github/aphp/edspdf-poppler?logo=codecov&style=flat-square)](https://codecov.io/gh/aphp/edspdf-poppler)
[![DOI](https://zenodo.org/badge/517726737.svg)](https://zenodo.org/badge/latestdoi/517726737)

# edspdf-poppler

edspdf-poppler provides a Poppler-based PDF parser component for [EDS-PDF](https://github.com/aphp/edspdf).
We only provide prebuilt binaries for linux and macos. If you are on windows, you will need to build this lib from source.

Beware, Poppler is **GPL-licensed**: edspdf-poppler is therefore also GPL-licensed, and any model depending on this component must be too.

## Getting started

Install the library with pip:

<div class="termy">

```console
$ pip install edspdf-poppler
```

</div>

## Usage

```
from edspdf import Pipeline

model = Pipeline()
model.add_pipe('poppler-extractor')

model(pdf_bytes)
```

Visit the [documentation](https://aphp.github.io/edspdf-poppler/) for more information!

## Acknowledgement

We would like to thank [Assistance Publique – Hôpitaux de Paris](https://www.aphp.fr/)
and [AP-HP Foundation](https://fondationrechercheaphp.fr/) for funding this project.
