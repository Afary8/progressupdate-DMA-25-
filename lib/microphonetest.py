import time
import board
import analogio

# Setup analog input on A0 for microphone
mic = analogio.AnalogIn(board.A0)

# Settings
GRAPH_WIDTH = 50  # Width of the bar graph
UPDATE_DELAY = 0.05  # Update 20 times per second

print("Microphone Audio Visualizer")
print("Press Ctrl+C to stop\n")

# Variables to track baseline (quiet level)
baseline_samples = []
baseline_voltage = 1.65  # Default center voltage

# Collect baseline samples
print("Calibrating baseline (stay quiet)...")
for i in range(20):
    voltage = (mic.value * 3.3) / 65535
    baseline_samples.append(voltage)
    time.sleep(0.05)

baseline_voltage = sum(baseline_samples) / len(baseline_samples)
print(f"Baseline voltage: {baseline_voltage:.3f}V\n")

try:
    while True:
        # Read voltage
        voltage = (mic.value * 3.3) / 65535
        
        # Calculate deviation from baseline
        deviation = abs(voltage - baseline_voltage)
        
        # Scale deviation for display (adjust multiplier to change sensitivity)
        level = min(int(deviation * 100), GRAPH_WIDTH)
        
        # Create bar graph
        bar = '█' * level
        empty = '·' * (GRAPH_WIDTH - level)
        
        # Display
        print(f"{voltage:.3f}V |{bar}{empty}| {deviation:.4f}V  ", end='\r')
        
        time.sleep(UPDATE_DELAY)

except KeyboardInterrupt:
    print("\n\nStopped reading microphone")