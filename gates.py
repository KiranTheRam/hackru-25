import serial

# Adjust the port based on your OS
SERIAL_PORT = "/dev/ttyACM0"  # Linux/Mac
# SERIAL_PORT = "COM3"  # Windows (Change to the correct COM port)

BAUD_RATE = 9600

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    input("Press Enter to move servos...")  # Wait for user input
    ser.write(b"MOVE\n")  # Send command to Arduino
    ser.close()

if __name__ == "__main__":
    main()
