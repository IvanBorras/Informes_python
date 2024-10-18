import sys
import pandas as pd
from PyQt5 import QtWidgets
import json
from calculator import Calculator  # Importar la clase Calculator

class ModernApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.customers_data = {}  # Estructura JSON para los clientes
        self.calculator = Calculator()  # Instancia de la clase Calculator
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calculadora de Consumo')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout(self)

        # ComboBox para seleccionar cliente
        self.client_combo_box = QtWidgets.QComboBox()
        layout.addWidget(self.client_combo_box)

        # Cargar clientes desde el JSON
        self.load_customers()

        # Botón para cargar el archivo Excel
        load_button = QtWidgets.QPushButton('Cargar Excel')
        load_button.clicked.connect(self.load_data)
        layout.addWidget(load_button)
        
        # Botón para reiniciar la aplicación (limpiar datos y resultados)
        reset_button = QtWidgets.QPushButton('Reiniciar')
        reset_button.clicked.connect(self.reset_app)
        layout.addWidget(reset_button)

        # Botones para calcular
        calculate_total_button = QtWidgets.QPushButton('Calcular Consumo Total')
        calculate_total_button.clicked.connect(self.calculate_total)
        layout.addWidget(calculate_total_button)

        calculate_percentage_button = QtWidgets.QPushButton('Calcular %')
        calculate_percentage_button.clicked.connect(self.calculate_percentage)
        layout.addWidget(calculate_percentage_button)

        calculate_relation_button = QtWidgets.QPushButton('Calcular Relación de Consumo')
        calculate_relation_button.clicked.connect(self.calculate_relation)
        layout.addWidget(calculate_relation_button)

        calculate_total_value_button = QtWidgets.QPushButton('Calcular Total')
        calculate_total_value_button.clicked.connect(self.calculate_total_value)
        layout.addWidget(calculate_total_value_button)

        # Área para mostrar los datos en formato de tabla
        self.table_widget = QtWidgets.QTableWidget()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        
        
        

    def load_customers(self):
        try:
            with open('customers.json', 'r') as f:
                self.customers_data = json.load(f)
                self.client_combo_box.addItems(self.customers_data.keys())
        except FileNotFoundError:
            print("El archivo 'customers.json' no fue encontrado.")

    def load_data(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Cargar Excel", "", "Excel Files (*.xls *.xlsx);;All Files (*)", options=options)
        if file_name:
            self.data = pd.read_excel(file_name)
            self.populate_table()
            
            
    def populate_table(self):
        self.table_widget.setRowCount(0)  # Limpiar tabla
        self.table_widget.setColumnCount(self.data.shape[1])
        self.table_widget.setHorizontalHeaderLabels(self.data.columns)

        for index, row in self.data.iterrows():
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            for column in range(self.data.shape[1]):
                self.table_widget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(row.iloc[column])))


    
    def get_selected_rows(self):
        return [index.row() for index in self.table_widget.selectedIndexes()]

    def insert_into_json(self, selected_services, value, key):
        selected_client = self.client_combo_box.currentText()
        if selected_client not in self.customers_data:
            self.customers_data[selected_client] = {}

        if key not in self.customers_data[selected_client]:
            self.customers_data[selected_client][key] = {}

        self.customers_data[selected_client][key][selected_services] = value

    def update_results_table(self):
        self.results_table.setRowCount(0)  # Limpiar tabla

        for client, data in self.customers_data.items():
            for key, services in data.items():
                for service, value in services.items():
                    row_position = self.results_table.rowCount()
                    self.results_table.insertRow(row_position)
                    self.results_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(client))
                    self.results_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(key))
                    self.results_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(service))
                    self.results_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(value)))

    
    def calculate_total(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione al menos una fila.")
            return
        
        # Sumar todas las columnas de las filas seleccionadas
        total_consumo = self.data.iloc[selected_rows, 2:].sum()  # Suponiendo que la primera columna no se suma

        selected_services = ", ".join(self.data.iloc[row, 1] for row in selected_rows)  # Obtener nombres de los servicios

        self.insert_into_json(selected_services, total_consumo, "consumo total")
        self.update_results_table()

    
    
    
    def calculate_percentage(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione al menos una fila.")
            return

        percentage = self.calculator.calculate_percentage(self.data, selected_rows)
        selected_services = ", ".join(self.data.iloc[row, 0] for row in selected_rows)

        self.insert_into_json(selected_services, percentage, "%")
        self.update_results_table()

    def calculate_relation(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione al menos una fila.")
            return

        relation_consumo = self.calculator.calculate_relation(self.data, selected_rows)
        selected_services = ", ".join(self.data.iloc[row, 0] for row in selected_rows)

        self.insert_into_json(selected_services, relation_consumo, "relacion consumo")
        self.update_results_table()

    def calculate_total_value(self):
        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione al menos una fila.")
            return

        total_value = self.calculator.calculate_total_value(self.data, selected_rows)
        selected_services = ", ".join(self.data.iloc[row, 0] for row in selected_rows)

        self.insert_into_json(selected_services, total_value, "total")
        self.update_results_table()
        
    def reset_app(self):
        """Reinicia la aplicación limpiando los datos y resultados."""
        self.data = None
        self.customer_structure = None
        self.table_widget.clear()  # Limpia la tabla de datos
        self.result_label.setText('')  # Limpia el área de resultados
        self.client_combo_box.setCurrentIndex(0)  # Reinicia la selección de cliente
        QtWidgets.QMessageBox.information(self, "Reinicio", "La aplicación ha sido reiniciada.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ModernApp()
    window.show()
    sys.exit(app.exec_())
