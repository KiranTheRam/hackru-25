import serial
import serial.tools.list_ports
import time

# First, let's list all available ports
print("Available ports:")
ports = list(serial.tools.list_ports.comports())
for port in ports:
    print(f"- {port}")

# Look specifically for Arduino port (ttyACM*)
arduino_port = None
for port in ports:
    if 'ttyACM' in port.device:
        arduino_port = port.device
        break

if arduino_port:
    try:
        print(f"\nTrying to connect to Arduino on {arduino_port}...")
        ser = serial.Serial(arduino_port, 9600, timeout=1)
        ser.reset_input_buffer()
        print(f"Connected to {arduino_port}")

        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace').strip()
                if line:
                    print(f"Received: {line}")
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'ser' in locals():
            ser.close()
else:
    print("\nNo Arduino found! Make sure it's connected and the correct code is uploaded.")