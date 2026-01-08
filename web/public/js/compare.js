const file1Path = document.getElementById("file1Path");
const file2Path = document.getElementById("file2Path");
const compareBtn = document.getElementById("compareBtn");
const compareResults = document.getElementById("compareResults");

async function compareDocuments() {
  const path1 = file1Path.value.trim();
  const path2 = file2Path.value.trim();

  if (!path1 || !path2) {
    alert("Vui lòng nhập đường dẫn của cả 2 file");
    return;
  }

  // Show loading
  compareResults.innerHTML = '<div class="loading">📊 Đang so sánh...</div>';

  try {
    const response = await fetch("/api/compare", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        file1: path1,
        file2: path2,
      }),
    });

    const data = await response.json();

    if (data.error) {
      compareResults.innerHTML = `<div class="error">❌ Lỗi: ${data.error}</div>`;
      return;
    }

    // Display results
    let html = `
            <div class="result-item">
                <h2>📊 Kết quả so sánh</h2>
                <p><strong>File 1:</strong> ${data.file1}</p>
                <p><strong>File 2:</strong> ${data.file2}</p>
                <p><strong>Độ tương đồng:</strong> ${data.similarity}</p>
            </div>
            
            <div class="result-item">
                <h3>📝 Tóm tắt</h3>
                <pre style="white-space: pre-wrap; line-height: 1.8;">${data.summary}</pre>
            </div>
        `;

    // Show changes
    const changes = data.changes;

    if (changes.added_content && changes.added_content.length > 0) {
      html += `
                <div class="result-item">
                    <h3>➕ Nội dung thêm mới (mẫu)</h3>
                    <pre style="background: #e8f5e9; padding: 15px; border-radius: 5px; overflow-x: auto;">`;

      changes.added_content.slice(0, 10).forEach((line) => {
        html += `+ ${line}\n`;
      });

      html += `</pre></div>`;
    }

    if (changes.removed_content && changes.removed_content.length > 0) {
      html += `
                <div class="result-item">
                    <h3>➖ Nội dung bị xóa (mẫu)</h3>
                    <pre style="background: #ffebee; padding: 15px; border-radius: 5px; overflow-x: auto;">`;

      changes.removed_content.slice(0, 10).forEach((line) => {
        html += `- ${line}\n`;
      });

      html += `</pre></div>`;
    }

    compareResults.innerHTML = html;
  } catch (error) {
    compareResults.innerHTML = `<div class="error">❌ Lỗi kết nối: ${error.message}</div>`;
  }
}

// Event listener
compareBtn.addEventListener("click", compareDocuments);
