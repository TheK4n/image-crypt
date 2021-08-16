import sys

from PyQt5 import QtGui

from src.Crypto import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from src import design

project_path = Path(__file__).parent


class MainWindow(QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.image_directory_dec = None
        self.image_directory_enc = None

        self.pushButton.clicked.connect(self.btn_load_image_clicked_enc)
        self.pushButton_4.clicked.connect(self.encrypt_image)
        self.pushButton_2.clicked.connect(self.btn_load_image_clicked_dec)
        self.pushButton_3.clicked.connect(self.decrypt_image)

    def btn_load_image_clicked_enc(self):
        directory = QFileDialog.getOpenFileName(self, "Choose image", filter='*.jpg *.bmp *.png')[0]

        if directory != '':
            self.image_directory_enc = directory
            self.Debug_area_1.setText('Image to encrypt: ' + os.path.basename(directory))

    def encrypt_image(self):

        if self.image_directory_enc is None:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Error")
            error_dialog.setInformativeText('Choose image!')
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        try:

            crt = CryptImageSave(self.image_directory_enc)

            crt.save_encrypted_image(self.text_input.toPlainText(), self.lineEdit.text())

            self.Debug_area_1.setText(f'Encrypted image saved')

        except MoreThanImgError:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Error")
            error_dialog.setInformativeText('Message size more than image size!')
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

    def btn_load_image_clicked_dec(self):
        directory = QFileDialog.getOpenFileName(self, "Choose image", filter='*.jpg *.bmp *.png')[0]
        if directory != '':
            self.image_directory_dec = directory
            self.Debug_area_2.setText('Image to decrypt: ' + os.path.basename(directory))

    def decrypt_image(self):

        if self.image_directory_dec is None:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Error")
            error_dialog.setInformativeText('Choose image!')
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        crt = CryptImageSave(self.image_directory_dec)

        res = crt.get_msg_from_image(self.lineEdit_2.text())
        self.text_output.setText(res)

        if self.checkBox.isChecked():
            with open(os.path.join(project_path, 'results', 'res.txt'), 'w') as file:
                file.write(res)
            self.Debug_area_2.setText('Successfully decrypted image, saved to res.txt')
        else:
            self.Debug_area_2.setText('Successfully decrypted image')


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setWindowIcon(QtGui.QIcon(os.path.join(project_path, 'src', 'icon.ico')))
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()
    sys.exit(app.exec_())  # запускаем приложение


if __name__ == '__main__':
    main()
