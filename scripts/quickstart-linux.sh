#!/bin/bash
set -e

# Quickstart script for Shell Assistant (Linux)

echo "🚀 Setting up Shell Assistant for Linux..."
echo "=========================================="

# 1. Install Ollama if not present
if ! command -v ollama &> /dev/null; then
  echo "📦 Ollama not found. Installing..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "✅ Ollama already installed"
fi

# 2. Start Ollama in the background (if not running)
if ! pgrep -x "ollama" > /dev/null; then
  echo "🚀 Starting Ollama..."
  nohup ollama serve > ollama.log 2>&1 &
  sleep 2
else
  echo "✅ Ollama already running"
fi

# 3. Pull recommended model
echo "🤖 Pulling deepseek-coder model..."
ollama pull deepseek-coder

# 4. Set up Python venv
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv
else
  echo "✅ Virtual environment already exists"
fi
source venv/bin/activate

# 5. Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 6. Verify CLI dependencies
echo "🔍 Checking CLI dependencies..."
if python3 -c "import rich, colorama" 2>/dev/null; then
  echo "✅ CLI dependencies installed successfully"
else
  echo "⚠️  CLI dependencies missing, installing..."
  pip install rich colorama
fi

echo ""
echo "🎉 Setup complete! Choose your interface:"
echo ""
echo "🌐 Web Interface (default):"
echo "   python main.py"
echo ""
echo "💻 CLI Mode (recommended):"
echo "   python main.py --cli"
echo ""
echo "🎬 Demo CLI features:"
echo "   python demo_cli.py"
echo ""
echo "📚 Help:"
echo "   python main.py --help"
echo ""

# Ask user which mode they want to start
read -p "Which mode would you like to start? (web/cli/demo/help): " choice

case $choice in
  "cli"|"CLI")
    echo "🚀 Starting CLI mode..."
    python main.py --cli
    ;;
  "demo"|"Demo")
    echo "🎬 Running CLI demo..."
    python demo_cli.py
    ;;
  "help"|"Help")
    echo "📚 Showing help..."
    python main.py --help
    ;;
  "web"|"Web"|"")
    echo "🌐 Starting web interface..."
    echo "Visit http://localhost:5000 in your browser"
    python main.py
    ;;
  *)
    echo "❌ Invalid choice. Starting web interface..."
    echo "Visit http://localhost:5000 in your browser"
    python main.py
    ;;
esac 