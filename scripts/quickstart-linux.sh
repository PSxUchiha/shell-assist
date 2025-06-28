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
echo "🤖 Checking for deepseek-coder:6.7b model..."
if ollama list | grep -q "deepseek-coder:6.7b"; then
    echo "✅ Model deepseek-coder:6.7b already available"
else
    echo "📥 Model not found. Pulling deepseek-coder:6.7b model..."
    ollama pull deepseek-coder:6.7b
    echo "✅ Model pulled successfully"
fi

# 4. Set up Python venv
if [ ! -d "venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv venv
else
  echo "✅ Virtual environment already exists"
fi
source venv/bin/activate

# 5. Install dependencies only if necessary
echo "🔍 Checking Python dependencies..."
python3 check_dependencies.py
dependency_status=$?

if [ $dependency_status -eq 0 ]; then
    echo "✅ All dependencies are already satisfied"
elif [ $dependency_status -eq 1 ] || [ $dependency_status -eq 2 ]; then
    echo "📦 Installing/updating Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error checking dependencies"
    exit 1
fi

# 6. Final verification
echo "🔍 Final dependency verification..."
python3 check_dependencies.py
if [ $? -eq 0 ]; then
    echo "✅ All dependencies verified successfully"
else
    echo "❌ Dependency verification failed"
    exit 1
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