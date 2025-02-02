import serial
import time

arduino_port = "/dev/ttyACM0"  # Adjust as needed
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    ser.flush()
    print(f"Connected to {arduino_port}")

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            if "Object detected!" in line:
                print("🔴 ALERT: Object within 5 inches!")
            elif "No object" in line:
                print("✅ Area clear")
        time.sleep(0.01)  # Match Arduino's timing

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()
