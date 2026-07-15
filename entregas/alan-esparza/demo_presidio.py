# -*- coding: utf-8 -*-
"""
Bonus S6 - Anonimizacion de PII con Microsoft Presidio
Sector: Banca (NovaBank). Autor: Alan Esparza.

Detecta y anonimiza PII en 3 mensajes ficticios de clientes:
nombre, email, telefono y numero de operacion/pedido.
"""
from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# NLP en espanol (spaCy es_core_news_md) para detectar PERSON en castellano
nlp_config = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "es", "model_name": "es_core_news_md"}],
}
nlp_engine = NlpEngineProvider(nlp_configuration=nlp_config).create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["es"])

# Reconocedor personalizado: numero de operacion NovaBank (p.ej. OP-2026-000123)
op_pattern = Pattern(name="op_num", regex=r"\bOP-\d{4}-\d{6}\b", score=0.9)
op_recognizer = PatternRecognizer(
    supported_entity="NUM_OPERACION",
    patterns=[op_pattern],
    supported_language="es",
)
analyzer.registry.add_recognizer(op_recognizer)

anonymizer = AnonymizerEngine()

# Sustituye cada tipo de PII por un token con contexto (estilo Protecto/Skyflow)
operators = {
    "PERSON":        OperatorConfig("replace", {"new_value": "<NOMBRE>"}),
    "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "<EMAIL>"}),
    "PHONE_NUMBER":  OperatorConfig("replace", {"new_value": "<TELEFONO>"}),
    "NUM_OPERACION": OperatorConfig("replace", {"new_value": "<NUM_OPERACION>"}),
    "IBAN_CODE":     OperatorConfig("replace", {"new_value": "<IBAN>"}),
    "DEFAULT":       OperatorConfig("replace", {"new_value": "<PII>"}),
}

mensajes = [
    "Hola, soy Alan Esparza y no reconozco un cargo en mi cuenta. "
    "Mi email es alan.esparza@correo.com y mi telefono 612 345 678. "
    "El movimiento es el OP-2026-000123.",

    "Buenas, necesito el justificante de la operacion OP-2026-000777. "
    "Podeis enviarmelo a maria.lopez99@gmail.com? Soy Maria Lopez, "
    "podeis llamarme al +34 699 112 233.",

    "Quiero disputar un reembolso. Me llamo Carlos Ruiz Fernandez, "
    "telefono 611223344, correo c.ruiz@empresa.es, "
    "referencia OP-2026-000555.",
]

print("=" * 70)
print("DEMO PRESIDIO - Anonimizacion de PII (banca / NovaBank)")
print("=" * 70)

for i, texto in enumerate(mensajes, 1):
    resultados = analyzer.analyze(text=texto, language="es")
    anonimizado = anonymizer.anonymize(
        text=texto, analyzer_results=resultados, operators=operators
    )
    print(f"\n--- MENSAJE {i} ---")
    print("ANTES:")
    print(f"  {texto}")
    print("DETECTADO:")
    for r in sorted(resultados, key=lambda x: x.start):
        frag = texto[r.start:r.end]
        print(f"  - {r.entity_type:14s} score={r.score:.2f}  ->  '{frag}'")
    print("DESPUES:")
    print(f"  {anonimizado.text}")

print("\n" + "=" * 70)
