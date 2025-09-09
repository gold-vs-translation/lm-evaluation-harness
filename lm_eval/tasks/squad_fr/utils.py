import re
import string


def process_results_qa(doc, results):
    preds = results[0]
    reference = doc["answers"]["text"][0]
    exact_match = exact(reference, preds)
    return {"exact_match": exact_match}


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        regex = re.compile(r"\b(un|une|des|le|la|les)\b", re.UNICODE)
        return re.sub(regex, " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


# Exact match (the normalized answer exactly match the gold answer)
def exact(predictions, references):
    return int(normalize_answer(references[0]) == normalize_answer(predictions[0]))
