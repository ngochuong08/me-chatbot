"""
Vector Store - Quản lý vector database cho semantic search
Sử dụng FAISS cho performance tốt hơn với large dataset
"""

import os
import pickle
from typing import List, Optional
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings


class VectorStore:
    def __init__(self, persist_directory: str = "./vector_db"):
        self.persist_directory = persist_directory
        self.embeddings = self._initialize_embeddings()
        self.vectorstore = None
        
    def _initialize_embeddings(self) -> Embeddings:
        """Initialize embedding model - sử dụng multilingual model cho tiếng Việt"""
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def create_vectorstore(self, documents: List[Document]) -> FAISS:
        """Tạo vector store từ documents"""
        if not documents:
            raise ValueError("No documents provided")
        
        print(f"Creating vector store from {len(documents)} documents...")
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        return self.vectorstore
    
    def add_documents(self, documents: List[Document]):
        """Thêm documents vào vector store hiện tại"""
        if self.vectorstore is None:
            self.vectorstore = self.create_vectorstore(documents)
        else:
            self.vectorstore.add_documents(documents)
    
    def save(self):
        """Lưu vector store vào disk"""
        if self.vectorstore is None:
            print("No vector store to save")
            return
        
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Save FAISS index
        self.vectorstore.save_local(self.persist_directory)
        print(f"Vector store saved to {self.persist_directory}")
    
    def load(self) -> bool:
        """Load vector store từ disk"""
        index_path = os.path.join(self.persist_directory, "index.faiss")
        
        if not os.path.exists(index_path):
            print(f"No saved vector store found at {self.persist_directory}")
            return False
        
        try:
            self.vectorstore = FAISS.load_local(
                self.persist_directory,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Vector store loaded from {self.persist_directory}")
            return True
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    
    def similarity_search(
        self, 
        query: str, 
        k: int = 4,
        filter: Optional[dict] = None
    ) -> List[Document]:
        """Tìm kiếm documents tương tự"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")
        
        results = self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filter
        )
        
        return results
    
    def similarity_search_with_score(
        self, 
        query: str, 
        k: int = 4
    ) -> List[tuple]:
        """Tìm kiếm với similarity score"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")
        
        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=k
        )
        
        return results
    
    def get_retriever(self, k: int = 4):
        """Lấy retriever để dùng trong chain"""
        if self.vectorstore is None:
            raise ValueError("Vector store not initialized")
        
        return self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )


if __name__ == "__main__":
    # Test
    from document_processor import DocumentProcessor
    
    processor = DocumentProcessor()
    vector_store = VectorStore()
    
    # Try to load existing vector store
    if not vector_store.load():
        # Create new one if not exists
        docs_path = "./documents"
        if os.path.exists(docs_path):
            print("Processing documents...")
            chunks = processor.process_directory(docs_path)
            
            if chunks:
                vector_store.create_vectorstore(chunks)
                vector_store.save()
                
                # Test search
                results = vector_store.similarity_search("quy định nghỉ phép", k=2)
                print(f"\nSearch results: {len(results)}")
                for i, doc in enumerate(results, 1):
                    print(f"\n{i}. {doc.metadata.get('filename', 'Unknown')}")
                    print(f"   {doc.page_content[:200]}...")
        else:
            print(f"Create '{docs_path}' directory and add documents")
    else:
        print("Vector store loaded successfully!")
