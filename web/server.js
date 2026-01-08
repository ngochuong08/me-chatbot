const express = require("express");
const axios = require("axios");
const multer = require("multer");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || "http://localhost:5000";

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("public"));
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "../documents/");
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + "-" + file.originalname);
  },
});
const upload = multer({ storage });

// Routes
app.get("/", (req, res) => {
  res.render("index");
});

app.get("/search", (req, res) => {
  res.render("search");
});

app.get("/compare", (req, res) => {
  res.render("compare");
});

// API Proxy endpoints
app.post("/api/chat", async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: error.response?.data?.error || error.message,
    });
  }
});

app.post("/api/search", async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/api/search`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: error.response?.data?.error || error.message,
    });
  }
});

app.post("/api/compare", async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/api/compare`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: error.response?.data?.error || error.message,
    });
  }
});

app.post("/api/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const formData = new FormData();
    formData.append("file", req.file);

    const response = await axios.post(`${API_URL}/api/upload`, formData, {
      headers: formData.getHeaders(),
    });

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: error.response?.data?.error || error.message,
    });
  }
});

app.post("/api/reset", async (req, res) => {
  try {
    const conversationId = req.body.conversation_id || "default";
    const response = await axios.post(
      `${API_URL}/api/conversations/${conversationId}/reset`
    );
    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      error: error.response?.data?.error || error.message,
    });
  }
});

app.listen(PORT, () => {
  console.log("\n" + "=".repeat(60));
  console.log(`ME Chatbot Web Interface`);
  console.log("=".repeat(60));
  console.log(`\nServer running at: http://localhost:${PORT}`);
  console.log(`API Server: ${API_URL}`);
  console.log("\nMake sure the Python API server is running!");
  console.log("=".repeat(60) + "\n");
});
