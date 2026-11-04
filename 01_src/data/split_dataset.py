
import json
import random
from pathlib import Path


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Original COCO directories
ORIGINAL_DATA = PROJECT_ROOT / "00_original_data"

ANNOTATIONS_DIR = ORIGINAL_DATA / "annotations"

TRAIN_CAPTIONS = ANNOTATIONS_DIR / "captions_train2017.json"
VAL_CAPTIONS = ANNOTATIONS_DIR / "captions_val2017.json"

TRAIN_IMAGES_DIR = ORIGINAL_DATA / "train2017"
VAL_IMAGES_DIR = ORIGINAL_DATA / "val2017"

# Output directory for split information
SPLITS_DIR = PROJECT_ROOT / "02_processed_data" / "splits"


# ============================================================
# 2. SPLIT PARAMETERS
# ============================================================

RANDOM_SEED = 45

TOTAL_TRAIN_POOL = 10_000
TRAINING_SIZE = 9_900
VALIDATION_SIZE = 100
TEST_SIZE = 100


# ============================================================
# 3. HELPER FUNCTION: LOAD IMAGE IDS
# ============================================================

def load_image_ids(annotation_file):
    """
    Read a COCO captions JSON file and return its image IDs.
    """

    with open(annotation_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    image_ids = [image["id"] for image in data["images"]]

    return sorted(image_ids)


# ============================================================
# 4. CHECK INPUT FILES AND DIRECTORIES
# ============================================================

def check_inputs():

    required_paths = [
        TRAIN_CAPTIONS,
        VAL_CAPTIONS,
        TRAIN_IMAGES_DIR,
        VAL_IMAGES_DIR
    ]

    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(
                f"Required file or directory not found: {path}"
            )


# ============================================================
# 5. CREATE THE SPLITS
# ============================================================

def create_splits():

    check_inputs()

    # Load available image IDs
    train_pool_ids = load_image_ids(TRAIN_CAPTIONS)
    test_pool_ids = load_image_ids(VAL_CAPTIONS)

    print("Available training images:", len(train_pool_ids))
    print("Available test-pool images:", len(test_pool_ids))

    # Check that enough images are available
    if len(train_pool_ids) < TOTAL_TRAIN_POOL:
        raise ValueError("Not enough images in train2017.")

    if len(test_pool_ids) < TEST_SIZE:
        raise ValueError("Not enough images in val2017.")

    # Use a fixed seed for reproducibility
    rng = random.Random(RANDOM_SEED)

    # Select 10,000 images from train2017
    selected_train_pool = rng.sample(
        train_pool_ids,
        TOTAL_TRAIN_POOL
    )

    # Shuffle selected images before dividing them
    rng.shuffle(selected_train_pool)

    # Divide into training and validation
    training_ids = selected_train_pool[:TRAINING_SIZE]

    validation_ids = selected_train_pool[
        TRAINING_SIZE:
        TRAINING_SIZE + VALIDATION_SIZE
    ]

    # Select test images from val2017
    test_ids = rng.sample(test_pool_ids, TEST_SIZE)

    # Sort IDs before saving
    training_ids = sorted(training_ids)
    validation_ids = sorted(validation_ids)
    test_ids = sorted(test_ids)

    return training_ids, validation_ids, test_ids


# ============================================================
# 6. SAVE SPLIT INFORMATION
# ============================================================

def save_splits(training_ids, validation_ids, test_ids):

    SPLITS_DIR.mkdir(parents=True, exist_ok=True)

    split_lists = {
        "training_ids.json": training_ids,
        "validation_ids.json": validation_ids,
        "test_ids.json": test_ids
    }

    for filename, ids in split_lists.items():

        output_file = SPLITS_DIR / filename

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(ids, file, indent=4)

        print(f"Saved: {output_file}")

    # Save configuration for reproducibility
    config = {
        "random_seed": RANDOM_SEED,
        "source_training_dataset": "COCO train2017",
        "source_test_dataset": "COCO val2017",
        "total_selected_from_train2017": TOTAL_TRAIN_POOL,
        "training_images": len(training_ids),
        "validation_images": len(validation_ids),
        "test_images": len(test_ids),
        "selection_method": "Random sampling with fixed seed"
    }

    config_file = SPLITS_DIR / "split_config.json"

    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

    print(f"Saved: {config_file}")


# ============================================================
# 7. CHECK SPLIT CONSISTENCY
# ============================================================

def check_splits(training_ids, validation_ids, test_ids):

    training_set = set(training_ids)
    validation_set = set(validation_ids)
    test_set = set(test_ids)

    assert len(training_ids) == TRAINING_SIZE
    assert len(validation_ids) == VALIDATION_SIZE
    assert len(test_ids) == TEST_SIZE

    assert training_set.isdisjoint(validation_set)
    assert training_set.isdisjoint(test_set)
    assert validation_set.isdisjoint(test_set)

    print("\nSplit consistency checks passed.")


# ============================================================
# 8. MAIN EXECUTION
# ============================================================

def main():

    print("Starting dataset splitting...\n")

    training_ids, validation_ids, test_ids = create_splits()

    check_splits(training_ids, validation_ids, test_ids)

    save_splits(training_ids, validation_ids, test_ids)

    print("\nDataset splitting completed successfully!")

    print("\nFinal split sizes:")
    print("Training:", len(training_ids))
    print("Validation:", len(validation_ids))
    print("Test:", len(test_ids))


if __name__ == "__main__":
    main()
