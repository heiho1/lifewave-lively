#!/Users/heiho1/dev/lifewave/lifewave-env/bin/python3
import re
import os
from pathlib import Path

def remove_html_tags_from_file(file_path):
    """Remove HTML tags from a markdown file"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove HTML tags using regex
        # This pattern matches any HTML tag: <tag>, </tag>, <tag attribute="value">, etc.
        cleaned_content = re.sub(r'<[^>]+>', '', content)
        
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def clean_html_tags_in_markdown_files():
    """Remove HTML tags from all markdown files that contain them"""
    
    # List of files that contain HTML tags (from grep results)
    files_with_html = [
        "lifewave-strength-test-morehouse-college.md",
        "changes-in-ghk-and-ghk-cu-in-blood-produced-by-the-lifewave-x39-patch.md",
        "study-a.md",
        "lifewave-x39-pilot-demonstrates-light-triggered-changes-may-2020.md",
        "acupressure-and-mental-clarity.md",
        "metabolic-implications-of-the-lifewave-x39-patch-study-4.md",
        "changes-in-tripeptides.md",
        "metabolic-implications-of-the-lifewave-x39-patch-study-1.md",
        "double-blind.md",
        "experimental-study-of-lifewave-x-39-patches-report-final-draft-3.md"
    ]
    
    markdown_dir = Path("markdown")
    
    if not markdown_dir.exists():
        print(f"Error: {markdown_dir} directory not found")
        return
    
    print(f"Cleaning HTML tags from {len(files_with_html)} markdown files...")
    
    success_count = 0
    for filename in files_with_html:
        file_path = markdown_dir / filename
        
        if file_path.exists():
            print(f"Processing {filename}...")
            if remove_html_tags_from_file(file_path):
                print(f"  ✓ Cleaned HTML tags from {filename}")
                success_count += 1
            else:
                print(f"  ✗ Failed to process {filename}")
        else:
            print(f"  ⚠ File not found: {filename}")
    
    print(f"Successfully processed {success_count}/{len(files_with_html)} files")

if __name__ == "__main__":
    clean_html_tags_in_markdown_files()