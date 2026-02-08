#!/bin/bash
set -e

PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"
DIFFSINGER_DIR="$PROJECT_DIR/DiffSinger"

echo "🚀 Starting smart installer for StudyWithMiku..."

# ---------- Step 1: Check or create venv ----------
if [ -d "$VENV_DIR" ]; then
  echo "✅ Virtual environment already exists: $VENV_DIR"
else
  echo "🛠 Creating virtual environment..."
  python3 -m venv venv
fi

# Activate venv
echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ---------- Step 2: Install PyTorch only if missing ----------
echo "🔍 Checking for PyTorch..."
python3 - << 'EOF'
import importlib.util
import sys

if importlib.util.find_spec("torch") is None:
    print("TORCH_MISSING")
else:
    print("TORCH_OK")
EOF

if [ "$(python3 - << 'EOF'
import importlib.util
print("TORCH_MISSING" if importlib.util.find_spec("torch") is None else "TORCH_OK")
EOF
)" = "TORCH_MISSING" ]; then

  echo "⚡ Installing PyTorch (CUDA 11.8)..."
  pip install torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu118
else
  echo "✅ PyTorch already installed — skipping."
fi

# ---------- Step 3: Install your project requirements ----------
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  echo "📦 Installing project requirements (if missing)..."
  pip install -r "$PROJECT_DIR/requirements.txt"
else
  echo "⚠️ No requirements.txt found in project root."
fi

# ---------- Step 4: Clone DiffSinger only if not present ----------
if [ -d "$DIFFSINGER_DIR" ]; then
  echo "✅ DiffSinger already cloned — skipping git clone."
else
  echo "📥 Cloning DiffSinger..."
  git clone https://github.com/openvpi/DiffSinger.git
fi

# ---------- Step 5: Install DiffSinger requirements ----------
cd "$DIFFSINGER_DIR"

if [ -f "requirements.txt" ]; then
  echo "📦 Installing DiffSinger requirements (if missing)..."
  pip install -r requirements.txt
else
  echo "⚠️ No DiffSinger requirements.txt found."
fi

# ---------- Step 6: Add DiffSinger to PYTHONPATH ----------
EXPORT_LINE='export PYTHONPATH=$PYTHONPATH:'"$DIFFSINGER_DIR"

if grep -Fxq "$EXPORT_LINE" ~/.bashrc; then
  echo "✅ PYTHONPATH already configured."
else
  echo "🔧 Adding DiffSinger to PYTHONPATH..."
  echo "$EXPORT_LINE" >> ~/.bashrc
fi

echo "🎉 Installation finished successfully!"
echo "Run: source venv/bin/activate"
