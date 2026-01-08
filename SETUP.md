# Hướng dẫn cài đặt và chạy ứng dụng

## 🚀 Quick Start

### 1. Cài đặt Python Dependencies

```bash
# Tạo virtual environment
python -m venv venv

# Activate virtual environment
# MacOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt
```

### 2. Cấu hình Environment

```bash
# Copy file .env
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn
nano .env
```

**Cấu hình quan trọng trong .env:**

- `OPENAI_API_KEY`: API key của OpenAI (nếu dùng OpenAI)
- `LLM_API_BASE`: URL của local LLM server (nếu dùng vLLM)
- `LLM_MODEL_NAME`: Tên model (VD: Qwen3-14B-AWQ)

### 3. Thêm tài liệu

```bash
# Tạo thư mục documents
mkdir -p documents

# Copy các file PDF, DOCX, TXT vào thư mục documents/
# Ví dụ:
# cp ~/path/to/quy_dinh_2024.pdf documents/
```

## 💻 Chạy ứng dụng

### Option 1: Chạy với Gradio (Đơn giản nhất)

```bash
python app_gradio.py
```

Mở browser: `http://localhost:7860`

### Option 2: Chạy với Node.js Web Interface

**Terminal 1 - Python API Server:**

```bash
python api_server.py
```

**Terminal 2 - Node.js Web Server:**

```bash
cd web
npm install
npm start
```

Mở browser: `http://localhost:3000`

## 🔧 Setup vLLM (Optional - để chạy local LLM)

### Cài đặt vLLM

```bash
pip install vllm
```

### Chạy vLLM với Qwen3-14B-AWQ

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen3-14B-AWQ \
    --quantization awq \
    --dtype half \
    --max-model-len 4096 \
    --port 8000
```

### Cập nhật .env

```bash
LLM_API_BASE=http://localhost:8000/v1
LLM_MODEL_NAME=Qwen3-14B-AWQ
```

### Cập nhật code để dùng local LLM

Trong `app_gradio.py` hoặc `api_server.py`, đổi:

```python
chatbot = MEChatbot(
    use_local_llm=True  # Đổi thành True
)
```

## 📝 Test thử

### Test Python chatbot

```bash
python src/chatbot.py
```

### Test document processing

```bash
python src/document_processor.py
```

### Test vector store

```bash
python src/vector_store.py
```

## ⚠️ Troubleshooting

### Lỗi: "No module named 'langchain'"

```bash
pip install -r requirements.txt
```

### Lỗi: "Vector store not initialized"

Đảm bảo có tài liệu trong thư mục `./documents/` và chạy:

```bash
python src/vector_store.py
```

### Lỗi: "API connection failed"

- Kiểm tra Python API server đang chạy (`python api_server.py`)
- Kiểm tra port 5000 không bị chiếm dụng
- Kiểm tra OPENAI_API_KEY trong `.env` (nếu dùng OpenAI)

### Lỗi: "Permission denied" khi install packages

```bash
pip install --user -r requirements.txt
```

## 🎯 Sử dụng

### 1. Chat với Bot

- Mở Gradio hoặc Web interface
- Nhập câu hỏi về tài liệu
- Bot sẽ tìm kiếm và trả lời với trích dẫn nguồn

### 2. Tìm kiếm Tài liệu

- Vào tab "Tìm kiếm"
- Nhập từ khóa
- Xem kết quả tìm kiếm từ tài liệu

### 3. So sánh Tài liệu

- Vào tab "So sánh"
- Nhập đường dẫn 2 file
- Xem sự khác biệt giữa 2 phiên bản

### 4. Upload Tài liệu Mới

- Vào tab "Upload"
- Chọn file PDF/DOCX/TXT
- Hệ thống tự động index

## 📦 Production Deployment

### Sử dụng Docker (Recommended)

Tạo `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "api_server.py"]
```

Build và chạy:

```bash
docker build -t ME-chatbot .
docker run -p 5000:5000 -v $(pwd)/documents:/app/documents ME-chatbot
```

### Sử dụng PM2 cho Node.js

```bash
npm install -g pm2

# Start API server
pm2 start api_server.py --interpreter python --name ME-api

# Start Web server
cd web
pm2 start server.js --name ME-web

# Save configuration
pm2 save
pm2 startup
```

## 🔐 Security Notes

- **Không commit file .env vào git**
- **Bảo mật API keys**
- **Giới hạn upload file size**
- **Implement authentication cho production**
- **Sử dụng HTTPS trong production**

## 📚 Tài liệu tham khảo

- [Langchain Documentation](https://python.langchain.com/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Express.js Documentation](https://expressjs.com/)
