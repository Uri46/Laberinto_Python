 🧩 Laberinto Python

Generación procedural y resolución automática de laberintos bidimensionales mediante **Búsqueda en Profundidad (DFS)** y **Backtracking**. Diseñado bajo arquitectura desacoplada para separar la lógica de matrices de la interfaz gráfica.

---

## 📁 Estructura del Proyecto

```text
.
├── laberinto.py      # Núcleo lógico: matrices, generación aleatoria y resolución
├── interfaz.py       # Renderizado gráfico y visualización
└── README.md         # Documentación principal
```

---

## 🚀 Inicio Rápido

```python
import laberinto

# 1. Generar estructura de 10x10
pn, ps, pe, po = laberinto.generar_laberinto(10, 10)

# 2. Resolver desde (0,0) hasta (9,9)
recorrido, solucion = laberinto.resolver_laberinto(
    10, 10, pn, ps, pe, po, 0, 0, 9, 9
)

print(f"Pasos explorados: {len(recorrido)} | Camino limpio: {len(solucion)}")
```

---

## 🛠️ API de `laberinto.py`

| Función | Descripción | Retorno |
| :--- | :--- | :--- |
| `generar_laberinto(f, c, semilla=None)` | Derriba muros mediante DFS aleatorio. | Tupla (4 matrices de paredes) |
| `resolver_laberinto(...)` | Encuentra la salida desde inicio a fin. | `(camino_completo, camino_final)` |
| `se_puede_avanzar(...)` | Comprueba si hay pared en una dirección. | `(pudo_avanzar, nueva_f, nueva_c)` |
| `crear_matriz_de_booleanos(f, c, val)` | Inicializa matriz 2D de booleanos. | `list[list[bool]]` |

---

## 🧠 Algoritmos

- **Generación (DFS):** Comienza con todas las paredes cerradas (`True`). Explora vecinos al azar y aplica *backtracking* al llegar a callejones sin salida.
- **Resolución:** Agente autónomo con regla de prioridad fija por casilla: **Frente → Derecha → Izquierda → Retroceso**.

---
