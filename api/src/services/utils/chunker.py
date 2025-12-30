"""
Chunker utility for processing markdown files.

This module provides functionality to:
- Load markdown files
- Split content by ## headings
- Apply token limits with overlap
- Extract and preserve metadata
"""
import re
import tiktoken
from typing import List, Dict, Any
from pathlib import Path


def load_markdown_file(file_path: str) -> str:
    """
    Load content from a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Content of the markdown file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def split_by_headings(content: str) -> List[str]:
    """
    Split markdown content by ## headings.

    Args:
        content: The markdown content to split

    Returns:
        List of content chunks split by ## headings
    """
    # Pattern to match ## headings
    heading_pattern = r'(##\s+.*?)(?=\n##\s+|\Z)'

    # Find all sections that start with ## and include content until next ## or end
    sections = re.split(heading_pattern, content)

    # Process sections - odd indices are headings, even indices are content
    chunks = []
    i = 0
    while i < len(sections):
        if i + 1 < len(sections) and sections[i].strip().startswith('##'):
            # This is a heading followed by content
            heading = sections[i].strip()
            content_section = sections[i + 1] if i + 1 < len(sections) else ""
            chunks.append(heading + "\n" + content_section)
            i += 2
        else:
            # This is content without a heading, or just a heading at the end
            if sections[i].strip() and not sections[i].strip().startswith('##'):
                chunks.append(sections[i])
            i += 1

    # Filter out empty chunks
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    return chunks


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in a text using tiktoken.

    Args:
        text: The text to count tokens for

    Returns:
        Number of tokens in the text
    """
    # Use the cl100k_base encoding which is used by GPT-4, GPT-3.5-turbo, etc.
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def chunk_with_token_limit(texts: List[str], max_tokens: int = 1000, overlap_tokens: int = 100) -> List[str]:
    """
    Split texts that exceed the token limit while maintaining context with overlap.

    Args:
        texts: List of text chunks to potentially split further
        max_tokens: Maximum number of tokens per chunk
        overlap_tokens: Number of tokens to overlap between chunks

    Returns:
        List of text chunks that respect the token limit
    """
    result_chunks = []

    for text in texts:
        if count_tokens(text) <= max_tokens:
            # If the text is within the limit, add it as is
            result_chunks.append(text)
        else:
            # Split the text into smaller chunks
            sub_chunks = split_large_text(text, max_tokens, overlap_tokens)
            result_chunks.extend(sub_chunks)

    return result_chunks


def split_large_text(text: str, max_tokens: int, overlap_tokens: int) -> List[str]:
    """
    Split a large text into smaller chunks with token overlap.

    Args:
        text: The large text to split
        max_tokens: Maximum number of tokens per chunk
        overlap_tokens: Number of tokens to overlap between chunks

    Returns:
        List of smaller text chunks
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    start_idx = 0

    while start_idx < len(tokens):
        # Determine the end index for this chunk
        end_idx = start_idx + max_tokens

        # If we're near the end, just take the remaining tokens
        if end_idx > len(tokens):
            end_idx = len(tokens)

        # Decode the tokens back to text
        chunk_tokens = tokens[start_idx:end_idx]
        chunk_text = encoding.decode(chunk_tokens)

        chunks.append(chunk_text)

        # Move the start index forward, accounting for overlap
        if start_idx + max_tokens < len(tokens):
            # Calculate the overlap by moving back overlap_tokens from the end of the current chunk
            start_idx = end_idx - overlap_tokens
        else:
            # We've reached the end
            break

    return chunks


def extract_metadata(file_path: str, text: str) -> Dict[str, Any]:
    """
    Extract metadata from the file path and content.

    Args:
        file_path: Path to the original file
        text: The text content of the chunk

    Returns:
        Dictionary containing metadata
    """
    path_obj = Path(file_path)

    # Extract chapter and lesson from path
    parts = path_obj.parts

    # Look for chapter pattern in the path
    chapter = "unknown"
    lesson = "unknown"
    section_title = "unknown"

    for part in parts:
        if "chapter" in part.lower():
            chapter = part
        if "lesson" in part.lower():
            lesson = part

    # If no specific chapter/lesson found, use the parent directory name
    if chapter == "unknown":
        chapter = path_obj.parent.name or "general"

    # Extract the first heading as the section title
    lines = text.split('\n')
    for line in lines:
        if line.strip().startswith('## '):
            section_title = line.strip()[3:]  # Remove '## ' prefix
            break
        elif line.strip().startswith('# '):
            section_title = line.strip()[2:]  # Remove '# ' prefix
            break

    # Create a source URL based on the file path
    # Convert file path to a URL-friendly format
    relative_path = path_obj.relative_to(Path(file_path).parent.parent.parent)  # Go up to docs/
    source_url = f"/{relative_path.with_suffix('').as_posix().replace('docs/', 'chapter-').replace('/', '-')}"

    return {
        "chapter": chapter,
        "lesson": lesson,
        "section_title": section_title,
        "source_url": source_url,
        "file_path": str(path_obj)
    }


def chunk_file(file_path: str, max_tokens: int = 1000, overlap_tokens: int = 100) -> List[Dict[str, Any]]:
    """
    Process a markdown file into chunks with metadata.

    Args:
        file_path: Path to the markdown file to process
        max_tokens: Maximum number of tokens per chunk
        overlap_tokens: Number of tokens to overlap between chunks

    Returns:
        List of dictionaries, each containing 'id', 'text', and 'metadata'
    """
    content = load_markdown_file(file_path)

    # First, split by headings
    heading_chunks = split_by_headings(content)

    # Then, ensure each chunk respects the token limit
    final_chunks = chunk_with_token_limit(heading_chunks, max_tokens, overlap_tokens)

    # Create the result with IDs and metadata
    result = []
    for i, chunk in enumerate(final_chunks):
        if chunk.strip():  # Only add non-empty chunks
            metadata = extract_metadata(file_path, chunk)
            result.append({
                "id": f"{Path(file_path).stem}_chunk_{i}",
                "text": chunk,
                "metadata": metadata
            })

    return result


def chunk_multiple_files(file_paths: List[str], max_tokens: int = 1000, overlap_tokens: int = 100) -> List[Dict[str, Any]]:
    """
    Process multiple markdown files into chunks with metadata.

    Args:
        file_paths: List of paths to markdown files to process
        max_tokens: Maximum number of tokens per chunk
        overlap_tokens: Number of tokens to overlap between chunks

    Returns:
        List of dictionaries, each containing 'id', 'text', and 'metadata'
    """
    all_chunks = []

    for file_path in file_paths:
        chunks = chunk_file(file_path, max_tokens, overlap_tokens)
        all_chunks.extend(chunks)

    return all_chunks