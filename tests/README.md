# PSI Cloud SDK 🚀

El SDK oficial en Python para conectarse al motor de **Suficiencia Informativa (PSI)**.

PSI es un motor propietario que evalúa si un sistema puede resolverse de forma determinística antes de ejecutarse.
Está diseñado para detectar **insuficiencia estructural de información** en modelos complejos.

> ⚠️ Si tu sistema no tiene suficiente información, PSI te lo dirá antes de que pierdas tiempo, cómputo o dinero.

---

## 🧠 ¿Por qué PSI?

La mayoría de los sistemas fallan no por bugs…
sino porque **no tienen suficiente información para resolverse**.

PSI analiza tu sistema y responde una sola pregunta crítica:

👉 *¿Este sistema puede resolverse… o está condenado a fallar?*

---

## 🛠 Instalación

```bash
pip install psi-cloud
```

*(Asegúrate de usar la versión >= 1.1.0 para acceder a las funciones de Gating)*

---

## 🛑 NUEVO: "The Entropy-Gate" (Decorador de Ahorro de GPU)

¿Cansado de quemar créditos de AWS o Render en datos basura? El SDK ahora incluye el decorador `@psi_gated`. 

Protege tus funciones de inferencia pesadas con 1 línea de código. La función **solo se ejecutará** si el motor PSI confirma que hay suficiente información. Si no, se inhibe automáticamente.

```python
from psi_cloud import PSIClient

client = PSIClient(api_key="TU_API_KEY_AQUÍ")

# 1. Define cómo calcular los bits de entrada de tu sistema
def calcular_señal(datos_usuario):
    # Ejemplo: 0.5 bits por cada dato válido aportado
    return len([k for k, v in datos_usuario.items() if v is not None]) * 0.5

# 2. Protege tu inferencia costosa con The Entropy-Gate
@client.psi_gated(n=8, bits_extractor=calcular_señal, fallback_response={"status": "Inhibido por falta de información"})
def ejecutar_modelo_ia(datos_usuario):
    print("Consumiendo créditos de GPU...")
    # Tu lógica pesada de Machine Learning aquí
    return {"prediccion": "Exitosa"}

# --- PRUEBA DEL SISTEMA ---

# ❌ Intento pobre (1.0 bits): La IA NUNCA se ejecuta, ahorras dinero.
transaccion_mala = {"ip": "192...", "device": None, "location": None, "history": None}
print(ejecutar_modelo_ia(transaccion_mala)) 
# Salida: {'status': 'Inhibido por falta de información'}

# ✅ Intento rico (2.0 bits): Pasa la validación, la IA se ejecuta.
transaccion_buena = {"ip": "192...", "device": "Mac", "location": "NY", "history": "Valido"}
print(ejecutar_modelo_ia(transaccion_buena))
# Salida: Consumiendo créditos de GPU... {'prediccion': 'Exitosa'}
```

---

## ⚡ Uso Clásico (Validación Manual)

Si prefieres usar el motor paso a paso sin el decorador:

```python
from psi_cloud import PSIClient

client = PSIClient(api_key="TU_API_KEY_AQUÍ")

try:
    resultado = client.check_sufficiency(n=8, bits=3.5)

    if resultado["deterministic_achieved"]:
        print("✅ Sistema resoluble:", resultado["recommendation"])
    else:
        print("⚠️ Sistema insuficiente:", resultado["recommendation"])

    print(f"Créditos restantes: {resultado['credits_remaining']}")

except Exception as e:
    print(f"Error: {e}")
```

---

## 🔥 Ejemplo Real: Evitando un Modelo Inútil

### ❌ Sin PSI

Un equipo entrena un modelo de clasificación con:

* 8 posibles estados (`n = 8`)
* Features limitadas (≈ 2.5 bits efectivos)

Entrenan durante horas…
ajustan hiperparámetros…
optimizan el pipeline…

Resultado:

> ❌ El modelo nunca converge correctamente
> ❌ Resultados inconsistentes
> ❌ Tiempo y cómputo desperdiciado

---

### ✅ Con PSI

Antes de entrenar, ejecutan el chequeo y reciben la respuesta del motor:

```json
{
  "deterministic_achieved": False,
  "margin": -0.5,
  "recommendation": "Se requieren al menos 0.5 bits adicionales para garantizar resolución determinística"
}
```

### 💡 Insight crítico

PSI detecta instantáneamente que el sistema **no tiene suficiente información para resolverse**. Sin importar el modelo, el algoritmo o el tuning. **Evitó que resolvieran un problema imposible.**

---

### ⚠️ Regla de oro

> Si no hay suficiente información, ningún modelo te va a salvar.

PSI existe para detectar eso antes de que sea demasiado tarde.

---

## 📊 ¿Qué analiza PSI?

El motor PSI evalúa tres componentes clave:

* Entropía mínima requerida
* Información total disponible
* Margen de suficiencia estructural

Si el sistema no cumple el criterio interno, PSI calcula exactamente cuánta información falta.

---

## ⚙️ Casos de uso

* **MLOps / FinOps:** Reducción de costos de inferencia en la nube (Gating).
* Validación de modelos antes de entrenamiento.
* Sistemas de decisión y optimización.
* Arquitecturas distribuidas.
* Sistemas heurísticos complejos.

---

## 🔐 ¿Por qué usar el SDK?

Porque el criterio completo de PSI no es trivial, no es lineal y no depende solo de una fórmula. Está optimizado y validado en producción. 👉 El SDK te da acceso directo al motor sin tener que implementarlo desde cero.

---

## 📝 Licencia

MIT License
