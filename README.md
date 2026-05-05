# US GDP vs Public Debt Analysis (1947–2020)

Limpieza, transformación y análisis exploratorio de series temporales macroeconómicas de Estados Unidos. El dataset cubre 295 quarters de datos trimestrales del PIB nominal y la deuda pública total desde 1947 hasta 2020.

---

## Problema

El dataset original presentaba múltiples problemas de calidad que impedían cualquier análisis directo:

- **26.1% de valores nulos** en la columna de deuda pública (77 quarters sin dato)
- **Inconsistencia de unidades** entre columnas: el GDP estaba expresado en miles de millones (billions) mientras la deuda estaba en millones, a pesar de que ambas columnas indicaban `($mil)` en su encabezado
- **Columna de fecha** almacenada como `string` en lugar de `datetime`, bloqueando operaciones temporales
- **Columna `index` redundante** que duplicaba el índice de pandas sin agregar información

---

## Dataset

| Campo | Detalle |
|---|---|
| Fuente | FRED (Federal Reserve) + Departamento del Tesoro de EE.UU. |
| Cobertura | 1947 Q1 — 2020 Q3 |
| Granularidad | Trimestral |
| Filas | 295 |
| Columnas originales | 4 → 10 tras transformación |

---

## Proceso

### 1. Diagnóstico inicial
Análisis completo de nulos, tipos de datos, duplicados y rango temporal antes de aplicar cualquier transformación.

### 2. Limpieza
- Eliminación de la columna `index` redundante
- Conversión de `Quarter` de `object` a `datetime64`
- Estandarización de unidades: GDP multiplicado por 1,000 para expresarlo en millones, igual que la deuda
- Decisión documentada de **no imputar** los 77 nulos históricos — los datos de deuda trimestral no se reportaban sistemáticamente antes de 1966; imputarlos habría introducido datos ficticios en un período históricamente significativo

### 3. Feature engineering
Creación de 6 columnas derivadas de alto valor analítico:

| Columna | Descripción |
|---|---|
| `Year` | Año extraído de la fecha |
| `Q` | Quarter (Q1, Q2, Q3, Q4) |
| `Decade` | Década (1950s, 1960s, …) |
| `GDP_growth_pct` | Crecimiento trimestral del GDP (%) |
| `Recession` | Flag: `True` si hay dos quarters consecutivos de crecimiento negativo |
| `Debt_to_GDP_pct` | Ratio deuda/GDP × 100 |
| `Debt_growth_pct` | Crecimiento trimestral de la deuda (%) |

### 4. Validación
Suite de 10 checks automáticos que verifican tipos de datos, rangos esperados, integridad de las transformaciones y cobertura temporal.

---

## Resultados

```
Dataset original:   295 filas × 4 columnas
df (completo):      295 filas × 10 columnas
df_complete:        218 filas × 12 columnas  ← sin nulos, listo para análisis
```

**Hallazgo clave:** el ratio Deuda/GDP pasó de ~40% en 1966 a ~135% en 2020 Q2, con el salto más abrupto de toda la serie histórica ocurriendo en un único quarter: 2020 Q2 (+28 puntos porcentuales), producto de la caída del PIB y el aumento masivo del gasto fiscal durante el inicio de la pandemia de COVID-19.

---

## Estructura del repositorio

```
us-gdp-debt-analysis/
│
├── data/
│   ├── US_GDP_vs_Debt.csv          # Dataset original — no modificado
│   ├── gdp_debt_clean.csv          # Dataset limpio completo (295 filas)
│   └── gdp_debt_complete.csv       # Sin nulos, listo para análisis (218 filas)
│
├── notebooks/
│   ├── 01_limpieza.ipynb           # Limpieza y transformación ← este notebook
│   ├── 02_analisis.ipynb           # Análisis exploratorio (próximamente)
│   └── 03_visualizacion.ipynb      # Dashboard y visualizaciones (próximamente)
│
├── src/
│   └── cleaning_functions.py       # Funciones reutilizables extraídas del notebook
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Cómo reproducir

```bash
# 1. Clonar el repositorio
git clone https://github.com/yustin-prz/us-gdp-debt-analysis.git
cd us-gdp-debt-analysis

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Abrir el notebook
jupyter notebook notebooks/01_limpieza.ipynb
```

---

## Herramientas

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-2.2-blue?style=flat-square)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square)

---

## Autor

**Yustin Eduardo Pérez Castro**  
[LinkedIn](www.linkedin.com/in/yustin-prz) · [GitHub](https://github.com/yustin-prz)
