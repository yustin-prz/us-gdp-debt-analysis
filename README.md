# US GDP vs Public Debt Analysis (1947–2020)

Limpieza, transformación, análisis exploratorio y visualización de series temporales macroeconómicas de Estados Unidos. El dataset cubre 295 quarters de datos trimestrales del PIB nominal y la deuda pública total desde 1947 hasta 2020.

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
Creación de 7 columnas derivadas de alto valor analítico:

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

### 5. Análisis exploratorio
5 preguntas de negocio respondidas con visualizaciones en Python:
- Evolución histórica del GDP (1947–2020)
- Severidad comparativa de cada recesión
- Evolución del ratio Deuda/GDP desde 1966
- Crecimiento económico promedio por década
- Comparativa directa: Crisis 2008 vs COVID-19

### 6. Dashboard en Power BI
Dashboard interactivo de 3 páginas construido sobre los datasets limpios:

**Página 1 — Visión general**
- 4 tarjetas KPI: GDP máximo, Deuda máxima, Ratio Deuda/GDP pico, Quarters sobre 100%
- Gráfico de área: evolución histórica del GDP (1947–2020)
- Gráfico de barras: crecimiento promedio del GDP por década
- Segmentador interactivo por década

**Página 2 — Análisis de deuda**
- Gráfico de línea: ratio Deuda/GDP con línea de referencia al 100%
- Gráfico de barras: crecimiento trimestral de la deuda
- Scatter plot: GDP vs Deuda coloreado por década
- Tarjeta: quarters históricos con deuda superior al 100% del GDP

**Página 3 — Recesiones**
- Gráfico de columnas con formato condicional: barras rojas para quarters negativos
- Tabla filtrada: solo quarters en recesión con su variación del GDP
- Tarjeta: peor quarter histórico (-9.47% en 2020 Q2)

---

## Resultados

```
Dataset original:   295 filas × 4 columnas
df (completo):      295 filas × 10 columnas
df_complete:        218 filas × 12 columnas  ← sin nulos, listo para análisis
```

**Hallazgos principales:**

- El COVID-19 generó la caída trimestral más severa de toda la serie: **-9.47% en 2020 Q2**, casi el triple que el peor quarter de 2008
- El ratio Deuda/GDP pasó de ~40% en 1966 a **135.6% en 2020**, superando el umbral del 100% por primera vez en 2013
- Las décadas de los **1970s y 1980s** registraron el mayor crecimiento trimestral promedio del GDP
- Cada crisis desde 1980 dejó el ratio Deuda/GDP en un piso más alto que el anterior, sin retornar nunca a niveles pre-crisis

---

## Estructura del repositorio

```
us-gdp-debt-analysis/
│
├── data/
│   ├── US_GDP_vs_Debt.csv               # Dataset original — no modificado
│   ├── gdp_debt_clean.csv               # Dataset limpio completo (295 filas)
│   └── gdp_debt_complete.csv            # Sin nulos, listo para análisis (218 filas)
│
├── notebooks/
│   ├── 01_limpieza.ipynb                # Limpieza y transformación
│   ├── 02_analisis.ipynb                # Análisis exploratorio con Python
│   └── 03_visualizacion.ipynb           # Visualizaciones adicionales
│
├── src/
│   └── cleaning_functions.py            # Pipeline de limpieza modular y reutilizable
│
├── US_GDP_Debt_Dashboard.pbix           # Dashboard interactivo en Power BI
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

# 3. Correr el notebook de limpieza primero (genera los CSVs limpios)
python -m jupyter notebook notebooks/01_limpieza.ipynb

# 4. Correr el análisis exploratorio
python -m jupyter notebook notebooks/02_analisis.ipynb

# 5. Abrir el dashboard en Power BI Desktop
# Archivo → Abrir → US_GDP_Debt_Dashboard.pbix
```

> **Nota:** Es necesario correr `01_limpieza.ipynb` primero para generar `gdp_debt_clean.csv` y `gdp_debt_complete.csv` antes de abrir el dashboard en Power BI.

---

## Herramientas

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-2.2-blue?style=flat-square)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8-blue?style=flat-square)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-blue?style=flat-square)

---

## Autor

**[Tu nombre]**  
[LinkedIn](https://linkedin.com/in/tu-perfil) · [GitHub](https://github.com/yustin-prz)
