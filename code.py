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

titles = bitmap_label.Label(terminalio.FONT, scale=2)
titles.anchor_point = (.95, 0.5)
titles.anchored_position = (display.width // 2, display.height // 2)

co2_text = bitmap_label.Label(terminalio.FONT, scale=2)
co2_text.anchor_point = (0.4, 1.7)
co2_text.anchored_position = (display.width // 2, display.height // 2)

temp_text = bitmap_label.Label(terminalio.FONT, scale=2)
temp_text.anchor_point = (0.5, 0.5)
temp_text.anchored_position = (display.width // 2, display.height // 2)

rh_text = bitmap_label.Label(terminalio.FONT, scale=2)
rh_text.anchor_point = (-0.1, -0.7)
rh_text.anchored_position = (display.width // 2, display.height // 2)

main_group.append(titles)
main_group.append(co2_text)
main_group.append(temp_text)
main_group.append(rh_text)

print("Let's go!")
print(display.width)
print(display.height)

display.show(main_group)

titles.text = "CO2: \nTemp: \nHumidity: "

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
        
        co2_text.text = "{:.1f} PPM".format(scd.CO2)
        temp_text.text = "{:.1f} C".format(scd.temperature)
        rh_text.text = "{:.1f} % rH".format(scd.relative_humidity)
    time.sleep(0.5)
