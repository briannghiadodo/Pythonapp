import sys, subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QTextEdit
import subprocess
import requests
import xmltodict
import openpyxl


class PhoneInfo(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

	    # create labels for the information
        self.imei = QLabel('IMEI:')
        self.marketing_name = QLabel('Marketing Name:')
        self.tac_number = QLabel('TAC Number:')
        self.network_technology = QLabel('Network Technology:')
        self.model = QLabel('Model:')
        self.year_released = QLabel('Year Released:')
        
        # create a button
        self.button = QPushButton('Submit', self)
        self.button.clicked.connect(self.get_imei)

        # create a layout for the labels and button
        vbox = QVBoxLayout()
        vbox.addWidget(self.imei)
        vbox.addWidget(self.marketing_name)
        vbox.addWidget(self.tac_number)
        vbox.addWidget(self.network_technology)
        vbox.addWidget(self.model)
        vbox.addWidget(self.year_released)
        vbox.addWidget(self.button)
        self.setLayout(vbox)
        
        # set window properties
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Device Information')
        self.show()

    def get_imei(self):
        sdk_version_cmd = 'adb shell getprop ro.build.version.sdk'
        sdk_version = subprocess.check_output(sdk_version_cmd, shell=True).strip().decode('utf-8')
        print("sdk_version:", sdk_version)
        if int(sdk_version) >= 31:  # Android 12 or higher
            cmd = 'adb shell "service call iphonesubinfo 1 s16 com.android.shell | cut -c 52-66 | tr -d \' & \".[:space:]\'\" & \' "'
        else:
            cmd = 'adb shell "service call iphonesubinfo 1 | grep -o \'[0-9a-f]\\{8\\} \' | tail -n+3 | while read a; do echo -n ${a:6:2}${a:4:2}${a:2:2}${a:0:2}; done"'

        output = subprocess.check_output(cmd, shell=True)
        imei_hex_str = output.strip().decode('utf-8').upper()
        imeiX = ''.join(chr(int(imei_hex_str[i:i+2], 16)) for i in range(0, len(imei_hex_str), 2)).replace('\x00', '').strip()

        tac = imeiX[0:7]
        print(imeiX)
        print(tac)
        self.imei.setText(f'IMEI: {imeiX}')

        url = "http://52.223.31.163/pwgapi/QueryDevice/index.php"

        # IMEIVar = '353281710471201'
        # IMEIVar = '862929059006707'
        IMEIVar = imeiX

        url = 'http://52.223.31.163/pwgapi/QueryDevice/index.php'
        headers = {
            'Content-Type': 'text/plain',
            'Cookie': 'PHPSESSID=bkg9qcljr25rlgplsu8uh5l7u5ddddddx'
        }

        xml_body = '''<?xml version="1.0" encoding="utf-8"?>
        <SoftelsApi xmlns="http://www.softtels.com/SoftelsGenesisApi" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

            <Authentication>

                <AccountID>txmobile</AccountID>

                <passphrase>CyxZHkWCd8LEFAg5</passphrase>

                <key>TX Mobile2795</key>

            </Authentication>

            <ApiRequest type="QueryDevice">

                <IMEI>{}</IMEI>

                <TAC></TAC>

                <MODEL></MODEL>

                <NAME></NAME>

            </ApiRequest>

        </SoftelsApi>'''.format(IMEIVar)

        response = requests.post(url, headers=headers, data=xml_body)
        xml_response = response.text

        # print(response.text)
        print("got response")

        response_dict = xmltodict.parse(response.content)

        print("response_dict: ", response_dict, type(response_dict))
        marketing_name = response_dict['SoftelsApi']['ApiResponse']['MARKETINGNAME']
        TAC_number = response_dict['SoftelsApi']['ApiResponse']['TAC']
        NETWORKTECHNOLOGY = response_dict['SoftelsApi']['ApiResponse']['NETWORKTECHNOLOGY']
        MODEL = response_dict['SoftelsApi']['ApiResponse']['MODEL']
        YEARRELEASED = response_dict['SoftelsApi']['ApiResponse']['YEARRELEASED']

        print(imeiX, marketing_name, TAC_number, NETWORKTECHNOLOGY, MODEL, YEARRELEASED)
        self.imei.setText(imeiX)
        self.marketing_name.setText(marketing_name)
        self.tac_number.setText(TAC_number)
        self.network_technology.setText(NETWORKTECHNOLOGY)
        self.model.setText(MODEL)
        self.year_released.setText(YEARRELEASED)

        # save to excel file
        # Open the Excel file
        workbook = openpyxl.load_workbook('result.xlsx')

        # Select the worksheet you want to append to
        worksheet = workbook['Sheet1']

        # Create a list with the values you want to append
        new_row = [imeiX, marketing_name, TAC_number, NETWORKTECHNOLOGY, MODEL, YEARRELEASED]


        # Append the new row to the worksheet
        worksheet.append(new_row)

        # Save the changes to the Excel file
        workbook.save('result.xlsx')




# ======================================================================================== #
if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = PhoneInfo()
        win.show()
        sys.exit(app.exec_())
