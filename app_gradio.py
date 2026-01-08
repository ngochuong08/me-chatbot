"""
Gradio Interface cho ME Chatbot
Giao diện web đơn giản để chat và so sánh tài liệu
"""

import gradio as gr
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.chatbot import MEChatbot
from src.document_compare import DocumentCompare


# Initialize chatbot
print("Initializing ME Chatbot...")
chatbot = MEChatbot(
    documents_path="./documents",
    vector_db_path="./vector_db",
    llm_provider="ollama"  # "ollama" (miễn phí), "openai", hoặc "vllm"
)

document_compare = DocumentCompare()


def chat_interface(message, history):
    """Chat interface cho Gradio"""
    if not message.strip():
        return history, ""
    
    # Call chatbot
    result = chatbot.chat(message)
    
    # Format response with sources
    response = result['answer']
    
    if result['sources']:
        response += "\n\n📚 **Nguồn tham khảo:**\n"
        for i, source in enumerate(result['sources'][:3], 1):
            response += f"{i}. {source['filename']}\n"
    
    # Add to history
    history.append((message, response))
    
    return history, ""


def reset_chat():
    """Reset conversation"""
    chatbot.reset_conversation()
    return [], "✓ Đã reset hội thoại"


def search_documents(query):
    """Search documents"""
    if not query.strip():
        return "Vui lòng nhập từ khóa tìm kiếm"
    
    results = chatbot.search_documents(query, k=5)
    
    if not results:
        return "Không tìm thấy tài liệu nào"
    
    output = f"Tìm thấy {len(results)} kết quả:\n\n"
    
    for i, doc in enumerate(results, 1):
        output += f"**{i}. {doc.metadata.get('filename', 'Unknown')}**\n"
        output += f"{doc.page_content[:300]}...\n\n"
        output += "---\n\n"
    
    return output


def compare_files(file1, file2):
    """Compare two uploaded files"""
    if file1 is None or file2 is None:
        return "Vui lòng upload 2 file để so sánh"
    
    try:
        # Get file paths
        path1 = file1.name if hasattr(file1, 'name') else file1
        path2 = file2.name if hasattr(file2, 'name') else file2
        
        # Compare
        result = chatbot.compare_documents(path1, path2)
        
        if 'error' in result:
            return result['error']
        
        # Format output
        output = f"## So sánh tài liệu\n\n"
        output += f"**File 1:** {os.path.basename(path1)}\n"
        output += f"**File 2:** {os.path.basename(path2)}\n\n"
        output += f"### {result['summary']}\n\n"
        
        # Show some changes
        changes = result['changes']
        if changes['added_content']:
            output += "**Nội dung thêm mới (mẫu):**\n```\n"
            for line in changes['added_content'][:5]:
                output += f"+ {line}\n"
            output += "```\n\n"
        
        if changes['removed_content']:
            output += "**Nội dung bị xóa (mẫu):**\n```\n"
            for line in changes['removed_content'][:5]:
                output += f"- {line}\n"
            output += "```\n"
        
        return output
    
    except Exception as e:
        return f"Lỗi: {str(e)}"


def upload_document(file):
    """Upload và index document mới"""
    if file is None:
        return "Vui lòng chọn file"
    
    try:
        # Save to documents folder
        filename = os.path.basename(file.name)
        dest_path = os.path.join("./documents", filename)
        
        # Copy file
        import shutil
        shutil.copy(file.name, dest_path)
        
        # Add to vector store
        chatbot.add_document(dest_path)
        
        return f"✓ Đã upload và index tài liệu: {filename}"
    
    except Exception as e:
        return f"Lỗi: {str(e)}"


# Create Gradio interface
with gr.Blocks(
    title="ME Employee Assistant Chatbot",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    """
) as demo:
    
    gr.Markdown("""
    # 🤖 ME Employee Assistant Chatbot
    
    Chatbot hỗ trợ 10,000 nhân viên ME - Tìm kiếm tài liệu và so sánh phiên bản
    
    **Công nghệ:** LLM (Qwen3-14B-AWQ), Langchain, vLLM
    """)
    
    with gr.Tabs():
        # Tab 1: Chat
        with gr.TabItem("💬 Chat với Bot"):
            with gr.Row():
                with gr.Column(scale=4):
                    chatbot_ui = gr.Chatbot(
                        label="Hội thoại",
                        height=500,
                        show_copy_button=True
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="Tin nhắn",
                            placeholder="Nhập câu hỏi của bạn...",
                            scale=4
                        )
                        send_btn = gr.Button("Gửi", variant="primary", scale=1)
                    
                    with gr.Row():
                        reset_btn = gr.Button("🔄 Reset hội thoại")
                        status_text = gr.Textbox(label="Trạng thái", interactive=False)
                
                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### 💡 Hướng dẫn
                    
                    **Ví dụ câu hỏi:**
                    - Quy định về nghỉ phép là gì?
                    - Làm thế nào để xin tăng ca?
                    - Chính sách làm việc từ xa?
                    - So sánh quy định cũ và mới
                    
                    **Tính năng:**
                    - ✅ Tìm kiếm tài liệu
                    - ✅ Trả lời câu hỏi
                    - ✅ Trích dẫn nguồn
                    - ✅ Nhớ ngữ cảnh
                    """)
            
            # Event handlers
            msg_input.submit(
                chat_interface, 
                inputs=[msg_input, chatbot_ui], 
                outputs=[chatbot_ui, msg_input]
            )
            
            send_btn.click(
                chat_interface, 
                inputs=[msg_input, chatbot_ui], 
                outputs=[chatbot_ui, msg_input]
            )
            
            reset_btn.click(
                reset_chat,
                outputs=[chatbot_ui, status_text]
            )
        
        # Tab 2: Document Search
        with gr.TabItem("🔍 Tìm kiếm Tài liệu"):
            gr.Markdown("### Tìm kiếm tài liệu bằng từ khóa")
            
            with gr.Row():
                search_input = gr.Textbox(
                    label="Từ khóa tìm kiếm",
                    placeholder="Ví dụ: quy định nghỉ phép, chính sách OT...",
                    scale=4
                )
                search_btn = gr.Button("Tìm kiếm", variant="primary", scale=1)
            
            search_output = gr.Markdown(label="Kết quả")
            
            search_btn.click(
                search_documents,
                inputs=[search_input],
                outputs=[search_output]
            )
            
            search_input.submit(
                search_documents,
                inputs=[search_input],
                outputs=[search_output]
            )
        
        # Tab 3: Document Compare
        with gr.TabItem("📊 So sánh Tài liệu"):
            gr.Markdown("### So sánh 2 phiên bản tài liệu")
            
            with gr.Row():
                file1_input = gr.File(
                    label="Tài liệu 1 (Phiên bản cũ)",
                    file_types=[".pdf", ".docx", ".txt"]
                )
                file2_input = gr.File(
                    label="Tài liệu 2 (Phiên bản mới)",
                    file_types=[".pdf", ".docx", ".txt"]
                )
            
            compare_btn = gr.Button("So sánh", variant="primary")
            compare_output = gr.Markdown(label="Kết quả so sánh")
            
            compare_btn.click(
                compare_files,
                inputs=[file1_input, file2_input],
                outputs=[compare_output]
            )
        
        # Tab 4: Upload Document
        with gr.TabItem("📤 Upload Tài liệu"):
            gr.Markdown("""
            ### Upload tài liệu mới vào hệ thống
            
            Hệ thống sẽ tự động xử lý và index tài liệu để chatbot có thể trả lời câu hỏi.
            
            **Định dạng hỗ trợ:** PDF, DOCX, TXT
            """)
            
            upload_file = gr.File(
                label="Chọn tài liệu",
                file_types=[".pdf", ".docx", ".txt"]
            )
            
            upload_btn = gr.Button("Upload & Index", variant="primary")
            upload_output = gr.Textbox(label="Kết quả", interactive=False)
            
            upload_btn.click(
                upload_document,
                inputs=[upload_file],
                outputs=[upload_output]
            )
    
    gr.Markdown("""
    ---
    **ME Internal Chatbot** | Powered by Langchain, vLLM, Qwen3-14B-AWQ
    """)


if __name__ == "__main__":
    # Create documents folder if not exists
    os.makedirs("./documents", exist_ok=True)
    
    print("\n" + "="*60)
    print("Starting ME Chatbot Gradio Interface...")
    print("="*60)
    print("\nĐể sử dụng:")
    print("1. Thêm tài liệu PDF/DOCX vào thư mục './documents'")
    print("2. Hoặc upload trực tiếp qua tab 'Upload Tài liệu'")
    print("3. Chat với bot trong tab 'Chat với Bot'")
    print("\n" + "="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
