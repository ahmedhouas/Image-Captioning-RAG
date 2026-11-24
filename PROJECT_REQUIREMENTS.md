# Project Requirements

## 1. Purpose and scope

This project prepares a reproducible MS COCO 2017 dataset and retrieval
knowledge base for image-captioning research. The current implementation
covers dataset inspection, preprocessing, embedding generation, index
construction, and release quality checks. Caption generation, RAG method
comparisons, and final evaluation are future work, not current capabilities.

## 2. Users and operating context

- Researchers can configure and run the dataset pipeline.
- Experimenters can use the generated training knowledge base with held-out
  validation and test splits.
- The project runs on Windows 11 with Python 3.11 or 3.12. CPU execution is
  supported; a compatible CUDA setup is optional.
- The COCO dataset and model weights are external inputs. The project does not
  download the COCO dataset automatically. Model weights may be downloaded
  from Hugging Face when first used.

## 3. Functional requirements

| ID | Requirement |
|---|---|
| FR-01 | Read split sizes, random seed, model names, and embedding settings from `01_src/config/pipeline_config.py`. |
| FR-02 | Create reproducible training, validation, and test splits from COCO 2017 sources and record the split configuration. |
| FR-03 | Extract image, caption, and instance-annotation data for the configured splits. |
| FR-04 | Validate required inputs, extracted records, image readability, and split integrity; report failures rather than silently accepting invalid data. |
| FR-05 | Apply EXIF-aware RGB image handling and conservative caption whitespace normalization while retaining source captions. |
| FR-06 | Generate normalized CLIP image embeddings and Sentence-Transformer caption embeddings, preserving row-to-record mappings and metadata. |
| FR-07 | Build separate FAISS inner-product indexes for the CLIP and Sentence-Transformer embedding spaces; do not compare vectors across these spaces. |
| FR-08 | Keep test images and reference captions out of the retrieval knowledge base, and run quality and retrieval-compatibility checks on generated artifacts. |
| FR-09 | Provide a single pipeline entry point and a `--skip-notebooks` option for split, extraction, and validation stages. |
| FR-10 | Keep original data and large generated artifacts out of version control. |

## 4. Data and configuration requirements

Place the COCO 2017 images and annotations under `00_original_data/`:

```text
00_original_data/
├── train2017/
├── val2017/
└── annotations/
    ├── captions_train2017.json
    ├── captions_val2017.json
    ├── instances_train2017.json
    └── instances_val2017.json
```

The current configured release uses seed `45`, 9,900 training images, 100
validation images, and 100 test images. Training and validation are selected
from `train2017`; test is selected from `val2017`. Keep validation and test
references out of their corresponding retrieval evidence.

The configured encoders are `openai/clip-vit-base-patch32` (512 dimensions)
and `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions). Embeddings are
float32 and L2-normalized. These encoders define distinct vector spaces.

## 5. Quality attributes and constraints

- **Reproducibility:** use the centralized pipeline configuration and retain
  split snapshots, model metadata, and vector-row mappings.
- **Data integrity:** fail validation when required files, relationships,
  vectors, or index metadata are invalid.
- **Leakage prevention:** only training data may populate the current
  knowledge base; validation and test references remain held out.
- **Resource use:** COCO images, generated embeddings, indexes, and model
  weights require substantial disk space and may require extended CPU runtime.
  Keep adequate free disk space before generating a release.
- **Portability:** use paths relative to the repository and a project-local
  Python virtual environment; do not rely on machine-specific absolute paths.
- **Version control:** commit source, notebooks, configuration, and
  documentation, not the original dataset or large generated data.

## 6. Acceptance criteria

A release is ready for formal validation when:

1. The required COCO image and annotation files are present.
2. The configured split counts and split snapshot are generated and validated.
3. Processed images and captions pass the dataset and preprocessing checks.
4. Embeddings have expected dimensions, finite values, L2 normalization, and
   correct row mappings.
5. Separate FAISS indexes and matching documents/metadata are present and pass
   quality-control checks.
6. Leakage checks confirm validation and test references are not in the
   training knowledge base.
7. Retrieval compatibility succeeds for a held-out query.
8. The formal preprocessing validation and release-freezing work is completed
   and recorded before downstream RAG evaluation.

## 7. Current status and gaps

The repository reports dataset preparation, embeddings, knowledge-base
construction, quality checks, and a retrieval compatibility smoke test as
completed. Formal validation and release freezing remain pending. A
caption-generation model, assigned RAG technique, baselines, and final caption
and retrieval evaluation are not implemented yet.

## 8. Environment

Supported project dependencies and Windows setup instructions are maintained
in [`requirements.txt`](requirements.txt) and the README's Development
Environment section. The statistical-exploration notebook also requires the
spaCy English model `en_core_web_sm`, installed separately as described there.
