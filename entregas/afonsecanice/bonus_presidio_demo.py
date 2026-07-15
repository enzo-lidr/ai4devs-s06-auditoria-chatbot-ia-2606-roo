# -*- coding: utf-8 -*-
"""
Bonus 2 — Anonimizacion en accion con Microsoft Presidio
Colegio Carlos Fonseca · Auditoria de privacidad, seguridad y cumplimiento
Autor: Ariel Fonseca (afonsecanice)

Este script acompana la seccion "Bonus 2" de auditoria-chatbot-ia.md.
Procesa 5 mensajes ficticios de padres en DOS pasadas:

  PASADA A (de fabrica): reconocedores por defecto de Presidio. Detecta PII
    generica (nombre, email, telefono, ubicacion) pero SE LE ESCAPAN los
    identificadores mexicanos/escolares criticos: CURP, RFC y matricula.

  PASADA B (a medida): se anaden PatternRecognizer propios para CURP, RFC y
    matricula. Ahora SI se detectan y anonimizan -> demuestra que el hueco de
    la Pasada A se cierra con reconocedores de dominio.

--- Como ejecutarlo ---
1. pip install presidio-analyzer presidio-anonymizer
2. python -m spacy download es_core_news_md
3. python bonus_presidio_demo.py
"""

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

NLP_CONFIG = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "es", "model_name": "es_core_news_md"}],
}

provider = NlpEngineProvider(nlp_configuration=NLP_CONFIG)
nlp_engine = provider.create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["es"])
anonymizer = AnonymizerEngine()

MENSAJES = [
    "Hola, soy Maria Fernanda Lopez Ruiz, mama de un alumno de tercero de primaria, su CURP es LORM150304MDFXXX01 y mi correo es maria.lopez84@gmail.com, quiero saber si ya quedo aceptado para el ciclo escolar.",
    "Buenas, soy Carlos Alberto Mendez, necesito la factura de la colegiatura de mi hijo del mes de junio para deducirla de impuestos, mi RFC es MECA800521XXX.",
    "Hola equipo, soy Ana Sofia Torres, mama de la matricula EXP-2026-00871, quiero ver las calificaciones del segundo bimestre de mi hija.",
    "Buenos dias, soy Jorge Alberto Ramirez Soto, quiero inscribir a mi hija a primero; vivimos en Calle Hidalgo 123, Jiquilpan, Michoacan (para validar la zona), su CURP es RALE120815MMNXYZ08 y mi numero es 33-1234-5678.",
    "Hola, ya pague la colegiatura de agosto del alumno con matricula EXP-2025-01199; necesito la factura, mi RFC es GOPP850612AB3, enviela a mi correo la.rodriguez88@gmail.com.",
]


def correr(titulo):
    print(f"\n############## {titulo} ##############")
    for i, texto in enumerate(MENSAJES, 1):
        hallazgos = analyzer.analyze(text=texto, language="es")
        anonimizado = anonymizer.anonymize(text=texto, analyzer_results=hallazgos)
        print(f"=== Mensaje {i} ===")
        print("ANTES:", texto)
        for h in hallazgos:
            print(f"  - {h.entity_type} [{h.start}:{h.end}] score={h.score:.2f} -> '{texto[h.start:h.end]}'")
        print("DESPUES:", anonimizado.text)


# ---------- PASADA A: reconocedores de fabrica ----------
correr("PASADA A — Presidio de fabrica (CURP/RFC/matricula SE ESCAPAN)")

# ---------- PASADA B: se anaden reconocedores a medida ----------
# CURP (18): 4 letras + 6 digitos (fecha) + H/M (sexo) + 5 letras + 1 alfanumerico + 1 digito
curp = PatternRecognizer(
    supported_entity="CURP",
    supported_language="es",
    patterns=[Pattern(name="curp", regex=r"\b[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d\b", score=0.9)],
    context=["curp"],
)
# RFC persona fisica (13) o moral (12): 3-4 letras + 6 digitos (fecha) + 3 de homoclave
rfc = PatternRecognizer(
    supported_entity="RFC",
    supported_language="es",
    patterns=[Pattern(name="rfc", regex=r"\b[A-Z]{3,4}\d{6}[A-Z0-9]{3}\b", score=0.85)],
    context=["rfc", "factura"],
)
# Matricula/expediente del colegio: formato EXP-AAAA-NNNNN
matricula = PatternRecognizer(
    supported_entity="MATRICULA",
    supported_language="es",
    patterns=[Pattern(name="matricula", regex=r"\bEXP-\d{4}-\d{5}\b", score=0.9)],
    context=["matricula", "expediente"],
)

analyzer.registry.add_recognizer(curp)
analyzer.registry.add_recognizer(rfc)
analyzer.registry.add_recognizer(matricula)

correr("PASADA B — con reconocedores a medida (CURP/RFC/matricula DETECTADOS)")
