from machine import ADC, Pin
from time import sleep

# Use the correct pin for your sensor (GP26 = ADC0)
moisture = ADC(Pin(26))

min_raw = 30000
max_raw = 65535

while True:
    value = moisture.read_u16()
    percent = (max_raw - value) / (max_raw - min_raw) * 100
    percent = max(0, min(percent, 100))  # Clamp between 0 and 100

    # Determine the "height" level (1 to 6)
    Depth = int(percent // (100/6)) + 1
    if Depth > 6:
        Depth = 6

    if value >= 60000:
        print("Dry | Moisture: {:.2f}% | Depth: {}/6".format(percent, Depth))
    else:
        print("Wet | Moisture: {:.2f}% | Depth: {}/6".format(percent, Depth))
    sleep(0.5)
    