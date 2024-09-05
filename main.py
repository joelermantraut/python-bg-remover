import sys
# common
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout
from PyQt5.QtCore import Qt
# gui
import rembg
import numpy as np
from PIL import Image
# background remover
import os
import fnmatch
# search images

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interfaz Gráfica Moderna')

        # Estilos para la interfaz
        self.setStyleSheet("""
            QWidget {
                background-color: #9893DA;
                color: #FFFFFF;
            }
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #9893DA;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #BBBDF6;
            }
        """)

        # Etiqueta de bienvenida
        lbl_bienvenida = QLabel('Bienvenido', self)
        lbl_bienvenida.setAlignment(Qt.AlignCenter)

        # Botón para elegir directorio de imágenes
        btn_elegir_imagenes = QPushButton('Elegir imágenes', self)
        btn_elegir_imagenes.clicked.connect(self.elegir_imagenes)

        # Botón para elegir directorio de guardado
        btn_elegir_guardar = QPushButton('Elegir donde guardar', self)
        btn_elegir_guardar.clicked.connect(self.elegir_guardar)

        # Botón para borrar fondo
        btn_borrar_fondo = QPushButton('Borrar fondo', self)
        btn_borrar_fondo.clicked.connect(self.borrar_fondo)

        # Botón para cerrar la aplicación
        btn_cerrar = QPushButton('Cerrar', self)
        btn_cerrar.clicked.connect(self.close)

        # Layout vertical
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_bienvenida)
        vbox.addWidget(btn_elegir_imagenes)
        vbox.addWidget(btn_elegir_guardar)
        vbox.addWidget(btn_borrar_fondo)
        vbox.addWidget(btn_cerrar)

        self.setLayout(vbox)
        self.show()

    def elegir_imagenes(self):
        directorio_imagenes = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio de Imágenes")
        if directorio_imagenes:
            print(f'Se ha seleccionado el directorio de imágenes: {directorio_imagenes}')
            self.directorio_imagenes = directorio_imagenes

    def elegir_guardar(self):
        directorio_guardar = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio de Guardado")
        if directorio_guardar:
            print(f'Se ha seleccionado el directorio de guardado: {directorio_guardar}')
            self.directorio_guardar = directorio_guardar
            print(self.directorio_guardar)

    def buscar_imagenes(self, directorio):
        patrones = ['*.jpg', '*.jpeg', '*.png']
        imagenes = []

        for ruta, _, archivos in os.walk(directorio):
            for patron in patrones:
                for archivo in fnmatch.filter(archivos, patron):
                    imagenes.append(os.path.join(ruta, archivo))

        return imagenes

    def borrar_fondo(self):
        imagenes = self.buscar_imagenes(self.directorio_imagenes)
        for imagen in imagenes:
            image_filename = imagen.split(os.sep)[-1]
            image_filename = image_filename.split(".")
            ext = image_filename.pop()
            image_filename = ".".join(image_filename)

            input_image = Image.open(imagen)
            input_array = np.array(input_image)
            output_array = rembg.remove(input_array)
            output_image = Image.fromarray(output_array)
            output_image.save(f'{self.directorio_guardar}/{image_filename}_output.png')
            print("Imagen guardada")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())
