# SimilCode Benchmark

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21271491.svg)](https://doi.org/10.5281/zenodo.21271491)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A controlled benchmark of **120 source-code pairs in C# and Java** for evaluating source-code similarity detectors, together with every raw result reported in the companion manuscript: a replicated evaluation of four commercial large language models (LLMs), the outputs of three classical detectors (Moss, JPlag, Dolos) on the same pairs, and the validation of the Big O estimator of SimilCode.

The DOI badge above is the **concept DOI** and always resolves to the latest archived version. Cite the version DOI shown on Zenodo for the release you use.

---

## 1. Corpus and ground truth

15 reference programs per language, each paired with four counterparts:

| Category | Pair | Expected similarity band |
|---|---|---|
| identical | reference vs itself | 100 % |
| functional | reference vs an independent implementation with the same behaviour | 70–90 % |
| structural | reference vs a variant that keeps the control flow | 40–60 % |
| different | reference vs an unrelated program | 0–20 % |

15 pairs × 4 categories × 2 languages = **120 pairs** (`metadata.csv`). All files were written by the research team or taken from the public domain; no student code is included.

The categories were verified by a second programming instructor who received the files without labels: Cohen's κ = 0.989 (119/120). Files: `fiabilidad/categorias_evaluador2.csv`, `fiabilidad/clave_categorias_ref.csv`. The single disagreement exposed an archived functional variant that was an exact copy; it was replaced before the benchmark reached that pair.

File names: `CODE_<CATEGORY>_<LANG>_<NNN>.<ext>` with `<CATEGORY>` ∈ {IDENT, FUN, ESTRU, DIF} and `<LANG>` ∈ {CS, JAVA}. `CS` replaces `C#` because `#` breaks raw GitHub URLs.

## 2. Contents

| File / folder | Content |
|---|---|
| `metadata.csv` | Ground truth for the 120 pairs. |
| `csharp/`, `java/` | The 120 source files. |
| `prompt.txt`, `PROMPT_HASH.txt` | Standardised similarity prompt (Spanish, verbatim) and its SHA-256 hash (`c443efea…a99c`). |
| `resultados_replicas.csv` | **Main LLM results**: 1,440 valid evaluations (120 pairs × 4 models × 3 replicas) plus 182 failed calls kept for transparency (`error` column). |
| `resumen_estabilidad.csv`, `sensibilidad_banda.csv` | Summaries produced by `benchmark_replicas.py analyze` (see note in §4). |
| `baselines_raw.csv` | Similarity of the 120 pairs according to Moss, JPlag and Dolos (cohort mode) and Dolos with `-m 10` (sensitivity run). |
| `moss_cs.html`, `moss_java.html`, `moss_raw.csv` | Archived Moss reports and parsed scores. |
| `out_jplag_*/`, `out_dolos_*/`, `jplag_*_utf8.log`, `antlr_cs.csv` | Raw JPlag and Dolos outputs, JPlag logs and C# parse errors. |
| `bigo/` | Big O validation: 40 canonical + 8 adversarial programs, ground truth (corrected and original), prompt, predictions of the production model (`predicciones_api*.csv`) and per-item scoring. |
| `benchmark_replicas.py` | Harness that ran the 1,440 evaluations (`run`) and its summary (`analyze`). |
| `baselines.py`, `ejecutar_moss.sh`, `PROTOCOLO_dolos_jplag.md`, `README_baselines.md`, `README_moss.md` | Protocol and scripts for the classical detectors. |
| `analisis_manuscrito.py` | **Reproduces every number reported in the manuscript** from the archived files, without calling any API. |
| `results_llm_comparison.csv`, `results_codebook.csv` | **Legacy (v1.0.0)**: preliminary single-run evaluation of earlier models (2025). Not used in the current manuscript; kept only for traceability. |

## 3. LLM benchmark

| Provider | Identifier invoked |
|---|---|
| OpenAI | `gpt-5.5-2026-04-23` (production model of SimilCode) |
| DeepSeek | `deepseek-v4-pro` |
| Google | `gemini-3.1-pro-preview` |
| Anthropic | `claude-opus-5` |

* Official APIs, fresh context per call, three replicas per pair and model, collected 30 July – 1 August 2026.
* Temperature 0 requested; `claude-opus-5` rejects it (HTTP 400), so its calls used the provider default.
* Failed calls (kept in the file, `error` not empty): Gemini 128 × HTTP 429, 5 × HTTP 503, 4 timeouts; Anthropic 30 × HTTP 400 (temperature); OpenAI 15 × HTTP 401 (credential set-up).
* 4 Claude Opus 5 responses have no parsable global score; the manuscript counts them as non-coincident.
* Except for GPT-5.5, the identifiers are aliases, not dated snapshots.

## 4. Reproducing the manuscript

```bash
pip install pandas numpy scipy statsmodels pingouin scikit-learn
python analisis_manuscrito.py --validation ../SimilCode-Validation
```

Rules fixed before the analysis: majority verdict = coincident in ≥ 2 of 3 replicas, unparsable responses count as misses; tolerance of 5 points in the identical category for every system; `different` band 0–20 (0–30 as sensitivity); band sensitivity changes only non-identical bands; BCa bootstrap, 10,000 resamples, seed 20260730.

> **Note.** `benchmark_replicas.py analyze` (and therefore `resumen_estabilidad.csv` and `sensibilidad_banda.csv`) uses a more lenient rule: it ignores unparsable responses and also shifts the identical band in the sensitivity analysis. This is why it reports 48.3 % for Claude Opus 5 instead of 47.5 %. The figures of the manuscript are those of `analisis_manuscrito.py`.

## 5. Classical detectors

Moss (Stanford server, `-d -m 10`, 1 Aug 2026), JPlag 6.3.0 (average similarity, threshold 0) and Dolos 2.9.3 (WSL/Ubuntu, defaults), each run once per language on the whole cohort (60 files + 15 materialised copies = 75 submissions, 2,775 comparisons). See `README_baselines.md` and `README_moss.md`. **The Moss user id must never be committed** (`moss` is in `.gitignore`).

## 6. Big O validation

GPT-5.5 via API, 3 August 2026, three replicas per program: 144/144 correct in time and space; 92.5 % space accuracy on the canonical set under the original ground truth (`bigo/ground_truth_v1_original.csv`). See `bigo/README_validacion_bigo.md`. The files `predicciones_opus5.csv` and `predicciones_adversarial_opus5.csv` are a preliminary run and are not reported.

## 7. Related resources

| Artefact | Repository | Concept DOI |
|---|---|---|
| Validation data (expert questionnaire, quality ratings) | [SimilCode-Validation](https://github.com/gleiston-guerrero/SimilCode-Validation) | [10.5281/zenodo.21284183](https://doi.org/10.5281/zenodo.21284183) |
| Backend | [BackEnd-SimilCode](https://github.com/gleiston-guerrero/BackEnd-SimilCode) | [10.5281/zenodo.21265177](https://doi.org/10.5281/zenodo.21265177) |
| Frontend | [FrontEnd-SimilCode](https://github.com/gleiston-guerrero/FrontEnd-SimilCode) | [10.5281/zenodo.21265976](https://doi.org/10.5281/zenodo.21265976) |

Companion manuscript: Guerrero-Ulloa, G. C., Navas Rivera, R. A., Díaz-Macías, E., Hornos, M. J., & Rodríguez-Domínguez, C. *SimilCode: A Web Application for Source Code Similarity Detection and Algorithmic Efficiency Analysis using Generative Artificial Intelligence.* Submitted to *Discover Computing* (Springer Nature).

## 8. Licence and citation

Data and documentation: CC BY 4.0 (`LICENSE`). Machine-readable citation metadata: `CITATION.cff`.
