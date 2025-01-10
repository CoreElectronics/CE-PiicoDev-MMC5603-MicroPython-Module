# Calibrate the sensor by turning it in a circle
# Display the heading with compensation for magnetic declination

from PiicoDev_MMC5603 import PiicoDev_MMC5603
from PiicoDev_Unified import sleep_ms          # Cross-platform compatible sleep function

compass = PiicoDev_MMC5603() # Initialise the sensor

# Calibration recommended for best results.
compass.calibrate() # only need to calibrate once

# Optional: Declination is the difference between magnetic-north and true-north ("heading") and depends on location
# compass.setDeclination(12.3) # Found with: https://www.magnetic-declination.com/Australia/Newcastle/122944.html

while True:
    heading = compass.readHeading()   # get the heading from the sensor
    if compass.dataValid():           # Rejects invalid data
        heading = round(heading)      # round to the nearest degree
        print( str(heading) + "°")    # print the data with a degree symbol
    sleep_ms(100)
