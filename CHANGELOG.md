# Changelog

All notable changes to the **SimilCode Benchmark** dataset are documented in
this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.3.0] — 2026-10-25 (in preparation; reviewer comment M1, second run)

### Added
- AI-rewritten copies and their second-run scores. Light (`CODE_IAL_*`) and heavy (`CODE_IAI_*`) rewrites generated locally with `ollama:qwen2.5-coder:14b` (rewrite prompts v2, temperature 0.7); heavy rewrites generated through the APIs (`CODE_IAP_*`, same heavy prompt, generators assigned in rotation). Copies kept only if they compiled and printed the same output as the original for three input sets; up to three regenerations; programs with random output reviewed by hand (`copias_ia/marcar_revision_manual.py`).
- `copias_ia/rechazos_ia.csv`: generators that declined the heavy-rewrite prompt (GPT-5.5 declined 8 of 8 requests, Claude Opus 5 declined 3 of 8); the declined copies were requested again, with the same prompt, from the generators that complied.
- Second-run results: `copias_ia/resultados_replicas_ia.csv` (four LLMs, three replicas, 114 pairs), `copias_ia/baselines_raw_ia.csv` (Moss, JPlag and Dolos on the new cohort), `copias_ia/resultados_copias_ia.json` (analysis) and `copias_ia/resultados_copias_ia_local_qwen.json` (analysis before the API copies were added).

### Changed
- `generar_copias_ia.py`: level `api` (`CODE_IAP_*`), option `--solo-fallidas`.
- `verificar_equivalencia.py`: recognises `CODE_IAP_*`.
- `construir_casos_ia.py`, `analisis_copias_ia.py`, `benchmark_replicas.py`, `baselines.py`: category `ia_api`.
- `ejecutar_moss.sh`: follows the redirect of the results URL (`curl -L`).

## [2.2.0] — 2026-10-23 (in preparation; reviewer comment M1)

### Added
- `analisis_tipos_clon.py`: reclassifies the pairs with the clone taxonomy of Roy, Cordy and Koschke (2009) using a deterministic rule (normalised token sequences) and measures how well each system separates copies (types 1–3) from independent solutions (type 4), with cluster-bootstrap intervals over the 30 reference programs and flag rates at review thresholds. Outputs: `tipos_clon.csv`, `resultados_tipos_clon.json`.
- `copias_ia/`: pipeline to generate copies rewritten with generative AI (light and heavy), verify their functional equivalence by compiling and running them, build the second-run cases (`metadata_ia.csv`), and analyse them (`analisis_copias_ia.py`). See `copias_ia/README_COPIAS_IA.md`.

### Changed
- `benchmark_replicas.py`: accepts the categories `ia_ligera` and `ia_intensa`, and records input and output tokens per call in new result files.
- `baselines.py`: accepts the new categories.
- `ejecutar_moss.sh`: `TRABAJO` and `SUFIJO` can be set from outside, so a second cohort does not overwrite the original reports.

## [2.1.0] — 2026-10-21

### Added
- `analisis_manuscrito.py`: reproduces every number of the manuscript (Discover Computing, version 13) from the archived files, without API calls.

### Changed
- `README.md` rewritten: documents the replicated 2026 benchmark (`resultados_replicas.csv`), the classical detectors, the Big O validation and the reproduction rules; marks `results_llm_comparison.csv` as legacy.
- `CITATION.cff`: version 2.1.0, abstract and keywords updated, companion journal changed to *Discover Computing*, concept DOI described as such.

### Fixed
- `benchmark_replicas.py` contained two concatenated copies of the program, so `main()` ran twice per invocation. The duplicate copy was removed; the code is otherwise unchanged.

### Notes
- Tag `v2.0.0` was never archived on Zenodo; the latest archived version before this release was v1.0.1 (10.5281/zenodo.21790027).
- `README_moss.md` contained the Moss user id in commits ca686f8 to 9d30491 (removed in fe88387). That id must be considered public and a new one requested.

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
