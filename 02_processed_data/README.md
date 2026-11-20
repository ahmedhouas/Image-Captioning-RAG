# Processed data

This directory contains the reproducible dataset release and derived
knowledge-base artifacts produced by the pipeline.

Versioned JSON, metadata, reports, indexes, and embedding samples document
the current release. Split `images/` directories are generated runtime
inputs and are ignored by Git because they can be recreated from
`00_original_data/`. Run `python 01_src/setup_directories.py` to create the
expected directory layout before running individual stages.
