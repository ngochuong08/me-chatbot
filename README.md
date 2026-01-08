# AI Chatbot cho 10,000 Nhân Viên - ME

Chatbot hỗ trợ nhân viên với khả năng:

- 🔍 Tìm kiếm tài liệu bằng ngôn ngữ tự nhiên
- 📊 So sánh các phiên bản tài liệu khác nhau
- 🤖 Sử dụng LLM local **MIỄN PHÍ** qua Ollama
- 🇻🇳 Hỗ trợ tiếng Việt xuất sắc với Qwen2

## Công nghệ sử dụng

- **LLM**: Qwen2 (4.4GB) - Hỗ trợ tiếng Việt tốt nhất
- **LLM Runtime**: Ollama (miễn phí, chạy local, không cần API key)
- **Framework**: Langchain
- **Language**: Python
- **UI**: Gradio & Node.js Web Interface
- **Vector DB**: FAISS
- **Embeddings**: Sentence Transformers (multilingual)

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

### 2. Cài đặt Ollama (LLM miễn phí)

**macOS:**

```bash
# Tải và cài đặt từ website
open https://ollama.com/download

# HOẶC dùng Homebrew
brew install ollama
```

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Tải installer từ: https://ollama.com/download

**Khởi động Ollama:**

```bash
# Start Ollama service (chạy trong terminal riêng)
ollama serve

# Download model Qwen2 (4.4GB - tốt nhất cho tiếng Việt)
ollama pull qwen2
```

### 3. Cấu hình

```bash
# Copy file cấu hình
cp .env.example .env

# File .env đã được cấu hình sẵn cho Ollama + Qwen2
# Không cần chỉnh sửa gì thêm!
```

### 4. Thêm tài liệu

```bash
# Tạo thư mục documents
mkdir -p documents

# Copy các file PDF, DOCX vào thư mục documents/
# Hệ thống sẽ tự động xử lý và index
```

## Chạy ứng dụng

**Lưu ý:** Đảm bảo Ollama đang chạy trước khi start chatbot!

### Option 1: Gradio Interface (Khuyên dùng)

```bash
python app_gradio.py
```

Mở browser tại: `http://localhost:7860`

### Option 2: Node.js Web Interface

**Terminal 1 - Python API Server:**

```bash
python api_server.py
```

**Terminal 2 - Node.js Web Server:**

```bash
cd web
npm install  # Chỉ cần chạy lần đầu
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

- Hỏi bằng ngôn ngữ tự nhiên (tiếng Việt hoặc tiếng Anh)
- Tìm kiếm semantic search với FAISS
- Trả về nguồn tài liệu tham khảo

### 2. So sánh tài liệu

- So sánh 2 phiên bản tài liệu
- Highlight các thay đổi
- Tóm tắt sự khác biệt

### 3. Hoàn toàn miễn phí

- ✅ Không cần API key
- ✅ Chạy offline trên máy của bạn
- ✅ Không lo về quota hay chi phí
- ✅ Dữ liệu được bảo mật hoàn toàn

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

## Các LLM Models được hỗ trợ

Bạn có thể thay đổi model trong file `.env`:

| Model        | Tiếng Việt | Size  | RAM cần | Khuyên dùng       |
| ------------ | ---------- | ----- | ------- | ----------------- |
| **qwen2** ⭐ | ⭐⭐⭐⭐⭐ | 4.4GB | 8GB     | ✅ Tốt nhất       |
| llama3       | ⭐⭐⭐⭐   | 4.7GB | 8GB     | ✅ Chất lượng cao |
| mistral      | ⭐⭐⭐     | 4.1GB | 8GB     | ✅ Nhanh          |
| phi3         | ⭐⭐       | 2.2GB | 4GB     | ⚠️ Yếu tiếng Việt |

**Đổi model:**

```bash
# Download model khác
ollama pull llama3

# Sửa file .env
OLLAMA_MODEL=llama3
```

## Tùy chọn LLM khác

Ngoài Ollama (mặc định), bạn có thể dùng:

### Option A: OpenAI API (trả phí)

```bash
# Trong .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

### Option B: vLLM (Advanced)

```bash
# Cài đặt vLLM
pip install vllm

# Chạy vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2-7B-Instruct

# Trong .env
LLM_PROVIDER=vllm
LLM_API_BASE=http://localhost:8000/v1
```

## Xem thêm

- [OLLAMA_SETUP.md](OLLAMA_SETUP.md) - Hướng dẫn chi tiết về Ollama
- [SETUP.md](SETUP.md) - Hướng dẫn setup đầy đủ

## License

MIT
