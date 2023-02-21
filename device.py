import subprocess
import requests
import xmltodict
import csv
import tkinter as tk
from tkinter import messagebox

# Execute "adb shell getprop" command to get carrier code
output = subprocess.check_output(["adb", "shell", "getprop"]).decode("utf-8")
carrier_code = ""
for line in output.splitlines():
    if "persist.sys.carrierid_etcpath" in line:
        carrier_code = line.split(": ")[1]
    # Set IMEI number and API endpoint
    IMEI = entry_imei.get()
    url = "http://52.223.31.163/pwgapi/QueryDevice/index.php"

    # Create API request payload
    payload = {
        "SoftelsApi": {
            "@xmlns": "http://www.softtels.com/SoftelsGenesisApi",
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "Authentication": {
                "AccountID": "txmobile",
                "passphrase": "CyxZHkWCd8LEFAg5",
                "key": "TX Mobile2795"
            },
            "ApiRequest": {
                "@type": "QueryDevice",
                "IMEI": IMEI,
                "TAC": "",
                "MODEL": "",
                "NAME": ""
            }
        }
    }

    # Send API request and parse response
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    response_dict = xmltodict.parse(response.content)

    # Extract necessary information from response dictionary
    marketing_name = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["MarketingName"]
    tac = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["TAC"]
    name = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["Name"]
    network_technology = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["NetworkTechnology"]
    model = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["Model"]
    year_released = response_dict["SoftelsApi"]["ApiResponse"]["Device"]["YearReleased"]

    # Write information to CSV file
    with open("phone_specs.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([marketing_name, tac, name, network_technology, model, year_released, carrier_code])

    messagebox.showinfo("Information", "Device information saved to phone_specs.csv")

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

