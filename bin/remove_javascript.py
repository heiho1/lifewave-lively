#!/Users/heiho1/dev/lifewave/lifewave-env/bin/python3
import re
import os
from pathlib import Path

def remove_javascript_from_file(file_path):
    """Remove (javascript:.*) blocks from a markdown file"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove (javascript:.*) blocks using regex
        # This pattern matches (javascript: followed by anything until closing parenthesis)
        cleaned_content = re.sub(r'\(javascript:[^)]*\)', '', content)
        
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def remove_javascript_from_markdown_files():
    """Remove (javascript:.*) blocks from all markdown files in the markdown directory"""
    
    markdown_dir = Path("markdown")
    
    if not markdown_dir.exists():
        print(f"Error: {markdown_dir} directory not found")
        return
    
    # Get all markdown files
    markdown_files = list(markdown_dir.glob("*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {markdown_dir}")
        return
    
    print(f"Checking {len(markdown_files)} markdown files for (javascript:.*) blocks...")
    
    processed_count = 0
    for file_path in markdown_files:
        # First check if the file contains javascript blocks
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if re.search(r'\(javascript:[^)]*\)', content):
                print(f"Processing {file_path.name}...")
                if remove_javascript_from_file(file_path):
                    print(f"  ✓ Removed javascript blocks from {file_path.name}")
                    processed_count += 1
                else:
                    print(f"  ✗ Failed to process {file_path.name}")
        except Exception as e:
            print(f"  ⚠ Error reading {file_path.name}: {e}")
    
    if processed_count == 0:
        print("No files contained (javascript:.*) blocks")
    else:
        print(f"Successfully processed {processed_count} files")

if __name__ == "__main__":
    remove_javascript_from_markdown_files()