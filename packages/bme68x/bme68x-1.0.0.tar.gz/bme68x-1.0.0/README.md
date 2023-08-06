**BME68X and BSEC2.0 for Python by pi3g**

This Python extension enables you to read measurement data by the BME68X sensor and the BSEC2.0 library from BOSCH

How to install the extension without BSEC
- run 'pip3 install bme68x'

How to install the extension with BSEC
- unzip this folder to a location of your choice
- download the licensed BSEC2.0 library from BOSCH https://www.bosch-sensortec.com/software-tools/software/bme688-software/
- unzip it into the AirQuality folder, next to this README
- open a new terminal window inside the AirQuality folder
- execute: sudo python3 setup.py install
- this will build and install the extension

How to use the extension
- to import in Python use: 'import bme68x' or 'from bme68x import BME68X'
- see PythonDocumentation.md for reference
- to test the installation make sure you connected your BME68X sensor via I2C
- run the following code in a Python3 interpreter:
	from bme68x import BME68X
	BME68X(I2C_ADDR, 0).get_data()
- I2C_ADDR should be either 0x76 or 0x77

For documentation and examples see our [GitHub](https://github.com/pi3g/bme68x-python-library)

pi3g is an official approved Raspberry Pi reseller, and a Coral Machine Learning Platform (from Google) distribution partner.
We take care of all your Raspberry Pi and Coral related hardware and software development, sourcing, accessory and consulting needs!
Check out [our homepage](https://pi3g.com) and file your personal software or hardware request.