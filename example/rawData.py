# Prints the raw axis readings in micro-Tesla

from PiicoDev_MMC5603 import PiicoDev_MMC5603
from PiicoDev_Unified import sleep_ms

magSensor = PiicoDev_MMC5603() # Initialise the sensor
while True:
    raw_data = magSensor.read() # Read the field strength on each axis in uT
#    raw_data = magSensor.read(raw=True) # Read the raw, unscaled data on each axis
    print(raw_data)             # Print the data
    sleep_ms(200)
