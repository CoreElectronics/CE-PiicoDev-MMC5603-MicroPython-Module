from PiicoDev_Unified import *
import math
import time

class PiicoDev_MMC5603(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr=0x30, odr=100, calibrationFile='calibration.cal', suppress_warnings=False):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
        self._ctrl2_cache = 0x00
        
        self.calibrationFile = calibrationFile
        self.suppress_warnings = suppress_warnings
        
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        self.declination = 0
        self.data = {}

        # Perform initialization
        self.reset()
        self.setOutputDataRate(odr)
        self.enableContinuousMode()
        if calibrationFile is not None:
            self.loadCalibration()
        sleep_ms(5)

    def reset(self):
        """Reset the sensor."""
        self.i2c.writeto_mem(self.addr, 0x1C, bytes([0x80]))
        time.sleep(0.02)

    def setOutputDataRate(self, odr):
        """Set the output data rate."""
        if not (1 <= odr <= 255):
            raise ValueError("ODR must be between 1 and 255.")
        self.i2c.writeto_mem(self.addr, 0x1A, bytes([odr]))

    def setRange(self, range):
        """Set the range (not directly configurable, placeholder for compatibility)."""
        pass  # MMC5603 has a fixed range; this function is provided for interface consistency.

    def enableContinuousMode(self):
        """Enable continuous measurement mode."""
        self.i2c.writeto_mem(self.addr, 0x1B, bytes([0x80]))  # Enable CMM frequency
        self._ctrl2_cache |= 0x10  # Enable continuous mode
        self.i2c.writeto_mem(self.addr, 0x1D, bytes([self._ctrl2_cache]))

    def read(self, raw=False):
        """Read raw magnetic field data in microteslas (uT)."""
        data_ready = False
        for _ in range(10):  # Timeout loop
            status = int.from_bytes(self.i2c.readfrom_mem(self.addr, 0x18, 1), 'big')
            if status & 0x04:  # Data ready bit
                data_ready = True
                break
            time.sleep(0.001)
        
#         if not data_ready:
#             raise RuntimeError("Data not ready.")
        # Read 9 bytes of raw magnetic data
        raw_data = self.i2c.readfrom_mem(self.addr, 0x00, 9)
        x = ((raw_data[0] << 12) | (raw_data[1] << 4) | (raw_data[6] >> 4)) - (1 << 19)
        y = ((raw_data[2] << 12) | (raw_data[3] << 4) | (raw_data[7] >> 4)) - (1 << 19)
        z = ((raw_data[4] << 12) | (raw_data[5] << 4) | (raw_data[8] >> 4)) - (1 << 19)

        if raw:
            return {'x': x, 'y': y, 'z': z}
        else:
            scale = 0.00625  # Conversion factor to microteslas
            return {'x': (x  - self.x_offset)* scale, 'y': (y - self.y_offset) * scale , 'z': (z - self.z_offset) * scale }

    def readMagnitude(self):
        """Calculate the magnitude of the magnetic field."""
        data = self.read()
        return math.sqrt(data['x'] ** 2 + data['y'] ** 2 + data['z'] ** 2)

    def readHeading(self):
        """Calculate the heading (angle in degrees)."""
        data = self.read()
        heading = math.atan2(data['y'], data['x']) * (180 / math.pi)
        if heading < 0:
            heading += 360
        return heading

    def readPolar(self):
        """Read the magnitude and heading."""
        magnitude = self.readMagnitude()
        heading = self.readHeading()
        return {'magnitude': magnitude, 'heading': heading}

    def calibrate(self, enable_logging=False, disable_z=True):
        try:
            self.setOutputDataRate(3)
        except Exception as e:
            print(i2c_err_str.format(self.addr))
            raise e
        x_min = 65535
        x_max = -65535
        y_min = 65535
        y_max = -65535
        z_min = 65535
        z_max = -65535
        log = ''
        print('*** Calibrating.\n    Slowly rotate your sensor until the bar is full')
        print('[          ]', end='')
        range = 1000
        i = 0
        x=0;y=0;z=0;
        a=0.5 # EMA filter weight
        while i < range:
            i += 1
            sleep_ms(5)
            d = self.read(raw=True)
            x = a*d['x'] + (1-a)*x # EMA filter
            y = a*d['y'] + (1-a)*y
            z = a*d['z'] + (1-a)*z
            if x < x_min: x_min = x; i=0
            if x > x_max: x_max = x; i=0
            if y < y_min: y_min = y; i=0
            if y > y_max: y_max = y; i=0
            if disable_z:
                if z < z_min: z_min = z; i=0
                if z > z_max: z_max = z; i=0
            j = round(10*i/range);
            print( '\015[' + int(j)*'*' + int(10-j)*' ' + ']'+'     ' +(str(d['x']) + ',' + str(d['y']) + ',' + str(d['z'])), end='') # print a progress bar
            if enable_logging:
                log = log + (str(d['x']) + ',' + str(d['y']) + ',' + str(d['z']) + '\n')
#         self.setOutputDataRate(self.odr) # set the output data rate back to the user selected rate
        self.x_offset = (x_max + x_min) / 2
        self.y_offset = (y_max + y_min) / 2
        self.z_offset = (z_max + z_min) / 2
        f = open(self.calibrationFile, "w")
        f.write('x_min:\n' + str(x_min) + '\nx_max:\n' + str(x_max) + '\ny_min:\n' + str(y_min) + '\ny_max:\n' + str(y_max) + '\nz_min\n' + str(z_min) + '\nz_max:\n' + str(z_max) + '\nx_offset:\n')
        f.write(str(self.x_offset) + '\ny_offset:\n' + str(self.y_offset) + '\nz_offset:\n' + str(self.z_offset))
        f.close()
        if enable_logging:
            flog = open("calibration.log", "w")
            flog.write(log)
            flog.close

    def loadCalibration(self):
        try:
            f = open(self.calibrationFile, "r")
            for i in range(13): f.readline()
            self.x_offset = float(f.readline())
            f.readline()
            self.y_offset = float(f.readline())
            f.readline()
            self.z_offset = float(f.readline())
            sleep_ms(5)
        except:
            if not self.suppress_warnings:
                print("No calibration file found. Run 'calibrate()' for best results.  Visit https://piico.dev/p15 for more info.")
            sleep_ms(1000)
