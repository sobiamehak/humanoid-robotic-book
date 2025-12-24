import os
import re
from typing import List, Dict, Any
from pathlib import Path

from .content_ingestion import ContentIngestionService


class TextbookContentLoader:
    """
    Service to load textbook content from MD/MDX files and prepare them for RAG
    """
    
    def __init__(self, docs_path: str = "../../../docs"):
        self.docs_path = Path(docs_path)
        self.content_ingestion_service = ContentIngestionService()
        
    def extract_frontmatter(self, content: str) -> tuple:
        """
        Extract frontmatter (metadata) from MD/MDX files
        """
        # Look for YAML frontmatter between ---
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            content_without_frontmatter = content[frontmatter_match.end():].strip()
            
            # Parse frontmatter
            metadata = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    metadata[key] = value
            
            return metadata, content_without_frontmatter
        else:
            return {}, content
    
    def clean_markdown_content(self, content: str) -> str:
        """
        Clean up markdown content, removing headers and code blocks for RAG purposes
        """
        # Remove markdown headers (lines starting with #)
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip header lines
            if line.strip().startswith('#'):
                continue
            cleaned_lines.append(line)
            
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Remove code blocks (triple backticks)
        cleaned_content = re.sub(r'```.*?```', '', cleaned_content, flags=re.DOTALL)
        
        # Remove links but keep the link text
        cleaned_content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned_content)
        
        # Clean up extra whitespace
        cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content).strip()
        
        return cleaned_content
    
    def load_chapter_content(self, file_path: Path) -> Dict[str, Any]:
        """
        Load content from a single chapter file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
            
        metadata, content_without_frontmatter = self.extract_frontmatter(raw_content)
        clean_content = self.clean_markdown_content(content_without_frontmatter)
        
        # Extract chapter/module ID from filename
        filename = file_path.stem
        if filename.startswith('chapter-'):
            # Format: chapter-XX-title
            parts = filename.split('-', 2)
            if len(parts) >= 2:
                chapter_id = f"chapter-{parts[1]}"
                module_id = self._determine_module_from_filename(filename)
            else:
                chapter_id = filename
                module_id = "unknown"
        elif filename == "intro":
            chapter_id = "intro"
            module_id = "introduction"
        else:
            chapter_id = filename
            module_id = "unknown"
        
        title = metadata.get('title', filename.replace('-', ' ').title())
        
        return {
            'content': clean_content,
            'chapter_id': chapter_id,
            'module_id': module_id,
            'title': title,
            'metadata': metadata
        }
    
    def _determine_module_from_filename(self, filename: str) -> str:
        """
        Determine the module based on the chapter number
        """
        if filename.startswith('chapter-01') or filename.startswith('chapter-02'):
            return 'module-1-foundations'
        elif filename.startswith('chapter-03') or filename.startswith('chapter-04') or filename.startswith('chapter-05') or filename.startswith('chapter-06') or filename.startswith('chapter-07'):
            return 'module-2-core-concepts'
        elif filename.startswith('chapter-08') or filename.startswith('chapter-09'):
            return 'module-3-intelligence-learning'
        elif filename.startswith('chapter-10') or filename.startswith('chapter-11') or filename.startswith('chapter-12') or filename.startswith('chapter-13'):
            return 'module-4-applications-future'
        elif filename.startswith('appendix'):
            return 'appendices'
        else:
            return 'unknown'
    
    def load_all_content(self) -> List[Dict[str, Any]]:
        """
        Load content from all textbook files
        """
        content_items = []
        
        # Get all MD and MDX files
        for file_path in self.docs_path.glob('*.md*'):
            if file_path.name != 'intro.md':  # We'll handle intro separately or differently
                print(f"Loading content from {file_path.name}")
                content_data = self.load_chapter_content(file_path)
                content_items.append(content_data)
        
        # Add the intro file
        intro_path = self.docs_path / 'intro.md'
        if intro_path.exists():
            print(f"Loading content from {intro_path.name}")
            content_data = self.load_chapter_content(intro_path)
            content_items.append(content_data)
        
        return content_items
    
    def ingest_textbook_content(self) -> Dict[str, Any]:
        """
        Load all textbook content and ingest it into the RAG system
        """
        print("Starting textbook content ingestion...")
        
        # Load all content
        content_items = self.load_all_content()
        
        print(f"Loaded {len(content_items)} content items")
        
        # Ingest into RAG system
        result = self.content_ingestion_service.bulk_ingest(content_items)
        
        print(f"Ingestion completed - Successful: {result['successful']}, Failed: {result['failed']}")
        
        if result['errors']:
            print("Errors occurred during ingestion:")
            for error in result['errors']:
                print(f"  - {error}")
        
        return result