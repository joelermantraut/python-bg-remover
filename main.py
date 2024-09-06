import sys
# common
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QSlider, QProgressBar, QMessageBox
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
        self.setWindowTitle('Modern GUI')

        # Styles for the interface
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
            QProgressBar {
                background-color: #625F63;
                border-radius: 10px;
                color: #FFFFFF;
                text-align: center;
            }
        """)

        # Welcome label
        lbl_welcome = QLabel('¡Bienvenido!', self)
        lbl_welcome.setAlignment(Qt.AlignCenter)

        # Button to choose images directory
        btn_choose_images = QPushButton('Elegir imágenes', self)
        btn_choose_images.clicked.connect(self.choose_images)

        # Button to choose save directory
        btn_choose_save = QPushButton('Elegir donde guardar', self)
        btn_choose_save.clicked.connect(self.choose_save_location)

        # Button to remove background
        btn_remove_bg = QPushButton('Borrar fondo', self)
        btn_remove_bg.clicked.connect(self.remove_background)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # Button to close the application
        btn_close = QPushButton('Cerrar', self)
        btn_close.clicked.connect(self.close)

        # Vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_welcome)
        vbox.addWidget(btn_choose_images)
        vbox.addWidget(btn_choose_save)
        vbox.addWidget(btn_remove_bg)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(btn_close)

        self.setLayout(vbox)
        self.show()

    def choose_images(self):
        images_directory = QFileDialog.getExistingDirectory(self, "Select Images Directory")
        if images_directory:
            print(f'Images directory selected: {images_directory}')
            self.images_directory = images_directory

    def choose_save_location(self):
        save_directory = QFileDialog.getExistingDirectory(self, "Select Save Location")
        if save_directory:
            print(f'Save directory selected: {save_directory}')
            self.save_directory = save_directory

    def show_error_message(self, message):
        # Function to show an error message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

    def remove_background(self):
        # Check if image directory is selected
        if not hasattr(self, 'images_directory'):
            self.show_error_message("Debe seleccionar un directorio de imágenes antes de continuar.")
            return

        # Check if save directory is selected
        if not hasattr(self, 'save_directory'):
            self.show_error_message("Debe seleccionar un directorio de guardado antes de continuar.")
            return

        images = self.search_images(self.images_directory)
        total_images = len(images)
        processed_images = 0

        if total_images == 0:
            self.show_error_message("No se encontraron imágenes en el directorio seleccionado.")
            return

        for image in images:
            image_filename = image.split(os.sep)[-1]
            image_filename = image_filename.split(".")
            ext = image_filename.pop()
            image_filename = ".".join(image_filename)

            input_image = Image.open(image)
            input_array = np.array(input_image)
            output_array = rembg.remove(input_array)
            output_image = Image.fromarray(output_array)
            output_image.save(f'{self.save_directory}/{image_filename}_output.png')

            # Update progress
            processed_images += 1
            progress_percentage = int((processed_images / total_images) * 100)
            self.progress_bar.setValue(progress_percentage)
            print(f"Processed {processed_images}/{total_images} images")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    sys.exit(app.exec_())
