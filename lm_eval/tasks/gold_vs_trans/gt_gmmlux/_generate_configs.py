import argparse
import os

from pathlib import Path

import yaml

LANGS = [
    "DA",
    "ET",
    "LT",
    # "NB",
    "SV",
]


PROMPT_WORDS = {
    "DA": ("Spørgsmål", "Svarmuligheder", "Svar"),
    "ET": ("Küsimus", "Vastusevariandid", "Vastus"),
    "LT": ("Klausimas", "Pasirinkimai", "Atsakymas"),
    # "NB": ("Spørsmål", "Svaralternativer", "Svar"),
    "SV": ("Fråga", "Svarsalternativ", "Svar"),
}

CHOICES = {
    "DA": ("A", "B", "C", "D"),
    "ET": ("A", "B", "C", "D"),
    "LT": ("A", "B", "C", "D"),
    # "NB": ("A", "B", "C", "D"),
    "SV": ("A", "B", "C", "D"),
}

SUBJECTS = {
    "abstract_algebra": "stem",
    "anatomy": "stem",
    "astronomy": "stem",
    "business_ethics": "other",
    "clinical_knowledge": "other",
    "college_biology": "stem",
    "college_chemistry": "stem",
    "college_computer_science": "stem",
    "college_mathematics": "stem",
    "college_medicine": "other",
    "college_physics": "stem",
    "computer_security": "stem",
    "conceptual_physics": "stem",
    "econometrics": "social_sciences",
    "electrical_engineering": "stem",
    "elementary_mathematics": "stem",
    "formal_logic": "humanities",
    "global_facts": "other",
    "high_school_biology": "stem",
    "high_school_chemistry": "stem",
    "high_school_computer_science": "stem",
    "high_school_european_history": "humanities",
    "high_school_geography": "social_sciences",
    "high_school_government_and_politics": "social_sciences",
    "high_school_macroeconomics": "social_sciences",
    "high_school_mathematics": "stem",
    "high_school_microeconomics": "social_sciences",
    "high_school_physics": "stem",
    "high_school_psychology": "social_sciences",
    "high_school_statistics": "stem",
    "high_school_us_history": "humanities",
    "high_school_world_history": "humanities",
    "human_aging": "other",
    "human_sexuality": "social_sciences",
    "international_law": "humanities",
    "jurisprudence": "humanities",
    "logical_fallacies": "humanities",
    "machine_learning": "stem",
    "management": "other",
    "marketing": "other",
    "medical_genetics": "other",
    "miscellaneous": "other",
    "moral_disputes": "humanities",
    "moral_scenarios": "humanities",
    "nutrition": "other",
    "philosophy": "humanities",
    "prehistory": "humanities",
    "professional_accounting": "other",
    "professional_law": "humanities",
    "professional_medicine": "other",
    "professional_psychology": "social_sciences",
    "public_relations": "social_sciences",
    "security_studies": "social_sciences",
    "sociology": "social_sciences",
    "us_foreign_policy": "social_sciences",
    "virology": "other",
    "world_religions": "humanities",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-dir", type=Path, default=Path(__file__).parent)
    parser.add_argument("--base-yaml", default="_default_gt_gmmlux_template_yaml")
    parser.add_argument("--prefix", default="gt_gmmlux")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    base_yaml_name = os.path.split(args.base_yaml)[-1]

    for lang in LANGS:
        _, _, answer = PROMPT_WORDS[lang]
        a, b, c, d = CHOICES[lang]

        for subj, cat in SUBJECTS.items():
            yaml_dict = {
                "include": base_yaml_name,
                "dataset_name": f"{subj}_{lang}",
                "task": f"{args.prefix}_{lang.lower()}-{subj}",
                "tag": f"{args.prefix}_{cat}",
                "doc_to_choice": f"['{a}', '{b}', '{c}', '{d}']",
                "doc_to_text": f"{{{{question.strip()}}}}\n{a}. {{{{choices[0]}}}}\n{b}. {{{{choices[1]}}}}\n{c}. {{{{choices[2]}}}}\n{d}. {{{{choices[3]}}}}\n{answer}:",
            }

            file_save_path = args.save_dir / f"{args.prefix}_{lang.lower()}-{subj}.yaml"

            with open(file_save_path, "w", encoding="utf-8") as yaml_file:
                yaml.dump(
                    yaml_dict,
                    yaml_file,
                    allow_unicode=True,
                    default_style='"',
                    sort_keys=False,
                )
