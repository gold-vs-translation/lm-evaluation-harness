# Adapted from noreval/nrk_quiz_qa


def prompt_nb(doc):
    prompt = "Spørsmål: {question}{choices}\n\nSvar:"
    choices = "".join(
        [
            f"\n({label}) {option}"
            for label, option in zip(doc["choices"]["label"], doc["choices"]["text"])
        ]
    )
    return prompt.format(question=doc["question"], choices=choices)


def prompt_nn(doc):
    prompt = "Spørsmål: {question}{choices}\n\nSvar:"
    choices = "".join(
        [
            f"\n({label}) {option}"
            for label, option in zip(doc["choices"]["label"], doc["choices"]["text"])
        ]
    )
    return prompt.format(question=doc["question"], choices=choices)
