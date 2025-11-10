import board
import analogio
import time

analog_in = analogio.AnalogIn(board.A0)

while True:
    voltage = (analog_in.value * 3.3) / 65535
    print(f"Raw: {analog_in.value}")
    print(f"Voltage: {voltage:.2f}V")
    time.sleep(0.1)