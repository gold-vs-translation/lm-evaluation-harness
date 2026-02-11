import re
import string

from evaluate import load

squad_metric = load("squad")

NORM_RE = re.compile(f"[{re.escape(string.punctuation)} ]+")


def normalize_answer(answer: str):
    return NORM_RE.sub(" ", answer.lower()).strip()


def process_results_qa(doc: dict, results: list[str], lang: str):
    prediction_text = results[0]
    assert isinstance(prediction_text, str)

    doc_id = str(doc["id"])

    normalized_prediction = normalize_answer(prediction_text)
    normalized_reference = normalize_answer(doc[f"answer_{lang}"])

    predictions = [
        {
            "id": doc_id,
            "prediction_text": normalized_prediction,
        }
    ]

    references = [
        {
            "id": doc_id,
            "answers": {
                "text": [normalized_reference],
                "answer_start": [0],
            },
        }
    ]
    results = squad_metric.compute(predictions=predictions, references=references)

    return results


def process_results_qa_sv(doc: dict, results: list[str]):
    return process_results_qa(doc, results, "sv")


def process_results_qa_en(doc: dict, results: list[str]):
    return process_results_qa(doc, results, "en")
