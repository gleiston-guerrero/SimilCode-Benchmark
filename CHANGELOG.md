# Changelog

All notable changes to the **SimilCode Benchmark** dataset are documented in
this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-07-08

Initial public, DOI-minted release of the **SimilCode Benchmark** dataset,
accompanying the manuscript submitted to the *International Journal for
Educational Integrity* (Springer Nature).

### Added
- **Ground-truth dataset** (`metadata.csv`) — 120 test-case pairs (60 C# + 60
  Java), organised in 15 reference groups per language, four similarity
  categories per group (identical, functional, structural, different).
- **Source-code corpus** — 60 C# source files under `csharp/` and 60 Java
  source files under `java/`, all authored by the research team specifically
  for this dataset.
- **Experimental results** (`results_llm_comparison.csv`) — 480 rows recording
  the outcome of a controlled within-subjects evaluation of four commercial
  large language models acting as source-code similarity analysts:
  Claude Opus 4.1 (Anthropic), GPT-5 (OpenAI), Gemini 2.5 Pro (Google), and
  DeepSeek-V3 (DeepSeek). Evaluation campaign conducted between 2025-08-29 and
  2025-09-14.
- **Codebook** (`results_codebook.csv`) — machine-readable variable
  dictionary for the experimental results file.
- **Citation metadata** (`CITATION.cff`) — Citation File Format 1.2.0 record
  with `preferred-citation` pointing to the companion manuscript.
- **Open-data license** (`LICENSE`) — Creative Commons Attribution 4.0
  International (CC BY 4.0).
- **Documentation** (`README.md`) — dataset overview, filename convention,
  variable descriptions, loading example, ethical considerations, and
  citation guidance.

### Notes
- All 120 source files were authored by the research team; no file is
  derived from an authentic student submission and no personal data is
  contained in the dataset.
- The dataset is designed as a screening-aid evaluation resource for
  source-code similarity detection systems and is explicitly not intended
  as an evidentiary instrument for adjudicating academic misconduct.

[1.0.0]: https://github.com/gleiston-guerrero/SimilCode-Benchmark/releases/tag/v1.0.0
