from PyQt5 import QtWidgets
import sys
import pandas as pd
from calculator import calculate_totals, calculate_percentage  # Asegúrate de tener estas funciones
import json

class ModernApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.data = None
        self.customer_structure = None

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

        # Botón para procesar el Excel en función de la estructura del cliente
        process_button = QtWidgets.QPushButton('Procesar Datos')
        process_button.clicked.connect(self.process_data)
        layout.addWidget(process_button)

        # Botón para reiniciar la aplicación (limpiar datos y resultados)
        reset_button = QtWidgets.QPushButton('Reiniciar')
        reset_button.clicked.connect(self.reset_app)
        layout.addWidget(reset_button)

        # Área para mostrar los datos en formato de tabla
        self.table_widget = QtWidgets.QTableWidget()
        layout.addWidget(self.table_widget)

        # Etiqueta para mostrar los resultados
        self.result_label = QtWidgets.QLabel('')
        layout.addWidget(self.result_label)

        # Establecer el layout en la ventana principal
        self.setLayout(layout)

    def load_customers(self):
        """Carga la lista de clientes del archivo JSON."""
        with open('customers.json', 'r') as f:
            self.customers_data = json.load(f)

        # Agregar los nombres de los clientes al combo box
        self.client_combo_box.addItems(self.customers_data.keys())

    def load_data(self):
        """Carga el archivo Excel seleccionado por el usuario."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Cargar Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            self.data = pd.read_excel(file_path)  # Carga el archivo en un DataFrame de Pandas
            QtWidgets.QMessageBox.information(self, "Éxito", "Archivo cargado correctamente.")
            
            # Mostrar los datos en el QTableWidget
            self.show_data_in_table()

    def show_data_in_table(self):
        """Muestra los datos del DataFrame en el QTableWidget."""
        self.table_widget.setRowCount(self.data.shape[0])
        self.table_widget.setColumnCount(self.data.shape[1])

        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                value = self.data.iat[i, j]
                item = QtWidgets.QTableWidgetItem(str(value) if pd.notna(value) else "")
                self.table_widget.setItem(i, j, item)

        # Ajustar el tamaño de las columnas al contenido
        for j in range(self.data.shape[1]):
            self.table_widget.resizeColumnToContents(j)
    def process_data(self):
        selected_client = self.client_combo_box.currentText()

        if self.data is not None:
            results = calculate_totals(self.data, service_col=0, total_col=-1)  
            percentages = calculate_percentage(self.data, service_col=0, total_col=-1)

            if selected_client:
                customer_structure = self.customers_data.get(selected_client)
                if customer_structure is not None:
                    self.insert_results_into_structure(results, percentages, customer_structure)
                else:
                    QtWidgets.QMessageBox.warning(self, "Advertencia", "No se encontró la estructura del cliente.")
            else:
                QtWidgets.QMessageBox.warning(self, "Advertencia", "Seleccione un cliente primero.")
        else:
            QtWidgets.QMessageBox.warning(self, "Advertencia", "Cargue el archivo Excel primero.")
            
    def insert_results_into_structure(self, results, percentages, customer_structure):
    # Obtener la estructura del cliente seleccionado
        customer_structure = self.customers_data.get(self.client_combo_box.currentText())

        # Crear una tabla para mostrar los resultados
        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Servicio", "Consumo (kWh)", "Porcentaje"])

        # Llenar la tabla con los datos
        row = 0
        for service, consumption in results['servicios_consumo'].items():
            if service in customer_structure['servicios']:
                percentage = percentages.get(service, 0)  # Obtener el porcentaje
                table.insertRow(row)
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(service))
                table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(consumption)))
                table.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{percentage:.2f}%"))
                row += 1

        # Agregar la tabla a la interfaz (por ejemplo, en un layout)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)
        """Inserta los resultados calculados en la estructura definida."""
        total_consumo = results.get('total_consumo')
        servicios_consumo = results.get('servicios_consumo')

        result_text = f"Consumo Total: {total_consumo:.2f} kWh\n"
        for service, percentage in percentages.items():
            result_text += f"{service}: {percentage:.2f}% del consumo total\n"

            self.result_label.setText(result_text)

    def reset_app(self):
        """Reinicia la aplicación limpiando los datos y resultados."""
        self.data = None
        self.customer_structure = None
        self.table_widget.clear()  # Limpia la tabla de datos
        self.result_label.setText('')  # Limpia el área de resultados
        self.client_combo_box.setCurrentIndex(0)  # Reinicia la selección de cliente
        QtWidgets.QMessageBox.information(self, "Reinicio", "La aplicación ha sido reiniciada.")

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ModernApp()
    window.show()
    sys.exit(app.exec_())
