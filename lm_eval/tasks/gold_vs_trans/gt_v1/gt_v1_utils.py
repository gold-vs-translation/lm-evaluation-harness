from datasets import Dataset
from evaluate import load

squad_metric = load("squad")


def process_results_qa(doc: dict, results: list[str]):
    predictions = results
    references = doc["answers"]["text"]
    results = squad_metric.compute(predictions=predictions, references=references)

    return results


def filter_docs_nonempty_answers(dataset: Dataset) -> Dataset:
    return dataset.filter(lambda doc: len(doc["answers"]["text"]) > 0)
