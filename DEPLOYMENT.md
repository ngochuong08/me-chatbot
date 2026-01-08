# Hướng Dẫn Deploy Miễn Phí

## ⚠️ Lưu ý quan trọng

**Ollama không thể chạy trên free hosting** do cần 4-8GB RAM và GPU. Để deploy miễn phí, bạn cần:

- Sử dụng OpenAI API (trả phí nhưng rẻ: ~$0.002/1K tokens)
- Hoặc deploy backend riêng và frontend riêng

## Option 1: Gradio trên Hugging Face Spaces (Khuyên dùng)

### Ưu điểm

- ✅ Hoàn toàn miễn phí
- ✅ Dễ deploy nhất
- ✅ Auto SSL/HTTPS
- ✅ Có thể public hoặc private

### Bước 1: Chuẩn bị

```bash
# Tạo file requirements.txt cho HF Spaces
cat > requirements_hf.txt << EOF
langchain==0.1.0
openai==1.3.0
python-dotenv==1.0.0
gradio==4.8.0
sentence-transformers==2.2.2
faiss-cpu==1.7.4
PyPDF2==3.0.1
python-docx==1.1.0
numpy<2.0.0
EOF
```

### Bước 2: Tạo Hugging Face Space

1. Truy cập https://huggingface.co/spaces
2. Click "Create new Space"
3. Chọn:
   - **SDK**: Gradio
   - **Hardware**: CPU basic (miễn phí)
   - **Visibility**: Private (nếu muốn bảo mật)

### Bước 3: Upload code

```bash
# Clone space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy files cần thiết
cp -r /path/to/project/src .
cp /path/to/project/app_gradio.py .
cp requirements_hf.txt requirements.txt

# Tạo file .env (secrets)
# Không commit file này, sẽ config trên web
```

### Bước 4: Sửa app_gradio.py

```python
# Thêm vào đầu file
import os

# Đảm bảo sử dụng OpenAI
os.environ['LLM_PROVIDER'] = 'openai'

# Phần khởi tạo chatbot
chatbot = Chatbot(
    documents_path="./documents",
    llm_provider="openai"  # Force OpenAI
)
```

### Bước 5: Config Secrets trên HF

1. Vào Settings của Space
2. Thêm Repository secrets:
   - `OPENAI_API_KEY`: sk-your-key-here
   - `LLM_PROVIDER`: openai

### Bước 6: Push code

```bash
git add .
git commit -m "Initial deploy"
git push
```

Space sẽ tự động build và deploy! Truy cập tại: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

---

## Option 2: Web Interface trên Render (Miễn phí)

### Ưu điểm

- ✅ Miễn phí với 750 giờ/tháng
- ✅ Auto deploy từ GitHub
- ✅ Hỗ trợ Node.js + Python

### Bước 1: Chuẩn bị GitHub Repo

```bash
# Tạo .gitignore
cat > .gitignore << EOF
venv/
__pycache__/
.env
*.pyc
node_modules/
vector_db/
.DS_Store
EOF

# Push lên GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

### Bước 2: Deploy Python Backend lên Render

1. Truy cập https://render.com
2. Tạo **Web Service** mới:

   - **Repository**: Chọn GitHub repo của bạn
   - **Name**: chatbot-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_server.py`
   - **Instance Type**: Free

3. Thêm Environment Variables:
   - `LLM_PROVIDER`: openai
   - `OPENAI_API_KEY`: sk-your-key-here
   - `PORT`: 5000

### Bước 3: Deploy Node.js Frontend lên Render

1. Tạo **Web Service** mới:

   - **Repository**: Same GitHub repo
   - **Name**: chatbot-web
   - **Root Directory**: web
   - **Environment**: Node
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Instance Type**: Free

2. Thêm Environment Variables:
   - `API_URL`: URL của backend (từ bước 2)
   - `PORT`: 3000

### Bước 4: Sửa web/server.js

```javascript
// Thay đổi API URL
const API_URL = process.env.API_URL || "http://localhost:5000";

// Sử dụng trong routes
app.post("/chat", async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

---

## Option 3: Railway (Miễn phí $5 credit/tháng)

### Ưu điểm

- ✅ $5 free credit mỗi tháng
- ✅ Deploy cả Python + Node.js cùng lúc
- ✅ Rất dễ setup

### Bước 1: Deploy

1. Truy cập https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Chọn repository của bạn

### Bước 2: Config Services

Railway sẽ tự động detect 2 services:

**Service 1: Python Backend**

```bash
# Railway sẽ tự chạy
python api_server.py
```

**Service 2: Node.js Frontend**

```bash
# Railway sẽ tự chạy
cd web && npm install && npm start
```

### Bước 3: Environment Variables

Thêm vào Python service:

- `LLM_PROVIDER`: openai
- `OPENAI_API_KEY`: sk-your-key-here

Thêm vào Node.js service:

- `API_URL`: URL của Python service (Railway tự generate)

---

## Option 4: Vercel (Chỉ Frontend)

Nếu chỉ muốn deploy frontend và dùng backend local:

```bash
cd web
npm install -g vercel
vercel
```

Follow prompts và deploy!

---

## So sánh các nền tảng

| Platform  | Free Tier    | Python | Node.js | Ease       | Uptime          |
| --------- | ------------ | ------ | ------- | ---------- | --------------- |
| HF Spaces | ✅ Vĩnh viễn | ✅     | ❌      | ⭐⭐⭐⭐⭐ | 99%             |
| Render    | 750h/tháng   | ✅     | ✅      | ⭐⭐⭐⭐   | Sleep sau 15min |
| Railway   | $5/tháng     | ✅     | ✅      | ⭐⭐⭐⭐⭐ | 99%             |
| Vercel    | ✅ Vĩnh viễn | ❌     | ✅      | ⭐⭐⭐⭐⭐ | 99%             |

---

## Chi phí ước tính với OpenAI

Với 10,000 nhân viên, mỗi người hỏi 10 câu/ngày:

```
100,000 câu hỏi/ngày
× ~500 tokens/câu (input + output)
× $0.002/1K tokens
= ~$100/ngày = $3,000/tháng
```

### Giải pháp tiết kiệm:

1. **Cache câu trả lời** - giảm 50-70% chi phí
2. **Giới hạn rate** - 5 câu/user/ngày
3. **Dùng GPT-3.5** thay vì GPT-4 - rẻ hơn 10x
4. **Self-host nhỏ** - Deploy Ollama trên VPS ($20-50/tháng)

---

## Troubleshooting

### Lỗi: "Out of memory"

→ Giảm `CHUNK_SIZE` trong .env xuống 500

### Lỗi: "Cold start timeout"

→ Dùng Railway hoặc HF Spaces (không sleep)

### Lỗi: "OpenAI rate limit"

→ Thêm retry logic hoặc nâng tier OpenAI

### Documents không load

→ Upload documents folder lên cloud (S3, Google Drive) và mount

---

## Best Practices

1. ✅ **Luôn dùng environment variables** cho API keys
2. ✅ **Enable CORS** nếu frontend và backend khác domain
3. ✅ **Giới hạn file size upload** (< 10MB)
4. ✅ **Add rate limiting** để tránh abuse
5. ✅ **Monitor usage** OpenAI để tránh bill shock
6. ✅ **Backup vector_db** định kỳ

---

## Next Steps

1. Chọn platform phù hợp với nhu cầu
2. Tạo OpenAI API key tại https://platform.openai.com
3. Follow hướng dẫn deploy ở trên
4. Test kỹ trước khi share link cho users
5. Monitor logs và usage thường xuyên

Nếu cần support, tạo issue trên GitHub repo!
