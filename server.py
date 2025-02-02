import socket
import time
from threading import Thread

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345  # Port for communication

car_times = {}  # Dictionary to store start and finish times
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            print(f"Received: {data}")
            parts = data.split(',')
            if len(parts) == 2:
                car_id, event = parts[0], parts[1]
                if event == "start":
                    car_times[car_id] = time.time()
                elif event == "finish" and car_id in car_times:
                    finish_time = time.time() - car_times[car_id]
                    print(f"Car {car_id} finished in {finish_time:.3f} seconds")
                    car_times[car_id] = finish_time  # Store final time
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()