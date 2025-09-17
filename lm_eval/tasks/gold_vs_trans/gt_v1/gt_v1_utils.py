from datasets import Dataset
from evaluate import load

squad_metric = load("squad")


def process_results_qa(doc: dict, results: list[str]):
    prediction_text = results[0]
    assert isinstance(prediction_text, str)

    doc_id = str(doc["id"])

    predictions = [
        {
            "id": doc_id,
            "prediction_text": prediction_text,
        }
    ]

    gold_texts = doc["answers"]["text"]
    if not isinstance(gold_texts, list):
        gold_texts = [gold_texts]

    gold_answer_starts = doc["answers"].get("answer_start", [0] * len(gold_texts))
    if not isinstance(gold_answer_starts, list):
        assert isinstance(gold_texts, str)
        gold_answer_starts = [gold_answer_starts]

    references = [
        {
            "id": doc_id,
            "answers": {
                "text": gold_texts,
                "answer_start": gold_answer_starts,
            },
        }
    ]
    results = squad_metric.compute(predictions=predictions, references=references)

    return results


def filter_docs_nonempty_answers(dataset: Dataset) -> Dataset:
    return dataset.filter(lambda doc: len(doc["answers"]["text"]) > 0)
