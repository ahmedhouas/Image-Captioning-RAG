# Training images

This directory contains the generated training-image subset used by the
pipeline and knowledge base. The images are copied from
`00_original_data/train2017/` during extraction and are intentionally ignored
by Git because they are reproducible and large.

Run `python 01_src/setup_directories.py` followed by the extraction stage to
create or repopulate this directory.
