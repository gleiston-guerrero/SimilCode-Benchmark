# SimilCode Benchmark

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.NNNNNNN.svg)](https://doi.org/10.5281/zenodo.NNNNNNN)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A curated benchmark of source-code snippets in **C#** and **Java**, purpose-built for the empirical evaluation of source-code similarity detection systems that rely on generative artificial intelligence. This repository contains both the ground-truth dataset (`metadata.csv`) and the raw experimental results (`results_llm_comparison.csv`) obtained when the benchmark was used to evaluate four commercial large language models as similarity analysts.

---

## 1. Overview

The benchmark comprises **120 source files** distributed evenly across two programming languages (60 in C# and 60 in Java). Files are organised into **60 test-case pairs per language**, split into **15 reference groups**. Every reference group instantiates the same four similarity scenarios:

| Category | Files paired | Expected similarity |
|---|---|---|
| **identical** | reference file compared with itself | 100 % |
| **functional** | reference vs a functionally equivalent implementation | 70–90 % |
| **structural** | reference vs a structurally similar variant | 40–60 % |
| **different** | reference vs an unrelated solution | 0–20 % |

The design is fully balanced: 15 pairs × 4 categories × 2 languages = 120 test-case pairs.

---

## 2. Repository structure

```
SimilCode-Benchmark/
├── README.md                     (this file)
├── LICENSE                       (CC-BY 4.0)
├── CITATION.cff                  (machine-readable citation metadata)
├── metadata.csv                  (ground-truth annotations for 120 pairs)
├── results_llm_comparison.csv    (experimental results, 4 LLMs × 120 cases)
├── results_codebook.csv          (variable dictionary for results file)
├── csharp/                       (60 .cs files)
│   ├── CODE_IDENT_CS_001.cs
│   ├── CODE_FUN_CS_001.cs
│   ├── CODE_ESTRU_CS_001.cs
│   ├── CODE_DIF_CS_001.cs
│   ├── …
│   └── CODE_DIF_CS_015.cs
└── java/                         (60 .java files)
    ├── CODE_IDENT_JAVA_001.java
    ├── …
    └── CODE_DIF_JAVA_015.java
```

Filename convention: `CODE_<CATEGORY>_<LANGUAGE>_<REF_NUMBER>.<ext>`, where `<CATEGORY>` is one of `IDENT`, `FUN`, `ESTRU`, `DIF`, `<LANGUAGE>` is `CS` or `JAVA`, and `<REF_NUMBER>` is a zero-padded reference group identifier (001–015). The `CS` token is used in file names in place of `C#` because the hash character breaks GitHub raw-file URLs; the human-readable language remains `C#` in every `language` column of the CSV files.

---

## 3. `metadata.csv` — ground truth

One row per test-case pair (120 rows). Key columns:

| Column | Description |
|---|---|
| `case_id` | Unique case identifier, e.g. `CASE_CODE_CS_001`. |
| `language` | `C#` or `Java`. |
| `reference_group` | 1–15; groups the four cases derived from the same reference file. |
| `similarity_category` | `identical`, `functional`, `structural`, or `different`. |
| `code_a_id`, `code_b_id` | Identifiers of the two source files being compared. |
| `code_a_filename`, `code_b_filename`, `code_a_path`, `code_b_path` | File-system references (relative to repository root). |
| `code_a_loc`, `code_b_loc` | Non-blank lines of code (author-verified). |
| `code_a_methods`, `code_b_methods` | Number of methods/functions declared. |
| `expected_similarity_min`, `expected_similarity_max` | Ground-truth similarity range for the category. |
| `evaluator`, `evaluation_date` | Provenance of the annotations (ISO 8601 dates). |
| `notes` | Free-text observations. |

---

## 4. `results_llm_comparison.csv` — experimental results

One row per (case × model) combination (**480 rows** = 120 cases × 4 models). Documents the outcome of a controlled evaluation of four contemporary commercial LLMs acting as source-code similarity analysts:

- **Claude Opus 4.1** (Anthropic)
- **GPT-5** (OpenAI)
- **Gemini 2.5 Pro** (Google)
- **DeepSeek-V3** (DeepSeek)

Each row records the model's classification (`classified_similarity_percent`), whether it fell within the expected range (`coincidence`), the confusion-matrix entry (`true_positive`, `true_negative`, `false_positive`, `false_negative`), per-case accuracy/sensitivity/specificity, response time, and Likert-scale ratings of justification quality (clarity, technical terminology, logical structure, internal consistency, dimension coverage). The full variable dictionary is provided in `results_codebook.csv`.

The evaluation campaign was conducted between **2025-08-29 and 2025-09-14** by Rafael Navas on a workstation running Windows 11 Pro (Intel Core i5-10400, 16 GB RAM); the exact hardware and network parameters for each case are stored per row in the results file.

---

## 5. Loading the dataset

A minimal Python example that joins the ground-truth and the experimental results:

```python
import pandas as pd
from pathlib import Path

root   = Path("SimilCode-Benchmark")
meta   = pd.read_csv(root / "metadata.csv")
result = pd.read_csv(root / "results_llm_comparison.csv")

# Read the source of a specific pair
row   = meta.iloc[0]
src_a = (root / row["code_a_path"]).read_text(encoding="utf-8")
src_b = (root / row["code_b_path"]).read_text(encoding="utf-8")

# Coincidence rate per model
print(result.groupby("llm_model")["coincidence"].mean() * 100)
```

---

## 6. Intended use

This benchmark was designed to support:

1. Empirical comparison of commercial large language models acting as source-code similarity analysts.
2. Calibration and threshold selection for academic-integrity tools that flag suspected similarity in programming assignments.
3. Reproducibility of the experiments reported in the accompanying manuscript.

Researchers are free to reuse the benchmark for related studies provided that the citation and licence terms below are respected.

---

## 7. Ethical considerations

All 120 source files in this benchmark were authored by the research team specifically for the purposes of this dataset. No file reveals the identity of any student, instructor, or institution, and no file is derived from an authentic student submission. The dataset therefore contains no personal data and required no informed-consent procedure.

---

## 8. Related resources

- **Backend REST service** — <https://github.com/gleiston-guerrero/BackEnd-SimilCode>
- **Frontend web application** — <https://github.com/gleiston-guerrero/FrontEnd-SimilCode>
- **Companion manuscript** — Guerrero-Ulloa, G. C., Navas Rivera, R. A., Díaz-Macías, E., Hornos, M. J., & Rodríguez-Domínguez, C. *SimilCode: A Web Application for Source Code Similarity Detection and Algorithmic Efficiency Analysis using Generative Artificial Intelligence.* Manuscript submitted to the *International Journal for Educational Integrity* (Springer Nature).

---

## 9. How to cite

When using this benchmark, please cite the archived Zenodo record associated with the tagged release. Full machine-readable citation metadata is provided in `CITATION.cff`.

Suggested textual citation:

```
Guerrero-Ulloa, G. C., Navas Rivera, R. A., Díaz-Macías, E., Hornos, M. J., &
Rodríguez-Domínguez, C. (2026). SimilCode Benchmark: A Dual-Language
Source-Code Similarity Dataset for the Evaluation of AI-Based Detectors
(Version 1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.NNNNNNN
```
<!-- Replace NNNNNNN once minted -->

---

## 10. Licence

Released under the **Creative Commons Attribution 4.0 International Licence (CC BY 4.0)**. See `LICENSE` for the full text.

---

## 11. Authors

| Author                              | Affiliation                                                                                                                                        | ORCID                                                        | Contact                        |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------ |
| Gleiston Cicerón Guerrero-Ulloa     | Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo (UTEQ), Quevedo, Los Ríos, Ecuador                                  | [0000-0001-5990-2357](https://orcid.org/0000-0001-5990-2357) | <gguerrero@uteq.edu.ec>        |
| Rafael Alexander Navas Rivera       | Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo (UTEQ), Quevedo, Los Ríos, Ecuador                                  | [0009-0005-7926-2648](https://orcid.org/0009-0005-7926-2648) | <rafael.navas2017@uteq.edu.ec> |
| Efraín Díaz-Macías                  | Facultad de Ciencias de la Computación, Universidad Técnica Estatal de Quevedo (UTEQ), Quevedo, Los Ríos, Ecuador                                  | [0000-0003-4087-029X](https://orcid.org/0000-0003-4087-029X) | <efraindiaz@uteq.edu.ec>       |
| Miguel J. Hornos                    | Department of Software Engineering, University of Granada (UGR), Granada, Spain                                                                    | [0000-0001-5722-9816](https://orcid.org/0000-0001-5722-9816) | <mhornos@ugr.es>               |
| Carlos Rodríguez-Domínguez ⭐        | Department of Software Engineering, and Research Center for Information and Communication Technologies (CITIC), University of Granada (UGR), Spain | [0000-0001-5626-3115](https://orcid.org/0000-0001-5626-3115) | <carlosrodriguez@ugr.es>       |

⭐ **Corresponding author:** Carlos Rodríguez-Domínguez — <carlosrodriguez@ugr.es>

---

## 12. Acknowledgements

This dataset was developed as part of the *Curricular Integration Work* for the Bachelor's Degree in Software Engineering at Universidad Técnica Estatal de Quevedo, in collaboration with researchers from Universidad de Granada.
