import time
import board
import analogio

# Read pressure/photoresistors on A0, A1, A2 and print values every 0.5s
sensor0 = analogio.AnalogIn(board.A0)
sensor1 = analogio.AnalogIn(board.A1)
sensor2 = analogio.AnalogIn(board.A2)

while True:
    v0 = sensor0.value                  # 0..65535
    p0 = int((v0 * 100) / 65535)        # % approx

    v1 = sensor1.value                  # 0..65535
    p1 = int((v1 * 100) / 65535)        # % approx

    v2 = sensor2.value                  # 0..65535
    p2 = int((v2 * 100) / 65535)        # % approx

    # Fixed-width columns so labels don't shift as values change
    # Uses spaces and field widths instead of tabs
    print(
        "A0: {v0:5d} ({p0:3d}%) | A1: {v1:5d} ({p1:3d}%) | A2: {v2:5d} ({p2:3d}%)".format(
            v0=v0, p0=p0, v1=v1, p1=p1, v2=v2, p2=p2
        )
    )
    time.sleep(0.5)


