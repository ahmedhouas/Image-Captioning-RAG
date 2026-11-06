from pathlib import Path

# ============================================================
# 1. PROJECT DIRECTORIES
# ============================================================

# This file is located in 01_src/config/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORIGINAL_DATA = PROJECT_ROOT / "00_original_data"
ORIGINAL_ANNOTATIONS = ORIGINAL_DATA / "annotations"

PROCESSED_DATA = PROJECT_ROOT / "02_processed_data"
SPLITS_DIR = PROCESSED_DATA / "splits"


# ============================================================
# 2. DATASET SOURCES
# ============================================================

TRAIN_SOURCE = "train2017"
TEST_SOURCE = "val2017"

TRAIN_IMAGES_DIR = ORIGINAL_DATA / TRAIN_SOURCE
TEST_IMAGES_DIR = ORIGINAL_DATA / TEST_SOURCE

TRAIN_CAPTIONS_FILE = (
    ORIGINAL_ANNOTATIONS / "captions_train2017.json"
)
TEST_CAPTIONS_FILE = (
    ORIGINAL_ANNOTATIONS / "captions_val2017.json"
)

TRAIN_INSTANCES_FILE = (
    ORIGINAL_ANNOTATIONS / "instances_train2017.json"
)
TEST_INSTANCES_FILE = (
    ORIGINAL_ANNOTATIONS / "instances_val2017.json"
)


# ============================================================
# 3. SPLIT CONFIGURATION
# ============================================================

RANDOM_SEED = 45

TRAINING_SIZE = 9900
VALIDATION_SIZE = 100
TEST_SIZE = 100

# Automatically calculated: training + validation
TOTAL_TRAIN_POOL = TRAINING_SIZE + VALIDATION_SIZE

# Number of captions retained per image
CAPTIONS_PER_IMAGE = 5


# ============================================================
# 4. EMBEDDING CONFIGURATION
# ============================================================

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

SBERT_MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

CLIP_BATCH_SIZE = 32
SBERT_BATCH_SIZE = 64

EMBEDDING_DTYPE = "float32"
NORMALIZE_EMBEDDINGS = True


# ============================================================
# 5. RETRIEVAL CONFIGURATION
# ============================================================

RETRIEVAL_TOP_K = 3