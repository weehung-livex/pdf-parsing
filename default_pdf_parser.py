# Standard library imports
import io
import base64
import os
import shutil
import sys
import time

# Third-party imports
import pdfplumber

def extract_content_from_pdf(pdf_path):
    # Open the PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        extracted_content = []
        
        # Iterate through each page
        for i, page in enumerate(pdf.pages):
            # Extract text from the page
            text = page.extract_text()
            if text:
                extracted_content.append(text)
            else:
                print(f"Warning: No text found on page {i + 1}")
                extracted_content.append("")
    
    # Create folder with same name as PDF in test-pdfs directory
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(os.getcwd(), 'test-pdfs', pdf_name)
    os.makedirs(output_folder, exist_ok=True)
    
    # Move PDF file to the new folder
    new_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path))
    if pdf_path != new_pdf_path:  # Only copy if not already in destination
        shutil.copy2(pdf_path, new_pdf_path)
    
    # Update output path to use the new folder
    output_path = os.path.join(output_folder, f'{pdf_name}_extracted_text.md')
    result = []
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write content from each page
        for i, content in enumerate(extracted_content, 1):
            f.write(f"# Page {i}\n\n")
            f.write(content)
            f.write("\n\n---\n\n")
            result.append(content)
    return output_path, result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python default_pdf_parser.py <pdf_filename>")
        sys.exit(1)
        
    pdf_filename = sys.argv[1]
    pdf_path = os.path.join("test-pdfs", pdf_filename)
    
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found")
        sys.exit(1)
    
    start_time = time.time()
    extract_content_from_pdf(pdf_path)
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Processing time for Default PDF Parser: {processing_time:.2f} seconds ({processing_time/60:.2f} minutes)")

    # remove the original pdf
    os.remove(pdf_path)
    print("Parsing")