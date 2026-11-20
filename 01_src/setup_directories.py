"""Create directories required by the pipeline and future source modules."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RUNTIME_DIRECTORIES = (
    "02_processed_data/embedding_experiments",
    "02_processed_data/knowledge_base/documents",
    "02_processed_data/knowledge_base/indexes/clip_image_index",
    "02_processed_data/knowledge_base/indexes/sbert_caption_index",
    "02_processed_data/knowledge_base/manifest",
    "02_processed_data/knowledge_base/metadata",
    "02_processed_data/splits",
    "03_analysis/01_statistical_exploration/outputs/figures",
    "03_analysis/01_statistical_exploration/outputs/statistics",
    "03_analysis/01_statistical_exploration/outputs/tables",
)

for split in ("training", "validation", "test"):
    for subdirectory in ("annotations", "captions", "embeddings", "images", "metadata"):
        RUNTIME_DIRECTORIES += (f"02_processed_data/{split}/{subdirectory}",)


def main() -> None:
    """Create missing runtime directories without changing existing files."""

    for relative_path in RUNTIME_DIRECTORIES:
        (PROJECT_ROOT / relative_path).mkdir(parents=True, exist_ok=True)
    print(f"Ensured {len(RUNTIME_DIRECTORIES)} pipeline directories exist.")


if __name__ == "__main__":
    main()
