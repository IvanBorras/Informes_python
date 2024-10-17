import pandas as pd

def calculate_percentage(df, service_col=0, total_col=-1):
  """
  Calcula el porcentaje de consumo de cada servicio respecto al consumo total.

  Args:
      df (pandas.DataFrame): El DataFrame que contiene los datos de consumo.
      service_col (int, optional): La posición (índice) de la columna que contiene los nombres de los servicios. Defaults to 0 (primera columna).
      total_col (int, optional): La posición (índice) de la columna que contiene el consumo total. Defaults to -1 (última columna).

  Returns:
      dict: Un diccionario que mapea los nombres de los servicios a sus respectivos porcentajes de consumo.
  """

  # Obtiene el consumo total de la columna especificada
  total_consumo = df.iloc[:, total_col].sum()
  percentages = {}

  # Itera por cada fila del DataFrame
  for index, row in df.iterrows():
    service_name = row.iloc[service_col]  # Access using iloc
    consumption = row.iloc[total_col] if pd.notna(row.iloc[total_col]) else 0

    # Evita divisiones por cero
    if total_consumo > 0:
      percentages[service_name] = (consumption / total_consumo) * 100
    else:
      percentages[service_name] = 0

  return percentages

def calculate_totals(data, service_col=0, total_col=-1):
  """
  Calcula el consumo total y el consumo de cada servicio individualmente.

  Args:
      data (pandas.DataFrame): El DataFrame que contiene los datos de consumo.
      service_col (int, optional): La posición (índice) de la columna que contiene los nombres de los servicios. Defaults to 0 (primera columna).
      total_col (int, optional): La posición (índice) de la columna que contiene el consumo total. Defaults to -1 (última columna).

  Returns:
      dict: Un diccionario que contiene dos claves:
          * 'total_consumo': El consumo total de todos los servicios.
          * 'servicios_consumo': Un diccionario que mapea los nombres de los servicios a sus respectivos consumos individuales.
  """

  # Obtiene el consumo total de la columna especificada
  total_consumo = data.iloc[:, total_col].sum()
  servicios_consumo = {}

  # Itera por cada fila del DataFrame y acumula el consumo por servicio
  for index, row in data.iterrows():
    service_name = row[service_col]
    consumo = row[total_col] if pd.notna(row[total_col]) else 0
    servicios_consumo[service_name] = consumo

  return {
    'total_consumo': total_consumo,
    'servicios_consumo': servicios_consumo
  }