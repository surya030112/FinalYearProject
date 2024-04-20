#import serial
import time

# Replace with the port your NodeMCU is connected to
port = 'COM9'

# Set the baud rate
baudrate = 9600

# Open the serial connection
ser = serial.Serial(port, baudrate)

while True:
    # Send the character 'y' to the NodeMCU
    ser.write(b'y')

    # Wait for 5 seconds
    time.sleep(5)
