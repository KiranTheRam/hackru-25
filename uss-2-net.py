import serial
import socket
import time

# Arduino and server details
arduino_port = "/dev/ttyACM0"  # Adjust as needed
baud_rate = 9600
server_host = "172.20.10.3"  # Change if server is remote

server_port = 12345

# Establish serial connection to Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    ser.flush()
    print(f"Connected to Arduino on {arduino_port}")

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(f"Received from Arduino: {line}")
            parts = line.split(',')
            if len(parts) == 2:
                car_id, event = parts[0], parts[1]
                if event == "finish":
                    # Send to server
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            s.connect((server_host, server_port))
                            s.sendall(line.encode())
                            print(f"Sent to server: {line}")
                        except Exception as e:
                            print(f"Error sending to server: {e}")

        time.sleep(0.03)  # 10ms delay

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()
