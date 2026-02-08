#!/bin/bash
set -e

PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"
DIFFSINGER_DIR="$PROJECT_DIR/DiffSinger"
MODELS_DIR="$PROJECT_DIR/models"

echo "🚀 Starting smart installer for StudyWithMiku..."

# ---------- Step 1: Check or create venv ----------
if [ -d "$VENV_DIR" ]; then
  echo "✅ Virtual environment already exists: $VENV_DIR"
else
  echo "🛠 Creating virtual environment..."
  python3 -m venv venv
fi

echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ---------- Step 2: Install PyTorch only if missing ----------
if [ "$(python3 - << 'EOF'
import importlib.util
print("MISSING" if importlib.util.find_spec("torch") is None else "OK")
EOF
)" = "MISSING" ]; then
  echo "⚡ Installing PyTorch..."
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
else
  echo "✅ PyTorch already installed"
fi

# ---------- Step 3: Install project requirements ----------
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  echo "📦 Installing project requirements..."
  pip install -r "$PROJECT_DIR/requirements.txt"
fi

# ---------- Step 4: Clone DiffSinger if missing ----------
if [ ! -d "$DIFFSINGER_DIR" ]; then
  echo "📥 Cloning DiffSinger..."
  git clone https://github.com/openvpi/DiffSinger.git
else
  echo "📌 DiffSinger already exists"
fi

# ---------- Step 5: Install DiffSinger requirements ----------
cd "$DIFFSINGER_DIR"
if [ -f "requirements.txt" ]; then
  echo "📦 Installing DiffSinger requirements..."
  pip install -r requirements.txt
fi

# Fix dependency conflicts if present
pip install librosa==0.10.0 --force-reinstall
pip install protobuf==3.19.5 --force-reinstall
echo "🔧 Fixed potential dependency conflicts for librosa and protobuf"

# ---------- Step 6: Add DiffSinger to PYTHONPATH ----------
EXPORT_LINE="export PYTHONPATH=\$PYTHONPATH:$DIFFSINGER_DIR"
if ! grep -Fxq "$EXPORT_LINE" ~/.bashrc; then
  echo "$EXPORT_LINE" >> ~/.bashrc
  echo "🔧 Added DiffSinger to PYTHONPATH in ~/.bashrc"
else
  echo "📌 PYTHONPATH already configured in ~/.bashrc"
fi

# Set PYTHONPATH immediately for the current session
export PYTHONPATH="${PYTHONPATH}:$DIFFSINGER_DIR"
echo "🔧 Set PYTHONPATH for current session"

# ---------- Step 7: Download NSF-HiFiGAN vocoder model (v1) ----------
mkdir -p "$MODELS_DIR/vocoder"
cd "$MODELS_DIR/vocoder"

echo "📥 Downloading NSF-HiFiGAN vocoder model (v1)..."
VOCODER_URL="https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-v1/nsf_hifigan_20221211.zip"
VOCODER_ZIP="nsf_hifigan_20221211.zip"

if [ -f "$VOCODER_ZIP" ]; then
  echo "📌 Vocoder model already downloaded"
else
  curl -L -o "$VOCODER_ZIP" "$VOCODER_URL"
  # Basic size check (v1 zip is ~93MB; adjust if using other versions)
  MIN_SIZE=90000000  # 90MB minimum
  if [ $(stat -c%s "$VOCODER_ZIP") -lt $MIN_SIZE ]; then
    echo "❌ Download failed (file too small). Removing invalid file."
    rm "$VOCODER_ZIP"
    exit 1
  fi
fi

# Unzip with error handling
unzip -o "$VOCODER_ZIP" || { echo "❌ Unzip failed. The file may be corrupted. Try re-downloading."; rm "$VOCODER_ZIP"; exit 1; }

# ---------- Step 8: Import test ----------
echo "🧪 Testing DiffSinger import..."
python3 - << 'EOF'
try:
    import utils.hparams
    print("✅ DiffSinger import OK")
except Exception as e:
    print("❌ DiffSinger import FAILED:", e)
EOF

echo "🎉 Install + Test Complete!"
source venv/bin/activate
echo "Activate venv: source venv/bin/activate"
echo "Note: For new terminals, source ~/.bashrc to apply PYTHONPATH changes."