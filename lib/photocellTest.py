import time
import board
import analogio

# Setup photocell on A1
photocell = analogio.AnalogIn(board.A1)

print("Photocell Test - Reading from A1")
print("Press Ctrl+C to stop\n")
print("Test your lighting conditions:")
print("- Cover the sensor with your hand (dark)")
print("- Shine a light on it (bright)")
print("- Normal room lighting\n")
print("-" * 60)
print("Raw Value | Voltage | Bar Graph")
print("-" * 60)

# Track min and max values
min_value = 65535
max_value = 0

try:
    while True:
        # Read raw value (0-65535)
        raw_value = photocell.value
        
        # Convert to voltage (0-3.3V)
        voltage = (raw_value * 3.3) / 65535
        
        # Update min/max tracking
        if raw_value < min_value:
            min_value = raw_value
        if raw_value > max_value:
            max_value = raw_value
        
        # Create bar graph (scale to 40 characters)
        bar_length = int((raw_value / 65535) * 40)
        bar = '█' * bar_length
        empty = '·' * (40 - bar_length)
        
        # Print current reading
        print(f"{raw_value:5d}     | {voltage:.3f}V  | {bar}{empty}", end='\r')
        
        time.sleep(0.1)  # Update 10 times per second

except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("Test Complete - Summary:")
    print("=" * 60)
    min_voltage = (min_value * 3.3) / 65535
    max_voltage = (max_value * 3.3) / 65535
    print(f"Minimum (darkest):  {min_value:5d} ({min_voltage:.3f}V)")
    print(f"Maximum (brightest): {max_value:5d} ({max_voltage:.3f}V)")
    print(f"Range: {max_value - min_value:5d} ({max_voltage - min_voltage:.3f}V)")
    print("\nUse these values to set your BRIGHT_THRESHOLD!")
    print(f"Suggested threshold: {(min_voltage + max_voltage) / 2:.3f}V (midpoint)")
    print("\nStopped reading photocell")