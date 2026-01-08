const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const searchResults = document.getElementById("searchResults");

async function searchDocuments() {
  const query = searchInput.value.trim();

  if (!query) {
    alert("Vui lòng nhập từ khóa tìm kiếm");
    return;
  }

  // Show loading
  searchResults.innerHTML = '<div class="loading">🔍 Đang tìm kiếm...</div>';

  try {
    const response = await fetch("/api/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
        k: 5,
      }),
    });

    const data = await response.json();

    if (data.error) {
      searchResults.innerHTML = `<div class="error">❌ Lỗi: ${data.error}</div>`;
      return;
    }

    if (data.results.length === 0) {
      searchResults.innerHTML =
        '<div class="result-item">Không tìm thấy kết quả nào</div>';
      return;
    }

    // Display results
    let html = `<h3>Tìm thấy ${data.count} kết quả:</h3>`;

    data.results.forEach((result, index) => {
      html += `
                <div class="result-item">
                    <h3>📄 ${index + 1}. ${result.filename}</h3>
                    <p>${result.content}</p>
                </div>
            `;
    });

    searchResults.innerHTML = html;
  } catch (error) {
    searchResults.innerHTML = `<div class="error">❌ Lỗi kết nối: ${error.message}</div>`;
  }
}

// Event listeners
searchBtn.addEventListener("click", searchDocuments);
searchInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") searchDocuments();
});
