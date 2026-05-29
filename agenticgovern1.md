

# Manual de buenas prácticas para desarrollo paralelo con agentes en Antigravity y herramientas afines

Este informe sintetiza documentación oficial reciente de Google sobre Antigravity, Gemini API, Agents CLI, ADK y A2A, junto con documentación oficial de Codex y artículos técnicos de OpenAI sobre subagentes, compaction, prompt caching y orquestación. La conclusión transversal es que la productividad no escala por “tener más agentes”, sino por separar bien contexto estable, flujos reutilizables, ownership técnico, mecanismos de handoff y límites de ejecución. 

## Criterio rector

La idea más importante que aparece de forma convergente en Google y OpenAI es que un sistema agentic serio debe parecerse más a una arquitectura de microservicios que a un “superprompt” monolítico. Google recomienda romper el monolito en agentes especializados con prompts acotados y guardrails deterministas; Antigravity se diseñó precisamente para lanzar, orquestar y observar múltiples agentes trabajando de forma asíncrona en workspaces distintos; y Codex usa subagentes para sacar trabajo ruidoso del hilo principal y evitar la “context pollution” y la “context rot”. 

También convergen en que no todo debe vivir en el mismo plano. Google diferencia entre **Rules**, que aportan contexto persistente y reutilizable a nivel de prompt, y **Workflows**, que guían una secuencia de pasos a nivel de trayectoria; ambos pueden convivir con **Skills**, que son paquetes reutilizables de conocimiento e instrucciones. En Codex, la división equivalente es **AGENTS.md** para guía durable del repositorio, **skills** para flujos reutilizables, **MCP** para acceso a herramientas y sistemas, y **subagents** para delegación. 

La consecuencia práctica es clara: empieza con pocos roles, muy bien definidos, y aumenta después. El propio codelab oficial de Google para Antigravity usa una composición de cuatro personas artificiales muy concreta —PM, Engineer, QA y DevOps— para evitar que “una sola IA” tenga que ser arquitecto, implementador, tester y operador a la vez. En paralelo, OpenAI explica que, cuando el trabajo con agentes creció, el problema dejó de ser la capacidad del modelo y pasó a ser el coste de atención humana y el cambio de contexto; en sus pruebas, una persona podía gestionar cómodamente solo unas pocas sesiones interactivas a la vez antes de perder productividad. 

Mi lectura operativa es que tu intuición es correcta: **la unidad de escala no es “más prompts”, sino “más responsabilidad bien acotada”**. El mejor primer salto no es desplegar diez agentes, sino definir cuatro o cinco con ownership real, contratos claros y un supervisor que gobierne prioridades, dependencias y definición de terminado. Ese patrón está alineado con Antigravity Manager, con las recomendaciones de multi‑agent de Google y con los subagentes explícitos de Codex. 

## Arquitectura documental del proyecto

Aquí es donde hoy existe más fragmentación entre herramientas. En Google, **Agents CLI** pide que lo primero sea un DESIGN\_SPEC.md que actúe como *source of truth* con overview, casos de uso, herramientas, restricciones y criterios de éxito. El codelab oficial de Antigravity, en cambio, enseña a centralizar el equipo en .agents/agents.md, las habilidades en .agents/skills/ y la orquestación en archivos de workflow invocables por slash commands. Además, los proyectos generados por Agents CLI incluyen un GEMINI.md como archivo de guidance para coding agents. En Codex, la pieza central es AGENTS.md, con descubrimiento por capas globales y por directorio, y precedencia de los ficheros más cercanos al directorio de trabajo. 

Eso significa que, si quieres trabajar en **Antigravity \+ Codex \+ similares**, conviene tratar la documentación como una **arquitectura de doble capa**: una capa canónica y una capa de adaptación por herramienta. La capa canónica debe responder a tres preguntas: qué estoy construyendo, cómo se trabaja aquí y quién es dueño de qué. La capa de adaptación debe traducir ese contenido a los ficheros que cada agente consume mejor.

Una estructura base razonable sería esta:

text  
Copiar  
repo/  
├── DESIGN\_SPEC.md  
├── AGENTS.md  
├── OWNERSHIP.md  
├── ADR/  
│   └── 0001-...  
├── CONTRACTS/  
│   ├── api/  
│   ├── events/  
│   └── ui/  
├── .agents/  
│   ├── agents.md  
│   ├── skills/  
│   │   ├── implement\_feature.md  
│   │   ├── propose\_interface\_change.md  
│   │   ├── lint\_test\_fix.md  
│   │   └── browser\_verify.md  
│   └── workflows/  
│       ├── start\_feature.md  
│       └── request\_contract\_change.md  
├── tests/  
│   ├── unit/  
│   ├── integration/  
│   └── eval/  
│       ├── eval\_config.json  
│       └── evalsets/  
├── .codex/  
│   └── config.toml  
└── GEMINI.md

La lógica detrás de esa estructura sí está muy bien soportada por la documentación oficial. DESIGN\_SPEC.md es la verdad del producto y del alcance; AGENTS.md debe ser pequeño y durable, con comandos de build/test, expectativas de revisión, convenciones del repo e instrucciones locales por directorio; .agents/agents.md y .agents/skills/ sirven muy bien para Antigravity; y Google insiste en incorporar evaluaciones tempranas y repetir un bucle de *eval-fix* varias veces antes de dar un agente por estable. Codex, además, recomienda actualizar AGENTS.md precisamente cuando detectas errores repetidos, demasiado “lecturismo” o feedback recurrente en PRs. 

Hay dos advertencias importantes. La primera: no conviertas AGENTS.md en un vertedero de normas. Codex lo concatena desde la raíz hasta el directorio actual y deja de añadir ficheros cuando alcanza su límite configurado de tamaño combinado, que por defecto es 32 KiB; además, su propia guía insiste en mantenerlo pequeño. La segunda: tampoco conviertas los workflows en una miniplataforma de orquestación sin fin; en Antigravity los workflows son markdown secuenciales y cada archivo tiene un límite de 12.000 caracteres, así que deben ser “wrappers” finos sobre reglas y skills, no manuales enciclopédicos. 

Mi recomendación concreta es esta: DESIGN\_SPEC.md **define el “qué”**, AGENTS.md **define el “cómo permanente”**, OWNERSHIP.md **y** CONTRACTS/ **definen el “quién toca qué”**, y **skills/workflows** definen el “cómo se ejecuta un tipo de trabajo repetible”. Esa separación evita mezclar estrategia, política, ownership y procedimiento en un único prompt gigante. 

## Organización del equipo de agentes

Para un proyecto de software con varios desarrollos en paralelo, el patrón más sano es un **equipo pequeño de especialistas** alrededor de un coordinador. Google, en su codelab oficial de Antigravity, demuestra que centralizar personas artificiales reduce la confusión del modelo y mejora el foco: PM para especificación, Engineer para generación de código, QA para detección y corrección de fallos y DevOps para entorno de ejecución. Yo añadiría un quinto rol que en la práctica se vuelve esencial en proyectos reales: **API Steward o Interface Owner**, responsable de contratos, versionado y validación de cambios de interfaz entre dominios. Esa ampliación encaja con la lógica de ownership y con el A2A Agent Card, que existe precisamente para publicar capacidades y endpoints de un agente. 

En términos de paralelismo, no todos los agentes deben tener el mismo poder de escritura. La documentación de Codex es explícita: los subagentes son especialmente útiles para trabajo **read-heavy** —exploración, tests, triage, análisis de logs, resúmenes— y hay que ser más cuidadoso con flujos **write-heavy**, porque varios agentes editando a la vez incrementan conflictos y coste de coordinación. Al mismo tiempo, la app de Codex incorpora worktrees para que varios agentes trabajen sobre el mismo repo sin tocar el estado local ni pisarse, y Antigravity puede operar múltiples workspaces simultáneamente desde el Manager. 

De ahí sale una política sencilla y eficaz: **un solo agente escritor por bounded context**, y tantos agentes lectores o analizadores paralelos como te compense. Por ejemplo, el frontend puede tener un owner escritor; en paralelo, puedes lanzar un subagente de test gap analysis, otro de accesibilidad y otro de verificación visual. El backend de pagos puede tener otro owner escritor, mientras un agente de seguridad y otro de contratos hacen exploración paralela. Esa es, de hecho, la lógica que Google muestra en incident response y distributed code migration con especialistas coordinados mediante A2A. 

Para organizar conversaciones, la mejor práctica emergente es **una conversación o hilo por trabajo real**, no por persona humana. Antigravity propone el Manager Surface para despachar y seguir agentes asíncronos por workspace; OpenAI, con Symphony, empuja aún más esa idea y convierte el issue tracker en un *control plane* en el que cada ticket abierto obtiene su workspace y su agente dedicado; y la app de Codex organiza agentes por *threads* de proyecto. Eso reduce muchísimo el caos frente a “un chat largo con todo mezclado”. 

También conviene rutear el trabajo por **modo de ejecución**. En Antigravity, el modo **Planning** se recomienda para deep research, tareas complejas o trabajo colaborativo y genera task groups y Artifacts; el modo **Fast** está pensado para tareas simples y localizadas, como renombrar variables o lanzar unos pocos comandos bash. Esa distinción es una pista excelente para diseñar roles: orquestador, arquitecto e interface owner deben vivir casi siempre en planificación; agentes de triage, búsqueda, clasificación o cambios pequeños pueden trabajar en modo rápido. 

## Rules, skills, workflows y enforcement

Aquí hay una jerarquía útil que merece la pena fijar desde el principio. **Rules** sirven para contexto persistente y reutilizable a nivel de prompt; **Workflows** para secuencias reproducibles; **Skills** para instrucciones especializadas que el agente solo carga cuando son relevantes; y **permissions / approval / sandbox** para lo verdaderamente coercitivo. Google describe Rules y Workflows exactamente así en Antigravity, y Codex documenta que AGENTS, skills, MCP y subagents son piezas complementarias; además, recomienda emparejar la guía textual con hooks, linters y type checkers para que las reglas no dependan solo de “obediencia del modelo”. 

El **conjunto mínimo de reglas** que yo implantaría en cualquier repo agentic es el siguiente, expresado de forma normativa y corta. **Regla de terminado**: ningún trabajo se considera completo sin los comandos concretos de build, lint, test y, si aplica, verificación visual. **Regla de ownership**: cada agente tiene paths y contratos de su dominio; fuera de ahí, solo puede proponer cambios. **Regla de interfaces**: un cambio en API, evento o contrato UI exige un artefacto de solicitud y aprobación del owner de contrato. **Regla de dependencias**: añadir dependencias nuevas requiere aprobación o workflow específico. **Regla de evidencia**: el agente debe entregar siempre los ficheros tocados, comandos ejecutados y resultado de validaciones. Esto está directamente alineado con lo que Codex recomienda poner en AGENTS.md y con el sistema de permisos de Antigravity. 

El **catálogo mínimo de actions o skills** tampoco tiene que ser grande. Con muy poco ya obtienes orden: una skill de implement\_feature para implementar dentro de un scope propio; una de propose\_interface\_change para generar una solicitud de cambio de contrato; una de lint\_test\_fix para el bucle de calidad; una de browser\_verify para verificación con navegador o Artifacts; una de generate\_adr para decisiones de arquitectura; una de review\_pr para revisión estructurada por categorías; y una de update\_guidance para actualizar AGENTS o reglas cuando aparece un error repetido. Google enseña precisamente a separar capacidades en archivos .md dentro de skills y a encadenarlas con workflows; Codex usa la misma lógica con SKILL.md y progressive disclosure. 

La parte clave es el **enforcement real**. Antigravity tiene un sistema unificado de permisos con tres listas: **Allow**, **Deny** y **Ask**. Codex, cuando se orquesta por MCP o configuración local, expone políticas equivalentes: approval-policy para comandos de shell y modos de sandbox como read-only, workspace-write o danger-full-access. Eso permite trasladar tus políticas de gobierno a decisiones concretas de ejecución: lectura y análisis en Allow; edición del workspace en Ask o workspace-write; acciones irreversibles, de producción o fuera del scope del repo en Deny salvo workflow explícito. 

Un detalle importante para FinOps y mantenibilidad: las skills y las reglas deben ser **cortas y discriminativas**, no largas y generales. En Codex, la lista inicial de skills se limita para no invadir el contexto —aproximadamente el 2% de la ventana o 8.000 caracteres cuando esa ventana no se conoce—, y solo se carga el SKILL.md completo cuando el agente decide usarla. Antigravity sigue una filosofía similar: al iniciar una conversación, el agente ve la lista de skills disponibles con nombre y descripción y solo lee la instrucción completa cuando esa skill parece relevante. Esa convergencia es una señal clarísima de buena práctica: **poco contexto upfront, más contexto on demand**. 

## FinOps de tokens y elección de modelos

La primera regla de FinOps es casi aburrida, pero imprescindible: **deja de estimar y empieza a medir**. Gemini permite contar tokens antes de enviar la petición con count\_tokens, y después te da en usage\_metadata el desglose de prompt\_token\_count, candidates\_token\_count, thoughts\_token\_count y cached\_content\_token\_count. En Vertex AI, además, puedes añadir **labels** a las llamadas generateContent para desglosar los cargos facturados por caso de uso, equipo o flujo. Si no tienes ese observability layer, no estás haciendo FinOps: solo estás adivinando. 

La segunda gran palanca es la **reutilización de prefijos**. Google documenta el *explicit context caching* de Gemini: puedes cachear contenido común y reutilizarlo después con menor coste que reenviarlo entero; además, recomienda poner los contenidos grandes y comunes al principio del prompt y enviar solicitudes con prefijos similares en un intervalo corto. OpenAI, por su parte, activa Prompt Caching automáticamente en prompts suficientemente largos y explica que los cache hits solo ocurren con coincidencias exactas del prefijo, por lo que conviene colocar contenido estático al principio y contenido variable al final. En castellano llano: **tu prompt base, tus instrucciones estables, tus tools y tus ejemplos deben ser muy repetibles**. 

La tercera palanca es la **higiene del contexto**. Google recomienda usar instrucciones claras y específicas, priorizar las restricciones críticas en system instructions o al principio del prompt, estructurar el prompt con etiquetas o markdown, y para contextos largos poner el bloque de contexto antes de la pregunta concreta. También recomienda few-shot examples, pero advierte que demasiados ejemplos pueden hacer overfit. Para prompts complejos, propone partir instrucciones en componentes, encadenar prompts secuenciales o agregar respuestas de tareas paralelas. OpenAI llega a una conclusión parecida desde otro ángulo: no arrastres sin más todas las instrucciones heredadas de stacks antiguos, porque la sobre‑especificación añade ruido; empieza con el prompt más pequeño que pase tus evals y estructura salidas compactas y explícitas. 

Eso tiene una traducción muy operativa a nivel de repositorio. AGENTS.md **debe contener solo reglas durables**; si empieza a crecer, muévelo a skills o a guías por directorio. **Los documentos largos no deben copiarse en cada prompt**; si usas Antigravity, aprovéchate de **Knowledge Items**, cuyas síntesis están disponibles para el agente y cuyos artefactos se estudian automáticamente cuando son relevantes. Si tu patrón es documental o de memoria organizativa, Google ya ofrece plantillas agentic\_rag y casos de uso de *organizational memory* precisamente para evitar que cada conversación vuelva a “releer el mundo” desde cero. 

La cuarta palanca es **compactar sesiones largas y externalizar memoria**. OpenAI explica que, para no explotar la ventana de contexto en bucles largos, Codex compacta automáticamente la conversación a partir de cierto umbral y sustituye el historial por una representación más pequeña que preserva la comprensión latente del modelo. Antigravity resuelve parte del mismo problema llevando información significativa a Artifacts y a Knowledge Items, en vez de obligarte a monitorizar logs crudos o a mantener toda la historia inline. Si un hilo ya no necesita detalle fino, compacta; si el conocimiento debe sobrevivir entre tareas, promuévelo a memoria duradera. 

La quinta palanca es **escoger el modelo correcto para el trabajo correcto**. En Google, **Gemini 3.1 Pro** se posiciona para tareas complejas que requieren amplio conocimiento del mundo y razonamiento avanzado, y el nivel de thinking **HIGH** se recomienda explícitamente para *multi-step planning*, *verified code generation* o *advanced function calling*; **LOW** es ideal para tareas simples y de alto throughput, y **MEDIUM** para complejidad moderada. **Gemini 3 Flash** y **2.5 Flash** se describen como opciones de gran relación precio-rendimiento para casos agentic, gran volumen y baja latencia, mientras que **Flash-Lite** está pensado para extracción simple, tareas agentic de gran volumen y restricciones fuertes de presupuesto y velocidad. En Codex, la recomendación análoga es usar **gpt-5.5** o **gpt-5.4** para el trabajo complejo y **gpt-5.4-mini** para subagentes o tareas ligeras y más baratas. 

Con eso, una definición práctica de **caso complejo** sería esta: una tarea es compleja cuando combina al menos dos de estos rasgos: ambigüedad alta, planificación en varias etapas, uso profundo de herramientas, necesidad de verificación independiente, impacto transversal sobre varios bounded contexts, o alto blast radius si se equivoca. Es exactamente el tipo de trabajo para el que Google recomienda Planning mode y thinking HIGH, y para el que OpenAI reserva sus modelos principales. En cambio, clasificación, búsqueda, resumen, exploración de ficheros, triage de logs, extracción de datos y primeros pases de review suelen encajar mejor en Flash o mini. 

Si tuviera que convertir esto en una política simple de routing, sería así: **orquestador, arquitecto, interface owner y revisor final** con modelo Pro o flagship; **scanners, triagers, test agents, summarizers, document retrievers y verificadores de rutina** con Flash o mini; **Flash-Lite** solo para extracción, clasificación o validación ultrabarata. Esa es la forma más consistente de bajar coste sin degradar la calidad en los puntos donde más importa. 

## Comunicación asíncrona y ausencia de colusión

Para evitar “colusión” entre agentes —es decir, cambios cruzados fuera de ownership, decisiones implícitas no auditables y handoffs opacos— conviene separar con claridad **agente‑a‑sistema** de **agente‑a‑agente**. Google lo explica muy bien en su guía de protocolos: **MCP** sirve para conectar un agente con herramientas, APIs y datos; **A2A** sirve para que agentes distintos se descubran, se comuniquen y coordinen. En A2A, cada agente publica un **Agent Card** en una URL conocida que describe nombre, capacidades y endpoint. Aunque no montes A2A completo dentro de tu repo, esa idea te da un patrón muy potente: cada agente de tu equipo debería tener una ficha pública de ownership y capacidades. 

La especificación A2A aporta otra idea excelente para diseño interno: **Messages y Artifacts cumplen funciones diferentes**. Los mensajes se usan para iniciar tareas, pedir aclaraciones, informar de estado o aportar nuevas instrucciones; los resultados no deberían entregarse como mensajes, sino como **Artifacts** asociados a una tarea. Antigravity usa exactamente esa lógica: el agente comunica progreso con Artifacts, y tú puedes comentar sobre ellos sin romper el flujo. Para un equipo de agentes, esta separación es oro puro: los mensajes sirven para coordinar, los artefactos para transferir producto de trabajo verificable. 

Mi recomendación es implementar un **protocolo de handoff muy explícito**. No hace falta que sea sofisticado al principio; basta con que todas las solicitudes de cambio entre dominios tengan un formato estable y auditable.

md  
Copiar  
\# CHANGE\_REQUEST

requester: frontend-agent  
owner: api-steward  
task\_id: story-123  
requested\_change: add payment\_method\_type to CheckoutResponse  
why: frontend cannot render payment badges without discriminated type  
impact\_scope:  
  \- CONTRACTS/api/checkout.yaml  
  \- app/payments/\*  
required\_artifacts:  
  \- contract\_diff.md  
  \- migration\_notes.md  
  \- updated\_examples.json  
status: proposed

Con una disciplina así, el frontend no “entra” a tocar la API de pagos por su cuenta. Pide un cambio; el owner del contrato responde con un artifact de contrato, otro de migración y, si procede, un ticket dependiente para los consumidores. Ese patrón encaja con A2A, con Symphony como control plane basado en tickets y con los ejemplos de Google para coordinación de especialistas mediante A2A. 

También es importante que el paralelismo no se convierta en conflicto de escritura. Codex ya empuja a usar worktrees y threads separados; sus subagent workflows son explícitos, no automáticos, y deben lanzarse cuando el usuario lo pida, precisamente porque cada subagente consume su propio trabajo de modelo y herramientas. Antigravity, por su lado, distribuye conversaciones por workspace y está diseñado para observar trabajo asíncrono entre ellos. Así que tu intuición de “quizá no automático, pero sí bajo pedido” coincide bastante con la práctica oficial recomendada: **delegación explícita, bounded work y consolidación posterior**. 

En proyectos más maduros, merece mucho la pena elevar el nivel y usar un **control plane externo**. OpenAI describe Symphony como un orquestador donde cada issue abierto obtiene un agente y un workspace, con reinicio si se queda atascado y con dependencias entre tareas. Google, desde otra familia de herramientas, propone adk\_a2a precisamente para sistemas distribuidos multiagente, y en sus ejemplos de incident response o code migration cada especialista corre como servicio separado y un coordinador orquesta la ejecución. La lección es común: cuando el trabajo paralelo crece, deja de pensar en “chat sessions” y piensa en **tickets, estados y dependencias**. 

## Conclusiones y recursos prioritarios

La mejor síntesis que puedo darte es esta: **un buen sistema de desarrollo paralelo con agentes no es una colección de modelos, sino una arquitectura de trabajo**. Google y OpenAI coinciden en que la calidad aparece cuando separas especificación, ejecución, evaluación, ownership y handoff; usas agentes especializados en paralelo para trabajo acotado; y transfieres el control desde el prompt improvisado hacia artefactos, skills, workflows, permisos y evaluaciones. 

Si tuviera que implantar el **stack mínimo viable** para un equipo como el que describes, sería este. Un DESIGN\_SPEC.md como verdad del producto; un AGENTS.md pequeño para normas permanentes; un .agents/agents.md para personas y routing en Antigravity; un catálogo corto de **skills** centradas en implementación, contrato, test y verificación; **permissions** y **sandbox** restrictivos por defecto; un **OWNERSHIP registry** por bounded context; **evals** desde el principio; y un control plane basado en tickets o workspaces, no en un único chat largo. Ese patrón está mucho más alineado con la documentación oficial que intentar que un único agente recuerde todo, decida todo y edite todo. 

En cuanto a recursos prioritarios, yo daría prioridad a cuatro bloques. Para **Google Antigravity**, el post de lanzamiento, la documentación de Agent Manager, Artifacts, Rules/Workflows y el codelab de .agents/agents.md y skills.md son la base. Para **Google Agent Platform**, la Development Guide de Agents CLI, las plantillas adk, adk\_a2a y agentic\_rag, y la guía de protocolos MCP/A2A son lo más estructurante. Para **Gemini FinOps**, las guías de prompt strategies, token counting, context caching, media resolution y prompt optimizer son las piezas clave. Y para **Codex**, las páginas de AGENTS.md, skills, subagents, models, prompt caching, compaction, harness engineering y Symphony son probablemente el mejor complemento para consolidar una disciplina de paralelismo y supervisión seria. 

La frase final, si quieres dejarla como principio de diseño, sería esta: **más agentes no significa más velocidad; más ownership, más compacidad de contexto, mejores handoffs y mejores guardrails sí**.   
