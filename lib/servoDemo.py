import time
import board
import pwmio
from digitalio import DigitalInOut, Direction
from adafruit_motor import servo

# Enable external power pin - REQUIRED for servo to work
# This powers the servo, NeoPixels, and speaker
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

# Setup servo on the dedicated servo pin
pwm = pwmio.PWMOut(board.EXTERNAL_SERVO, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

# Example 1: Move servo to specific angles
print("Movixng to 5 degrees")
my_servo.angle = 1
time.sleep(5)

# print("Moving to 90 degrees")
# my_servo.angle = 90
# time.sleep(5)

print("Moving to 180 degrees")
my_servo.angle = 180
time.sleep(5)

# # Example 2: Sweep back and forth
# print("Starting sweep")
# angle = 0
# angle_increasing = True


# print("Moving to 270 degrees")
# my_servo.angle = 180
# time.sleep(5)

# while True:
#     my_servo.angle = angle
    
#     if angle_increasing:
#         angle += 5
#         if angle >= 180:
#             angle_increasing = False
#     else:
#         angle -= 5
#         if angle <= 0:
#             angle_increasing = True
    
#     time.sleep(0.05)  # Adjust speed of movement