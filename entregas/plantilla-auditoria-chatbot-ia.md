# Auditoría de privacidad, seguridad y cumplimiento — Chatbot de atención al cliente

> Plantilla opcional. Puedes reorganizarla como quieras, siempre que el documento cubra las tres partes del ejercicio.

**Autora:** Tatiana Camelo

**Fecha:** _2026-07-14_

---

## Paso 0 · Sector elegido

**Sector:** _e-commerce_

_Empresa de e-commerce de ropas. El chatbot puede acceder a informaciones de tracking de pedidos, status, cancelamiento de pedidos, devoluciones. Tiene acceso a el pedido integralmente, datos de contacto del cliente, historico de comunicaciones._

---

## Parte 1 · Clasificación regulatoria

### 1.1 Categoría de riesgo según el EU AI Act

**Categoría:** _riesgo limitado_

**Justificación (condicionada por el sector):**
- Acceso a datos personales
- Interactuan con personas
- No está en infraestructura critica - context de e-commerce
- Sin identificación biométrica

### 1.2 Obligaciones y sanciones

| Obligación | Qué implica para nuestro chatbot |
|---|---|
| _Informar que es una IA_ | _Por comunicarse con personar, necesita comunicar con transparencia_ |
| _Acceso a datos personales_ | _Proteccione spor tener acceso a hsitorial, nombre, telefono, direccion_ |

**Sanciones máximas por incumplimiento (vigentes desde agosto de 2026):** _EU AI Act: Sanciones de hasta 35M€ o el 7% de la facturación anual._

### 1.3 Principios del GDPR aplicables

- **Base legal del tratamiento:** _Interes legitimo y concientimento claro._
- **Minimización de datos:** _Solo acceder a datos necesarios, aplicar anonimizacion_
- **Privacidad por diseño y por defecto:** _Control por OPT-IN, privacidad como MVP en el sistema_

---

## Parte 2 · Análisis de riesgos

### 2.1 Los 3 riesgos más críticos (OWASP Top 10 for LLM Applications 2025)

#### Riesgo 1 — _LLMXX: LLM accesible_

**Por qué es crítico para este chatbot:** _Utilizando LLMs de terceros, la responsabilidad es dividida entre el creador y el implementador._

**Escenario de ataque concreto:** _Error o mal uso del creador de la LLM, expondo las informaciones. Con modelos locales, esto nos eria un problem, ya que seria de 100% control del implementador_

#### Riesgo 2 — _LLMXX: Anonimización de PII_

**Por qué es crítico:** _Puede permitir acceso a datos eprsonales y estafas_

**Escenario de ataque concreto:** _Interceptacion de informacion con el envio para la LLM_

#### Riesgo 3 — _LLMXX: Retencion del provador_

**Por qué es crítico:** _Los termos del provador del modelo pueder cambiar_

**Escenario de ataque concreto:** _El sistema muy anidado con el provedor puede bloquear osistema en caso de falla o quebra de los atos legales_

### 2.2 Inventario de PII

| Dato (PII) | Origen | ¿Necesario para responder? |
|---|---|---|
| _Nombre_ | _Pedido_ | _Si_ |
| _Telefono_ | _Pedido_ | _No_ |
| _Dirección_ | _Pedido_ | _Si_ |

**Qué pasaría si estas conversaciones llegan sin filtrar al proveedor del LLM:** _Usuarios pueden tener sus datos expostos._

---

## Parte 3 · ¿Local, cloud o híbrido? (máx. media página)

| Dimensión | LLM comercial (cloud) | Modelo local (p. ej. Ollama + Qwen 2.5) |
|---|---|---|
| Coste | _x_ | __ |
| Privacidad | __ | _x_ |
| Cumplimiento | __ | _x_ |
| Calidad | _x_ | _x_ |

**Recomendación final (coherente con el sector del Paso 0):** _Modelo local, para menor riesgo de conformidade con los actos y sin posibilidad de exponer datos a terceros._

---
