
import json
import shutil
from collections import Counter
from pathlib import Path


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORIGINAL_DATA = PROJECT_ROOT / "00_original_data"
ORIGINAL_ANNOTATIONS = ORIGINAL_DATA / "annotations"

PROCESSED_DATA = PROJECT_ROOT / "02_processed_data"
SPLITS_DIR = PROCESSED_DATA / "splits"


# ============================================================
# 2. LOAD SAVED IMAGE IDS
# ============================================================

def load_split_ids(filename):
    """
    Load image IDs from one of the split JSON files.
    """

    file_path = SPLITS_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Split file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        image_ids = json.load(file)

    if len(image_ids) != len(set(image_ids)):
        raise ValueError(
            f"Duplicate image IDs found in {filename}"
        )

    return image_ids


# ============================================================
# 3. LOAD ORIGINAL COCO ANNOTATIONS
# ============================================================

def load_json(file_path):
    """
    Load a JSON file.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Annotation file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================
# 4. FILTER COCO ANNOTATIONS
# ============================================================

def filter_annotations(data, selected_ids):
    """
    Keep only the image records and annotations
    belonging to the selected image IDs.

    Other metadata, such as categories, licenses and info,
    is preserved.
    """

    selected_set = set(selected_ids)

    # Keep the selected image records
    filtered_images = [
        image
        for image in data["images"]
        if image["id"] in selected_set
    ]

    # Keep annotations belonging to selected images
    filtered_annotations = [
        annotation
        for annotation in data["annotations"]
        if annotation["image_id"] in selected_set
    ]

    # Copy the original structure and replace the two lists
    filtered_data = data.copy()

    filtered_data["images"] = filtered_images
    filtered_data["annotations"] = filtered_annotations

    # Verify that every selected image was found
    found_ids = {image["id"] for image in filtered_images}

    missing_ids = selected_set - found_ids

    if missing_ids:
        raise ValueError(
            f"{len(missing_ids)} selected image IDs "
            f"were not found in the annotation file."
        )

    return filtered_data
def filter_caption_annotations(data, selected_ids):
    """
    Keep selected images and exactly five captions per image.

    If an image has more than five captions, retain the five
    captions with the lowest annotation IDs.

    If an image has fewer than five captions, raise an error.
    """

    selected_set = set(selected_ids)

    # Filter image records
    filtered_images = [
        image
        for image in data["images"]
        if image["id"] in selected_set
    ]

    found_ids = {image["id"] for image in filtered_images}

    missing_ids = selected_set - found_ids

    if missing_ids:
        raise ValueError(
            f"{len(missing_ids)} selected images "
            "were not found in the captions file."
        )

    # Group captions by image ID
    captions_by_image = {}

    for annotation in data["annotations"]:
        image_id = annotation["image_id"]

        if image_id in selected_set:
            captions_by_image.setdefault(image_id, []).append(
                annotation
            )

    retained_annotations = []
    discarded_annotations = []

    # Select exactly five captions per image
    for image_id in sorted(selected_set):

        captions = captions_by_image.get(image_id, [])

        # Deterministic ordering
        captions = sorted(
            captions,
            key=lambda item: item["id"]
        )

        if len(captions) < 5:
            raise ValueError(
                f"Image {image_id} has only {len(captions)} "
                "captions. Cannot retain exactly five."
            )

        retained_annotations.extend(captions[:5])
        discarded_annotations.extend(captions[5:])

    # Preserve the original COCO structure
    filtered_data = data.copy()
    filtered_data["images"] = filtered_images
    filtered_data["annotations"] = retained_annotations

    return filtered_data, discarded_annotations


# ============================================================
# 5. SAVE EXTRACTED ANNOTATIONS
# ============================================================

def save_json(data, output_path):
    """
    Save a dictionary as a formatted JSON file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# ============================================================
# 6. COPY SELECTED IMAGES
# ============================================================

def copy_selected_images(image_records, source_dir, destination_dir):
    """
    Copy the selected original images into the processed dataset.
    """

    destination_dir.mkdir(parents=True, exist_ok=True)

    # Check all source images before starting the copy
    missing_files = []

    for image in image_records:
        source_file = source_dir / image["file_name"]

        if not source_file.is_file():
            missing_files.append(source_file)

    if missing_files:
        raise FileNotFoundError(
            f"{len(missing_files)} image files are missing. "
            f"First missing file: {missing_files[0]}"
        )

    # Copy images
    for image in image_records:

        source_file = source_dir / image["file_name"]
        destination_file = destination_dir / image["file_name"]

        shutil.copy2(source_file, destination_file)

    print(f"Copied {len(image_records)} images to {destination_dir}")


# ============================================================
# 7. PROCESS ONE DATASET SPLIT
# ============================================================

def process_split(
    split_name,
    selected_ids,
    captions_file,
    instances_file,
    source_images_dir
):
    """
    Extract annotations and copy images for one split.
    """

    print(f"\nProcessing {split_name}...")

    # Load original COCO JSON files
    captions_data = load_json(captions_file)
    instances_data = load_json(instances_file)

    # Check that selected IDs exist in both files
    captions_ids = {
        image["id"] for image in captions_data["images"]
    }

    instances_ids = {
        image["id"] for image in instances_data["images"]
    }

    selected_set = set(selected_ids)

    if not selected_set.issubset(captions_ids):
        raise ValueError(
            f"Some {split_name} IDs are missing from captions."
        )

    if not selected_set.issubset(instances_ids):
        raise ValueError(
            f"Some {split_name} IDs are missing from instances."
        )

    # Extract the selected records
    filtered_captions, discarded_captions = (
        filter_caption_annotations(
            captions_data,
            selected_ids
        )
    )

    filtered_instances = filter_annotations(
        instances_data,
        selected_ids
    )

    # Check that both annotation files describe the same images
    captions_image_ids = {
        image["id"] for image in filtered_captions["images"]
    }

    instances_image_ids = {
        image["id"] for image in filtered_instances["images"]
    }

    if captions_image_ids != instances_image_ids:
        raise ValueError(
            f"Image ID mismatch in {split_name} annotations."
        )

    # Create output directories
    split_dir = PROCESSED_DATA / split_name

    images_output_dir = split_dir / "images"
    annotations_output_dir = split_dir / "annotations"

    annotations_output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save filtered JSON files
    save_json(
        filtered_captions,
        annotations_output_dir / "captions.json"
    )

    save_json(
        filtered_instances,
        annotations_output_dir / "instances.json"
    )
    save_json(
    {
        "split": split_name,
        "selection_rule": "Five captions with the lowest annotation IDs",
        "discarded_caption_count": len(discarded_captions),
        "discarded_annotations": discarded_captions
    },
    annotations_output_dir / "discarded_captions.json"
    )   

    # Copy the selected image files
    copy_selected_images(
        filtered_captions["images"],
        source_images_dir,
        images_output_dir
    )

    # Count captions per image
    caption_counts = Counter(
        annotation["image_id"]
        for annotation in filtered_captions["annotations"]
    )

    unusual_caption_counts = {
        image_id: caption_counts[image_id]
        for image_id in selected_ids
        if caption_counts[image_id] != 5
    }

    # Display summary
    print(f"{split_name} summary:")
    print(f"  Images: {len(filtered_captions['images'])}")
    print(f"  Captions: {len(filtered_captions['annotations'])}")
    print(f"  Object annotations: {len(filtered_instances['annotations'])}")

    if unusual_caption_counts:
        print(
            "  WARNING: Images without exactly 5 captions:",
            len(unusual_caption_counts)
        )
    else:
        print("  Caption count check: 5 captions per image")


# ============================================================
# 8. MAIN EXECUTION
# ============================================================

def main():

    print("Starting annotation extraction...\n")

    # Load the three previously generated ID lists
    training_ids = load_split_ids("training_ids.json")
    validation_ids = load_split_ids("validation_ids.json")
    test_ids = load_split_ids("test_ids.json")

    # Training: COCO train2017
    process_split(
        split_name="training",
        selected_ids=training_ids,
        captions_file=ORIGINAL_ANNOTATIONS / "captions_train2017.json",
        instances_file=ORIGINAL_ANNOTATIONS / "instances_train2017.json",
        source_images_dir=ORIGINAL_DATA / "train2017"
    )

    # Validation: COCO train2017
    process_split(
        split_name="validation",
        selected_ids=validation_ids,
        captions_file=ORIGINAL_ANNOTATIONS / "captions_train2017.json",
        instances_file=ORIGINAL_ANNOTATIONS / "instances_train2017.json",
        source_images_dir=ORIGINAL_DATA / "train2017"
    )

    # Test: COCO val2017
    process_split(
        split_name="test",
        selected_ids=test_ids,
        captions_file=ORIGINAL_ANNOTATIONS / "captions_val2017.json",
        instances_file=ORIGINAL_ANNOTATIONS / "instances_val2017.json",
        source_images_dir=ORIGINAL_DATA / "val2017"
    )

    print("\nAnnotation extraction completed successfully!")


if __name__ == "__main__":
    main()
