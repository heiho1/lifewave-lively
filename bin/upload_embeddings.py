#! ../lifewave-env/bin/python3
"""
Upload Embeddings to Pinecone Index

Uploads vector embeddings from the embeddings/ directory to a Pinecone index
named "lifewave-x39". Creates the index if it doesn't exist.
"""

import os
import json
import time
import uuid
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec

def create_index_if_not_exists(pc, index_name="lifewave-x39", dimension=1024):
    """
    Create Pinecone index if it doesn't exist.
    
    Args:
        pc (Pinecone): Pinecone client instance
        index_name (str): Name of the index
        dimension (int): Vector dimension
    
    Returns:
        bool: True if index exists/created, False on error
    """
    try:
        # Check if index exists
        existing_indexes = pc.list_indexes()
        index_names = [idx['name'] for idx in existing_indexes]
        
        if index_name in index_names:
            print(f"Index '{index_name}' already exists")
            return True
        
        # Create new index
        print(f"Creating index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",  # Good for text embeddings
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"  # Choose appropriate region
            )
        )
        
        # Wait for index to be ready
        while not pc.describe_index(index_name).status['ready']:
            print("  Waiting for index to be ready...")
            time.sleep(1)
        
        print(f"✓ Index '{index_name}' created successfully")
        return True
        
    except Exception as e:
        print(f"Error creating index: {str(e)}")
        return False

def prepare_vectors_from_embedding_file(embedding_file_path):
    """
    Prepare vectors from an embedding JSON file for Pinecone upload.
    
    Args:
        embedding_file_path (Path): Path to embedding JSON file
    
    Returns:
        list: List of vector dictionaries for Pinecone upsert
    """
    try:
        with open(embedding_file_path, 'r', encoding='utf-8') as f:
            embedding_data = json.load(f)
        
        vectors = []
        source_file = embedding_data.get('source_file', 'unknown')
        
        for chunk_data in embedding_data.get('chunks', []):
            # Create unique ID for each chunk
            vector_id = f"{Path(source_file).stem}_chunk_{chunk_data['chunk_id']}"
            
            # Prepare metadata
            metadata = {
                'source_file': source_file,
                'chunk_id': chunk_data['chunk_id'],
                'text': chunk_data.get('text', ''),
                'full_text_length': chunk_data.get('full_text_length', 0),
                'embedding_model': embedding_data.get('embedding_model', 'unknown')
            }
            
            # Prepare vector for upload
            vector = {
                'id': vector_id,
                'values': chunk_data['embedding'],
                'metadata': metadata
            }
            
            vectors.append(vector)
        
        return vectors
        
    except Exception as e:
        print(f"  Error processing {embedding_file_path.name}: {str(e)}")
        return []

def upload_vectors_to_index(pc, index_name, vectors, batch_size=100):
    """
    Upload vectors to Pinecone index in batches.
    
    Args:
        pc (Pinecone): Pinecone client instance
        index_name (str): Name of the index
        vectors (list): List of vector dictionaries
        batch_size (int): Number of vectors per batch
    
    Returns:
        bool: True if successful, False on error
    """
    try:
        index = pc.Index(index_name)
        
        # Upload in batches
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            
            print(f"    Uploading batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size}")
            
            # Upsert vectors
            upsert_response = index.upsert(
                vectors=batch,
                namespace=""  # Use default namespace
            )
            
            # Check response
            if hasattr(upsert_response, 'upserted_count'):
                print(f"      Upserted {upsert_response.upserted_count} vectors")
            
            # Small delay between batches
            time.sleep(0.5)
        
        return True
        
    except Exception as e:
        print(f"    Error uploading vectors: {str(e)}")
        return False

def process_embedding_file(embedding_file, pc, index_name):
    """
    Process a single embedding file and upload to Pinecone.
    
    Args:
        embedding_file (Path): Path to embedding JSON file
        pc (Pinecone): Pinecone client instance
        index_name (str): Name of the Pinecone index
    
    Returns:
        int: Number of vectors uploaded, 0 on error
    """
    print(f"Processing: {embedding_file.name}")
    
    # Prepare vectors from embedding file
    vectors = prepare_vectors_from_embedding_file(embedding_file)
    
    if not vectors:
        print("  ✗ No vectors to upload")
        return 0
    
    print(f"  Prepared {len(vectors)} vectors for upload")
    
    # Upload vectors to index
    if upload_vectors_to_index(pc, index_name, vectors):
        print(f"  ✓ Successfully uploaded {len(vectors)} vectors")
        return len(vectors)
    else:
        print("  ✗ Failed to upload vectors")
        return 0

def main():
    """Main function to upload all embeddings to Pinecone index."""
    embeddings_dir = Path("embeddings")
    index_name = "lifewave-x39"
    
    # Check if embeddings directory exists
    if not embeddings_dir.exists():
        print(f"Embeddings directory '{embeddings_dir}' does not exist.")
        print("Run text_to_embeddings.py first to generate embeddings.")
        return
    
    # Initialize Pinecone client
    try:
        pc = Pinecone(api_key="pcsk_4UEAM7_MY5HKHJ7W6VnnBLrBpKYitHDVycJbEjWpCUqjQp1qdqnuy1dqRjLNmGY3WD1WhQ")
        print("Connected to Pinecone successfully")
    except Exception as e:
        print(f"Failed to connect to Pinecone: {str(e)}")
        return
    
    # Create or verify index exists
    if not create_index_if_not_exists(pc, index_name, dimension=1024):
        print("Failed to create/access index. Exiting.")
        return
    
    # Get all embedding files
    embedding_files = list(embeddings_dir.glob("*_embeddings.json"))
    
    if not embedding_files:
        print("No embedding files found in the embeddings directory.")
        return
    
    print(f"\nFound {len(embedding_files)} embedding files to upload...")
    print(f"Target index: {index_name}")
    
    total_vectors = 0
    successful_files = 0
    failed_files = 0
    
    for embedding_file in embedding_files:
        vectors_uploaded = process_embedding_file(embedding_file, pc, index_name)
        
        if vectors_uploaded > 0:
            successful_files += 1
            total_vectors += vectors_uploaded
        else:
            failed_files += 1
        
        # Delay between files to respect rate limits
        time.sleep(1)
    
    print(f"\nUpload completed:")
    print(f"  Successful files: {successful_files}")
    print(f"  Failed files: {failed_files}")
    print(f"  Total vectors uploaded: {total_vectors}")
    
    # Get index stats
    try:
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"  Index '{index_name}' now contains {stats.total_vector_count} vectors")
    except Exception as e:
        print(f"  Could not retrieve index stats: {str(e)}")

if __name__ == "__main__":
    main()