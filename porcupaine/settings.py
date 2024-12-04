from pathlib import Path


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MORPHODITA_MODEL_DIR = BASE_DIR / "czech-morfflex2.0-pdtc1.0-220710"
MODELS_DIR = DATA_DIR / "models"
CZECH_STOPWORDS = DATA_DIR / "czech_stopwords.txt"
