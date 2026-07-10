from machine import Pin, SoftI2C
import ssd1306
import onewire
import ds18x20
import time

import LED


# OLED screen display

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# DS18B20 sensor and configuration

dat = Pin(4)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(dat))

roms = ds_sensor.scan()

print("Devices Found:", roms)


# LED = A red LED that blinks upon the sensor working

led = Pin(18, Pin.OUT)


# Buzzer = It buzzes once the temperature exceeds 30 degrees

buzzer = Pin(19, Pin.OUT)


# Button = To turn everythin on or off

button = Pin(15, Pin.IN, Pin.PULL_UP)


# Main Loop

while True:

    ds_sensor.convert_temp()

    time.sleep_ms(750)

    for rom in roms:

        temp = ds_sensor.read_temp(rom)

        print("Temperature:", temp)

        oled.fill(0)

        oled.text("TEMP MONITOR", 10, 0)

        oled.text("Temperature:", 0, 20)

        oled.text("{:.2f} C".format(temp), 15, 35)

        # LED always ON
        led.value(1)

        if temp > 35:

            buzzer.value(1)

            oled.text("WARNING!", 20, 52)

        else:

            buzzer.value(0)

        oled.show()

    time.sleep(1)