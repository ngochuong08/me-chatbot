"""
Chatbot Core - Sử dụng Langchain và LLM
Hỗ trợ cả OpenAI API và local LLM (vLLM)
"""

import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import Document

from vector_store import VectorStore
from document_processor import DocumentProcessor
from document_compare import DocumentCompare

load_dotenv()


class MEChatbot:
    def __init__(
        self, 
        documents_path: str = "./documents",
        vector_db_path: str = "./vector_db",
        use_local_llm: bool = False
    ):
        self.documents_path = documents_path
        self.vector_db_path = vector_db_path
        
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore(persist_directory=vector_db_path)
        self.document_compare = DocumentCompare()
        
        # Initialize LLM
        self.llm = self._initialize_llm(use_local_llm)
        
        # Memory for conversation
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Initialize or load vector store
        self._setup_vector_store()
        
        # Create QA chain
        self.qa_chain = self._create_qa_chain()
    
    def _initialize_llm(self, use_local: bool = False):
        """Initialize LLM - OpenAI hoặc local vLLM"""
        if use_local:
            # Sử dụng local LLM endpoint (vLLM)
            base_url = os.getenv("LLM_API_BASE", "http://localhost:8000/v1")
            model_name = os.getenv("LLM_MODEL_NAME", "Qwen3-14B-AWQ")
            
            return ChatOpenAI(
                model_name=model_name,
                openai_api_base=base_url,
                openai_api_key="EMPTY",  # vLLM không cần API key
                temperature=float(os.getenv("TEMPERATURE", 0.7)),
                max_tokens=int(os.getenv("MAX_TOKENS", 2048))
            )
        else:
            # Sử dụng OpenAI API
            return ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=float(os.getenv("TEMPERATURE", 0.7)),
                max_tokens=int(os.getenv("MAX_TOKENS", 2048)),
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
    
    def _setup_vector_store(self):
        """Setup hoặc load vector store"""
        if not self.vector_store.load():
            print("Creating new vector store from documents...")
            self.rebuild_vector_store()
    
    def rebuild_vector_store(self):
        """Rebuild vector store từ documents folder"""
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)
            print(f"Created documents directory: {self.documents_path}")
            print("Please add documents to this directory and run again.")
            return
        
        chunks = self.document_processor.process_directory(self.documents_path)
        
        if chunks:
            self.vector_store.create_vectorstore(chunks)
            self.vector_store.save()
            print(f"Vector store created with {len(chunks)} chunks")
        else:
            print("No documents found to process")
    
    def _create_qa_chain(self):
        """Tạo Conversational Retrieval Chain"""
        
        # Custom prompt cho chatbot
        prompt_template = """Bạn là trợ lý AI của ngân hàng ME, hỗ trợ 10,000 nhân viên.
Nhiệm vụ của bạn là trả lời câu hỏi dựa trên tài liệu nội bộ được cung cấp.

Ngữ cảnh từ tài liệu:
{context}

Lịch sử hội thoại:
{chat_history}

Câu hỏi hiện tại: {question}

Hướng dẫn:
1. Trả lời chính xác dựa trên tài liệu được cung cấp
2. Nếu không tìm thấy thông tin, hãy nói rõ "Tôi không tìm thấy thông tin này trong tài liệu"
3. Trích dẫn nguồn tài liệu nếu có thể
4. Trả lời bằng tiếng Việt, rõ ràng và chuyên nghiệp
5. Nếu cần so sánh tài liệu, hãy đề xuất sử dụng tính năng so sánh

Trả lời:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        # Create chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.get_retriever(k=4),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            verbose=False
        )
        
        return chain
    
    def chat(self, question: str) -> Dict:
        """Chat với bot - tìm kiếm tài liệu và trả lời"""
        try:
            if self.qa_chain is None:
                return {
                    "answer": "Vector store chưa được khởi tạo. Vui lòng thêm tài liệu vào thư mục documents.",
                    "sources": []
                }
            
            result = self.qa_chain({"question": question})
            
            # Format sources
            sources = []
            for doc in result.get("source_documents", []):
                sources.append({
                    "filename": doc.metadata.get("filename", "Unknown"),
                    "content": doc.page_content[:200] + "...",
                    "source": doc.metadata.get("source", "")
                })
            
            return {
                "answer": result["answer"],
                "sources": sources
            }
        
        except Exception as e:
            return {
                "answer": f"Xin lỗi, đã có lỗi xảy ra: {str(e)}",
                "sources": []
            }
    
    def compare_documents(self, file1: str, file2: str) -> Dict:
        """So sánh 2 documents"""
        try:
            return self.document_compare.compare_documents(file1, file2)
        except Exception as e:
            return {
                "error": f"Error comparing documents: {str(e)}"
            }
    
    def search_documents(self, query: str, k: int = 4) -> List[Document]:
        """Tìm kiếm documents"""
        return self.vector_store.similarity_search(query, k=k)
    
    def add_document(self, file_path: str):
        """Thêm document mới vào vector store"""
        chunks = self.document_processor.process_document(file_path)
        if chunks:
            self.vector_store.add_documents(chunks)
            self.vector_store.save()
            print(f"Added {len(chunks)} chunks from {file_path}")
    
    def reset_conversation(self):
        """Reset lịch sử hội thoại"""
        self.memory.clear()


if __name__ == "__main__":
    # Test chatbot
    print("Initializing ME Chatbot...")
    
    # Sử dụng OpenAI (default) hoặc local LLM
    # Đổi use_local_llm=True nếu chạy vLLM local
    chatbot = MEChatbot(use_local_llm=False)
    
    print("\n" + "="*50)
    print("ME Employee Assistant Chatbot")
    print("="*50)
    print("\nCommands:")
    print("  - 'quit' hoặc 'exit': Thoát")
    print("  - 'reset': Reset hội thoại")
    print("  - Nhập câu hỏi để chat")
    print("="*50 + "\n")
    
    while True:
        question = input("Bạn: ").strip()
        
        if question.lower() in ['quit', 'exit', 'thoát']:
            print("Tạm biệt!")
            break
        
        if question.lower() == 'reset':
            chatbot.reset_conversation()
            print("✓ Đã reset hội thoại\n")
            continue
        
        if not question:
            continue
        
        print("\nĐang xử lý...\n")
        result = chatbot.chat(question)
        
        print(f"Bot: {result['answer']}\n")
        
        if result['sources']:
            print("📚 Nguồn tham khảo:")
            for i, source in enumerate(result['sources'][:3], 1):
                print(f"  {i}. {source['filename']}")
            print()
