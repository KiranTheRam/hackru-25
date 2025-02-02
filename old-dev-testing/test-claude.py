import serial  # Add this import!
import time
import sys


def test_serial(port="/dev/ttyACM1", baud_rate=9600):
    try:
        # Open serial port
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {port}")

        # Clear any stored data
        ser.flush()

        # Read and print data
        while True:
            if ser.in_waiting:
                try:
                    line = ser.readline().decode('utf-8').strip()
                    if line:
                        print(f"Raw data: {line}")
                except UnicodeDecodeError:
                    print("Error decoding line")
            time.sleep(0.1)

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        print("\nTrying to list available ports...")
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        if ports:
            print("\nAvailable ports:")
            for port in ports:
                print(f"- {port}")
        else:
            print("No ports found!")

    except KeyboardInterrupt:
        print("\nExiting...")
        if 'ser' in locals():
            ser.close()


if __name__ == "__main__":
    # Allow port to be specified as command line argument
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    test_serial(port)