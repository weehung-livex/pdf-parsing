import anthropic
import base64
from dotenv import load_dotenv
import os
import sys
import shutil
import tiktoken  # for token counting
from PyPDF2 import PdfReader, PdfWriter
import io

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

def estimate_tokens(text):
    """Estimate the number of tokens in a text using tiktoken"""
    encoding = tiktoken.get_encoding("cl100k_base")  # Claude uses cl100k_base encoding (estimation)
    return len(encoding.encode(text))

def process_pdf(pdf_path):
    try:

        layout_extraction_prompt = """You are a PDF layout extraction tool. Your task is to analyze and output just the structural layout and formatting of this PDF document as an empty template.

Output the bare layout structure in markdown format showing only:
# 
## 
### 
- 
  - 
    - 
| | | |
|-|-|-|
| | | |
"""

        extraction_prompt = """You are a PDF text extraction tool. Extract and output ALL text content from this PDF document exactly as it appears, with absolutely no modifications or meta-commentary.

        Always continue extracting the next part of the document. DO NOT stop.
Format requirements:
- Use markdown formatting
- Preserve all headers (#, ##, etc)
- Maintain **bold** text
- Keep all bullet points and numbering
- Include all tables and code blocks
- Include all image descriptions

ABSOLUTELY PROHIBITED - DO NOT ADD:
- "[Content continues...]"
- "[Content continues in next part...]"
- "[Continued in next message...]"
- Any text about continuation or length
- Any explanatory notes or comments
- Any indication that content is incomplete
- Any summaries of remaining content

IMPORTANT: If you reach a token limit:
1. Stop at the last complete sentence or section
2. Do not add ANY indication that you're stopping
3. Do not mention there's more content
4. Do not summarize remaining content
5. leave a note that you've reached the token limit

Output only the raw document content in markdown. Nothing else."""
# Validate input PDF
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        # Get file size for debugging
        file_size = os.path.getsize(pdf_path)
        print(f"Input PDF size: {file_size} bytes")
        
        # Read and encode the entire PDF
        with open(pdf_path, 'rb') as file:
            pdf_data = base64.b64encode(file.read()).decode('utf-8')
        
        # Create Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Estimate tokens for the input pdf
        prompt_tokens = estimate_tokens(pdf_data)
        print(f"input tokens: {prompt_tokens}")
        
        reader = PdfReader(pdf_path)
        num_pages = len(reader.pages)
        max_input_tokens = 200000000  # Adjust this value for chunking
        current_chunk = []
        current_tokens = 0
        all_extracted_text = []
        
        # First pass: determine page groupings based on tokens
        page_chunks = []
        current_chunk_pages = []
        
        for page_num in range(num_pages):
            # Create temporary PDF with single page
            temp_writer = PdfWriter()
            temp_writer.add_page(reader.pages[page_num])
            
            # Save to memory buffer and encode
            temp_buffer = io.BytesIO()
            temp_writer.write(temp_buffer)
            temp_buffer.seek(0)
            page_data = base64.b64encode(temp_buffer.read()).decode('utf-8')
            
            page_tokens = estimate_tokens(page_data)
            
            if page_tokens > max_input_tokens:
                print(f"Warning: Page {page_num + 1} alone exceeds token limit ({page_tokens} tokens)")
                # Process this page alone
                if current_chunk_pages:
                    page_chunks.append(current_chunk_pages)
                page_chunks.append([page_num])
                current_chunk_pages = []
                current_tokens = 0
            elif current_tokens + page_tokens > max_input_tokens:
                # Start new chunk
                page_chunks.append(current_chunk_pages)
                current_chunk_pages = [page_num]
                current_tokens = page_tokens
            else:
                current_chunk_pages.append(page_num)
                current_tokens += page_tokens
        
        # Add final chunk if exists
        if current_chunk_pages:
            page_chunks.append(current_chunk_pages)
        
        # Process each chunk
        for chunk_idx, page_numbers in enumerate(page_chunks):
            print(f"Processing chunk {chunk_idx + 1}/{len(page_chunks)} (pages {min(page_numbers) + 1}-{max(page_numbers) + 1})")
            
            # Create PDF with these pages
            pdf_writer = PdfWriter()
            for page_num in page_numbers:
                pdf_writer.add_page(reader.pages[page_num])
            
            # Save to memory and encode
            pdf_buffer = io.BytesIO()
            pdf_writer.write(pdf_buffer)
            pdf_buffer.seek(0)
            pdf_chunk_data = base64.b64encode(pdf_buffer.read()).decode('utf-8')
            
            chunk_tokens = estimate_tokens(pdf_chunk_data)
            print(f"Chunk tokens: {chunk_tokens}")
            
            try:
                message = client.beta.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    betas=["pdfs-2024-09-25"],
                    max_tokens=8192,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                # place pdf data first, before text prompt
                                {
                                    "type": "document",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "application/pdf",
                                        "data": pdf_chunk_data
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": extraction_prompt
                                }
                            ]
                        }
                    ]
                )
                
                # print out the output tokens
                print("input tokens: ", message.json())
                output_tokens = estimate_tokens(message.content[0].text)
                print(f"estimated output tokens: {output_tokens}")
                
                all_extracted_text.append(message.content[0].text)
                
            except anthropic.BadRequestError as e:
                print(f"Error processing chunk {chunk_idx + 1}: {str(e)}")
                continue
        
        # Combine all chunks
        extracted_text = "\n\n".join(all_extracted_text)
        
        # Write to file
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_folder = os.path.join(os.getcwd(), 'test-pdfs', pdf_name)
        output_path = os.path.join(output_folder, f'{pdf_name}_extracted_anthropic.md')
        
        os.makedirs(output_folder, exist_ok=True)
        with open(output_path, 'w') as file:
            file.write(extracted_text)
        
        return output_path
        
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_anthropic.py <pdf_filename>")
        sys.exit(1)
        
    pdf_filename = sys.argv[1]
    pdf_path = os.path.join("test-pdfs", pdf_filename)
    
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} does not exist")
        sys.exit(1)
        
    process_pdf(pdf_path)
