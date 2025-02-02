import serial

arduino_port = "/dev/ttyACM0"  # Adjust if necessary
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    ser.flush()
    print(f"Connected to {arduino_port}")

    prev_state = None  # Store previous state

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            try:
                sensor1, sensor2 = map(int, line.split(","))
                current_state = (sensor1, sensor2)

                if current_state != prev_state:
                    print(f"Sensor States: {sensor1}, {sensor2}")
                    prev_state = current_state  # Update previous state

            except ValueError:
                pass  # Ignore incomplete or corrupted data

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()
