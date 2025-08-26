#! ../lifewave-env/bin/python3
"""
PDF to Text Converter

Converts all PDF files in the documents/ directory to text files 
using PyMuPDF and saves them to the vectors/ directory.
"""

import os
import fitz
from pathlib import Path

def convert_pdf_to_text(pdf_path, output_path):
    """
    Convert a PDF file to text using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str): Path to save the output text file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        doc = fitz.open(pdf_path)
        text_content = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text_content += f"--- Page {page_num + 1} ---\n"
            text_content += page.get_text()
            text_content += "\n\n"
        
        doc.close()
        
        # Write text to output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        
        return True
    
    except Exception as e:
        print(f"Error converting {pdf_path}: {str(e)}")
        return False

def main():
    """Main function to process all PDF files."""
    documents_dir = Path("documents")
    vectors_dir = Path("vectors")
    
    # Ensure directories exist
    if not documents_dir.exists():
        print(f"Documents directory '{documents_dir}' does not exist.")
        return
    
    vectors_dir.mkdir(exist_ok=True)
    
    # Get all PDF files from documents directory
    pdf_files = list(documents_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in the documents directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert...")
    
    successful = 0
    failed = 0
    
    for pdf_file in pdf_files:
        # Create output filename (replace .pdf with .txt)
        output_filename = pdf_file.stem + ".txt"
        output_path = vectors_dir / output_filename
        
        print(f"Converting: {pdf_file.name} -> {output_filename}")
        
        if convert_pdf_to_text(pdf_file, output_path):
            successful += 1
            print(f"  ✓ Success")
        else:
            failed += 1
            print(f"  ✗ Failed")
    
    print(f"\nConversion completed:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Text files saved to: {vectors_dir}")

if __name__ == "__main__":
    main()