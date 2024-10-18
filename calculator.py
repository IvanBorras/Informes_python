import pandas as pd

class Calculator:
    @staticmethod
    def calculate_total(data, selected_rows):
        return sum(data.iloc[row, -1] for row in selected_rows)

    @staticmethod
    def calculate_percentage(data, selected_rows):
        total_consumo = sum(data.iloc[row, -1] for row in selected_rows)
        total_general = data.iloc[:, -1].sum()

        if total_general > 0:
            return (total_consumo / total_general) * 100
        else:
            return 0

    @staticmethod
    def calculate_relation(data, selected_rows):
        total_consumo = sum(data.iloc[row, -1] for row in selected_rows)
        return total_consumo / len(selected_rows) if len(selected_rows) > 0 else 0

    @staticmethod
    def calculate_total_value(data, selected_rows):
        return sum(data.iloc[row, -1] for row in selected_rows)
