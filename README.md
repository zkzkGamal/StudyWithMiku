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
└── install.sh                # Smart installer script
```

## 📦 Installation

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for TTS)
- Ubuntu/Linux (tested on Ubuntu)

### Quick Install

1. **Clone the repository**:

```bash
git clone <your-repo-url>
cd StudyWithMiku
```

2. **Run the smart installer**:

```bash
chmod +x install.sh
./install.sh
```

The installer will:

- Create a virtual environment
- Install PyTorch with CUDA support
- Install all Python dependencies
- Clone DiffSinger repository
- Download NSF-HiFiGAN vocoder model
- Configure PYTHONPATH
- Run import tests

3. **Configure environment variables**:

```bash
cp .env.example .env
nano .env  # Edit with your settings
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

[Your contact information]

---

**Made with ❤️ by the zkzk** 🎤✨
