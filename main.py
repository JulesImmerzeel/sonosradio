import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#displaystuff
from Adafruit_CharLCD import Adafruit_CharLCD
lcd = Adafruit_CharLCD(rs=26,en=19,d4=13,d5=6,d6=5,d7=3,cols=16,lines=2)
lcd.clear()
lcd.show_cursor(False)
lcd.blink(False)

def setMessage(chnl, volume):
    lcd.clear()
    message1 = chnl
    message2 = "Volume: " + str(volume)

    message = message1 + "\n" +  message2
    lcd.message(message)

#connection with sonos
from urllib import urlopen
# radio1 = 17523
# radio2 = 9483
# radio3 = 6707
# 538 = 6712
# studio Brussel = 2611

def radioAan(id):
    urlopen("http://localhost:5005/Tv-kamer/tunein/play/" + str(id))

def radioUit():
    urlopen("http://localhost:5005/Tv-kamer/pause/")
    
def volume(x):
    urlopen("http://localhost:5005/Tv-kamer/volume/" + str(x))

#volume control
import spidev # To communicate with SPI devices
from numpy import interp    # To scale values
from time import sleep  # To add delay
# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0)   
 
# Read MCP3008 data
def analogInput(channel=4):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

def x():
    volume = analogInput(4) # Reading from CH0
    volume = int(100 - interp(volume, [0, 1023], [0, 100]))
    print(int(volume))
    sleep(0.1)
    return volume

# button setup for the channel selectors
GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be annput pin and set initial value to be pulled low (off)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while True: # Run forever
    vol = None
    setMessage("Ready for use!", vol)
    if GPIO.input(15) == GPIO.HIGH:
        print("Button  15 was pushed!")
        radioAan(17523)
        setMessage("Radio 1", vol)
        while GPIO.input(15) == GPIO.HIGH:
            if x() != vol:
                setMessage("Radio 1", x())
                vol = x()
                volume(vol)
        radioUit()
    if GPIO.input(18) == GPIO.HIGH:
        print("Button  18 was pushed!")
        radioAan(9483)
        setMessage("Radio 2", vol)
        while GPIO.input(18) == GPIO.HIGH:
            if x() != vol:
                setMessage("Radio 2", x())
                vol = x()
                volume(vol)
        radioUit()
    if GPIO.input(23) == GPIO.HIGH:
        print("Button  23 was pushed!")
        radioAan(6707)
        setMessage("Radio 3", vol)
        while GPIO.input(23) == GPIO.HIGH:
            if x() != vol:
                setMessage("Radio 3", x())
                vol = x()
                volume(vol)
        radioUit()
    if GPIO.input(14) == GPIO.HIGH:
        print("Button 14 was pushed!")
        radioAan(6712)
        setMessage("Radio 538", vol)
        while GPIO.input(14) == GPIO.HIGH:
            if x() != vol:
                setMessage("Radio 538", x())
                vol = x()
                volume(vol)
        radioUit()
    if GPIO.input(24) == GPIO.HIGH:
        print("Button 24 was pushed!")
        radioAan(2611)
        setMessage("Studio Brussel", vol)
        while GPIO.input(24) == GPIO.HIGH:
            if x() != vol:
                setMessage("Studio Brussel", x())
                vol = x()
                volume(vol)
        radioUit()
        