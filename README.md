# StudyWithMiku 🎤📚

**StudyWithMiku** is an AI-powered animated study assistant that reads and embeds PDFs, understands their content, and explains concepts to users using Miku or Teto voices with interactive animations. The system acts as a virtual tutor that learns from your documents and answers questions in a friendly, visual, and engaging way.

## ✨ Features

### 🤖 AI-Powered Assistant

- **Multi-Provider LLM Support**: Works with Ollama (local), Google Gemini, and OpenAI models
- **LangGraph Agent Architecture**: Intelligent tool-calling and conversation flow management
- **Context-Aware Conversations**: Maintains conversation history and understands references

### 📄 Document Processing

- **PDF Embedding**: Automatically processes PDFs dropped in the `content/` folder
- **Vector Database**: Uses ChromaDB for semantic search and retrieval
- **RAG Pipeline**: Retrieves relevant context from embedded documents to answer questions
- **Background Processing**: PDF embedding runs in separate terminal windows without blocking

### 🎵 Text-to-Speech (TTS)

- **Multiple TTS Engines**:
  - Coqui TTS with multi-speaker support
  - DiffSinger vocoder integration for anime-style voices
- **Voice Options**: Miku and Teto character voices
- **Real-time Audio Playback**: Speaks responses using sounddevice

### 🛠️ System Tools

- **Browser Control**: Open URLs in default browser
- **Network Management**: Check internet connectivity, enable Wi-Fi, web search via DuckDuckGo
- **Process Management**: Find and terminate background processes
- **System Commands**: Execute shell commands (date, ls, pwd, etc.)
- **File Watching**: Monitors `content/` folder for new files

### 🔍 Intelligent Behavior

- **Automatic Context Retention**: Remembers previous conversation context
- **Smart Error Recovery**: Handles network failures, missing files, and process errors
- **Path Expansion**: Automatically expands `~` to user home directory
- **Web Search Integration**: Search the web without manual internet checks

## 🏗️ Architecture

```
StudyWithMiku/
├── main.py                    # Main entry point with event loop
├── core/
│   ├── agent.py              # LangGraph agent with tool binding
│   ├── state.py              # Agent state definition
│   └── tools.py              # Tool registry
├── models/
│   ├── LLM.py                # Multi-provider LLM wrapper
│   ├── embedding.py          # Embedding model configuration
│   ├── tts.py                # Text-to-speech engine
│   └── voice.py              # Voice configuration
├── config/
│   └── database.py           # ChromaDB vector store manager
├── tools/
│   ├── browser/              # Browser control tools
│   ├── embedded/             # PDF embedding tools
│   ├── network/              # Network and search tools
│   ├── processes_tools/      # Process management tools
│   └── system/               # System command tools
├── preprocessing/
│   └── pdf.py                # PDF text extraction and chunking
├── DiffSinger/               # DiffSinger vocoder (cloned during install)
├── content/                  # Drop PDFs here for auto-embedding
├── data/                     # ChromaDB storage
├── voices/                   # Voice model files
├── prompt.yaml               # System prompt configuration
├── requirements.txt          # Python dependencies
├── requirements.txt           # Python dependencies
└── install.sh                 # Smart installer script
```

## 📦 Installation

### Prerequisites

- **Operating System**: Ubuntu/Linux (tested on Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **GPU**: CUDA-compatible GPU recommended (for TTS and faster inference)
- **Disk Space**: ~2GB for dependencies and models
- **Internet**: Required for downloading dependencies and models

### Automated Installation (Recommended)

The installer script handles everything automatically - just run it and follow the prompts!

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd StudyWithMiku
```

2. **Run the automated installer**:

```bash
chmod +x install.sh
./install.sh
```

**The installer will automatically:**

- ✅ Check and install system dependencies (python3, git, curl, unzip, etc.)
- ✅ Create and activate a Python virtual environment
- ✅ Upgrade pip, setuptools, and wheel
- ✅ Install PyTorch with CUDA 11.8 support
- ✅ Install all Python dependencies from requirements.txt
- ✅ Clone the DiffSinger repository
- ✅ Install DiffSinger dependencies and fix conflicts
- ✅ Configure PYTHONPATH in ~/.bashrc
- ✅ Download NSF-HiFiGAN vocoder model (~93MB)
- ✅ Create .env file from .env.example
- ✅ Create content/ and data/ directories
- ✅ Verify all installations with dependency tests
- ✅ Optionally launch the application immediately

**Installation Progress:**

```
╔════════════════════════════════════════════════╗
║   🎤 StudyWithMiku - Automated Installer 🎤   ║
╚════════════════════════════════════════════════╝

[1/10] Checking system dependencies...
[2/10] Setting up virtual environment...
[3/10] Installing PyTorch...
[4/10] Installing project dependencies...
[5/10] Setting up DiffSinger...
[6/10] Installing DiffSinger dependencies...
[7/10] Configuring PYTHONPATH...
[8/10] Downloading vocoder model...
[9/10] Configuring environment variables...
[10/10] Verifying installation...

╔════════════════════════════════════════════════╗
║          🎉 Installation Complete! 🎉         ║
╚════════════════════════════════════════════════╝
```

3. **Configure your environment**:

```bash
nano .env  # Edit with your LLM provider settings
```

4. **Start the application**:

```bash
source venv/bin/activate
python main.py
```

### Manual Installation

If you prefer manual control or the automated installer fails:

1. **Install system dependencies**:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl unzip
```

2. **Create virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
```

3. **Install PyTorch**:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

5. **Setup DiffSinger**:

```bash
git clone https://github.com/openvpi/DiffSinger.git
cd DiffSinger
pip install -r requirements.txt
pip install librosa==0.10.0 protobuf==3.19.5 --force-reinstall
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)/DiffSinger
echo "export PYTHONPATH=\$PYTHONPATH:$(pwd)/DiffSinger" >> ~/.bashrc
```

6. **Download vocoder model**:

```bash
mkdir -p models/vocoder
cd models/vocoder
curl -L -o nsf_hifigan_20221211.zip https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-v1/nsf_hifigan_20221211.zip
unzip nsf_hifigan_20221211.zip
cd ../..
```

7. **Configure environment**:

```bash
cp .env.example .env
nano .env
```

### Environment Variables

```env
# LLM Configuration
MODEL_NAME="llama3.2:3b"           # Model name
MODEL_TYPE="ollama"                 # ollama | google | openai

# Embedding Configuration
EMBEDDING_MODEL_NAME="nomic-embed-text"
EMBEDDING_MODEL_TYPE="ollama"       # ollama | google

# TTS Configuration
MODEL_TTS_NAME="tts_models/en/vctk/vits"
MODEL_TTS_TYPE="tts"                # tts | vocoder

# API URLs
OLLAMA_BASE_URL="http://localhost:11434"

# API Keys (if using cloud providers)
GOOGLE_API_KEY=""
OPENAI_API_KEY=""

# Model Settings
MAX_OUTPUT_TOKEN=512
EMBEDDEDING_TRESHOLD=0.0

# Database
DB_LOCATION="./data"
CHROMA_COLLECTION_NAME="study_docs"
```

## 🚀 Usage

### Starting the Assistant

1. **Activate the virtual environment**:

```bash
source venv/bin/activate
```

2. **Run the assistant**:

```bash
python main.py
```

3. **Interact with Miku**:

```
🧑‍💻 You: Hello Miku!
🤖 AI: Hi there! ^_^ Miku is here to help you study! ★
```

### Adding Study Materials

Simply drop PDF files into the `content/` folder while the assistant is running:

```bash
cp my-textbook.pdf content/
```

The assistant will:

- Detect the new file automatically
- Launch a background process to extract and embed the content
- Notify you when embedding is complete
- Use the content to answer your questions

### Example Interactions

**Asking about embedded content**:

```
🧑‍💻 You: What is quantum mechanics?
🤖 AI: [Retrieves relevant sections from your physics textbook]
```

**Web search**:

```
🧑‍💻 You: Search for latest AI research papers
🤖 AI: [Performs DuckDuckGo search and presents results]
```

**Opening URLs**:

```
🧑‍💻 You: Open https://github.com
🤖 AI: [Checks internet, opens browser]
```

**System commands**:

```
🧑‍💻 You: What's the current date?
🤖 AI: [Runs 'date' command and shows result]
```

## 🧪 Testing

### Test PDF Embedding

```bash
python pdf_worker_runner.py path/to/test.pdf
```

### Test LLM Connection

```bash
python -c "from models.LLM import LLM; llm = LLM().initialize(); print(llm.invoke('Hello'))"
```

### Test Embedding Model

```bash
python -c "from models.embedding import EmbeddingConfig; emb = EmbeddingConfig(); print(len(emb.get_embedding_model().embed_query('test')))"
```

## 🎨 Customization

### Adding Custom Tools

1. Create a new tool in `tools/<category>/your_tool.py`:

```python
from langchain_core.tools import tool

@tool
def your_custom_tool(param: str) -> str:
    """Tool description for the LLM."""
    # Your implementation
    return "result"
```

2. Register it in `core/tools.py`:

```python
from tools.category.your_tool import your_custom_tool
__all__ = [..., your_custom_tool]
```

3. Update `prompt.yaml` to document the new tool

### Changing Miku's Personality

Edit `prompt.yaml` to customize:

- Personality traits
- Response style
- Tool usage instructions
- Safety rules

## 🔧 Troubleshooting

### DiffSinger Import Errors

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/DiffSinger
source ~/.bashrc
```

### ChromaDB Persistence Issues

Delete and recreate the database:

```bash
rm -rf data/
python main.py  # Will recreate automatically
```

### CUDA/GPU Issues

Install CPU-only PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Ollama Connection Failed

Start Ollama server:

```bash
ollama serve
```

## 📝 Dependencies

Core dependencies:

- `langchain` - LLM framework
- `langgraph` - Agent orchestration
- `chromadb` - Vector database
- `coqui-tts` - Text-to-speech
- `ollama` - Local LLM runtime
- `watchdog` - File system monitoring
- `ddgs` - DuckDuckGo search

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- **DiffSinger**: OpenVPI's neural vocoder for singing voice synthesis
- **Coqui TTS**: Open-source text-to-speech engine
- **LangChain**: Framework for LLM applications
- **ChromaDB**: Embedding database

## 📧 Contact
mailto:zekogml11@gmail.com
---

**Made with ❤️ by the zkzk** 🎤✨
