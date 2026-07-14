from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Configurar el motor NLP en español
nlp_configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "es", "model_name": "es_core_news_md"}],
}
provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
nlp_engine = provider.create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["es"])
anonymizer = AnonymizerEngine()

mensajes = [
    "Hola, soy Marcela Fernández, mi DNI es 28.451.902. Quería saber por qué no me llegó el resumen de mi tarjeta terminada en 4532 a mi mail marcela.fernandez88@gmail.com",
    "Buenas, necesito cambiar mi número de teléfono registrado, ahora es 011-4567-8932. Mi cuenta es la 0170123-40000012345678 y vivo en Av. Rivadavia 4521, CABA.",
    "Hola, hace un mes pedí la preaprobación de un préstamo, me llamo Julián Ibarra, nací el 14/03/1985 y mi CUIT es 20-31245678-9, ¿tienen novedades?",
]

print("=" * 90)
for i, texto in enumerate(mensajes, 1):
    print(f"\n--- Mensaje {i} ---")
    print(f"ANTES : {texto}")

    resultados = analyzer.analyze(text=texto, language="es")

    anonimizado = anonymizer.anonymize(
        text=texto,
        analyzer_results=resultados,
        operators={"DEFAULT": OperatorConfig("replace", {"new_value": None})},
    )

    print(f"DESPUÉS: {anonimizado.text}")
    print("Entidades detectadas:")
    for r in resultados:
        fragmento = texto[r.start:r.end]
        print(f"  - {r.entity_type:20s} score={r.score:.2f}  →  '{fragmento}'")
print("\n" + "=" * 90)
