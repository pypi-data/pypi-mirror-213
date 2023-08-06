import requests
from pathlib import Path

MODEL_DIR = Path(__file__).parent / "models"
LASER_2_URL = "https://tinyurl.com/nllblaser2"
SPM_NAME = "laser2.spm"
S3 = "https://dl.fbaipublicfiles.com/nllb/laser"  # available encoders


def download(file):
    print(f" - Downloading {file}")
    if file == "laser2.pt":
        response = requests.get(LASER_2_URL)
    else:
        response = requests.get(f"{S3}/{file}")
    file_path = MODEL_DIR / file
    with file_path.open(mode="wb") as f:
        f.write(response.content)


def load_or_download_file(file) -> Path:
    """Download file if not present in MODEL_DIR and return path to file"""
    if not MODEL_DIR.is_dir():
        MODEL_DIR.mkdir(parents=True)
    file_path = MODEL_DIR / file
    if not file_path.exists():
        download(file)
    return file_path
