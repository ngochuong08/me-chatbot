# AI Chatbot cho 10,000 Nhân Viên - ME

Chatbot hỗ trợ nhân viên với khả năng:

- 🔍 Tìm kiếm tài liệu bằng ngôn ngữ tự nhiên
- 📊 So sánh các phiên bản tài liệu khác nhau
- 🤖 Sử dụng LLM (Qwen3-14B-AWQ) qua vLLM

## Công nghệ sử dụng

- **LLM**: Qwen3-14B-AWQ (deployed with vLLM)
- **Framework**: Langchain, Langgraph
- **Language**: Python
- **UI**: Gradio & Node.js Web Interface
- **Vector DB**: ChromaDB / FAISS

## Cài đặt

### 1. Python Backend

```bash
# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc: venv\Scripts\activate  # Windows

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình

```bash
# Copy file cấu hình
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn
nano .env
```

### 3. Setup vLLM (Optional - nếu chạy local LLM)

```bash
# Cài đặt vLLM
pip install vllm

# Chạy vLLM server với Qwen3-14B-AWQ
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-14B-AWQ \
    --quantization awq \
    --dtype half \
    --max-model-len 4096
```

### 4. Thêm tài liệu

```bash
# Tạo thư mục documents
mkdir -p documents

# Copy các file PDF, DOCX vào thư mục documents/
# Hệ thống sẽ tự động xử lý và index
```

## Chạy ứng dụng

### Option 1: Gradio Interface

```bash
python app_gradio.py
```

Mở browser tại: `http://localhost:7860`

### Option 2: Node.js Web Interface

```bash
# Cài đặt Node.js dependencies
cd web
npm install

# Chạy Python API server
cd ..
python api_server.py

# Chạy Node.js web server (terminal khác)
cd web
npm start
```

Mở browser tại: `http://localhost:3000`

## Cấu trúc thư mục

```
internal-chatbot/
├── documents/              # Thư mục chứa tài liệu
├── vector_db/             # Vector database
├── src/
│   ├── chatbot.py         # Core chatbot logic
│   ├── document_processor.py  # Xử lý tài liệu
│   ├── vector_store.py    # Vector store management
│   └── document_compare.py    # So sánh tài liệu
├── app_gradio.py          # Gradio interface
├── api_server.py          # Flask API server
├── web/                   # Node.js web interface
│   ├── server.js
│   ├── package.json
│   └── public/
├── requirements.txt
├── .env.example
└── README.md
```

## Tính năng

### 1. Tìm kiếm tài liệu

- Hỏi bằng ngôn ngữ tự nhiên
- Tìm kiếm semantic search
- Trả về nguồn tài liệu tham khảo

### 2. So sánh tài liệu

- So sánh 2 phiên bản tài liệu
- Highlight các thay đổi
- Tóm tắt sự khác biệt

## API Endpoints

```
POST /api/chat
- Body: {"message": "câu hỏi", "conversation_id": "optional"}
- Response: {"answer": "...", "sources": [...]}

POST /api/compare
- Body: {"doc1": "path1", "doc2": "path2"}
- Response: {"differences": "...", "summary": "..."}

POST /api/upload
- Body: FormData with file
- Response: {"status": "success", "filename": "..."}
```

## License

MIT
