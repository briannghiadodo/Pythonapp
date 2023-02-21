import csv
import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

import docopt
import ipdb
import requests
import xmltodict

URL = "http://www.softtels.com/SoftelsGenesisApi:"
INPUT_PATH = "./input"

USAGE = """
Usage:
  device.py gui 
  device.py cli [--local | --api]
"""


def api_call(operating_system: str, imei):
    # Execute "adb shell getprop" command to get carrier code
    if operating_system == "Windows":
        output = subprocess.check_output(
            ["adb", "shell", "getprop"], shell == True
        ).decode("utf-8")
    else:
        output = subprocess.check_output(["adb", "shell", "getprop"], text=True).decode(
            "utf-8"
        )
    carrier_code = ""
    for line in output.splitlines():
        if "persist.sys.carrierid_etcpath" in line:
            carrier_code = line.split(": ")[1]
        # Set IMEI number and API endpoint
        IMEI = imei
        url = "http://52.223.31.163/pwgapi/QueryDevice/index.php"

        # Create API request payload
        payload = {
            "SoftelsApi": {
                "@xmlns": "http://www.softtels.com/SoftelsGenesisApi",
                "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "Authentication": {
                    "AccountID": "txmobile",
                    "passphrase": "CyxZHkWCd8LEFAg5",
                    "key": "TX Mobile2795",
                },
                "ApiRequest": {
                    "@type": "QueryDevice",
                    "IMEI": IMEI,  # Function to get IMEI
                    "TAC": "",
                    "MODEL": "",
                    "NAME": "",
                },
            }
        }

        # Send API request and parse response
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )
        return response.content
        # response_dict = xmltodict.parse(response.content)

        # # Extract necessary information from response dictionary
        # marketing_name = response_dict["SoftelsApi"]["ApiResponse"]["Device"][
        #     "MarketingName"
        # ]
        # tac = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["TAC"]
        # name = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["Name"]
        # network_technology = response_dict["SoftelsApi"]["ApiResponse"]["Device"][
        #     "NetworkTechnology"
        # ]
        # model = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["Model"]
        # year_released = response_dict["SoftelsApi"]["ApiResponse"]["Device"][
        #     "YearReleased"
        # ]


def build_dict_for_csv(xml_input: dict):
    base = xml_input[f"{URL}SoftelsApi"][f"{URL}ApiResponse"]
    ret = {
        "marketing_name": base[f"{URL}MARKETINGNAME"],
        "tac": base[f"{URL}TAC"],
        "name": base[f"{URL}NAME"],
        "network_technology": base[f"{URL}NETWORKTECHNOLOGY"],
        "model": base[f"{URL}MODEL"],
        "year_released": base[f"{URL}YEARRELEASED"],
        "carrier_code": base[f"{URL}MARKETINGNAME"],  # TODO change this
    }
    return ret


def write_csv(data: list):
    # Write information to CSV file

    with open("./output/phone_specs.csv", "w", newline="") as csvfile:
        headers = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for row in data:
            writer.writerow(row)


def run_tk():
    # Create main window
    root = tk.Tk()
    root.title("Get Device Info")

    # Create label and entry for IMEI
    label_imei = tk.Label(root, text="IMEI:")
    entry_imei = tk.Entry(root)

    # Create button to get device information
    button_get_info = tk.Button(root, text="Get Info", command=get_device_info)

    # Place label and entry in the window
    label_imei.grid(row=0, column=0, padx=10, pady=10)

    entry_imei.grid(row=0, column=1, padx=10, pady=10)

    # Place button in the window
    button_get_info.grid(row=1, column=1, pady=10)

    # Start event loop
    root.mainloop()
    messagebox.showinfo("Information", "Device information saved to phone_specs.csv")

# TODO implement this
def call_IMEI():
    return entry_imei.get()


if __name__ == "__main__":
    arguments = docopt.docopt(USAGE)
    o_s = platform.system()
    imei_info = call_IMEI()  # TODO parse IMEI here
    ipdb.set_trace()
    if arguments["gui"]:
        run_tk()
    elif arguments["--local"]:
        files = [
            f
            for f in os.listdir(INPUT_PATH)
            if os.path.isfile(os.path.join(INPUT_PATH, f))
        ]
        output_data = []
        for file in files:
            with open(f"{INPUT_PATH}/{file}", "r") as f:
                data = f.read()
            data = data.replace("&", "&amp;")
            xml_dict = xmltodict.parse(data, process_namespaces=True)
            dict_for_csv = build_dict_for_csv(xml_dict)
            output_data.append(dict_for_csv)
        write_csv(output_data)
    elif arguments["--api"]:
        output_data = []
        data = api_call(o_s, imei_info)
        data = data.replace("&", "&amp;")
        xml_dict = xmltodict.parse(data, process_namespaces=True)
        dict_for_csv = build_dict_for_csv(xml_dict)
        output_data.append(dict_for_csv)
        write_csv(output_data)
