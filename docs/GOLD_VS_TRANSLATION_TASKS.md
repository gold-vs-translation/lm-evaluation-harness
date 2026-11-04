# Gold vs. Translation — custom evaluation tasks

Custom task definitions used for [Gold vs. Translation (EMNLP 2026)](https://aclanthology.org/2026.emnlp-main.32/). **Evaluation code revision:** [`33adacb49b4cee8ab58dfaf3be3a961a2b9c62f6`](https://github.com/gold-vs-translation/lm-evaluation-harness/commit/33adacb49b4cee8ab58dfaf3be3a961a2b9c62f6). The fork is based on the LM Evaluation Harness; see the upstream project's instructions for model backends.

## Task overview

| Task directory / example ID | Purpose | HF dataset |
|---|---|---|
| `gt_danishcitizentest/` · `gt_danishcitizentest_citizenship` | Danish citizenship/residence multiple choice | [gold-vs-trans/danish-citizen-tests-dedup](https://huggingface.co/datasets/gold-vs-trans/danish-citizen-tests-dedup) |
| `gt_exam_et/` · `gt_exam_et_ajalugu` | Estonian subject-specific multiple choice | [gold-vs-trans/exam_et_with_ids](https://huggingface.co/datasets/gold-vs-trans/exam_et_with_ids) |
| `gt_includebase/` · `gt_includebase_et`, `gt_includebase_lt` | Estonian/Lithuanian INCLUDE-base multiple choice | [CohereLabs/include-base-44](https://huggingface.co/datasets/CohereLabs/include-base-44) |
| `gt_nrkquizqa/` · `gt_nrkquizqa_nb` | Norwegian quiz task; custom processing/metric helpers | [ltg/nrk_quiz_qa](https://huggingface.co/datasets/ltg/nrk_quiz_qa) |
| `gt_skolprov/` · `gt_skolprov_hogskoleprovet` | Swedish subject-specific exam tasks | [Ekgren/swedish_skolprov](https://huggingface.co/datasets/Ekgren/swedish_skolprov) |
| `gt_swedishfacts/` · `gt_swedishfacts_sv` | SwedishFacts generative answer evaluation (EM/F1 as configured) | [gold-vs-trans/swedish-facts-v1-normalized](https://huggingface.co/datasets/gold-vs-trans/swedish-facts-v1-normalized) |
| `gt_gmmlux/` · `gt_gmmlux_da-abstract_algebra` | Translated MMLU proxy tasks by language/subject | [gold-vs-trans/gmmlux](https://huggingface.co/datasets/gold-vs-trans/gmmlux) |

The local task collection also contains older `gt_v1`/`gt_v2` variants; these are not the recommended starting point for reconstructing the primary analysis. The untracked `gt_gmmlux.bak/` backup on TUD is **not** part of the Git revision above.

## Using the tasks

```bash
git clone https://github.com/gold-vs-translation/lm-evaluation-harness.git
cd lm-evaluation-harness
python -m pip install -e .
# List registered task names in this checkout:
python -m lm_eval --tasks list
# Example task (requires a model backend and the corresponding dataset access):
python -m lm_eval --model hf --model_args pretrained=YOUR_MODEL \
  --tasks gt_exam_et_ajalugu --batch_size 1
```

The example shows task selection and has **not** been validated as a complete model evaluation in this release. Run it only when your selected model/backend and the task's data-access terms permit it. Task config files specify the exact dataset paths, splits, prompts, answer mapping, and metrics; inspect them when reproducing an original setup.

## Data provenance, terms and reproducibility

The four evaluation-ready datasets maintained under `gold-vs-trans` are [Danish Citizen Tests](https://huggingface.co/datasets/gold-vs-trans/danish-citizen-tests-dedup), [Exam-ET with IDs](https://huggingface.co/datasets/gold-vs-trans/exam_et_with_ids), [normalized SwedishFacts](https://huggingface.co/datasets/gold-vs-trans/swedish-facts-v1-normalized) and [G-MMLUX](https://huggingface.co/datasets/gold-vs-trans/gmmlux). Each HF repository currently has a dataset card. **A card's existence does not establish a redistribution license**: check its content and the upstream author's terms. In particular, Exam-ET has source-access conditions, and the evaluation-ready HF version must be reviewed separately from the redacted GitHub analysis data.

The original 29-model evaluations are **not rerun** as part of the public paper release. For analysis without rerunning inference, use the [merged item/model scores](https://github.com/gold-vs-translation/cs-annotation-data) and the [analysis scripts](https://github.com/gold-vs-translation/annotation-and-analysis-scripts/blob/main/docs/ANALYSIS_GUIDE.md).
