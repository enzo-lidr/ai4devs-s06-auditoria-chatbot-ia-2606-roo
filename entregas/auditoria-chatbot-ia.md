# Auditoría de privacidad, seguridad y cumplimiento — Chatbot de atención al cliente

> Plantilla opcional. Puedes reorganizarla como quieras, siempre que el documento cubra las tres partes del ejercicio.

**Autor:** Javier VIllacis Castro 
**Fecha:** 2026-11-19

---

## Paso 0 · Sector elegido

**Sector:** _e-commerce | banca | salud | educación | RRHH_

_Breve descripción de la empresa ficticia y del chatbot (a qué datos accede, qué acciones puede ejecutar)._

Musiana Academy
- Accesos
  - Datos generales de los estudiantes: correo electrónico y nombre
  - Cursos en los que está enrolado
  - Estado de avance en la plataforma digital
  - Certificados y calificaciones
  - Estado de su membresía, pagos, cuotas
- Acciones
  - Guiar en el onboarding del estudiante en la plataforma digital
  - Asistencia para recuperación de contraseña
  - Consultas del estado de los cursos en los que está enrolado
  - Consulta de fechas e hitos importantes de los cursos

---

## Parte 1 · Clasificación regulatoria

### 1.1 Categoría de riesgo según el EU AI Act

**Categoría:** Riesgo limitado.

**Justificación:** Musiana Academy usa el chatbot para orientar a estudiantes, ayudarles a recuperar el acceso y responder consultas sobre sus cursos. Mostrar notas ya registradas es una consulta. La clasificación debe revisarse si el chatbot pasa a decidir admisiones, evaluar el aprendizaje, asignar niveles o vigilar exámenes. 

### 1.2 Obligaciones y sanciones

| Obligación | Qué implica para nuestro chatbot |
|---|---|
| Avisar que es una IA (art. 50.1 y 50.5) | Mostrar un aviso claro y accesible al iniciar el chat. Ejemplo: «Soy el asistente de IA de Musiana Academy». [info externa] |
| Marcar el texto generado (art. 50.2) | Si el chatbot genera respuestas, su proveedor debe marcarlas en un formato que el software pueda detectar. Para sistemas introducidos en el mercado antes del 2 de agosto de 2026, el plazo para este marcado es el 2 de diciembre de 2026. [info externa] |
| Promover el uso informado de la IA (art. 4) | Orientar al equipo de soporte sobre los límites del chatbot y cuándo derivar una consulta a una persona. [info externa] |

[EU AI Act, arts. 4, 50, 111.4 y 113](https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX%3A02024R1689-20260727)

**Sanciones máximas por incumplimiento:** Desde el 2 de agosto de 2026, infringir las obligaciones de transparencia aplicables del art. 50 puede costar hasta **15 millones de euros o el 3 % de la facturación mundial del ejercicio anterior**, lo que sea mayor. Dar información inexacta, incompleta o engañosa ante un requerimiento de la autoridad puede costar hasta **7,5 millones de euros o el 1 %**. En ambos casos se aplica el menor de los dos límites a las pymes y a las pequeñas empresas de mediana capitalización. [info externa] [EU AI Act, arts. 99.4–6 bis y 113](https://eur-lex.europa.eu/legal-content/ES/TXT/PDF/?uri=CELEX%3A02024R1689-20260727)

### 1.3 Principios del GDPR aplicables

- **Base legal del tratamiento:** Usar la ejecución del contrato cuando consultar los datos de matrícula o avance sea necesario para prestar el servicio educativo. Cada finalidad adicional, como entrenar el chatbot con conversaciones, requiere su propia evaluación y una base legal válida.
- **Minimización de datos:** Consultar solo lo necesario para cada respuesta. Para informar fechas generales basta el calendario. Para consultar el avance, limitar el acceso al curso solicitado y al estudiante autenticado.
- **Privacidad por diseño y por defecto:** Exigir inicio de sesión para consultas personales, limitar el acceso a los datos del propio estudiante y usar el flujo seguro de recuperación de la plataforma. Desactivar por defecto el uso de conversaciones para entrenamiento y limitar su conservación al tiempo necesario.

---

## Parte 2 · Análisis de riesgos

### 2.1 Los 3 riesgos más críticos (OWASP Top 10 for LLM Applications 2025)

#### Riesgo 1 — LLM01: Inyección de instrucciones

**Por qué es crítico para este chatbot:** Los estudiantes confían en las indicaciones del bot para entrar a la plataforma y recuperar el acceso.

**Escenario de ataque concreto:** Un usuario intenta que el bot presente una página ajena como el portal oficial de recuperación. Si el bot la recomienda como legítima, un estudiante que siga esa indicación podría entregar allí sus credenciales.

[OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

#### Riesgo 2 — LLM02: Divulgación de información sensible

**Por qué es crítico:** El chatbot puede consultar datos de matrícula, calificaciones y pagos vinculados a cada estudiante.

**Escenario de ataque concreto:** Un usuario pide las notas de otro estudiante. Si la plataforma entrega el expediente sin comprobar que pertenece a la cuenta autenticada, el bot podría revelar esas calificaciones.

#### Riesgo 3 — LLM06: Capacidad de acción excesiva

**Por qué es crítico:** La asistencia para recuperar el acceso requiere orientar al estudiante. Darle al bot permiso para modificar cuentas ampliaría el daño de una solicitud indebida.

**Escenario de ataque concreto:** Un usuario pide cambiar el correo de recuperación de una cuenta ajena. Si la integración permite cambios de cuenta sin verificar la identidad del titular, el bot podría cambiar el correo y dejar al estudiante sin control sobre la recuperación de su cuenta.

[OWASP LLM06:2025](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/?lang=us)

### 2.2 Inventario de PII

| Dato (PII) | Origen | ¿Necesario para responder? |
|---|---|---|
| Nombre | Perfil del estudiante | No. El saludo puede ser genérico. |
| Correo electrónico | Perfil del estudiante o texto del chat | Solo en el flujo oficial de recuperación, cuando se requiera identificar la cuenta. |
| Cursos en los que está inscrito | Matrícula en la plataforma | Sí, para consultas sobre su propia matrícula. |
| Avance en los cursos | Registro de actividad de la plataforma | Sí, para informar el avance del curso consultado. |
| Calificaciones y certificados | Expediente académico | Solo si el estudiante solicita ese dato y la consulta está autorizada. |
| Estado de membresía, pagos y cuotas | Registro administrativo y de pagos | Solo para una consulta autorizada sobre su propio estado. Basta el dato solicitado. |
| Datos personales que el usuario escriba en el chat | Mensajes del estudiante | Depende de la consulta. Excluir datos ajenos al trámite, contraseñas y códigos de recuperación. |

**Qué pasaría si estas conversaciones llegan sin filtrar al proveedor del LLM:** El proveedor podría recibir nombres, correos, notas y datos de pagos junto con el historial del chat. Según el contrato y la configuración, podría conservarlos en registros o reutilizarlos para entrenamiento. Si se procesan fuera de la UE y aplica el GDPR, también hay que verificar las garantías de la transferencia.

---

## Parte 3 · ¿Local, cloud o híbrido? (máx. media página)


| Dimensión | LLM comercial (cloud) | Modelo local (p. ej. Ollama + Qwen 2.5) |
|---|---|---|
| Coste | Menor inversión inicial. El gasto crece con el uso. | Requiere equipo, electricidad y mantenimiento. El módulo estima que un Mac Mini M4 se amortiza en 6–12 meses con 1.500–2.500 consultas mensuales. |
| Privacidad | El proveedor recibe los datos enviados. Revisar la retención y el uso para entrenamiento. | Las consultas se procesan en la infraestructura de la academia. Hay que proteger el acceso y los registros. |
| Cumplimiento | Si se envían datos personales, revisar el contrato y las garantías de cualquier transferencia internacional. | Facilita el control de los datos. Siguen aplicando la minimización y la transparencia. |
| Calidad | Puede rendir mejor en consultas complejas o ambiguas. | Puede cubrir preguntas frecuentes con información oficial. Conviene probar la precisión y la velocidad en español. |

**Recomendación final:** Empezar con un **modelo local** para orientar a los estudiantes. La plataforma muestra avance, notas y pagos tras verificar su identidad. El bot dirige la recuperación de acceso al flujo oficial. Consideraría un esquema híbrido solo si las pruebas muestran que la nube mejora las respuestas a consultas generales que puedan enviarse sin datos personales.
