python3 -m venv venv
source venv/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
git clone https://github.com/openvpi/DiffSinger.git
cd DiffSinger
pip install -r requirements.txt
pip install -e .
