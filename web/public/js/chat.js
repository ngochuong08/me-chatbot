const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const resetBtn = document.getElementById("resetBtn");
const chips = document.querySelectorAll(".chip");

let conversationId = "default";

// Add message to chat
function addMessage(content, isUser, sources = null) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user" : "bot"}`;

  let messageHTML = `
        <div class="message-content">
            ${content}
        </div>
    `;

  // Add sources if available
  if (sources && sources.length > 0) {
    messageHTML += `
            <div class="message-sources">
                <h4>📚 Nguồn tham khảo:</h4>
                <ul>
                    ${sources
                      .slice(0, 3)
                      .map(
                        (s) => `
                        <li>📄 ${s.filename}</li>
                    `
                      )
                      .join("")}
                </ul>
            </div>
        `;
  }

  messageDiv.innerHTML = messageHTML;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message
async function sendMessage() {
  const message = messageInput.value.trim();

  if (!message) return;

  // Add user message
  addMessage(message, true);
  messageInput.value = "";

  // Add loading message
  addMessage("Đang xử lý...", false);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
        conversation_id: conversationId,
      }),
    });

    const data = await response.json();

    // Remove loading message
    chatBox.removeChild(chatBox.lastChild);

    if (data.error) {
      addMessage(`❌ Lỗi: ${data.error}`, false);
    } else {
      addMessage(data.answer, false, data.sources);
    }
  } catch (error) {
    // Remove loading message
    chatBox.removeChild(chatBox.lastChild);
    addMessage(`❌ Lỗi kết nối: ${error.message}`, false);
  }
}

// Reset conversation
async function resetConversation() {
  if (!confirm("Bạn có chắc muốn reset hội thoại?")) return;

  try {
    await fetch("/api/reset", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        conversation_id: conversationId,
      }),
    });

    // Clear chat box
    chatBox.innerHTML = `
            <div class="welcome-message">
                <h2>Xin chào! 👋</h2>
                <p>Tôi là trợ lý AI của ME. Tôi có thể giúp bạn:</p>
                <ul>
                    <li>🔍 Tìm kiếm thông tin trong tài liệu nội bộ</li>
                    <li>💡 Trả lời câu hỏi về quy định, chính sách</li>
                    <li>📊 So sánh các phiên bản tài liệu</li>
                    <li>📚 Trích dẫn nguồn tham khảo</li>
                </ul>
                <p><strong>Hãy đặt câu hỏi để bắt đầu!</strong></p>
            </div>
        `;
  } catch (error) {
    alert(`Lỗi: ${error.message}`);
  }
}

// Event listeners
sendBtn.addEventListener("click", sendMessage);
messageInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});
resetBtn.addEventListener("click", resetConversation);

// Suggestion chips
chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    messageInput.value = chip.textContent;
    sendMessage();
  });
});
