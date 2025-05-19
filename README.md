# PiicoDev® Magnetometer QMC6310 MicroPython Module

This is the firmware repo for the [Core Electronics PiicoDev® Magnetometer MMC5603](https://core-electronics.com.au/catalog/product/view/sku/CE10107)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

See the [Quickstart Guides](https://piico.dev/p34)

## Details
### `PiicoDev_MMC5603(bus=, freq=, sda=, scl=, addr=0x30, odr=255,  range=, sign_x=0, sign_y=1, sign_z=1, cal_filename='calibration.cal')`


Parameter | Type | Range            | Default                               | Description
--------- | ---- | ---------------- | ------------------------------------- | --------------------------------------------------
bus       | int  | 0, 1             | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit
freq      | int  | 100-1000000      | Device dependent                      | I2C Bus frequency (Hz).  Ignored on Raspberry Pi
sda       | Pin  | Device Dependent | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only
scl       | Pin  | Device Dependent | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only
addr      | int  | 0x30             | 0x30                                  | This address cannot be changed
odr       | int  | 0 - 255          | 255                                   | Range from 0-  255 Hz
range     | int  | 3000             | 3000                                  | Not user configurable, Kept for compatibility.
sign_x    | int  | 0, 1             | 0                                     | Sign to represent the polarity of the magnetic field. 0 Matches the silk screen
sign_y    | int  | 0, 1             | 0                                     | Sign to represent the polarity of the magnetic field. 1 Matches the silk screen
sign_z    | int  | 0, 1             | 1                                     | Sign to represent the polarity of the magnetic field. 1 Matches the silk screen
calibrationFile | string |  | 'calibration.cal' | If more than one magnetometer (for example on separate I2C buses or if an I2C mux is used), use a different filename for each. If set to `None` calibration is skipped.

### `PiicoDev_MMC5603.readMagnitude()`
Reads the magnetic field magnitude using the calibration generated during the calibration routine if available.
Parameter   | Type  | Range                    | Description | Unit
----------- | ----- | ------------------------ | ----------- | ------
returned    | float | 0.0 to 3000.0            | Magnitude field strength | uT

### `PiicoDev_MMC5603.readHeading()`
Reads the magnetic field bearing from true north.  If no declination is provided the result is a bearing from magnetic north.  Uses the calibration generated during the calibration routine if available.
Parameter   | Type  | Range        | Description | Unit
----------- | ----- | ------------ | ----------- | ------
returned    | float | 0.0 to 360.0 | Bearing from true north or magnetic north if no declination is set | deg

### `PiicoDev_MMC5603.readPolar()`
Reads the raw magnetic field magnitude and angle (degrees) in the X and Y plane.
Parameter   | Type  | Range                   | Description | Unit
----------- | ----- | ----------------------- | ----------- | ----
**Returns** | **Dictionary**
polar       | float | 0.0 to 360.0            | Raw bearing from magnetic north | deg
Gauss       | float | 0.0 to 3.0              | Magnetic field strength | Gauss
returned    | float | 0.0 to 3000.0            | Magnitude field strength | uT

### `PiicoDev_MMC5603.read()`
Reads the X, Y and Z components of the magnetic field.
Parameter   | Type | Range           | Description
----------- | ---- | --------------- | -----------
**Returns** | **Dictionary**
x           | float  | 0.0 to 3000.0 | X magnetic field component
y           | float  | 0.0 to 3000.0 | Y magnetic field component
z           | float  | 0.0 to 3000.0 | Z magnetic field component

### `PiicoDev_MMC5603.calibrate()`
Routine to calibrate the magnetometer.  Rotate the magnetometer in the X and Y or X, Y, & Z directions until the routine is complete.

### `PiicoDev_MMC5603.setOutputDataRate(odr)`
Sets the Output Data Rate.
Parameter | Type | Range  | Description
--------- | ---- | ------ | -----------
odr       | int  | 0 to 255 | Set the data rate in updates per second (Hz)

### `PiicoDev_MMC5603.setRange(range)`
A function left in for compatibility
Parameter | Type | Range  | Description
--------- | ---- | ------ | -----------
range     | int  | -inf to inf | Prints a string regarding compatability

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
