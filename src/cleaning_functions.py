"""
cleaning_functions.py
---------------------
Funciones reutilizables de limpieza y transformación extraídas de
01_limpieza.ipynb. Proyecto: US GDP vs Public Debt Analysis (1947-2020).
"""

import pandas as pd
import numpy as np


def load_raw_data(filepath: str) -> pd.DataFrame:
    """
    Carga el dataset original sin modificaciones.

    Parameters
    ----------
    filepath : str
        Ruta al archivo CSV original.

    Returns
    -------
    pd.DataFrame
        Dataset crudo tal como viene del archivo.
    """
    return pd.read_csv(filepath)


def diagnose_quality(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un reporte de calidad de datos: nulos, porcentaje y tipo por columna.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset a diagnosticar.

    Returns
    -------
    pd.DataFrame
        Tabla resumen con columnas: dtype, nulos, pct_nulos.
    """
    report = pd.DataFrame({
        "dtype":     df.dtypes,
        "nulos":     df.isnull().sum(),
        "pct_nulos": (df.isnull().sum() / len(df) * 100).round(2),
    })
    return report


def drop_redundant_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina la columna 'index' si existe, ya que duplica el índice de pandas.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Dataset sin la columna 'index'.
    """
    if "index" in df.columns:
        df = df.drop(columns=["index"])
    return df


def parse_quarter_dates(df: pd.DataFrame, col: str = "Quarter") -> pd.DataFrame:
    """
    Convierte la columna de quarters de string a datetime64.

    El formato esperado es 'YYYY-MM-DD', donde el día representa
    el inicio del quarter: enero (Q1), abril (Q2), julio (Q3), octubre (Q4).

    Parameters
    ----------
    df  : pd.DataFrame
    col : str
        Nombre de la columna de fechas. Default: 'Quarter'.

    Returns
    -------
    pd.DataFrame
        Dataset con la columna convertida a datetime64.
    """
    df[col] = pd.to_datetime(df[col])
    return df


def standardize_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estandariza las unidades del GDP y la Deuda a millones de dólares.

    Problema original: el GDP venía expresado en miles de millones (billions)
    mientras que la Deuda venía en millones, a pesar de que ambas columnas
    indicaban '($mil)' en su encabezado. Esta función multiplica el GDP por
    1,000 para alinear ambas columnas en la misma unidad.

    Parameters
    ----------
    df : pd.DataFrame
        Debe contener las columnas originales:
        'Gross Domestic Product ($mil)' y 'Total Public Debt ($mil)'.

    Returns
    -------
    pd.DataFrame
        Dataset con columnas renombradas 'GDP ($mil)' y 'Debt ($mil)',
        ambas expresadas en millones de dólares.
    """
    df["GDP ($mil)"]  = df["Gross Domestic Product ($mil)"] * 1_000
    df["Debt ($mil)"] = df["Total Public Debt ($mil)"]

    df = df.drop(columns=[
        "Gross Domestic Product ($mil)",
        "Total Public Debt ($mil)"
    ])
    return df


def add_time_features(df: pd.DataFrame, date_col: str = "Quarter") -> pd.DataFrame:
    """
    Agrega columnas temporales derivadas de la columna de fecha.

    Columnas creadas:
        - Year   : año (int)
        - Q      : quarter en formato 'Q1'–'Q4'
        - Decade : década en formato '1950s', '1960s', etc.

    Parameters
    ----------
    df       : pd.DataFrame
    date_col : str
        Nombre de la columna datetime. Default: 'Quarter'.

    Returns
    -------
    pd.DataFrame
    """
    df["Year"]   = df[date_col].dt.year
    df["Q"]      = df[date_col].dt.quarter.map({1:"Q1", 2:"Q2", 3:"Q3", 4:"Q4"})
    df["Decade"] = (df["Year"] // 10 * 10).astype(str) + "s"
    return df


def add_gdp_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega métricas derivadas del GDP.

    Columnas creadas:
        - GDP_growth_pct : crecimiento porcentual trimestral del GDP
        - Recession      : True si hay dos quarters consecutivos de GDP negativo

    Parameters
    ----------
    df : pd.DataFrame
        Debe contener la columna 'GDP ($mil)'.

    Returns
    -------
    pd.DataFrame
    """
    df["GDP_growth_pct"] = df["GDP ($mil)"].pct_change() * 100
    gdp_neg = df["GDP_growth_pct"] < 0
    df["Recession"] = gdp_neg & gdp_neg.shift(1)
    return df


def add_debt_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega métricas derivadas de la Deuda. Solo aplicar a df_complete
    (filas sin nulos en ambas columnas).

    Columnas creadas:
        - Debt_to_GDP_pct : ratio (Deuda / GDP) × 100
        - Debt_growth_pct : crecimiento porcentual trimestral de la deuda

    Parameters
    ----------
    df : pd.DataFrame
        Debe contener 'Debt ($mil)' y 'GDP ($mil)' sin nulos.

    Returns
    -------
    pd.DataFrame
    """
    df["Debt_to_GDP_pct"] = (df["Debt ($mil)"] / df["GDP ($mil)"] * 100).round(2)
    df["Debt_growth_pct"] = df["Debt ($mil)"].pct_change() * 100
    return df


def run_pipeline(filepath: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ejecuta el pipeline completo de limpieza y transformación.

    Parameters
    ----------
    filepath : str
        Ruta al CSV original.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        df          : dataset completo con todas las filas (nulos preservados)
        df_complete : dataset sin nulos en Debt ($mil), listo para análisis
                      comparativo GDP vs Deuda.

    Example
    -------
    >>> from src.cleaning_functions import run_pipeline
    >>> df, df_complete = run_pipeline("data/US_GDP_vs_Debt.csv")
    """
    df = (
        load_raw_data(filepath)
        .pipe(drop_redundant_index)
        .pipe(parse_quarter_dates)
        .pipe(standardize_units)
        .pipe(add_time_features)
        .pipe(add_gdp_features)
    )

    df_complete = (
        df.dropna(subset=["Debt ($mil)"])
        .copy()
        .pipe(add_debt_features)
    )

    return df, df_complete
