#!/usr/bin/env python3
"""Demo Presidio para la auditoría del chatbot LMS JUMP Math."""

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

MESSAGES = [
    (
        "Mensaje 1 (padre)",
        "Soy María López, email maria.lopez@gmail.com, mi hijo Pablo (3º Primaria, "
        "colegio San José) sacó un 4 en la prueba de fracciones del 12/06. ¿Puede repetirla?",
    ),
    (
        "Mensaje 2 (profesor)",
        "Profesor Juan García, tel. +34 612 345 678, no puedo corregir la actividad "
        "ID-78432 del alumno Ana Ruiz.",
    ),
    (
        "Mensaje 3 (admin)",
        "Admin colegio Maple Leaf Toronto, contacto admin@mapleleaf.edu, necesito "
        "resetear la cuenta del alumno ID-STU-99102.",
    ),
]


def main() -> None:
    nlp_config = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "es", "model_name": "es_core_news_md"}],
    }
    nlp_engine = NlpEngineProvider(nlp_configuration=nlp_config).create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["es"])
    anonymizer = AnonymizerEngine()

    operators = {
        "DEFAULT": OperatorConfig("replace", {"new_value": "<PII>"}),
        "PERSON": OperatorConfig("replace", {"new_value": "<NOMBRE>"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "<TELEFONO>"}),
    }

    for label, text in MESSAGES:
        print("=" * 72)
        print(label)
        print("-" * 72)
        print("ANTES:")
        print(text)
        print()

        results = analyzer.analyze(text=text, language="es")
        anonymized = anonymizer.anonymize(
            text=text,
            analyzer_results=results,
            operators=operators,
        )

        print("DESPUÉS:")
        print(anonymized.text)
        print()
        print("ENTIDADES DETECTADAS:")
        if not results:
            print("  (ninguna)")
        for r in results:
            snippet = text[r.start : r.end]
            print(f"  - {r.entity_type}: '{snippet}' (score={r.score:.2f})")
        print()


if __name__ == "__main__":
    main()
