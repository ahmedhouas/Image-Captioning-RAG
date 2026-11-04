# Image Captioning RAG: A Comparative Study of RAG Techniques

## 1. Project Overview

This project investigates the application of Retrieval-Augmented Generation (RAG) techniques to image captioning.

The main objective is to compare different RAG approaches for generating accurate, relevant, and visually grounded descriptions of images. Particular attention is given to reducing hallucinations, omissions, imprecise attributes, and incorrect relationships in generated captions.

The project uses a subset of the **MS COCO dataset** and follows a shared data preparation and evaluation methodology.

## 2. Project Objectives

The main objectives are to:

- Explore and analyse the MS COCO dataset.
- Prepare and validate reproducible training, validation, and test datasets.
- Extract relevant visual and textual information.
- Generate image and text embeddings.
- Construct a knowledge base for retrieval.
- Implement and compare assigned RAG techniques.
- Evaluate caption quality, retrieval performance, and hallucination rates.
- Document experimental results and findings.

## 3. Repository Structure

```text
Image-Captioning-RAG/
│
├── 00_original_data/
│
├── 01_src/
│   ├── data/
│   │   ├── split_dataset.py
│   │   ├── extract_annotations.py
│   │   └── validate_dataset.py
│   │
│   └── notebooks/
│
├── 02_processed_data/
│
├── 03_analysis/
│   └── 01_statistical_exploration/
│       ├── outputs/
│       │   ├── tables/
│       │   ├── figures/
│       │   └── statistics/
│       ├── report/
│       └── README.md
│
├── .gitignore
└── README.md
```

### Directory descriptions

| Directory | Description |
|---|---|
| `00_original_data/` | Original MS COCO images and annotations. |
| `01_src/` | Source code and Jupyter notebooks used throughout the project. |
| `02_processed_data/` | Selected datasets, filtered annotations, and split definitions. |
| `03_analysis/` | Statistical analyses, generated results, and analytical documentation. |

Original and processed datasets are stored locally and excluded from Git version control.

## 4. Dataset Organisation

The project uses three separate data splits:

- **Training / Knowledge Base:** 9,900 images selected from COCO train2017.
- **Validation:** 100 images selected from COCO train2017 and kept separate from the training knowledge base.
- **Test:** 100 images selected from COCO val2017.

The split definitions are stored in `02_processed_data/splits/`.

A fixed random seed of `45` is used for reproducibility.

Each processed image is associated with five reference captions. The original COCO dataset remains unchanged.

## 5. Development Workflow

The project is organised into successive stages:

1. **Dataset setup:** Organise the original dataset and project environment.
2. **Dataset splitting and extraction:** Select the required images and annotations.
3. **Dataset validation:** Verify split integrity, image availability, annotation consistency, and leakage constraints.
4. **Statistical exploration:** Analyse object classes, scene complexity, caption characteristics, and dataset diversity.
5. **Preprocessing:** Prepare the data for subsequent embedding and retrieval operations.
6. **Embedding generation:** Generate visual and textual representations.
7. **Knowledge-base construction:** Build the retrieval index using the training data.
8. **RAG implementation:** Implement the assigned retrieval and generation technique.
9. **Evaluation:** Compare generated captions and retrieval performance using the defined metrics.

## 6. Data Integrity and Reproducibility

The project follows these principles:

- Original dataset files must not be modified.
- Training, validation, and test splits must remain separate.
- Validation and test reference captions must not be used as retrieval evidence.
- Test references must only be used for final evaluation.
- Data-processing scripts and analysis notebooks should be reproducible.
- Generated results and experimental configurations should be documented.

## 7. Technologies

The project may use the following tools and libraries, depending on the selected implementation:

- Python
- Jupyter Notebook
- NumPy and Pandas
- Matplotlib and Seaborn
- Pillow
- NLTK or spaCy
- PyTorch
- CLIP or other visual encoders
- FAISS, ChromaDB, or LanceDB

## 8. Version Control

Git and GitHub are used to manage source code, notebooks, documentation, and analysis outputs.

The original and processed datasets are excluded from version control through `.gitignore`.

