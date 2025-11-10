import time
import board
import pwmio
import analogio
from digitalio import DigitalInOut, Direction
from adafruit_motor import servo

# ========================================
# HARDWARE SETUP
# ========================================

# Enable external power for servo
external_power = DigitalInOut(board.EXTERNAL_POWER)
external_power.direction = Direction.OUTPUT
external_power.value = True

# Setup servo on the dedicated servo pin
pwm = pwmio.PWMOut(board.EXTERNAL_SERVO, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

# Setup microphone on A0
mic = analogio.AnalogIn(board.A0)

# Setup photocell (light sensor) on A1
light_sensor = analogio.AnalogIn(board.A1)

# ========================================
# CONFIGURATION - Adjust these values!
# ========================================

CHECK_INTERVAL = 10  # How often to check sensors (seconds)
IGNORE_DURATION = 5  # How long to ignore sensors after servo moves (seconds)

# Servo positions
HAPPY_ANGLE = 0      # Servo angle when happy (mouth closed/neutral)
SAD_ANGLE = 180      # Servo angle when sad (mouth open/frown)

# Sensor enable/disable
USE_LIGHT_SENSOR = False  # Set to False to ignore photocell and only use sound

# Thresholds - you may need to adjust these based on your environment
LOUD_THRESHOLD = 1.68    # Sound deviation above this = loud
BRIGHT_THRESHOLD = 2.0   # Voltage above this = bright

# ========================================
# CALIBRATION FUNCTION
# ========================================

def calibrate_sensors():
    """
    Calibrate the microphone baseline and check light levels.
    This runs once at startup to understand the environment.
    """
    print("Calibrating sensors...")
    print("Please keep environment quiet for calibration...")
    
    # Collect microphone baseline samples (quiet level)
    mic_samples = []
    for i in range(20):
        voltage = (mic.value * 3.3) / 65535
        mic_samples.append(voltage)
        time.sleep(0.05)
    
    # Calculate average baseline (center voltage when quiet)
    baseline = sum(mic_samples) / len(mic_samples)
    
    # Check initial light level
    light_voltage = (light_sensor.value * 3.3) / 65535
    
    print(f"Microphone baseline: {baseline:.3f}V")
    print(f"Current light level: {light_voltage:.3f}V")
    print("Calibration complete!\n")
    
    return baseline

# ========================================
# SENSOR READING FUNCTIONS
# ========================================

def read_sound_level(baseline, num_samples=10):
    """
    Read the microphone and return the average sound level.
    We measure how much the voltage deviates from the quiet baseline.
    More deviation = louder sound.
    
    Args:
        baseline: The quiet voltage level from calibration
        num_samples: How many readings to average together
    
    Returns:
        Average deviation from baseline (0 = quiet, higher = louder)
    """
    total_deviation = 0
    
    for i in range(num_samples):
        voltage = (mic.value * 3.3) / 65535
        # Calculate how far we are from the quiet baseline
        deviation = abs(voltage - baseline)
        total_deviation += deviation
        time.sleep(0.01)  # Small delay between samples
    
    # Return average deviation
    return total_deviation / num_samples

def read_light_level():
    """
    Read the photocell and return the voltage.
    Higher voltage = brighter light.
    If USE_LIGHT_SENSOR is False, returns 0 (always dark).
    
    Returns:
        Voltage from photocell (0-3.3V) or 0 if disabled
    """
    if not USE_LIGHT_SENSOR:
        return 0  # Always return "dark" if light sensor is disabled
    
    return (light_sensor.value * 3.3) / 65535

# ========================================
# STATE DETERMINATION
# ========================================

def should_be_happy(sound_level, light_level):
    """
    Determine if the robot should be happy based on environment.
    Happy = quiet AND dark (if light sensor enabled)
    Happy = quiet only (if light sensor disabled)
    Sad = loud OR bright
    
    Args:
        sound_level: Current sound deviation from baseline
        light_level: Current light voltage
    
    Returns:
        True if should be happy, False if should be sad
    """
    is_quiet = sound_level < LOUD_THRESHOLD
    is_dark = light_level < BRIGHT_THRESHOLD
    
    # If light sensor is disabled, only check sound
    if not USE_LIGHT_SENSOR:
        return is_quiet
    
    # Robot is happy only when BOTH quiet AND dark
    return is_quiet and is_dark

# ========================================
# SERVO CONTROL
# ========================================

def set_mood(is_happy, current_state):
    """
    Move the servo to match the desired mood (if different from current).
    
    Args:
        is_happy: True if should be happy, False if should be sad
        current_state: Current state ("happy" or "sad")
    
    Returns:
        New state after potential change ("happy" or "sad")
        Boolean indicating if state changed (True if moved servo)
    """
    if is_happy and current_state != "happy":
        print("😊 Switching to HAPPY (quiet and dark)")
        my_servo.angle = HAPPY_ANGLE
        return "happy", True
    
    elif not is_happy and current_state != "sad":
        print("😢 Switching to SAD (too loud or too bright)")
        my_servo.angle = SAD_ANGLE
        return "sad", True
    
    else:
        # No change needed
        return current_state, False

# ========================================
# MAIN PROGRAM
# ========================================

def main():
    print("=" * 50)
    print("INTROVERTED ROBOT")
    print("=" * 50)
    if USE_LIGHT_SENSOR:
        print("The robot is happy when it's quiet and dark.")
        print("It gets sad when it's loud or bright.")
    else:
        print("The robot is happy when it's quiet.")
        print("It gets sad when it's loud.")
        print("(Light sensor disabled)")
    print(f"Checking every {CHECK_INTERVAL} seconds...")
    print("=" * 50)
    print()
    
    # Calibrate sensors on startup
    mic_baseline = calibrate_sensors()
    
    # Start in happy state (assume quiet and dark initially)
    current_state = "happy"
    my_servo.angle = HAPPY_ANGLE
    print(f"Starting in HAPPY state (servo at {HAPPY_ANGLE}°)\n")
    
    # Main loop
    try:
        while True:
            # Read current environment
            sound_level = read_sound_level(mic_baseline)
            light_level = read_light_level()
            
            # Display current readings
            light_status = f"Light: {light_level:.2f}V" if USE_LIGHT_SENSOR else "Light: DISABLED"
            print(f"Sound: {sound_level:.4f}V  |  {light_status}  |  State: {current_state.upper()}")
            
            # Determine if robot should be happy or sad
            should_be_happy_now = should_be_happy(sound_level, light_level)
            
            # Update mood and check if we moved the servo
            current_state, state_changed = set_mood(should_be_happy_now, current_state)
            
            # If we moved the servo, ignore sensors during the movement
            if state_changed:
                print(f"Ignoring sensors for {IGNORE_DURATION} seconds (servo moving)...")
                time.sleep(IGNORE_DURATION)
                print("Ready to check sensors again\n")
            
            # Wait before next check
            print(f"Waiting {CHECK_INTERVAL} seconds until next check...\n")
            time.sleep(CHECK_INTERVAL)
    
    except KeyboardInterrupt:
        print("\n\nRobot stopped")
        # Return to happy state when stopping
        my_servo.angle = HAPPY_ANGLE

# Run the program
main()