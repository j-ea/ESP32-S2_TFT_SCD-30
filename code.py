import time
import board
import busio
import terminalio
import adafruit_scd30
from displayio import Group
from adafruit_display_text import bitmap_label

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)
text_area = bitmap_label.Label(terminalio.FONT, scale=2)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (board.DISPLAY.width // 2, board.DISPLAY.height // 2)

main_group = Group()

main_group.append(text_area)

print("Let Go!")

board.DISPLAY.show(main_group)

while True:
    if scd.data_available:
        text_area.text = "CO2: {} PPM \nTemp: {:.1f} C \nHumidity {:.1f} % rH".format(scd.CO2, scd.temperature, scd.relative_humidity)
    time.sleep(0.5)
