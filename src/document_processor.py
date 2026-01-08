"""
Document Processor - Xử lý và đọc các loại tài liệu
Hỗ trợ: PDF, DOCX, TXT
"""

import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader
)
from langchain.schema import Document


class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load document dựa vào extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif ext == '.docx':
                loader = Docx2txtLoader(file_path)
            elif ext == '.txt':
                loader = TextLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {ext}")
            
            documents = loader.load()
            return documents
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []
    
    def process_document(self, file_path: str) -> List[Document]:
        """Load và split document thành chunks"""
        documents = self.load_document(file_path)
        
        if not documents:
            return []
        
        # Add metadata
        for doc in documents:
            doc.metadata['source'] = file_path
            doc.metadata['filename'] = os.path.basename(file_path)
        
        # Split into chunks
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def process_directory(self, directory_path: str) -> List[Document]:
        """Xử lý tất cả documents trong thư mục"""
        all_chunks = []
        
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return all_chunks
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(file_path):
                print(f"Processing: {filename}")
                chunks = self.process_document(file_path)
                all_chunks.extend(chunks)
                print(f"  -> {len(chunks)} chunks created")
        
        return all_chunks
    
    def get_document_text(self, file_path: str) -> str:
        """Lấy toàn bộ text từ document"""
        documents = self.load_document(file_path)
        return "\n\n".join([doc.page_content for doc in documents])


if __name__ == "__main__":
    # Test
    processor = DocumentProcessor()
    docs_path = "./documents"
    
    if os.path.exists(docs_path):
        chunks = processor.process_directory(docs_path)
        print(f"\nTotal chunks: {len(chunks)}")
        if chunks:
            print(f"Sample chunk: {chunks[0].page_content[:200]}...")
    else:
        print(f"Create '{docs_path}' directory and add some documents to test")
