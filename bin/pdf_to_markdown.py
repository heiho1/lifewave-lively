#!/Users/heiho1/dev/lifewave/lifewave-env/bin/python3
import os
import pymupdf4llm
from pathlib import Path

def convert_pdfs_to_markdown():
    """Convert all PDF files from pdfs/ directory to markdown files in markdown/ directory using pymupdf4llm"""
    
    # Define directories
    pdfs_dir = Path("pdfs")
    markdown_dir = Path("markdown")
    
    # Create markdown directory if it doesn't exist
    markdown_dir.mkdir(exist_ok=True)
    
    # Check if pdfs directory exists
    if not pdfs_dir.exists():
        print(f"Error: {pdfs_dir} directory not found")
        return
    
    # Get all PDF files
    pdf_files = list(pdfs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {pdfs_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to convert")
    
    # Convert each PDF to markdown
    for pdf_file in pdf_files:
        try:
            print(f"Converting {pdf_file.name}...")
            
            # Generate output filename
            markdown_filename = pdf_file.stem + ".md"
            markdown_path = markdown_dir / markdown_filename
            
            # Convert PDF to markdown using pymupdf4llm
            md_text = pymupdf4llm.to_markdown(str(pdf_file))
            
            # Write markdown file
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(md_text)
            
            print(f"  ✓ Created {markdown_path}")
            
        except Exception as e:
            print(f"  ✗ Error converting {pdf_file.name}: {e}")
    
    print("Conversion complete!")

if __name__ == "__main__":
    convert_pdfs_to_markdown()