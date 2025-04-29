import Adafruit_DHT
import time
import Rpi.GPIO as GPIO

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

while True: 
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f'Temperature={temperature}*C Humidity={humidity}%')
    else:
        print('Failed to get reading. Try again!')
    time.sleep(2)

