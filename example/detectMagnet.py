# Read the magnetic field strength and determine if a magnet is nearby

from PiicoDev_MMC5603 import PiicoDev_MMC5603
from PiicoDev_Unified import sleep_ms

magSensor = PiicoDev_MMC5603() # initialise the magnetometer
# magSensor.calibrate()

threshold = 120 # microTesla or 'uT'.

while True:

    strength = magSensor.readMagnitude()       # Reads the magnetic-field strength in microTesla (uT)
    if compass.dataValid():                    # Rejects invalid data
        myString = str(strength) + ' uT'       # create a string with the field-strength and the unit
        print(myString)                        # Print the field strength
        
        if strength > threshold:               # Check if the magnetic field is strong
            print('Strong Magnet!')

    sleep_ms(1000)
