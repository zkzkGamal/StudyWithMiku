#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

PROJECT_DIR=$(pwd)
VENV_DIR="$PROJECT_DIR/venv"
DIFFSINGER_DIR="$PROJECT_DIR/DiffSinger"
MODELS_DIR="$PROJECT_DIR/models"
ENV_FILE="$PROJECT_DIR/.env"
ENV_EXAMPLE="$PROJECT_DIR/.env.example"

echo -e "${PURPLE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║   🎤 StudyWithMiku - Automated Installer 🎤   ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════╝${NC}"
echo ""

# ---------- Step 1: System Dependencies Check ----------
echo -e "${CYAN}[1/10]${NC} ${BLUE}Checking system dependencies...${NC}"

# Check for required system packages
REQUIRED_PACKAGES=("python3" "python3-venv" "python3-pip" "git" "curl" "unzip")
MISSING_PACKAGES=()

for pkg in "${REQUIRED_PACKAGES[@]}"; do
  if ! command -v $pkg &> /dev/null && ! dpkg -l | grep -q "^ii  $pkg"; then
    MISSING_PACKAGES+=($pkg)
  fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
  echo -e "${YELLOW}⚠️  Missing packages: ${MISSING_PACKAGES[*]}${NC}"
  echo -e "${BLUE}Installing missing packages...${NC}"
  sudo apt update
  sudo apt install -y "${MISSING_PACKAGES[@]}"
  echo -e "${GREEN}✅ System dependencies installed${NC}"
else
  echo -e "${GREEN}✅ All system dependencies present${NC}"
fi

# ---------- Step 2: Create Virtual Environment ----------
echo -e "\n${CYAN}[2/10]${NC} ${BLUE}Setting up virtual environment...${NC}"

if [ -d "$VENV_DIR" ]; then
  echo -e "${GREEN}✅ Virtual environment already exists${NC}"
else
  echo -e "${YELLOW}🛠  Creating virtual environment...${NC}"
  python3 -m venv venv
  echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# ---------- Step 3: Install PyTorch ----------
echo -e "\n${CYAN}[3/10]${NC} ${BLUE}Installing PyTorch...${NC}"

if python3 -c "import torch" 2>/dev/null; then
  echo -e "${GREEN}✅ PyTorch already installed${NC}"
else
  echo -e "${YELLOW}⚡ Installing PyTorch with CUDA 11.8 support...${NC}"
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  echo -e "${GREEN}✅ PyTorch installed${NC}"
fi

# ---------- Step 4: Install Project Requirements ----------
echo -e "\n${CYAN}[4/10]${NC} ${BLUE}Installing project dependencies...${NC}"

if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  pip install -r "$PROJECT_DIR/requirements.txt"
  echo -e "${GREEN}✅ Project dependencies installed${NC}"
else
  echo -e "${RED}❌ requirements.txt not found${NC}"
  exit 1
fi

# ---------- Step 5: Clone DiffSinger ----------
echo -e "\n${CYAN}[5/10]${NC} ${BLUE}Setting up DiffSinger...${NC}"

if [ ! -d "$DIFFSINGER_DIR" ]; then
  echo -e "${YELLOW}📥 Cloning DiffSinger repository...${NC}"
  git clone https://github.com/openvpi/DiffSinger.git
  echo -e "${GREEN}✅ DiffSinger cloned${NC}"
else
  echo -e "${GREEN}✅ DiffSinger already exists${NC}"
fi

# ---------- Step 6: Install DiffSinger Requirements ----------
echo -e "\n${CYAN}[6/10]${NC} ${BLUE}Installing DiffSinger dependencies...${NC}"

cd "$DIFFSINGER_DIR"
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
  echo -e "${GREEN}✅ DiffSinger dependencies installed${NC}"
fi

# Fix dependency conflicts
echo -e "${YELLOW}🔧 Fixing dependency conflicts...${NC}"
pip install librosa==0.10.0 --force-reinstall --quiet
pip install protobuf==3.19.5 --force-reinstall --quiet
echo -e "${GREEN}✅ Dependencies fixed${NC}"

cd "$PROJECT_DIR"

# ---------- Step 7: Configure PYTHONPATH ----------
echo -e "\n${CYAN}[7/10]${NC} ${BLUE}Configuring PYTHONPATH...${NC}"

EXPORT_LINE="export PYTHONPATH=\$PYTHONPATH:$DIFFSINGER_DIR"
if ! grep -Fxq "$EXPORT_LINE" ~/.bashrc; then
  echo "$EXPORT_LINE" >> ~/.bashrc
  echo -e "${GREEN}✅ PYTHONPATH added to ~/.bashrc${NC}"
else
  echo -e "${GREEN}✅ PYTHONPATH already configured${NC}"
fi

export PYTHONPATH="${PYTHONPATH}:$DIFFSINGER_DIR"

# ---------- Step 8: Download Vocoder Model ----------
echo -e "\n${CYAN}[8/10]${NC} ${BLUE}Downloading vocoder model...${NC}"

mkdir -p "$MODELS_DIR/vocoder"
cd "$MODELS_DIR/vocoder"

VOCODER_URL="https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-v1/nsf_hifigan_20221211.zip"
VOCODER_ZIP="nsf_hifigan_20221211.zip"

if [ -f "$VOCODER_ZIP" ] && [ -d "nsf_hifigan" ]; then
  echo -e "${GREEN}✅ Vocoder model already downloaded and extracted${NC}"
else
  echo -e "${YELLOW}📥 Downloading NSF-HiFiGAN vocoder (~93MB)...${NC}"
  curl -L -o "$VOCODER_ZIP" "$VOCODER_URL" --progress-bar
  
  # Verify download
  MIN_SIZE=90000000  # 90MB minimum
  if [ $(stat -c%s "$VOCODER_ZIP") -lt $MIN_SIZE ]; then
    echo -e "${RED}❌ Download failed (file too small)${NC}"
    rm "$VOCODER_ZIP"
    exit 1
  fi
  
  echo -e "${YELLOW}📦 Extracting vocoder model...${NC}"
  unzip -o "$VOCODER_ZIP" || { echo -e "${RED}❌ Extraction failed${NC}"; rm "$VOCODER_ZIP"; exit 1; }
  echo -e "${GREEN}✅ Vocoder model downloaded and extracted${NC}"
fi

cd "$PROJECT_DIR"

# ---------- Step 9: Setup Environment Variables ----------
echo -e "\n${CYAN}[9/10]${NC} ${BLUE}Configuring environment variables...${NC}"

if [ ! -f "$ENV_FILE" ]; then
  if [ -f "$ENV_EXAMPLE" ]; then
    echo -e "${YELLOW}📝 Creating .env file from .env.example...${NC}"
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your configuration${NC}"
  else
    echo -e "${RED}❌ .env.example not found${NC}"
    exit 1
  fi
else
  echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Create content and data directories
mkdir -p "$PROJECT_DIR/content"
mkdir -p "$PROJECT_DIR/data"
echo -e "${GREEN}✅ Created content/ and data/ directories${NC}"

# ---------- Step 10: Verify Installation ----------
echo -e "\n${CYAN}[10/10]${NC} ${BLUE}Verifying installation...${NC}"

# Test DiffSinger import
if python3 -c "import sys; sys.path.append('$DIFFSINGER_DIR'); import utils.hparams" 2>/dev/null; then
  echo -e "${GREEN}✅ DiffSinger import successful${NC}"
else
  echo -e "${YELLOW}⚠️  DiffSinger import test failed (may work at runtime)${NC}"
fi

# Test core dependencies
echo -e "${BLUE}Testing core dependencies...${NC}"
python3 - <<'EOF'
import sys
errors = []
try:
    import langchain
    print("✅ LangChain")
except Exception as e:
    errors.append(f"❌ LangChain: {e}")
    
try:
    import langgraph
    print("✅ LangGraph")
except Exception as e:
    errors.append(f"❌ LangGraph: {e}")
    
try:
    import chromadb
    print("✅ ChromaDB")
except Exception as e:
    errors.append(f"❌ ChromaDB: {e}")
    
try:
    import torch
    print("✅ PyTorch")
except Exception as e:
    errors.append(f"❌ PyTorch: {e}")

if errors:
    for error in errors:
        print(error)
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ All core dependencies verified${NC}"
else
  echo -e "${RED}❌ Some dependencies failed verification${NC}"
  exit 1
fi

# ---------- Installation Complete ----------
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          🎉 Installation Complete! 🎉         ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo -e "   1. ${YELLOW}Edit .env file${NC} with your configuration (LLM provider, API keys, etc.)"
echo -e "   2. ${YELLOW}Add PDF files${NC} to the content/ folder for study materials"
echo -e "   3. ${YELLOW}Run the application:${NC} python main.py"
echo ""
echo -e "${CYAN}💡 Quick Start Commands:${NC}"
echo -e "   ${GREEN}source venv/bin/activate${NC}  # Activate virtual environment"
echo -e "   ${GREEN}python main.py${NC}             # Start StudyWithMiku"
echo ""

# ---------- Ask to Run the Application ----------
echo -e "${PURPLE}════════════════════════════════════════════════${NC}"
read -p "$(echo -e ${CYAN}Would you like to start StudyWithMiku now? [y/N]: ${NC})" -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo -e "${GREEN}🚀 Starting StudyWithMiku...${NC}"
  echo ""
  python main.py
else
  echo -e "${BLUE}👋 Run 'python main.py' when you're ready to start!${NC}"
  echo -e "${YELLOW}⚠️  Remember to activate the virtual environment first:${NC}"
  echo -e "   ${GREEN}source venv/bin/activate${NC}"
fi