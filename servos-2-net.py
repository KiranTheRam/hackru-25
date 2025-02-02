import serial
import socket
import time

# Adjust the port based on your OS
SERIAL_PORT = "/dev/ttyACM0"  # Linux/Mac
# SERIAL_PORT = "COM3"  # Windows (Change to the correct COM port)

BAUD_RATE = 9600
SERVER_HOST = "172.20.10.3"  # Change if server is remote
SERVER_PORT = 12345


def send_to_server(message):
    """Send a message to the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.sendall(message.encode())
            print(f"Sent to server: {message}")
        except Exception as e:
            print(f"Error sending to server: {e}")


def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    input("Press Enter to start the race...")  # Wait for user input

    ser.write(b"start\n")  # Send command to Arduino
    time.sleep(1)  # Wait a moment to ensure Arduino processes it

    # Notify the server that both cars have started
    send_to_server("1,start")
    send_to_server("2,start")

    ser.close()


if __name__ == "__main__":
    main()
