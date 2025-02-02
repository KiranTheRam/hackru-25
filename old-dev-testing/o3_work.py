import serial
import serial.tools.list_ports
import time

DEBUG = False  # Set to True to print raw serial data for debugging


def parse_sensor_readings(line):
    """
    Given a line like:
      Sensor1: 56.18 cm    Sensor2: 58.86 cm
    this function extracts the two distances as floats.
    If parsing fails, returns (None, None).
    """
    try:
        # Check that the line contains both sensor labels.
        if "Sensor1:" not in line or "Sensor2:" not in line:
            return None, None

        # Extract Sensor1 reading.
        parts1 = line.split("Sensor1:")
        after_sensor1 = parts1[1]
        d1_str = after_sensor1.split("cm")[0].strip()
        distance1 = float(d1_str)

        # Extract Sensor2 reading.
        parts2 = line.split("Sensor2:")
        after_sensor2 = parts2[1]
        d2_str = after_sensor2.split("cm")[0].strip()
        distance2 = float(d2_str)

        return distance1, distance2
    except Exception as e:
        if DEBUG:
            print("Parsing error:", e, "for line:", line)
        return None, None


# List available ports and try to find an Arduino port (assumes it contains "ttyACM")
print("Available ports:")
ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(f"- {port}")

arduino_port = None
for port in ports:
    if 'ttyACM' in port.device:
        arduino_port = port.device
        break

if not arduino_port:
    print("\nNo Arduino found! Make sure it's connected and the correct code is uploaded.")
    exit(1)

try:
    print(f"\nTrying to connect to Arduino on {arduino_port}...")
    ser = serial.Serial(arduino_port, 115200, timeout=1)
    time.sleep(2)  # Give Arduino time to reset
    ser.reset_input_buffer()
    print(f"Connected to {arduino_port}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Configuration values.
THRESHOLD = 10.0  # cm; the detection threshold
CLEAR_THRESHOLD = THRESHOLD * 2  # cm; clear condition threshold

while True:
    # Reset flags for a new detection cycle.
    sensor1_triggered = False
    sensor2_triggered = False
    sensor1_time = None
    sensor2_time = None
    print(f"\nWaiting for both sensors to detect an object within {THRESHOLD} cm...")

    # Wait until both sensors have detected an object within THRESHOLD.
    while not (sensor1_triggered and sensor2_triggered):
        if ser.in_waiting:
            raw_line = ser.readline().decode('utf-8', errors='replace').strip()
            if DEBUG:
                print("Raw reading:", raw_line)
            if raw_line:
                d1, d2 = parse_sensor_readings(raw_line)
                if d1 is not None and d2 is not None:
                    # Only trigger if the reading is below THRESHOLD and is nonzero.
                    if not sensor1_triggered and d1 < THRESHOLD and d1 > 0:
                        sensor1_triggered = True
                        sensor1_time = time.time()
                        print(f"Sensor1 triggered (distance: {d1} cm)")
                    if not sensor2_triggered and d2 < THRESHOLD and d2 > 0:
                        sensor2_triggered = True
                        sensor2_time = time.time()
                        print(f"Sensor2 triggered (distance: {d2} cm)")
        time.sleep(0.05)  # Small delay to avoid hogging the CPU

    # Determine which sensor was triggered first.
    if sensor1_time is not None and sensor2_time is not None:
        if sensor1_time < sensor2_time:
            print(">>> Sensor1 detected an object within threshold first!")
        elif sensor2_time < sensor1_time:
            print(">>> Sensor2 detected an object within threshold first!")
        else:
            print(">>> Both sensors triggered simultaneously!")
    else:
        print("Unexpected error: one sensor's trigger time is None.")

    # Wait until both sensors are clear.
    # Clear means both sensor readings must be above CLEAR_THRESHOLD.
    print(f"Waiting for both sensors to clear (readings above {CLEAR_THRESHOLD} cm)...")
    while True:
        if ser.in_waiting:
            raw_line = ser.readline().decode('utf-8', errors='replace').strip()
            if DEBUG:
                print("Raw reading while waiting to clear:", raw_line)
            d1, d2 = parse_sensor_readings(raw_line)
            if d1 is not None and d2 is not None:
                if d1 > CLEAR_THRESHOLD and d2 > CLEAR_THRESHOLD:
                    print("Both sensors are clear. Ready for the next detection cycle.\n")
                    break
        time.sleep(0.05)

    # Wait for 5 seconds before starting a new detection cycle.
    print("Waiting for 5 seconds before restarting the detection cycle...")
    time.sleep(5)
