"""Utility functions for the backend"""
import os
import hashlib
import secrets
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_unique_id(prefix: str = "") -> str:
    """
    Generate a unique ID with optional prefix

    Args:
        prefix: Optional prefix for the ID

    Returns:
        Unique identifier string
    """
    unique_part = secrets.token_urlsafe(16)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"{prefix}{timestamp}_{unique_part}" if prefix else f"{timestamp}_{unique_part}"


def ensure_directory_exists(directory: str) -> bool:
    """
    Ensure a directory exists, create if it doesn't

    Args:
        directory: Path to directory

    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False


def get_file_hash(file_path: str) -> Optional[str]:
    """
    Get SHA256 hash of a file

    Args:
        file_path: Path to file

    Returns:
        Hash string or None if error
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        logger.error(f"Error hashing file {file_path}: {e}")
        return None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for filesystem

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')

    # Limit length
    max_length = 255
    if len(filename) > max_length:
        name, ext = os.path.splitext(filename)
        filename = name[:max_length - len(ext)] + ext

    return filename
