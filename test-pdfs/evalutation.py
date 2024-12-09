import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

MISSING_WORDS_THRESHOLD = 10

def test_pdf_to_markdown_conversion(markdown_content: str, expected_content: str):
    """
    Test a single markdown conversion against expected content.
    Returns percentage match and missed words.
    """
    logger.info("Comparing markdown content with expected content")
    
    # Normalize text by converting to lowercase and removing any markdown formatting
    markdown_text = markdown_content.lower()
    expected_text = expected_content.lower()
    # Remove markdown syntax
    markdown_text = markdown_text.replace('**', '')
    # replace empty spaces in markdown text
    markdown_text = "".join(markdown_text.split())

    # Compare words directly against full markdown text
    count = 0
    missed_words = []
    expected_words = expected_text.split()
    
    for word in expected_words:
        if word in markdown_text:
            count += 1
        else:
            missed_words.append(word)

    match_percentage = (count / len(expected_words)) * 100
    
    return match_percentage, missed_words

def run_markdown_tests(test_folder: str):
    """
    Run tests on all markdown files in the specified folder against original.txt
    """
    logger.info(f"Starting tests for folder: {test_folder}")
    
    # Read the original content
    original_path = os.path.join(test_folder, "original.txt")
    try:
        with open(original_path, 'r', encoding='utf-8') as f:
            expected_content = f.read()
    except FileNotFoundError:
        logger.error(f"original.txt not found in {test_folder}")
        return
    
    # Find all markdown files
    markdown_files = [f for f in os.listdir(test_folder) if f.endswith('.md') and f != 'test-results.md']
    
    # Prepare results
    results = []
    results.append("# Markdown Comparison Test Results\n")
    results.append(f"Test folder: {test_folder}\n")
    results.append("## Results by File\n")
    
    for md_file in markdown_files:
        logger.info(f"Testing file: {md_file}")
        
        # Read markdown content
        md_path = os.path.join(test_folder, md_file)
        with open(md_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Run test
        match_percentage, missed_words = test_pdf_to_markdown_conversion(markdown_content, expected_content)
        
        # Add results
        results.append(f"### {md_file}\n")
        results.append(f"- Match percentage: {match_percentage:.2f}%\n")
        if missed_words:
            results.append("- Missed words:\n")
            # Only show first 50 missed words to keep report manageable
            for word in missed_words[:MISSING_WORDS_THRESHOLD]:
                results.append(f"  - {word}\n")
            if len(missed_words) > MISSING_WORDS_THRESHOLD:
                results.append(f"  - ... and {len(missed_words) - MISSING_WORDS_THRESHOLD} more\n")
        results.append("\n")
    
    # Write results to test-results.md
    results_path = os.path.join(test_folder, "test-results.md")
    with open(results_path, 'w', encoding='utf-8') as f:
        f.writelines(results)
    
    logger.info(f"Test results written to {results_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python evaluation.py <test_folder>")
        sys.exit(1)
        
    test_folder = sys.argv[1]
    if not os.path.exists(test_folder):
        print(f"Error: Folder '{test_folder}' not found")
        sys.exit(1)
        
    run_markdown_tests(test_folder)
