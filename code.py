import time
import board
import busio
import terminalio
import adafruit_scd30
from displayio import Group
from adafruit_display_text import bitmap_label

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
display = board.DISPLAY
main_group = Group()

green=0x00ff00
yellow=0xffff00
red=0xff0000

co2_text = bitmap_label.Label(terminalio.FONT, scale=2)
co2_text.anchor_point = (0.0, 2.5)
co2_text.anchored_position = (0, display.height // 2)

temp_text = bitmap_label.Label(terminalio.FONT, scale=2)
temp_text.anchor_point = (0.0, 0.5)
temp_text.anchored_position = (0, display.height // 2)

rh_text = bitmap_label.Label(terminalio.FONT, scale=2)
rh_text.anchor_point = (0.0, -1.3)
rh_text.anchored_position = (0, display.height // 2)

main_group.append(co2_text)
main_group.append(temp_text)
main_group.append(rh_text)

print("Let's go!")
print(display.width)
print(display.height)

display.show(main_group)

while True:
    if scd.data_available:
        if scd.CO2 <= 800:
            co2_text.color = green
        elif scd.CO2 > 800 and scd.CO2 <= 1200:
            co2_text.color = yellow
        else:
            co2_text.color = red
        
        if scd.temperature >= 16 and scd.temperature <= 26:
            temp_text.color = green
        elif scd.temperature > 12 and scd.temperature < 16:
            temp_text.color = yellow
        elif scd.temperature > 26 and scd.temperature < 30:
            temp_text.color = yellow
        else:
            temp_text.color = red
        
        if scd.relative_humidity >= 75:
            rh_text.color = green
        elif scd.relative_humidity > 60 and scd.relative_humidity < 75:
            rh_text.color = yellow
        else:
            rh_text.color = red
        
        co2_text.text = "CO2: {} PPM".format(scd.CO2)
        temp_text.text = "Temp: {:.1f}".format(scd.temperature)
        rh_text.text = "Humidity {:.1f} % rH".format(scd.relative_humidity)
    time.sleep(0.5)
