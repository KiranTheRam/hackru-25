import serial

# Adjust COM port for Windows (e.g., "COM3") or "/dev/ttyUSB0" for Linux/macOS
arduino_port = "/dev/ttyACM0"  # Change this based on your system
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to {arduino_port}")

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(f"Sensor State: {line}")  # 1 = no car, 0 = car detected

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()
