# Gold vs. Translation — LM Evaluation Harness

This repository contains a **modified version of the [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)** with custom evaluation tasks and configurations used for our [EMNLP 2026 paper, *Gold vs. Translation*](https://aclanthology.org/2026.emnlp-main.32/).

The study examines how well performance on translated benchmarks reflects performance on native-language, culturally grounded benchmarks. This repository provides the **evaluation-side implementations**: benchmark task definitions, dataset integrations, prompts, answer processing, and scoring. It is **not registered as a GitHub fork** of the upstream repository; the upstream framework and its contributors remain acknowledged.

> **Paper evaluation code revision:** [`33adacb49b4cee8ab58dfaf3be3a961a2b9c62f6`](https://github.com/gold-vs-translation/lm-evaluation-harness/commit/33adacb49b4cee8ab58dfaf3be3a961a2b9c62f6). Subsequent documentation-only commits do not alter this historical evaluation revision.

## Where to start

| If you want to… | Start here |
|---|---|
| See the implemented benchmark tasks | [`lm_eval/tasks/gold_vs_trans/`](lm_eval/tasks/gold_vs_trans/) and the [Task Guide](docs/GOLD_VS_TRANSLATION_TASKS.md) |
| Find the exact evaluation-ready datasets | [Dataset overview](#benchmarks-and-hugging-face-datasets) and the task YAMLs |
| Use a custom task in LM Evaluation Harness | [Install and use](#installation-and-usage) |
| Reproduce analyses **without** evaluating models again | [Data repository](https://github.com/gold-vs-translation/cs-annotation-data) and [Analysis Guide](https://github.com/gold-vs-translation/annotation-and-analysis-scripts/blob/main/docs/ANALYSIS_GUIDE.md) |
| Learn about the underlying framework | [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) and its documentation in this checkout |

## What's in this repository?

The project adds task configurations under `lm_eval/tasks/gold_vs_trans/`. They describe dataset selection, prompts, answer formatting/extraction, metrics, and any task-specific helpers. The remaining framework comes from the upstream LM Evaluation Harness, with modifications preserved in the historical evaluation revision above.

The primary benchmark configurations are organized into the groups below. Some older task variants also exist (`gt_v1` and `gt_v2`); these are not the recommended entry point for the main paper analysis.

## Benchmarks and Hugging Face datasets

| Benchmark | Custom task directory | Hugging Face dataset | Purpose |
|---|---|---|---|
| DanishCitizenTest | [`gt_danishcitizentest/`](lm_eval/tasks/gold_vs_trans/gt_danishcitizentest/) | [`gold-vs-trans/danish-citizen-tests-dedup`](https://huggingface.co/datasets/gold-vs-trans/danish-citizen-tests-dedup) | Danish citizenship and residence questions |
| Exam-ET | [`gt_exam_et/`](lm_eval/tasks/gold_vs_trans/gt_exam_et/) | [`gold-vs-trans/exam_et_with_ids`](https://huggingface.co/datasets/gold-vs-trans/exam_et_with_ids) | Estonian subject-specific examinations |
| INCLUDE-base | [`gt_includebase/`](lm_eval/tasks/gold_vs_trans/gt_includebase/) | [`CohereLabs/include-base-44`](https://huggingface.co/datasets/CohereLabs/include-base-44) | Estonian and Lithuanian task configurations |
| NRK-Quiz-QA | [`gt_nrkquizqa/`](lm_eval/tasks/gold_vs_trans/gt_nrkquizqa/) | [`ltg/nrk_quiz_qa`](https://huggingface.co/datasets/ltg/nrk_quiz_qa) | Norwegian quiz QA with task-specific processing |
| Skolprov | [`gt_skolprov/`](lm_eval/tasks/gold_vs_trans/gt_skolprov/) | [`Ekgren/swedish_skolprov`](https://huggingface.co/datasets/Ekgren/swedish_skolprov) | Swedish subject-specific examinations |
| SwedishFacts | [`gt_swedishfacts/`](lm_eval/tasks/gold_vs_trans/gt_swedishfacts/) | [`gold-vs-trans/swedish-facts-v1-normalized`](https://huggingface.co/datasets/gold-vs-trans/swedish-facts-v1-normalized) | Swedish factual QA, using configured answer-processing metrics |
| G-MMLUX | [`gt_gmmlux/`](lm_eval/tasks/gold_vs_trans/gt_gmmlux/) | [`gold-vs-trans/gmmlux`](https://huggingface.co/datasets/gold-vs-trans/gmmlux) | Translated MMLU proxy configurations by language and subject |

The paper analyses also use **Belebele** as a control benchmark; its evaluation configuration is part of the harness ecosystem rather than one of the seven custom task directories listed above.

**Dataset provenance and access.** The four `gold-vs-trans` Hugging Face datasets are evaluation-ready versions maintained for this study. Their dataset cards are available on Hugging Face. Consult each card and the **original dataset's license and access conditions** before redistributing or reusing data. In particular, the existence of a public HF repository or dataset card does not by itself establish unrestricted redistribution rights. The Exam-ET source has specific access/usage conditions. Where the exact transformation matters, inspect the corresponding task YAMLs and dataset cards; this README does not claim that all upstream preprocessing has been rerun for the public release.

## Installation and usage

Clone **this project version**, not the upstream repository, to access our task implementations:

```bash
git clone https://github.com/gold-vs-translation/lm-evaluation-harness.git
cd lm-evaluation-harness
python -m pip install -e .
```

For the original paper's evaluation code, pin the revision:

```bash
git checkout 33adacb49b4cee8ab58dfaf3be3a961a2b9c62f6
```

> Checking out the historical revision also restores the documentation as it existed at that commit. Return to `main` to read the latest project guides.

List registered tasks in the installed checkout:

```bash
python -m lm_eval --tasks list
```

A minimal *illustrative* evaluation invocation is:

```bash
python -m lm_eval \
  --model hf \
  --model_args pretrained=YOUR_MODEL_ID \
  --tasks gt_exam_et_ajalugu \
  --batch_size 1 \
  --limit 10
```

Replace `YOUR_MODEL_ID` with an accessible model. This command illustrates the interface; **it has not been rerun as part of this documentation release**. Running the task may download its dataset and model and requires an appropriate environment and access permissions. The exact task name `gt_exam_et_ajalugu` is defined by the task YAML in this repository. For other task names, see the [Task Guide](docs/GOLD_VS_TRANSLATION_TASKS.md) or list registered tasks. For GPU and inference-backend options, consult the [upstream documentation](https://github.com/EleutherAI/lm-evaluation-harness).

## Reproducing the paper's analyses

**You do not need to rerun the original model evaluations to reproduce the downstream statistical analyses.** The public materials are split across three repositories:

| Repository | Contains |
|---|---|
| [LM Evaluation Harness (this repository)](https://github.com/gold-vs-translation/lm-evaluation-harness) | Task definitions, evaluation configurations and framework modifications |
| [Annotations and merged analysis data](https://github.com/gold-vs-translation/cs-annotation-data) | GPT/human annotation data, merged item-level model scores, frozen reference results |
| [Annotation and analysis scripts](https://github.com/gold-vs-translation/annotation-and-analysis-scripts) | Annotation pipeline, ranking analyses, incremental proxy validity, bootstrap/LOFO and meta-evaluation scripts |

Start with the [Analysis Guide](https://github.com/gold-vs-translation/annotation-and-analysis-scripts/blob/main/docs/ANALYSIS_GUIDE.md), which explains ranking consistency and incremental proxy validity and documents a successful limited-data smoke test. That smoke test checks the core regression and output-writing path; it is **not** a numerical reproduction of every paper table or a repeat of the original 29-model evaluation campaign.

## Original framework and licenses

This repository is **based on**, but is **not listed by GitHub as a fork of**, the [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness). We acknowledge the upstream maintainers and retain the applicable upstream licensing and copyright notices. Refer to the repository's license files and upstream documentation for framework-level terms. Dataset licenses and access restrictions are separate from the software license.

The extensive original Harness README may be retained as [`docs/UPSTREAM_README.md`](docs/UPSTREAM_README.md) in this repository; that link will work once the original README has been copied there and committed.

## Citation

If you use our custom tasks or the study's derived evaluation data, cite the [Gold vs. Translation paper (EMNLP 2026)](https://aclanthology.org/2026.emnlp-main.32/) and the relevant original benchmark publications. If you use the evaluation framework, also cite the [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness).
