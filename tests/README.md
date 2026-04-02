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

---

## ⚡ Uso Rápido

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

Antes de entrenar, ejecutan:

```python
resultado = client.check_sufficiency(n=8, bits=2.5)
print(resultado)
```

Respuesta del motor:

```
{
  "deterministic_achieved": False,
  "margin": -0.5,
  "recommendation": "Se requieren al menos 0.5 bits adicionales para garantizar resolución determinística"
}
```

---

### 💡 Insight crítico

PSI detecta instantáneamente que:

👉 El sistema **no tiene suficiente información para resolverse**

Sin importar:

* el modelo
* el algoritmo
* el tuning

---

### 🚀 Resultado

En lugar de perder horas:

* Añaden nuevas features
* Aumentan la señal informativa

Luego ejecutan nuevamente:

```python
resultado = client.check_sufficiency(n=8, bits=3.2)
```

Ahora:

```
{
  "deterministic_achieved": True,
  "margin": 0.2,
  "recommendation": "El sistema cumple el criterio de suficiencia"
}
```

---

### 🧠 Lo que PSI realmente hizo

No “optimizó” el modelo.
No “mejoró” el algoritmo.

👉 **Evitó que resolvieran un problema imposible.**

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

* Validación de modelos antes de entrenamiento
* Sistemas de decisión y optimización
* Arquitecturas distribuidas
* Machine Learning / AI pipelines
* Sistemas heurísticos complejos

---

## 🔐 ¿Por qué usar el SDK?

Porque el criterio completo de PSI:

* No es trivial
* No es lineal
* No depende solo de una fórmula
* Está optimizado y validado en producción

👉 El SDK te da acceso directo al motor sin tener que implementarlo desde cero.

---

## 📝 Licencia

MIT License
