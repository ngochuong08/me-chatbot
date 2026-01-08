# Hướng dẫn cài đặt Ollama (LLM miễn phí, chạy local)

## 🚀 Ollama là gì?

Ollama cho phép bạn chạy LLM (Large Language Models) trên máy tính của mình hoàn toàn **MIỄN PHÍ** mà không cần API key.

## 📥 Cài đặt Ollama

### macOS

```bash
# Cách 1: Download từ website
# Truy cập: https://ollama.ai/download
# Download và cài đặt file .dmg

# Cách 2: Sử dụng Homebrew
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

Download installer từ: https://ollama.ai/download

## 🎯 Khởi động Ollama

```bash
# Start Ollama service
ollama serve
```

Ollama sẽ chạy tại: `http://localhost:11434`

## 📦 Download models

### Llama 2 (Khuyên dùng cho tiếng Việt)

```bash
# Llama 2 7B (4GB RAM)
ollama pull llama2

# Llama 2 13B (8GB RAM) - tốt hơn nhưng cần nhiều RAM
ollama pull llama2:13b
```

### Các models khác

```bash
# Mistral 7B - rất tốt
ollama pull mistral

# Qwen2 - tốt cho tiếng Trung, tiếng Việt
ollama pull qwen2

# Gemma - từ Google
ollama pull gemma:7b

# Phi-3 - nhỏ gọn, nhanh
ollama pull phi3
```

## ⚙️ Cấu hình cho chatbot

### 1. Tạo file .env

```bash
cp .env.example .env
```

### 2. Chỉnh sửa .env

```bash
# Chọn Ollama làm provider
LLM_PROVIDER=ollama

# Chọn model (mặc định: llama2)
OLLAMA_MODEL=llama2

# URL của Ollama service
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. Chạy chatbot

```bash
python app_gradio.py
```

## 🧪 Test Ollama

```bash
# Test xem Ollama có hoạt động không
ollama run llama2 "Xin chào, bạn là ai?"

# List các models đã cài
ollama list

# Xóa model không dùng
ollama rm mistral
```

## 💡 Khuyến nghị models

| Model      | RAM cần | Tốc độ     | Chất lượng | Tiếng Việt |
| ---------- | ------- | ---------- | ---------- | ---------- |
| llama2     | 4GB     | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐     |
| llama2:13b | 8GB     | ⭐⭐       | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |
| mistral    | 4GB     | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   | ⭐⭐⭐     |
| qwen2      | 4GB     | ⭐⭐⭐     | ⭐⭐⭐     | ⭐⭐⭐⭐   |
| phi3       | 2GB     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐     | ⭐⭐       |

**Khuyên dùng cho dự án này:**

- **llama2**: Cân bằng tốt, hỗ trợ tiếng Việt ổn
- **mistral**: Chất lượng cao, nhanh
- **qwen2**: Tốt nhất cho tiếng Việt và tiếng Trung

## 🔧 Troubleshooting

### Lỗi: "connection refused"

```bash
# Kiểm tra Ollama có chạy không
ps aux | grep ollama

# Nếu chưa chạy, start lại
ollama serve
```

### Lỗi: "model not found"

```bash
# Pull model trước
ollama pull llama2
```

### Chậm quá / Hết RAM

```bash
# Dùng model nhỏ hơn
ollama pull phi3

# Hoặc dùng quantized version
ollama pull llama2:7b-q4_0
```

## 🎯 So sánh với các options khác

| Option     | Chi phí     | Setup  | Tốc độ     | Chất lượng |
| ---------- | ----------- | ------ | ---------- | ---------- |
| **Ollama** | ✅ Miễn phí | ✅ Dễ  | ⭐⭐⭐     | ⭐⭐⭐     |
| OpenAI     | ❌ Trả phí  | ✅ Dễ  | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| vLLM       | ✅ Miễn phí | ❌ Khó | ⭐⭐⭐⭐   | ⭐⭐⭐⭐   |

**✨ Ollama là lựa chọn tốt nhất để bắt đầu - MIỄN PHÍ và DỄ DÙNG!**

## 📚 Tài liệu tham khảo

- [Ollama Website](https://ollama.ai/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Model Library](https://ollama.ai/library)
