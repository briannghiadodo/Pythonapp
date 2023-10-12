import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
import subprocess

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 150)
        self.setWindowTitle('Get IMEI')

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 200, 30)
        self.label.setText('Click the button to get the IMEI number')

        self.button = QPushButton('Get IMEI', self)
        self.button.setGeometry(100, 90, 100, 30)
        self.button.clicked.connect(self.get_imei)

    def get_imei(self):
        cmd = 'adb shell "service call iphonesubinfo 1 | grep -o \'[0-9a-f]\\{8\\} \' | tail -n+3 | while read a; do echo -n ${a:6:2}${a:4:2}${a:2:2}${a:0:2}; done"'
        output = subprocess.check_output(cmd, shell=True)
        imei_hex_str = output.strip().decode('utf-8').upper()
        imei = ''.join(chr(int(imei_hex_str[i:i+2], 16)) for i in range(0, len(imei_hex_str), 2)).replace('\x00', '').strip()
        self.label.setText(f'IMEI: {imei}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
