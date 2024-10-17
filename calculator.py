import pandas as pd

def calculate_percentage(df):
    # Asumiendo que la primera columna contiene los servicios y la última columna es el total
    total_consumo = df.iloc[:, -1].sum()
    percentages = {}

    for index, row in df.iterrows():
        service_name = row[0]
        consumption = row[-1] if pd.notna(row[-1]) else 0

        if total_consumo > 0:
            percentages[service_name] = (consumption / total_consumo) * 100
        else:
            percentages[service_name] = 0

    return percentages

def calculate_totals(data):
    # Asumimos que la última columna es el total de consumo
    total_consumo = data.iloc[:, -1].sum()
    servicios_consumo = {}

    for index, row in data.iterrows():
        service_name = row[0]
        consumo = row[-1] if pd.notna(row[-1]) else 0
        servicios_consumo[service_name] = consumo

    return {
        'total_consumo': total_consumo,
        'servicios_consumo': servicios_consumo
    }
