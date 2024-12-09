# Standard library imports
import io
import json
import base64
import os

# Third-party imports
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from env
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# i need to parse the pdf file and extract the text, images, and tables
# i could use existing libraries like pdfplumber or camelot
# the purpose of this script is to experiment with gpt4o vision in extracting text, images, and tables

def convert_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def extract_content_from_pdf(pdf_path):
    # Read PDF file as bytes
    with open(pdf_path, 'rb') as file:
        pdf_bytes = file.read()
    
    # Create base64 string of PDF
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    
    # Prepare the prompt for GPT-4 Vision
    prompt = """Please analyze this PDF and extract:
    1. Text content
    2. Tables (if any)
    3. Image descriptions (if any)
    
    Format the response as JSON with the following structure:
    {
        "text": ["paragraph1", "paragraph2", ...],
        "tables": [{"caption": "table description", "content": "table content"}, ...],
        "images": [{"description": "image description", "location": "brief location description"}, ...]
    }"""
    
    # Call GPT-4 Vision API
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:application/pdf;base64,{base64_pdf}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=4096
    )
    
    # Track token usage
    tokens_used = response.usage.total_tokens
    total_tokens = tokens_used
    print(f"\nUsed {tokens_used} tokens")
    
    # Get the raw response content
    raw_content = response.choices[0].message.content
    
    # Try to parse as JSON, but store raw content if parsing fails
    try:
        content = json.loads(raw_content)
    except json.JSONDecodeError:
        content = {
            "raw_content": raw_content,
            "parse_error": "Could not parse as JSON"
        }
    
    content["page_number"] = 1
    content["tokens_used"] = tokens_used
    
    print(f"\nTotal tokens used: {total_tokens}")
    print(f"Average tokens per page: {total_tokens / 1:.2f}")
    
    # Save extracted content
    output_path = pdf_path.replace('.pdf', '_extracted_openai.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    return output_path

if __name__ == "__main__":
    output_file = extract_content_from_pdf("test-pdfs/TP-MVD8MV2.pdf")
    print(f"PDF processed successfully. Output saved to: {output_file}")
