# forensic_tool_web/hashing.py

import hashlib
import os

def get_supported_algorithms():
    """Returns a list of supported hashing algorithms."""
    return [
        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'blake2b', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'
    ]

def hash_text(text):
    """Computes hashes for a given text string."""
    hashes = {}
    for algorithm in get_supported_algorithms():
        h = hashlib.new(algorithm)
        h.update(text.encode('utf-8'))
        hashes[algorithm.upper()] = h.hexdigest()
    return hashes

def hash_file(file_path, chunk_size=8192):
    """Computes hashes for a single file with efficient chunk processing."""
    try:
        hashers = {alg: hashlib.new(alg) for alg in get_supported_algorithms()}
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                for hasher in hashers.values():
                    hasher.update(chunk)
        return {alg.upper(): hasher.hexdigest() for alg, hasher in hashers.items()}
    except Exception as e:
        print(f"Error hashing file {file_path}: {e}")
        return None

def hash_directory(directory_path, excluded_extensions=None):
    """Recursively hashes all files in a directory."""
    from utils import get_file_metadata
    if excluded_extensions is None:
        excluded_extensions = []
    
    results = []
    total_files = 0
    total_size = 0
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.splitext(file_path)[1] in excluded_extensions:
                continue

            metadata = get_file_metadata(file_path)
            if metadata:
                hashes = hash_file(file_path)
                if hashes:
                    results.append({"metadata": metadata, "hashes": hashes})
                    total_files += 1
                    total_size += metadata["File Size"]

    summary = {
        "Total Files Processed": total_files,
        "Total Directory Size": total_size
    }
    return results, summary
