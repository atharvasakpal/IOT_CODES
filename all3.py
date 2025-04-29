import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# GPIO Pin Definitions
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
DHT_PIN = board.D4  # Using board pin numbering
TRIG = 5
ECHO = 6
IR_SENSOR = 16

# Initialize DHT11 Sensor
dht_device = adafruit_dht.DHT11(DHT_PIN)

# LCD Constants
LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

# Initialize GPIO
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(IR_SENSOR, GPIO.IN)

# Send data to LCD
def lcd_send_byte(bits, mode):
    GPIO.output(LCD_RS, mode)
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()
    
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

# Toggle LCD enable pin
def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)

# Initialize LCD
def lcd_init():
    lcd_send_byte(0x33, LCD_CMD)
    lcd_send_byte(0x32, LCD_CMD)
    lcd_send_byte(0x28, LCD_CMD)
    lcd_send_byte(0x0C, LCD_CMD)
    lcd_send_byte(0x06, LCD_CMD)
    lcd_send_byte(0x01, LCD_CMD)
    time.sleep(0.005)

# Display text on LCD
def lcd_display(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_send_byte(line, LCD_CMD)
    for char in message:
        lcd_send_byte(ord(char), LCD_CHR)

# Measure distance using HC-SR04
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
    
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    return round(distance, 2)

# Read DHT11 sensor
def read_dht11():
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        return temperature, humidity
    except RuntimeError as error:
        print("DHT Read Error:", error)
        return None, None

# Main loop
def main():
    init_gpio()
    lcd_init()
    
    try:
        while True:
            # Read temperature and humidity
            temperature, humidity = read_dht11()
            if temperature is not None and humidity is not None:
                temp_str = f"Temp: {temperature}C"
                humid_str = f"Hum: {humidity}%"
            else:
                temp_str = "Temp: Error"
                humid_str = "Hum: Error"
            
            # Read distance
            distance = measure_distance()
            distance_str = f"Dist: {distance} cm"
            
            # Read IR sensor status
            ir_status = "Object!" if GPIO.input(IR_SENSOR) == 0 else "No Object"
            
            # Display data on LCD
            lcd_display(temp_str, LCD_LINE_1)
            time.sleep(1)
            lcd_display(humid_str, LCD_LINE_2)
            time.sleep(1)
            lcd_display(distance_str, LCD_LINE_1)
            time.sleep(1)
            lcd_display(ir_status, LCD_LINE_2)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Program Stopped")
        GPIO.cleanup()

if __name__ == "__main__":
    main()