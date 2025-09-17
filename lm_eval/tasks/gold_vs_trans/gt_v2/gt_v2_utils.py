from evaluate import load

squad_metric = load("squad_v2")


def process_results_qa(doc: dict, results: list[str]):
    predictions = results
    references = doc["answers"]["text"]
    results = squad_metric.compute(predictions=predictions, references=references)

    return {
        "exact_match": results["exact_match"],
        "f1": results["f1"],
        "has_answer_exact_match": results["HasAns_exact"],
        "has_answer_f1": results["HasAns_f1"],
    }
