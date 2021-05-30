import sys
from source.Crypto import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from source import design


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
        directory = QFileDialog.getOpenFileName(self, "Выберите картинку", filter='*.jpg *.bmp *.png')[0]

        if directory != '':
            self.image_directory_enc = directory
            self.Debug_area_1.setText('Image to encrypt: ' + directory.split('/')[-1])

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
            encrypt(self.image_directory_enc, self.text_input.toPlainText(), self.lineEdit.text())

            n = len(list(filter(lambda x: x.split('.')[-1] == 'bmp', list(os.listdir('results')))))
            self.Debug_area_1.setText(f'Encrypted image saved as encrypted_{n}.bmp')
        except MoreThanImgError:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Error")
            error_dialog.setInformativeText('Message size more than image size!')
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

    def btn_load_image_clicked_dec(self):
        directory = QFileDialog.getOpenFileName(self, "Выберите картинку", filter='*.jpg *.bmp *.png')[0]
        if directory != '':
            self.image_directory_dec = directory
            self.Debug_area_2.setText('Image to decrypt: ' + directory.split('/')[-1])

    def decrypt_image(self):

        if self.image_directory_dec is None:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Error")
            error_dialog.setInformativeText('Choose image!')
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
            return

        res = decrypt(self.image_directory_dec, self.lineEdit_2.text())
        self.text_output.setText(res)

        if self.checkBox.isChecked():
            with open('results\\res.txt', 'w') as file:
                file.write(res)
            self.Debug_area_2.setText('Successfully decrypted image, saved to res.txt')
        else:
            self.Debug_area_2.setText('Successfully decrypted image')


def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':
    main()
