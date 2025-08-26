#!/Users/heiho1/dev/lifewave/lifewave-env/bin/python3
import re
import os
from pathlib import Path

def clean_invisible_chars_from_file(file_path):
    """Remove null bytes and other problematic invisible characters from a markdown file"""
    try:
        # Read the file in binary mode first to handle any encoding issues
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        
        # Decode with error handling
        try:
            content = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            content = content_bytes.decode('utf-8', errors='replace')
        
        original_length = len(content)
        
        # Remove null bytes
        content = content.replace('\x00', '')
        
        # Remove other common problematic characters
        # Remove zero-width characters
        content = content.replace('\u200b', '')  # Zero-width space
        content = content.replace('\u200c', '')  # Zero-width non-joiner
        content = content.replace('\u200d', '')  # Zero-width joiner
        content = content.replace('\ufeff', '')  # Byte order mark
        
        # Remove control characters except for common ones (tab, newline, carriage return)
        content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', content)
        
        # Write the cleaned content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        chars_removed = original_length - len(content)
        return True, chars_removed
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0

def detect_problematic_chars_in_file(file_path):
    """Detect problematic characters in a file without modifying it"""
    try:
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        
        problems = []
        
        # Check for null bytes
        if b'\x00' in content_bytes:
            problems.append("null bytes")
        
        # Check for other control characters
        for i, byte in enumerate(content_bytes):
            if byte < 32 and byte not in [9, 10, 13]:  # Allow tab, LF, CR
                problems.append(f"control character {hex(byte)} at position {i}")
                break
        
        return problems
        
    except Exception as e:
        return [f"Error reading file: {e}"]

def clean_markdown_files():
    """Clean invisible characters from all markdown files"""
    
    markdown_dir = Path("markdown")
    
    if not markdown_dir.exists():
        print(f"Error: {markdown_dir} directory not found")
        return
    
    # Get all markdown files
    markdown_files = list(markdown_dir.glob("*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {markdown_dir}")
        return
    
    print(f"Checking {len(markdown_files)} markdown files for problematic characters...")
    
    files_with_issues = 0
    total_chars_removed = 0
    
    for file_path in markdown_files:
        # First detect issues
        problems = detect_problematic_chars_in_file(file_path)
        
        if problems:
            print(f"Issues found in {file_path.name}: {', '.join(problems)}")
            success, chars_removed = clean_invisible_chars_from_file(file_path)
            
            if success:
                print(f"  ✓ Cleaned {file_path.name} (removed {chars_removed} problematic characters)")
                files_with_issues += 1
                total_chars_removed += chars_removed
            else:
                print(f"  ✗ Failed to clean {file_path.name}")
    
    if files_with_issues == 0:
        print("No problematic characters found in any files")
    else:
        print(f"Successfully cleaned {files_with_issues} files, removed {total_chars_removed} problematic characters total")

if __name__ == "__main__":
    clean_markdown_files()