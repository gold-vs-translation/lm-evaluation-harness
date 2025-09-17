# Copyright 2020 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Very heavily inspired by the official evaluation script for SQuAD version 2.0 which was modified by XLNet authors to
update `find_best_threshold` scripts for SQuAD V2.0

Does not try to remove articles during answer normalization.

In addition to basic functionality, we also compute additional statistics and plot precision-recall curves if an
additional na_prob.json file is provided. This file is expected to map question ID's to the model's predicted
probability that a question is unanswerable.
"""

import collections
import string
import datasets


def normalize_answer(s):
    """Lower text and remove punctuation and extra whitespace."""

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_punc(lower(s)))


def get_tokens(s):
    if not s:
        return []
    return normalize_answer(s).split()


def compute_exact(a_gold, a_pred):
    return int(normalize_answer(a_gold) == normalize_answer(a_pred))


def compute_f1(a_gold, a_pred):
    gold_toks = get_tokens(a_gold)
    pred_toks = get_tokens(a_pred)
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def process_results_qa(doc, results):
    preds = results[0]
    reference = doc["answers"]["text"][0]
    f1_sum = compute_f1(reference, preds)
    exact_match = compute_exact(reference, preds)
    return {"f1": f1_sum, "exact_match": exact_match}

def filter_docs_nonempty_answers(
    dataset: datasets.Dataset
) -> datasets.Dataset:
    return dataset.filter(lambda doc: len(doc["answers"]["text"]) > 0)
