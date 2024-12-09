import os
import sys
import time
import shutil
from dotenv import load_dotenv
load_dotenv()

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

def extract_content_from_pdf(pdf_path):
    # Set up parser
    parser = LlamaParse(
        result_type="markdown"  # "markdown" and "text" are available
    )

    # Use SimpleDirectoryReader to parse the file
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=[pdf_path], file_extractor=file_extractor).load_data()

    # Get the PDF filename without extension
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Create output folder path
    output_folder = os.path.join(os.getcwd(), 'test-pdfs', pdf_name)
    os.makedirs(output_folder, exist_ok=True)

    # Move PDF file to the new folder
    new_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path))
    if pdf_path != new_pdf_path:  # Only copy if not already in destination
        shutil.copy2(pdf_path, new_pdf_path)

    # Create output file path
    output_path = os.path.join(output_folder, f'{pdf_name}_extracted_llama.md')

    # Write the extracted content to markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(doc.text)
            
    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python llama_parse_parser.py <pdf_filename>")
        sys.exit(1)
        
    pdf_filename = sys.argv[1]
    pdf_path = os.path.join("test-pdfs", pdf_filename)
    
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found")
        sys.exit(1)

    start_time = time.time()
    output_path = extract_content_from_pdf(pdf_path)
    end_time = time.time()
    processing_time = end_time - start_time

    print(f"PDF processed successfully. Output saved to: {output_path}")
    print(f"Processing time: {processing_time:.2f} seconds ({processing_time/60:.2f} minutes)")

    # Remove the original PDF
    os.remove(pdf_path)
