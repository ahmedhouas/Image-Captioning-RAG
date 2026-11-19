# Phase 1 – Dataset, Knowledge Base and Retrieval Pipeline Validation Report

## 1. Introduction

This report presents the validation results obtained at the end of Phase 1 of the Image Captioning RAG project.

The objective of this phase was to prepare and validate the MS-COCO dataset subset, construct the knowledge base, generate image and caption embeddings, establish the vector indexes, and verify that the retrieval pipeline operates correctly.

The validation covers:

- Dataset integrity and preprocessing.
- Knowledge base structure and consistency.
- Image and caption embedding integrity.
- Data leakage prevention.
- FAISS vector index integrity.
- Retrieval pipeline compatibility.

It also identifies the evaluations that have not yet been performed and should be addressed in subsequent work.

---

## 2. Dataset Validation

### 2.1 Dataset composition

The prepared dataset contains 10,100 images distributed across three subsets.

| Dataset split | Number of images | Number of captions |
|---|---:|---:|
| Knowledge Base (Training) | 9,900 | 49,500 |
| Validation | 100 | Not used as KB captions |
| External Test | 100 | 500 |
| **Total** | **10,100** | **50,000** |

Each knowledge-base image is associated with exactly five captions.

The external test set contains 100 images with five reference captions per image.

### 2.2 Preprocessing validation

The preprocessing validation report confirms that all expected images were processed successfully.

| Validation check | Expected | Actual | Result |
|---|---:|---:|---|
| Training images processed | 9,900 | 9,900 | PASS |
| Validation images processed | 100 | 100 | PASS |
| Test images processed | 100 | 100 | PASS |
| Processing failures | 0 | 0 | PASS |

The preprocessing validation was performed using random seed `45`.

### 2.3 Dataset integrity checks

The dataset validation script (`validate_dataset.py`) implements the following checks:

- Expected dataset split sizes.
- Uniqueness of image IDs.
- Separation between training, validation, and test image IDs.
- Existence of referenced image files.
- Detection of unexpected image files.
- Exactly five captions per image.
- Consistency between caption references and image IDs.
- Consistency between object annotation image IDs and split image IDs.
- Validity of category references.
- SHA-256-based detection of exact duplicate images across splits.

**Validation status:** The preprocessing validation report records successful processing of all 10,100 images with zero failures. The validation script implements the additional structural and integrity checks.

**Note:** A separate numerical duplicate-image count or duplicate rate was not identified in the reviewed quality-control results. Therefore, no specific duplicate rate is reported here.

---

## 3. Knowledge Base Quality Control

The knowledge base quality-control report was generated on:

`2026-11-06T00:51:15 UTC`

Report version: `1.0`

Overall quality-control status: **PASSED**

### 3.1 Knowledge base composition

| Component | Expected | Actual | Result |
|---|---:|---:|---|
| Image documents | 9,900 | 9,900 | PASS |
| Caption documents | 49,500 | 49,500 | PASS |
| Caption references | 49,500 | 49,500 | PASS |
| Unique caption references | 49,500 | 49,500 | PASS |
| Unreferenced captions | 0 | 0 | PASS |
| Duplicate caption references | 0 | 0 | PASS |

### 3.2 Document and mapping consistency

The following relationships were validated:

- Image documents are correctly represented in the knowledge base.
- Caption documents are correctly associated with their corresponding images.
- Caption references are unique.
- All expected captions are referenced.
- No unreferenced or duplicate caption references were detected.
- Embedding-to-document mappings are consistent.
- Image-caption relationships are preserved.

**Result: PASSED**

These checks establish the structural consistency of the knowledge base and its associated metadata.

---

## 4. Embedding Validation

Two embedding models were used to represent the visual and textual content of the knowledge base.

### 4.1 Image embeddings – CLIP

**Model:** `openai/clip-vit-base-patch32`

| Property | Result |
|---|---|
| Number of image vectors | 9,900 |
| Embedding dimension | 512 |
| Data type | float32 |
| NaN values | 0 |
| Infinite values | 0 |
| Zero vectors | 0 |
| L2 normalization | Applied |
| Validation status | PASS |

The generated image embeddings have the expected dimensions and numerical properties.

All vectors were L2-normalized, making them suitable for similarity search using inner-product scoring.

### 4.2 Caption embeddings – Sentence-BERT

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

| Property | Result |
|---|---|
| Number of caption vectors | 49,500 |
| Embedding dimension | 384 |
| Data type | float32 |
| NaN values | 0 |
| Infinite values | 0 |
| Zero vectors | 0 |
| L2 normalization | Applied |
| Validation status | PASS |

The caption embeddings satisfy the expected structural and numerical requirements.

The embedding-generation implementation also checks expected output dimensions, finite values, row mappings, and identifier consistency.

### 4.3 Embedding validation conclusion

Both embedding collections passed their reported technical integrity checks.

This confirms that:

- The expected number of vectors was generated.
- The embedding dimensions match the selected models.
- No invalid numerical values were detected.
- The vectors are normalized.
- The embedding collections can be associated with their corresponding knowledge-base documents.

**Important distinction:** These checks validate the technical integrity of the embeddings. They do not establish that the embeddings capture semantic similarity accurately. Semantic embedding evaluation remains a separate task.

---

## 5. Data Leakage Validation

Preventing data leakage is essential to ensure that the retrieval and evaluation stages produce meaningful results.

The quality-control report records the following results:

| Leakage check | Detected overlap | Result |
|---|---:|---|
| Training–Validation overlap | 0 | PASS |
| Training–Test overlap | 0 | PASS |
| Validation–Test overlap | 0 | PASS |
| Validation images present in KB | 0 | PASS |
| Test images present in KB | 0 | PASS |
| Non-training images present in KB | 0 | PASS |

### 5.1 Interpretation

The results confirm that:

- The training knowledge base contains only training images.
- Validation images are excluded from the knowledge base.
- Test images are excluded from the knowledge base.
- The three image splits are separated according to the reported image-ID checks.

This is particularly important for the next phase, where validation images will be used as queries against the knowledge base.

### 5.2 Limitation

The reported checks establish image-level split separation. They should not be interpreted as proof that every possible form of leakage in all future evaluation workflows has been eliminated.

The retrieval and evaluation procedures must continue to enforce the exclusion of query-associated information.

**Result: PASSED**

---

## 6. FAISS Vector Index Validation

Two FAISS indexes were constructed to support image and caption retrieval.

Both indexes use:

`IndexFlatIP`

This is an exact inner-product search index.

### 6.1 Image index

| Property | Result |
|---|---|
| Index type | IndexFlatIP |
| Number of vectors | 9,900 |
| Vector dimension | 512 |
| Original vectors match index | Yes |
| Validation status | PASS |

### 6.2 Caption index

| Property | Result |
|---|---|
| Index type | IndexFlatIP |
| Number of vectors | 49,500 |
| Vector dimension | 384 |
| Original vectors match index | Yes |
| Validation status | PASS |

### 6.3 Index integrity checks

The quality-control process verified:

- Index vector counts.
- Vector dimensions.
- Consistency between original embeddings and indexed vectors.
- Index metadata.
- Manifest information.
- Artifact inventory and file sizes.

Both indexes passed the reported integrity checks.

### 6.4 Similarity interpretation

Because the embeddings are L2-normalized, inner-product similarity is equivalent to cosine similarity.

Using `IndexFlatIP` also means that the current indexes perform exact search rather than approximate nearest-neighbour search.

Consequently, ANN Recall@k is not applicable as a performance measure for the current index implementation. If approximate indexes such as IVF or HNSW are introduced later, their results can be compared against the current exact index.

---

## 7. Retrieval Pipeline Smoke Test

A retrieval smoke test was executed in:

`05_retrieval_pipeline_validation.ipynb`

The purpose was to verify that the complete retrieval path operates correctly, from query-image encoding to the retrieval of associated captions.

### 7.1 Test configuration

| Parameter | Value |
|---|---|
| Query image ID | 250 |
| Query split | Validation |
| Query image present in KB | No |
| Image encoder | CLIP ViT-B/32 |
| Embedding dimension | 512 |
| Data type | float32 |
| Normalization | L2 |
| FAISS index | IndexFlatIP |
| Knowledge-base image vectors | 9,900 |

### 7.2 Retrieval results

The query image was encoded and used to retrieve the three most similar images from the knowledge base.

| Rank | Retrieved image ID | Similarity score |
|---:|---:|---:|
| 1 | 11,605 | 0.8479 |
| 2 | 401,670 | 0.8389 |
| 3 | 486,769 | 0.8303 |

The system also retrieved the captions associated with the returned images.

A total of 15 captions were verified, corresponding to five captions for each of the three retrieved images.

### 7.3 Smoke test validation

The following operations were successfully verified:

- Query image encoding.
- CLIP embedding generation.
- FAISS similarity search.
- Retrieval of the top-ranked image documents.
- Image-document mapping.
- Caption-document mapping.
- Retrieval of five associated captions per image.
- Validation/training split separation.

**Result: PASSED**

### 7.4 Interpretation and limitation

The smoke test demonstrates that the retrieval pipeline is technically functional and that the different components are compatible.

However, it is important to distinguish a successful smoke test from a retrieval-quality evaluation.

The test used one validation query. It does not establish that the system consistently retrieves semantically relevant images or captions across a representative set of queries.

The similarity scores indicate the ranking produced by the embedding model; they are not, by themselves, measurements of retrieval accuracy.

---

## 8. Validation Summary

The following table summarizes the validation activities and their outcomes.

| Validation area | Checks performed | Status |
|---|---|---|
| Dataset preprocessing | Image processing counts and failures | PASSED |
| Dataset structure | Split sizes, IDs, references and annotations | Implemented in validation script |
| Knowledge base integrity | Document counts and mapping consistency | PASSED |
| Image embeddings | Dimensions and numerical integrity | PASSED |
| Caption embeddings | Dimensions and numerical integrity | PASSED |
| Data leakage | Image-level split separation | PASSED |
| FAISS image index | Vector count, dimension and consistency | PASSED |
| FAISS caption index | Vector count, dimension and consistency | PASSED |
| Retrieval pipeline | End-to-end compatibility smoke test | PASSED |
| Semantic embedding quality | Semantic benchmark against reference judgments | NOT YET EVALUATED |
| Semantic retrieval quality | Precision@k, Recall@k, MRR and nDCG@k | NOT YET EVALUATED |
| Retrieval performance | Latency and performance benchmarking | NOT YET EVALUATED |
| Formal release freezing | Final release validation and freezing | PENDING |

---

## 9. Evaluations Not Yet Performed

Although the technical validation results are positive, several important evaluation activities remain outstanding.

### 9.1 Semantic embedding evaluation

The current validation confirms that the embeddings were generated correctly, but does not measure their semantic quality.

Recommended evaluations include:

**For Sentence-BERT:**

- Triplet accuracy.
- Spearman correlation with human similarity judgments.
- Pearson correlation with human similarity judgments.

**For CLIP:**

- Image-to-text retrieval evaluation.
- Text-to-image retrieval evaluation.
- Image-text alignment assessment.

These evaluations would provide evidence of how effectively the embedding models represent semantic relationships.

### 9.2 Semantic retrieval evaluation

A representative set of validation queries should be used to evaluate retrieval quality.

The evaluation should rely on human judgments or a clearly defined relevance-assessment protocol.

Recommended metrics:

| Metric | Purpose |
|---|---|
| Precision@k | Measures the proportion of retrieved items considered relevant among the top k results |
| Recall@k | Measures how many relevant items are retrieved among the top k results |
| MRR | Measures how highly the first relevant result is ranked |
| nDCG@k | Measures ranking quality while accounting for graded relevance |

The evaluation should cover more than one query and should preserve the validation/knowledge-base separation.

### 9.3 Retrieval performance evaluation

The current report validates index integrity and retrieval functionality, but does not provide a comprehensive performance benchmark.

Recommended measurements:

- Average retrieval latency.
- Median retrieval latency.
- P95 and P99 retrieval latency.
- Index construction time.
- Index storage size.
- Memory consumption, where practical.

These measurements will help characterize the efficiency of the retrieval system.

### 9.4 Formal release validation

The README indicates that formal validation and final release freezing remain pending.

Before declaring the knowledge base formally frozen, the project should verify:

- Final dataset and configuration versions.
- Consistency of all generated artifacts.
- Reproducibility of the preprocessing and embedding pipeline.
- Integrity of the final indexes and metadata.
- Checksums or other artifact-integrity records.
- Documentation of the final validated configuration.

The successful quality-control report should therefore be distinguished from the formal release-freezing process.

---

## 10. Recommended Next Steps

The following work is recommended after the completion of the current Phase 1 technical validation.

| Priority | Task | Expected outcome |
|---|---|---|
| 1 | Perform semantic embedding evaluation | Evidence of embedding quality |
| 2 | Build a representative validation query set | Consistent retrieval evaluation dataset |
| 3 | Establish relevance judgments | Ground truth for retrieval evaluation |
| 4 | Calculate Precision@k, Recall@k, MRR and nDCG@k | Quantitative retrieval-quality results |
| 5 | Benchmark retrieval latency and resource consumption | Performance characterization |
| 6 | Perform final artifact and configuration checks | Reproducible release candidate |
| 7 | Freeze and document the validated knowledge base | Formal Phase 1 release |

### Suggested notebook organization

The existing validation notebooks can be complemented with:

- `06_semantic_embedding_retrieval_evaluation.ipynb`
- `07_validation_and_freezing.ipynb`

The existing notebook `04_knowledge_base_quality_control.ipynb` should remain focused on structural and technical quality control.

The new evaluation notebook should focus on semantic embedding quality and retrieval effectiveness.

---

## 11. Final Assessment

Based on the reviewed repository artifacts and validation results, Phase 1 has successfully established the technical foundations required for the next stages of the Image Captioning RAG project.

The dataset was processed successfully, the knowledge base was constructed with the expected document counts, both embedding collections passed their numerical integrity checks, and the FAISS indexes passed their reported consistency checks.

The image-level leakage checks also reported no overlap between the training, validation, and test splits. Furthermore, the retrieval smoke test successfully demonstrated compatibility between image encoding, vector search, document mapping, and caption retrieval.

Nevertheless, the current results should be interpreted within their scope.

**Phase 1 technical implementation and structural quality control: successful.**

**Semantic embedding evaluation, comprehensive retrieval-quality evaluation, performance benchmarking, and formal release freezing: still outstanding.**

Therefore, the project has reached a technically validated state suitable for proceeding with the next stage of development, while the remaining evaluation and release activities should be completed and documented as part of the project's continued validation process.