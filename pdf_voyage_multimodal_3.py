import os
from voyageai import Client

import fitz  # PyMuPDF
from PIL import Image as PILImage
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

# VOYAGE CLIENT INITIALIZATION #################################################
# Load environment variables
load_dotenv()
api_key = os.getenv('VOYAGE_API_KEY')
MODEL_NAME = "voyage-multimodal-3"
vo = Client(api_key=api_key)

def pdf_file_to_screenshots(file_path: str, zoom: float = 1.0) -> tuple[list[PILImage.Image], list[str]]:
    # Ensure that the file path is valid
    if not file_path.endswith(".pdf"):
        raise ValueError("Invalid file path")

    # Open the PDF from the specified file path
    pdf = fitz.open(file_path)

    images = []
    texts = []
    # Loop through each page, render as pixmap, and convert to PIL Image
    mat = fitz.Matrix(zoom, zoom)
    for n in range(pdf.page_count):
        page = pdf[n]
        # Add debug print
        text = page.get_text()
        print(f"Page {n+1} text length: {len(text)}")
        print(f"First 100 chars: {text[:100]}")
        
        texts.append(text)
        
        # Get image
        pix = page.get_pixmap(matrix=mat)
        img = PILImage.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)

    pdf.close()
    return images, texts

def create_document_chunks(document: tuple[list[PILImage.Image], list[str]], chunk_size: int = 1) -> list[dict]:
    """
    Create chunks from document pages with their embeddings, content and metadata.
    
    Args:
        document: Tuple of (list of PIL Images, list of text content) from PDF
        chunk_size: Number of pages per chunk (default: 1)
    
    Returns:
        List of dictionaries containing chunk information
    """
    images, texts = document
    chunks = []
    total_pages = len(images)
    
    for i in range(0, total_pages, chunk_size):
        # Get pages for current chunk
        chunk_images = images[i:i + chunk_size]
        chunk_texts = texts[i:i + chunk_size]
        
        # Get embedding for chunk
        chunk_embedding = np.array(
            vo.multimodal_embed(
                inputs=[[img] for img in chunk_images],
                model=MODEL_NAME,
                input_type="document"
            ).embeddings
        ).mean(axis=0)  # Average if multiple pages
        
        # Create chunk metadata
        chunk_info = {
            "images": chunk_images,
            "content": "\n".join(chunk_texts),  # Join text content with newlines
            "metadata": {
                "page_numbers": list(range(i + 1, min(i + chunk_size + 1, total_pages + 1))),
                "chunk_index": i // chunk_size,
                "total_pages": total_pages
            },
            "embedding": chunk_embedding
        }
        chunks.append(chunk_info)
    
    return chunks

# Update show_screenshots to handle the new return type
def show_screenshots(document: tuple[list[PILImage.Image], list[str]]):
    images, _ = document
    fig, axes = plt.subplots(1, len(images), figsize=(66, 6))
    for n, img in enumerate(images):
        axes[n].imshow(img)
        axes[n].axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    document = pdf_file_to_screenshots("test-pdfs/7228422/7228422.pdf")
    chunks = create_document_chunks(document, chunk_size=2)  # Create chunks of 2 pages
    
    # Print chunk information
    for chunk in chunks:
        print(f"\nChunk {chunk['metadata']['chunk_index']}:")
        print(f"Pages: {chunk['metadata']['page_numbers']}")
        print(f"Content preview: {chunk['content'][:200]}...")  # First 200 chars
        print(f"Embedding shape: {chunk['embedding'].shape}")