# SimilCode Benchmark

<!-- TODO: replace ZENODO_ID once the tagged release is archived on Zenodo -->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.ZENODO_ID.svg)](https://doi.org/10.5281/zenodo.ZENODO_ID)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A curated benchmark of source-code snippets in **C#** and **Java**, purpose-built for the empirical evaluation of source-code similarity detection systems that rely on generative artificial intelligence. This dataset was assembled as part of the **SimilCode** research project and was used in the validation study reported in the accompanying manuscript.

---

## 1. Overview

The benchmark comprises **120 source files** evenly distributed across two programming languages (60 in C# and 60 in Java). The files are organised into **30 test-case pairs per language**, and each pair instantiates one of three canonical similarity scenarios:

| Scenario | Description |
|---|---|
| **Identical** | Two submissions whose source code is literally, or almost literally, the same. |
| **Similar** | Two submissions that share intent or structure but differ at the surface level: renamed identifiers, reordered statements, refactored control flow, equivalent data structures, alternative idioms, etc. |
| **Different** | Two submissions that either solve unrelated problems or address the same problem through substantially different approaches. |

This tripartite design allows researchers to probe the **sensitivity**, **specificity** and **calibration** of similarity detectors under conditions that mirror those observed in real programming courses.

---

## 2. Repository structure

```
similcode-benchmark/
├── README.md              # this file
├── LICENSE                # CC-BY 4.0
├── CITATION.cff           # citation metadata
├── metadata.csv           # ground-truth annotations for every pair
├── csharp/                # 60 files → 30 pairs
│   ├── case_01_a.cs
│   ├── case_01_b.cs
│   ├── ...
│   ├── case_30_a.cs
│   └── case_30_b.cs
└── java/                  # 60 files → 30 pairs
    ├── case_01_a.java
    ├── case_01_b.java
    ├── ...
    ├── case_30_a.java
    └── case_30_b.java
```

Files that belong to the same test case share a numeric identifier and are distinguished by the suffix `_a` / `_b`. All ground-truth annotations are consolidated in `metadata.csv`; the file system layout is provided only as a convenience.

---

## 3. `metadata.csv` schema

Each row of `metadata.csv` describes one test-case pair.

| Column | Type | Description |
|---|---|---|
| `case_id` | integer | Unique identifier of the test-case pair within a language (1–30). |
| `language` | string | `csharp` or `java`. |
| `file_a` | string | Relative path of the first file of the pair. |
| `file_b` | string | Relative path of the second file of the pair. |
| `scenario` | string | Ground-truth similarity category: `identical`, `similar`, or `different`. |
| `similarity_type` | string | Predominant nature of the resemblance for `similar` pairs (`lexical`, `structural`, `stylistic`, `functional`, `syntactic`, or a comma-separated combination). Empty for `identical` and `different` pairs. |
| `problem_description` | string | Brief natural-language description of the programming problem addressed by the pair. |
| `transformation` | string | Concise description of the transformation that produced `file_b` from `file_a` (e.g. *identifier renaming*, *loop-to-recursion*, *unrelated problem*). |
| `expected_big_o` | string | Expected asymptotic complexity of the solution when unambiguously defined (e.g. `O(n)`, `O(n log n)`); empty otherwise. |
| `notes` | string | Free-text observations. |

---

## 4. Loading the dataset

The benchmark is small enough to fit in memory. A minimal Python example:

```python
import pandas as pd
from pathlib import Path

root = Path("similcode-benchmark")
meta = pd.read_csv(root / "metadata.csv")

for _, row in meta.iterrows():
    src_a = (root / row["file_a"]).read_text(encoding="utf-8")
    src_b = (root / row["file_b"]).read_text(encoding="utf-8")
    # feed (src_a, src_b, row["scenario"]) to the similarity detector under test
```

---

## 5. Intended use

This benchmark was designed to support:

1. Empirical comparison of commercial large language models acting as source-code similarity analysts.
2. Calibration and threshold selection for academic-integrity tools that flag suspected plagiarism in programming assignments.
3. Reproducibility of the experiments reported in the accompanying manuscript.

Researchers are free to reuse the benchmark for related studies provided that the citation and licence terms below are respected.

---

## 6. Ethical considerations

No source file in this benchmark reveals the identity of any student, instructor, or institution. Where fragments were inspired by authentic student submissions, the corresponding participants provided **informed consent** and all identifying elements were removed prior to inclusion. Where fragments were authored or paraphrased *de novo*, they were produced by the research team specifically for the purposes of this benchmark. The study was conducted in accordance with the ethical guidelines of Universidad Técnica Estatal de Quevedo.

---

## 7. Related resources

- **Backend REST service** — <https://github.com/gleiston-guerrero/BackEnd-SimilCode>
- **Frontend web application** — <https://github.com/gleiston-guerrero/FrontEnd-SimilCode>
- **Manuscript** — Guerrero-Ulloa, G.; Navas Rivera, R. A.; Díaz-Macías, E.; Hornos, M. J.; Rodríguez-Domínguez, C. *A comparative evaluation of commercial large language models as source-code similarity analysts.* Manuscript submitted to the *International Journal for Educational Integrity*, Springer Nature.

---

## 8. How to cite

When using this benchmark in academic work, please cite the archived Zenodo record associated with the tagged release of this repository. The full citation metadata is provided in the `CITATION.cff` file at the root of the repository.

Suggested textual citation (BibTeX-friendly):

```
Navas Rivera, R. A., Guerrero-Ulloa, G., Díaz-Macías, E., Hornos, M. J., &
Rodríguez-Domínguez, C. (2026). SimilCode Benchmark: a dual-language
source-code similarity dataset for the evaluation of AI-based detectors
(v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.ZENODO_ID
```

<!-- TODO: replace ZENODO_ID after publishing the Zenodo release -->

---

## 9. Licence

This dataset is released under the **Creative Commons Attribution 4.0 International Licence (CC BY 4.0)**. See the `LICENSE` file for the full text. In short: you are free to share and adapt the material for any purpose, including commercial use, provided that appropriate credit is given, a link to the licence is provided, and any changes are indicated.

---

## 10. Authors and affiliations

| Author | Affiliation | ORCID |
|---|---|---|
| Rafael Alexander Navas Rivera | Universidad Técnica Estatal de Quevedo, Ecuador | 0009-0005-7926-2648 |
| Gleiston Guerrero-Ulloa, Ph.D. | Universidad Técnica Estatal de Quevedo, Ecuador | 0000-0001-5990-2357 |
| Efraín Díaz-Macías            | Universidad Técnica Estatal de Quevedo, Ecuador | 0000-0003-4087-029X |
| Miguel J. Hornos              | Universidad de Granada, Spain                   | 0000-0001-5722-9816 |
| Carlos Rodríguez-Domínguez    | Universidad de Granada, Spain                   | 0000-0001-5626-3115 |

**Corresponding author:** Gleiston Guerrero-Ulloa — [`gguerrero@uteq.edu.ec`](mailto:gguerrero@uteq.edu.ec) <!-- TODO: confirm the email address to be published -->

---

## 11. Acknowledgements

This work was developed as part of the *Curricular Integration Work* for the Bachelor's Degree in Software Engineering at Universidad Técnica Estatal de Quevedo. The authors thank the expert teachers who took part in the validation study for their time and constructive feedback.
