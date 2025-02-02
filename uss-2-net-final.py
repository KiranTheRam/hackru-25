import serial
import socket
import time

# Arduino and server details
arduino_port = "/dev/ttyACM0"  # Adjust as needed
baud_rate = 9600
server_host = "172.20.10.3"  # Change if the server is remote
server_port = 12345

try:
    # Establish serial connection to Arduino
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    ser.flush()
    print(f"Connected to Arduino on {arduino_port}")

    # Variables to store finish order
    first_finisher = None
    second_finisher = None

    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(f"Received from Arduino: {line}")
            parts = line.split(',')
            if len(parts) == 2:
                car_id, event = parts[0], parts[1]

                if event == "finish":
                    if first_finisher is None:
                        first_finisher = car_id
                        print(f"🏁 {car_id} finished FIRST!")
                    elif second_finisher is None:
                        second_finisher = car_id
                        print(f"🏁 {car_id} finished SECOND!")

                    # Once both racers finish, send results in order
                    if first_finisher and second_finisher:
                        def send_to_server(car):
                            try:
                                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                    s.connect((server_host, server_port))
                                    s.sendall(f"{car},finish".encode())
                                    print(f"✅ Sent: {car},finish")
                            except Exception as e:
                                print(f"❌ Error sending to server: {e}")

                        send_to_server(first_finisher)
                        time.sleep(0.05)  # 50ms delay
                        send_to_server(second_finisher)

                        # Reset for next race
                        first_finisher = None
                        second_finisher = None

        time.sleep(0.03)  # Small delay

except serial.SerialException as e:
    print(f"Error: {e}")

except KeyboardInterrupt:
    print("\nExiting...")
    ser.close()
