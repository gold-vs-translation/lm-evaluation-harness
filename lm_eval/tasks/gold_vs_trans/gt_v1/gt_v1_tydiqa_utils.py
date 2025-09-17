from datasets import Dataset


def filter_docs_by_id_prefix(dataset: Dataset, id_prefix: str) -> Dataset:
    return dataset.filter(lambda doc: doc["id"].startswith(id_prefix))


def process_docs_en(dataset: Dataset) -> Dataset:
    return filter_docs_by_id_prefix(dataset, "english-")


def process_docs_fi(dataset: Dataset) -> Dataset:
    return filter_docs_by_id_prefix(dataset, "finnish-")


def process_docs_ru(dataset: Dataset) -> Dataset:
    return filter_docs_by_id_prefix(dataset, "russian-")
