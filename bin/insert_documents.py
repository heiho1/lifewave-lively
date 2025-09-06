#!/Users/heiho1/dev/lifewave/lifewave-env/bin/python3

import os
import sys
from dotenv import load_dotenv
import requests
import json
import glob

def insert_document(title, content, supabase_url, supabase_key):
    """Insert a document into the Supabase documents table"""
    # Prepare the data
    data = {
        'title': title,
        'content': content
    }
    
    # Set up headers
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    # Make the request
    url = f"{supabase_url}/rest/v1/documents"
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully inserted document: {title}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error inserting document '{title}': {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}")
        return False

def process_markdown_files():
    """Process all markdown files in the markdown directory"""
    load_dotenv()
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
        return False
    
    markdown_dir = "markdown"
    if not os.path.exists(markdown_dir):
        print(f"Error: {markdown_dir} directory does not exist")
        return False
    
    # Get all markdown files
    markdown_files = glob.glob(os.path.join(markdown_dir, "*.md"))
    
    if not markdown_files:
        print(f"No markdown files found in {markdown_dir} directory")
        return False
    
    success_count = 0
    total_count = len(markdown_files)
    
    print(f"Found {total_count} markdown files to process...")
    
    for file_path in markdown_files:
        # Use filename (without extension) as title
        filename = os.path.basename(file_path)
        title = os.path.splitext(filename)[0]
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if insert_document(title, content, supabase_url, supabase_key):
                success_count += 1
                
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    print(f"\nProcessing complete: {success_count}/{total_count} documents inserted successfully")
    return success_count == total_count

def main():
    # Check if running in batch mode (no arguments) or single document mode
    if len(sys.argv) == 1:
        # Process all markdown files
        success = process_markdown_files()
        if not success:
            sys.exit(1)
    elif len(sys.argv) == 3:
        # Single document mode (original functionality)
        load_dotenv()
        
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env file")
            sys.exit(1)
        
        title = sys.argv[1]
        content = sys.argv[2]
        
        success = insert_document(title, content, supabase_url, supabase_key)
        if not success:
            sys.exit(1)
    else:
        print("Usage:")
        print("  ./insert_documents.py                    # Process all markdown files")
        print("  ./insert_documents.py <title> <content>  # Insert single document")
        print("Example: ./insert_documents.py 'My Document' 'This is the content'")
        sys.exit(1)

if __name__ == "__main__":
    main()