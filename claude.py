import serial
import socket
import time
import sys
from datetime import datetime


class RaceMonitor:
    def __init__(self, port="/dev/ttyACM1", baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None
        self.car1_finished = False
        self.car2_finished = False

    def connect_to_arduino(self):
        """Attempt to connect to Arduino with retry logic"""
        max_attempts = 5
        attempt = 0

        while attempt < max_attempts:
            try:
                self.serial = serial.Serial(self.port, self.baud_rate, timeout=1)
                self.serial.flush()
                print(f"{self._get_timestamp()} Connected to Arduino on {self.port}")
                return True
            except serial.SerialException as e:
                attempt += 1
                print(f"{self._get_timestamp()} Connection attempt {attempt} failed: {e}")
                if attempt < max_attempts:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)

        return False

    def _get_timestamp(self):
        """Return current timestamp for logging"""
        return datetime.now().strftime("[%Y-%m-%d %H:%M:%S.%f]")

    def process_line(self, line):
        """Process a line received from Arduino"""
        try:
            if line.endswith("finish"):
                car_id, event = line.split(',')
                if car_id == "1":
                    self.car1_finished = True
                    print(f"{self._get_timestamp()} Car 1 finished!")
                elif car_id == "2":
                    self.car2_finished = True
                    print(f"{self._get_timestamp()} Car 2 finished!")

                if self.car1_finished and self.car2_finished:
                    print(f"{self._get_timestamp()} Race complete! Both cars finished.")

            elif line == "RESET":
                self.car1_finished = False
                self.car2_finished = False
                print(f"{self._get_timestamp()} Race reset, ready for new race")

            # Debug messages from Arduino
            elif line.startswith("Status"):
                print(f"{self._get_timestamp()} {line}")

        except Exception as e:
            print(f"{self._get_timestamp()} Error processing line '{line}': {e}")

    def run(self):
        """Main loop to read from Arduino"""
        if not self.connect_to_arduino():
            print("Failed to connect to Arduino after maximum attempts")
            return

        print(f"{self._get_timestamp()} Starting race monitor...")

        try:
            while True:
                if self.serial.in_waiting:
                    line = self.serial.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        self.process_line(line)
                time.sleep(0.01)  # Small delay to prevent CPU overuse

        except KeyboardInterrupt:
            print(f"\n{self._get_timestamp()} Shutting down gracefully...")
        except Exception as e:
            print(f"{self._get_timestamp()} Unexpected error: {e}")
        finally:
            if self.serial:
                self.serial.close()
                print(f"{self._get_timestamp()} Serial connection closed")


if __name__ == "__main__":
    # Allow port to be specified as command line argument
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM1"

    monitor = RaceMonitor(port=port)
    monitor.run()