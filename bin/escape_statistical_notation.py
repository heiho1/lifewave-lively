#!/Users/heiho1/dev/lifewave/lifewave-env/bin/python3
import re
import os
from pathlib import Path

def escape_statistical_notation_in_file(file_path):
    """Escape statistical notation like p<0.001 to prevent MDX JSX parsing issues"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern to match statistical notation: p<number, P<number, etc.
        # This matches patterns like: p<0.001, P<0.05, p<0.0001, etc.
        pattern = r'\b([pP])<(\d+(?:\.\d+)?)\b'
        
        # Replace with escaped version using backticks to prevent JSX parsing
        content = re.sub(pattern, r'`\1<\2`', content)
        
        # Also handle cases where there might be spaces: p < 0.001
        pattern_with_spaces = r'\b([pP])\s*<\s*(\d+(?:\.\d+)?)\b'
        content = re.sub(pattern_with_spaces, r'`\1 < \2`', content)
        
        # Write the cleaned content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        changes_made = content != original_content
        return True, changes_made
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, False

def escape_statistical_notation_in_markdown_files():
    """Escape statistical notation in all markdown files"""
    
    markdown_dir = Path("markdown")
    
    if not markdown_dir.exists():
        print(f"Error: {markdown_dir} directory not found")
        return
    
    # Get all markdown files
    markdown_files = list(markdown_dir.glob("*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {markdown_dir}")
        return
    
    print(f"Escaping statistical notation in {len(markdown_files)} markdown files...")
    
    files_modified = 0
    
    for file_path in markdown_files:
        success, changes_made = escape_statistical_notation_in_file(file_path)
        
        if success:
            if changes_made:
                print(f"  ✓ Escaped statistical notation in {file_path.name}")
                files_modified += 1
        else:
            print(f"  ✗ Failed to process {file_path.name}")
    
    if files_modified == 0:
        print("No files needed modification")
    else:
        print(f"Successfully modified {files_modified} files")

if __name__ == "__main__":
    escape_statistical_notation_in_markdown_files()