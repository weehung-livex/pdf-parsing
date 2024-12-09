# PDF Enhancement Project

This project provides tools for parsing and analyzing PDF documents using different AI models.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

For running the respective parser, use the following command:

The target pdf file is specified as the first argument and should exist in the `test-pdfs` folder.

```bash
python pdf_anthropic.py test.pdf
```

The output will be saved in the `test-pdfs` folder with the same name as the input file, but with the model as suffix: like `test.pdf_extracted_anthropic.md`

For evaluating the output, under the test-pdfs folder, run

```bash
python evaluation.py <folder-name>
```

For this evaluation, there must be a `original.txt` file in the test-pdfs folder as reference.
