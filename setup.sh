#!/bin/bash

echo "================================================"
echo "ME Chatbot - Quick Setup Script"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-api.txt

# Create directories
echo ""
echo "Creating directories..."
mkdir -p documents
mkdir -p vector_db

# Create .env from example
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "✓ .env file already exists"
fi

# Install Node.js dependencies for web interface
echo ""
echo "Installing Node.js dependencies..."
cd web
if command -v npm &> /dev/null; then
    npm install
    echo "✓ Node.js dependencies installed"
else
    echo "⚠️  npm not found. Skipping Node.js setup."
    echo "   Install Node.js if you want to use the web interface"
fi
cd ..

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Add documents to ./documents/ folder"
echo "2. Edit .env file with your API keys"
echo "3. Run the application:"
echo ""
echo "   Option A - Gradio Interface:"
echo "   $ source venv/bin/activate"
echo "   $ python app_gradio.py"
echo ""
echo "   Option B - Node.js Web Interface:"
echo "   Terminal 1: $ python api_server.py"
echo "   Terminal 2: $ cd web && npm start"
echo ""
echo "================================================"
