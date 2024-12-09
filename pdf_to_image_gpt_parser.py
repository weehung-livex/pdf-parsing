# Standard library imports
import io
import json
import base64
import os
import shutil
import sys
import time

# Third-party imports
from pdf2image import convert_from_path
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

from default_pdf_parser import extract_content_from_pdf as extract_text_from_pdf

# Load environment variables
load_dotenv()

# MODEL = ["gpt-4o-mini", "gpt-4o", "gpt-4-vision-preview"] # have tested and decided to use gpt-4o-2024-11-20 instead
MODEL = ["gpt-4o-2024-11-20"]

# Prepare the prompt for GPT-4 Vision
ORIGINAL_PROMPT = """Please analyze this page and extract ALL text and content exactly as it appears, formatted in clean markdown.

        Important instructions:
        1. Extract everything in the exact order it appears on the page.
        2. Use proper markdown formatting:
        - # for main headings
        - ## for sub-headings
        - ### for smaller headings
        - Regular paragraphs as it is
        - Preserve nested bullet lists and numbered lists
        - Numbered lists with 1., 2., etc.
        - Tables using | markdown table syntax
        3. For texts, extract them exactly as it appears - do not summarize or modify.
        4. For images with texts, extract the texts without altering the original text and place them immediately after the respective image IF they are relevant to the neighboring texts.
        5. Preserve any special formatting like bold, italic, or code blocks if present.
        6. Ensure all text styles such as underline, strikethrough, and hyperlinks are properly captured using Markdown syntax where applicable. Use [Link Text](URL) for hyperlinks.
        7. If there are different font sizes to indicate hierarchy or emphasis, please use appropriate Markdown syntax (e.g., # for large headings, ## for smaller headings, etc.).
        8. For images, tables, and diagrams, include any captions or alt text provided in the document, and ensure it is placed directly below the visual element.
        9. If there are URLs or embedded links, preserve them and format them correctly as markdown links.
        10. For tables, if there are headers, use the appropriate pipe (`|`) characters to separate headers from content, and use `---` to separate the header row from the data rows.

        Format your entire response as markdown formatted text, need not include ```markdown at the beginning and end, maintaining the exact document structure and all content.
        """

def get_prompt_v1(context):
    '''Simple function that appends context to the base prompt.
    
    Args:
        context (str): The context text to append to the prompt
        
    Returns:
        str: The complete prompt with context appended
    '''
    print(f"Context in get_prompt_v1: {context}")
    return ORIGINAL_PROMPT + f"\n\nHere is the context for this page: {context}"

def get_prompt_v2(context):
    '''
    This prompt is used to extract additional text from images that is not already present in the context.
    '''
    print(f"Context in get_prompt_v2: {context}")
    return f"""Format the provided context text in proper markdown structure while preserving the exact PDF layout. Only extract additional text if it appears in images and is not already present in the context.

Key instructions:
1. Use the provided context as the primary source of text - do not modify or add to it.
2. Retain the exact order of information as it appears in the PDF image.
3. Format the context text using appropriate markdown:
   - Headings (#, ##, ###)
   - Lists (bullet points, numbers)
   - Tables (| syntax)
   - Code blocks (```)
4. Only extract new text if it appears in images and is missing from the context.
5. Maintain the exact document structure and hierarchy as shown in the PDF.
6. Do not summarize, interpret, or add any additional content. If it was a text block in the PDF, output a text block. If it was a nested bullet list, show it as a nested bullet list.

Context for this page: {context}"""

def get_prompt_v3(context):
    """
    Enhanced prompt that strictly preserves context text while only extracting missing visual elements
    and additional text from images that isn't present in the context.
    """
    print(f"Context in get_prompt_v3: {context}")
    return f"""You are tasked with creating a perfectly formatted markdown document. The context provided contains the accurate text content, which MUST be preserved exactly.

Your primary tasks:
1. Use the provided context text AS-IS - do not rephrase, modify, or remove ANY text from it
2. Format the context using proper markdown syntax while maintaining the exact structure:
   - Preserve all headings, lists, and paragraphs exactly as they appear
   - Use appropriate markdown for formatting (headers #, lists -, tables |)
3. ONLY add content in these specific cases:
   - Text that appears in images but is completely missing from the context
   - Image captions or labels that aren't in the context
   - Visual elements like diagrams, charts, or tables that need description
   - Mathematical formulas or special symbols that may have been missed

DO NOT:
- Do not rephrase or modify any text from the context
- Do not remove any content from the context
- Do not reorder the information
- Do not add explanatory text or interpretations

Context for this page (this text must be preserved exactly):
{context}

If you find additional text in the image that's not in the context above, insert it in the appropriate location using [IMAGE: additional text] markup."""

def get_prompt_v4(context):
    """
    Highly precise prompt focused on maximum context retention with minimal modifications.
    Target: 100% match rate with original context.
    """
    return f"""You are a precise text preservation system. Your ABSOLUTE PRIORITY is to retain the exact text from the provided context with 100% accuracy.

CRITICAL INSTRUCTION: The text in the context below must be preserved exactly.

Step 1: EXACT PRESERVATION
- Copy the context text VERBATIM - every single character matters
- Maintain exact spacing, line breaks, and formatting
- Keep all special characters, including Chinese characters, exactly as shown
- Preserve URLs, file paths, and technical terms without any modification
- For code blocks, use triple backticks (```) - never nest them

Step 2: FORMATTING
- Apply markdown syntax WITHOUT changing any text content
- Use proper markdown formatting:
    - Assign headings (# or ## or ###) to the text exactly as they appear, without changing the content
    - Regular paragraphs as is
    - Maintain nexted list items (-) and numbered lists (1., 2., etc.) precisely as shown
    - Tables using | markdown table syntax
- Preserve all numbers, percentages, and statistics exactly
- Ensure code blocks are properly closed and never nested
- Do not use any markdown quote indicators

Step 3: STRICT RULES
NEVER:
- Rephrase or reword ANY text from the context
- Include texts from UI screenshots or application screens
- Use nested or multiple triple backticks for code blocks
- Use any markdown quote indicators

LIMITATIONS OF THE CONTEXT:
- The context may not contain all the text from the page, especially if it is a label or description
- The context may not be show text in order, if the text is overlapping or rotated

RARE CASES:
If text provided in context does not make sense in the image due to being rotated or overlapping, 
override with your best judgement

FOR DIAGRAMS, CHARTS, AND TABLES:
- only include labels or short descriptions found in the image

Here is the context that MUST be preserved exactly:
{context}

Remember: Your success is measured by achieving 100% match with the original context."""

def get_prompt_v5(context):
    """
    Two-step prompt that first extracts text from images, then cross-references with context
    for maximum accuracy while maintaining logical flow.
    """
    return f"""You are a precise document analysis system working in two steps:

STEP 1: TEXT EXTRACTION
First, analyze the image and extract all visible text content (excluding UI screenshots):
- Extract all headings, paragraphs, lists, and table content
- Include text from diagrams and charts (but not from UI/application screenshots)
- Maintain the exact order and hierarchy as shown
- Use appropriate markdown formatting (headings #, lists -, tables |)
- Preserve all special characters, numbers, and formatting

STEP 2: CONTEXT VALIDATION & REFINEMENT
Then, compare your extraction with this context and make intelligent adjustments:
- If the context version of a text block is more complete or logical, use it instead
- When the context shows better paragraph organization or heading hierarchy, adopt it
- If the context contains technical terms or specific formatting that matches the image, preserve it
- For overlapping or rotated text, prefer the context version if it makes more logical sense

FORMATTING RULES:
- Use proper markdown syntax:
    - Headings: #, ##, ### (matching visual hierarchy)
    - Lists: - for bullets, 1. for numbered items
    - Tables: | markdown syntax
    - Code blocks: ``` (never nested)
- Preserve exact spacing and line breaks where meaningful
- Keep all special characters and technical terms intact

STRICT GUIDELINES:
- Never include text from UI screenshots or application screens
- Don't use nested code blocks or quote indicators
- Maintain consistent heading levels throughout
- Preserve URLs and file paths exactly as shown

Context for cross-reference and validation:
{context}

Output the final, refined version that combines accurate image extraction with context validation."""

# Initialize OpenAI client with API key from env
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def convert_image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def extract_content_from_pdf(model, pdf_path):
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    output_path, result = extract_text_from_pdf(pdf_path)
    
    extracted_content = []
    total_tokens = 0
    message_history = []  # Store conversation history
    
    for i, image in enumerate(images):
        # Convert image to base64
        base64_image = convert_image_to_base64(image)
        
        # Build current message with context from only the previous page
        current_messages = [
            {
                "role": "system",
                "content": f"You are processing page {i+1} of a {len(images)}-page document. Maintain consistent heading levels and formatting with previous pages."
            }
        ]
        
        # Add only the previous page's messages (2 messages - user + assistant)
        current_messages.extend(message_history[-2:])  # Changed from -4: to -2:
        
        # Add current page request
        current_messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": get_prompt_v5(result[i]),
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    },
                },
            ],
        })
        
        response = client.chat.completions.create(
            model=model,
            messages=current_messages,
            max_tokens=2000
        )

        # Store the conversation history
        message_history.append({
            "role": "user",
            "content": f"Page {i+1} content: {result[i]}"  # Store simplified version to save tokens
        })
        message_history.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        
        # Track token usage and store content as before
        tokens_used = response.usage.total_tokens
        total_tokens += tokens_used
        print(f"\nPage {i + 1}: Used {tokens_used} tokens")
        content = response.choices[0].message.content
        extracted_content.append(content)
    
    print(f"\nTotal tokens used: {total_tokens}")
    print(f"Average tokens per page: {total_tokens / len(images):.2f}")

    finalised_markdown = "\n".join(extracted_content)
    # wrap around ```markdown
    finalised_markdown = f"```markdown\n{finalised_markdown}\n```"
    
    # Create folder with same name as PDF in test-pdfs directory
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(os.getcwd(), 'test-pdfs', pdf_name)
    os.makedirs(output_folder, exist_ok=True)
    
    # Move PDF file to the new folder
    new_pdf_path = os.path.join(output_folder, os.path.basename(pdf_path))
    if pdf_path != new_pdf_path:  # Only copy if not already in destination
        shutil.copy2(pdf_path, new_pdf_path)
    
    # Update output path to use the new folder
    output_path = os.path.join(output_folder, f'{pdf_name}_extracted_openai_{model}_v5.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write statistics header
        # f.write(f'# Document Processing Statistics for model: {model}\n\n')
        # f.write(f"- Total Pages: {len(images)}\n")
        # f.write(f"- Total Tokens Used: {total_tokens}\n")
        # f.write(f"- Average Tokens per Page: {total_tokens / len(images):.2f}\n\n")
        # f.write("---\n\n")
        
        # Write content from each page
        f.write(finalised_markdown)
    
    ################# ATTEMPT REFORMATTING w GPT again #################
    # create another md file with suffix _reformatted 
    # this md file will take in the combined content from all pages and reformat it
    # to be more readable, which tries to maintain the original layout and heading levels as much as possible 
    
    # Create reformatted version
    # reformatted_path = os.path.join(output_folder, f'{pdf_name}_extracted_openai_{model}_v4_reformatted.md')
    # response = client.chat.completions.create(
    #         model=model,
    #         messages=[
    #             {
    #             "role": "user",
    #             "content": [
    #                 {
    #                 "type": "text",
    #                 "text": get_prompt_v4(result[i]),
    #                 },
    #                 {
    #                 "type": "image_url",
    #                 "image_url": {
    #                     "url":  f"data:image/jpeg;base64,{base64_image}",
    #                     "detail": "high"
    #                 },
    #                 },
    #             ],
    #             }
    #         ],
    #         max_tokens=2000
    #     )
    # reformatted_content = response.choices[0].message.content
    # print(f"Reformatted content: {reformatted_content}")
    
    # with open(reformatted_path, 'w', encoding='utf-8') as f:
    #     f.write(reformatted_content)
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_image_gpt_parser.py <pdf_filename>")
        sys.exit(1)
        
    pdf_filename = sys.argv[1]
    pdf_path = os.path.join("test-pdfs", pdf_filename)
    
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found")
        sys.exit(1)
    
    for model in MODEL:
        start_time = time.time()
        extract_content_from_pdf(model, pdf_path)
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"PDF processed successfully for model: {model}")
        print(f"Processing time for {model}: {processing_time:.2f} seconds ({processing_time/60:.2f} minutes)")

    # remove the original pdf
    os.remove(pdf_path)

    print("All models ran successfully")