#! ../lifewave-env/bin/python3
"""
Text to Embeddings Converter using llama-text-embed-v2

Converts text files from the vectors/ directory to embeddings using 
Pinecone's llama-text-embed-v2 model via inference API and saves 
them as JSON files in the embeddings/ directory.
"""

import os
import json
import time
from pathlib import Path
from pinecone import Pinecone

def chunk_text(text, max_chunk_size=8192, overlap=200):
    """
    Split text into chunks for embedding processing.
    
    Args:
        text (str): Input text to chunk
        max_chunk_size (int): Maximum characters per chunk
        overlap (int): Overlap between chunks in characters
    
    Returns:
        list: List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings near the chunk boundary
            sentence_ends = ['.', '!', '?', '\n\n']
            best_break = end
            
            for i in range(max(start + max_chunk_size - 200, start), min(end + 200, len(text))):
                if text[i] in sentence_ends:
                    best_break = i + 1
                    break
            
            end = best_break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = end - overlap
        if start >= len(text):
            break
    
    return chunks

def create_embeddings(text_chunks, pc, model="llama-text-embed-v2"):
    """
    Create embeddings for text chunks using Pinecone inference.
    
    Args:
        text_chunks (list): List of text strings to embed
        pc (Pinecone): Pinecone client instance
        model (str): Model name for embeddings
    
    Returns:
        list: List of embedding vectors
    """
    try:
        # Use Pinecone inference for embeddings
        response = pc.inference.embed(
            model=model,
            inputs=text_chunks,
            parameters={
                "input_type": "passage",  # For document/passage embedding
                "truncate": "END"        # Truncate from the end if too long
            }
        )
        
        # Handle Pinecone inference response format
        if hasattr(response, 'data') and response.data:
            # Extract embeddings from DenseEmbedding objects
            if hasattr(response.data[0], 'values'):
                return [data.values for data in response.data]
            elif isinstance(response.data[0], dict) and 'values' in response.data[0]:
                return [data['values'] for data in response.data]
            else:
                # Response might be a list of embeddings directly
                return response.data
        else:
            print(f"    Unexpected response format: {response}")
            return None
    
    except Exception as e:
        print(f"Error creating embeddings: {str(e)}")
        return None

def process_text_file(file_path, pc, output_dir):
    """
    Process a single text file to create embeddings.
    
    Args:
        file_path (Path): Path to input text file
        pc (Pinecone): Pinecone client instance
        output_dir (Path): Directory to save embedding files
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read text file
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        if not text_content.strip():
            print(f"  Warning: File {file_path.name} is empty")
            return False
        
        # Chunk the text
        text_chunks = chunk_text(text_content)
        print(f"  Split into {len(text_chunks)} chunks")
        
        # Create embeddings
        embeddings = create_embeddings(text_chunks, pc)
        
        if embeddings is None:
            return False
        
        # Prepare output data
        output_data = {
            "source_file": str(file_path.name),
            "total_chunks": len(text_chunks),
            "embedding_model": "llama-text-embed-v2",
            "embedding_dimension": len(embeddings[0]) if embeddings else 0,
            "chunks": []
        }
        
        for i, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
            output_data["chunks"].append({
                "chunk_id": i,
                "text": chunk[:500] + "..." if len(chunk) > 500 else chunk,  # Truncate for storage
                "full_text_length": len(chunk),
                "embedding": embedding
            })
        
        # Save embeddings as JSON
        output_filename = file_path.stem + "_embeddings.json"
        output_path = output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"  Error processing {file_path.name}: {str(e)}")
        return False

def main():
    """Main function to process all text files."""
    vectors_dir = Path("vectors")
    embeddings_dir = Path("embeddings")
    
    # Ensure directories exist
    if not vectors_dir.exists():
        print(f"Vectors directory '{vectors_dir}' does not exist.")
        print("Run pdf_to_text.py first to create text files.")
        return
    
    embeddings_dir.mkdir(exist_ok=True)
    
    # Initialize Pinecone client
    try:
        pc = Pinecone(api_key="pcsk_4UEAM7_MY5HKHJ7W6VnnBLrBpKYitHDVycJbEjWpCUqjQp1qdqnuy1dqRjLNmGY3WD1WhQ")
        print("Connected to Pinecone successfully")
    except Exception as e:
        print(f"Failed to connect to Pinecone: {str(e)}")
        return
    
    # Get all text files from vectors directory
    text_files = list(vectors_dir.glob("*.txt"))
    
    if not text_files:
        print("No text files found in the vectors directory.")
        return
    
    print(f"Found {len(text_files)} text files to process...")
    print(f"Using llama-text-embed-v2 model for embeddings")
    
    successful = 0
    failed = 0
    
    for text_file in text_files:
        print(f"\nProcessing: {text_file.name}")
        
        if process_text_file(text_file, pc, embeddings_dir):
            successful += 1
            print(f"  ✓ Success - embeddings saved")
        else:
            failed += 1
            print(f"  ✗ Failed")
        
        # Add small delay to respect rate limits
        time.sleep(1)
    
    print(f"\nEmbedding generation completed:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Embeddings saved to: {embeddings_dir}")
    
    if successful > 0:
        # Show sample embedding info
        sample_file = list(embeddings_dir.glob("*_embeddings.json"))[0]
        with open(sample_file, 'r') as f:
            sample_data = json.load(f)
        
        print(f"\nSample embedding info:")
        print(f"  Dimension: {sample_data['embedding_dimension']}")
        print(f"  Model: {sample_data['embedding_model']}")
        print(f"  Average chunks per file: {sum([len(data['chunks']) for data in [json.load(open(f)) for f in embeddings_dir.glob('*_embeddings.json')]]) // successful}")

if __name__ == "__main__":
    main()