# Pythonapp

Currently, I am constructing a database. this database is to store all the specifications of an android phone. I do it manually, and there are two main steps in this process. First, I turn on the debug mode in the phones, then plug it into the PC, i turn on the command prompt, and type adb shell getprop, this step is to collect the carrier code, i look at the line "[persist.sys.carrierid_etcpath]" and collect the data. Second, I have to manually read the IMEI number from the phone and enter it into a variable in API file to get some information from the response. And then I also use the API in the command prompt to execute the API. The API is written by node.js, and I will paste it below.
The information i need from the response are between 
<MARKETINGNAME> </MARKETINGNAME>
<TAC></TAC>
<NAME> </NAME>
<NETWORKTECHNOLOGY>5G</NETWORKTECHNOLOGY>
<MODEL> </MODEL>
<YEARRELEASED></YEARRELEASED>
After all, I will save the data get prop file and the response file based on this format marketingname_(carrier code from the getprop file) to a dedicated folder
For example, adb shell getprop >> Galaxy_A13_TMB_ATT.txt; node APIfile >> Galaxy_A13_TMB_ATT.xml 
After I got all the information, I will type it to the excel file. One by one, and I plan to submit this excel file to one of the Database applications which I have not known yet. I want to make an application in any language and with the GUI to do everything automatically. This is the API I have written by node.js, remember that the IMEI for the var below is the example and I have to assign to the variable var manually.
var request = require('request');
const xml2js = require('xml2js')
var fs = require('fs');
var IMEIVar = '350241600814251';

var options = {
  'method': 'POST',
  'url': 'http://52.223.31.163/pwgapi/QueryDevice/index.php',
  'headers': {
    'Content-Type': 'text/plain',
    'Cookie': 'PHPSESSID=bkg9qcljr25rlgplsu8uh5l7u5'
  },

  body: '<?xml version="1.0" encoding="utf-8"?>\r\n\r\n<SoftelsApi xmlns="http://www.softtels.com/SoftelsGenesisApi" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\r\n\r\n    <Authentication>\r\n\r\n        <AccountID>txmobile</AccountID>\r\n\r\n        <passphrase>CyxZHkWCd8LEFAg5</passphrase>\r\n\r\n        <key>TX Mobile2795</key>\r\n\r\n    </Authentication>\r\n\r\n    <ApiRequest type="QueryDevice">\r\n\r\n        <IMEI>' + IMEIVar + '</IMEI>\r\n\r\n        <TAC></TAC>\r\n\r\n        <MODEL></MODEL>\r\n\r\n        <NAME></NAME>\r\n\r\n    </ApiRequest>\r\n\r\n</SoftelsApi>'

};
request(options, function (error, response) {
  if (error) throw new Error(error);
  var xml = response.body;
  console.log(xml);

});



This is my solution and step. 
use python -> subprocess to execute the "adb shell getprop" string manipulation -> carrier code /// request library -> IMEI -> fill API file -> parse the xml file by XMLtodict library. Gather all information to the CSV file
![image](https://github.com/briannghiadodo/Pythonapp/assets/85943401/f7465f4a-2415-451a-a393-6bc4c7242972)
