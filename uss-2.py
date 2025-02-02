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
            if "Sensor 1" in line:
                if "Object detected!" in line:
                    print("🔴 ALERT: Sensor 1 detected an object within 5 inches!")
                else:
                    print("✅ Sensor 1 area clear")

            elif "Sensor 2" in line:
                if "Object detected!" in line:
                    print("🔴 ALERT: Sensor 2 detected an object within 5 inches!")
                else:
                    print("✅ Sensor 2 area clear")

        time.sleep(0.01)  # Match Arduino's timing

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()
