# # Install dependencies
# sudo apt-get update
# sudo apt-get install -y python3-pip gpsd gpsd-clients

# # Install Python libraries
# sudo pip3 install pyserial pynmea2

import serial
import time

# Define the serial port
port = "/dev/ttyAMA0"  # For Pi 3+ and newer use "/dev/ttyS0"
baud_rate = 9600

# Set up the serial connection
ser = serial.Serial(port, baud_rate, timeout=1)

try:
    print("Starting GPS reading...")
    while True:
        # Read one line from GPS module
        line = ser.readline().decode('ascii', errors='replace').strip()
        
        if line:  # Only print non-empty lines
            print(line)
        
        time.sleep(0.1)  # Small delay
        
except KeyboardInterrupt:
    print("\nProgram terminated by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    ser.close()
    print("Serial connection closed")