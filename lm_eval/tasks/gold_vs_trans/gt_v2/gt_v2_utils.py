from evaluate import load

squad_metric = load("squad_v2")


def process_results_qa(doc: dict, results: list[str]):
    prediction_text = results[0]
    assert isinstance(prediction_text, str)

    doc_id = str(doc["id"])

    predictions = [
        {
            "id": doc_id,
            "prediction_text": prediction_text,
            "no_answer_probability": 0.0,
        }
    ]

    gold_texts = doc["answers"]["text"]
    if not isinstance(gold_texts, list):
        assert isinstance(gold_texts, str)
        if len(gold_texts) == 0:
            gold_texts = []
        else:
            gold_texts = [gold_texts]

    gold_answer_starts = doc["answers"].get("answer_start", [0] * len(gold_texts))
    if not isinstance(gold_answer_starts, list):
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

    return {
        "exact_match": results["exact"],
        "f1": results["f1"],
        "has_answer_exact_match": results["HasAns_exact"],
        "has_answer_f1": results["HasAns_f1"],
    }
