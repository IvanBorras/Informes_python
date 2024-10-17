from PyQt5 import QtWidgets, QtCore
import pandas as pd

class TableWidget(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Crear un layout vertical para el QFrame
        self.layout = QtWidgets.QVBoxLayout(self)

        # Crear un canvas con scrollbars
        self.canvas = QtWidgets.QScrollArea(self)  # Cambiar Canvas a QScrollArea
        self.table_frame = QtWidgets.QFrame(self)  # Crear un frame para la tabla
        self.table_frame.setLayout(QtWidgets.QGridLayout())  # Usar un QGridLayout para la tabla

        # Conectar el canvas con el frame
        self.canvas.setWidget(self.table_frame)
        self.canvas.setWidgetResizable(True)

        # Agregar el canvas al layout del QFrame
        self.layout.addWidget(self.canvas)

    def display_data(self, df: pd.DataFrame):
        """Despliega los datos de un DataFrame en una tabla."""
        # Limpiar el contenido previo de la tabla
        for widget in self.table_frame.findChildren(QtWidgets.QWidget):
            widget.deleteLater()

        # Crear los encabezados de la tabla
        for i, column in enumerate(df.columns):
            label = QtWidgets.QLabel(self.table_frame)
            label.setText(f"Columna {i + 1}")
            label.setStyleSheet("background-color: lightgrey; font-weight: bold;")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFixedSize(100, 30)  # Ajustar tamaño de los encabezados
            self.table_frame.layout().addWidget(label, 0, i)  # Agregar con addWidget() en lugar de grid()

        # Crear la tabla con los valores
        for row in range(len(df)):
            for col in range(len(df.columns)):
                value = df.iloc[row, col]
                entry = QtWidgets.QLineEdit(self.table_frame)
                entry.setText(str(value))  # Mostrar valor en la celda
                entry.setReadOnly(True)  # Hacer la celda solo lectura
                self.table_frame.layout().addWidget(entry, row + 1, col)  # Agregar con addWidget()
