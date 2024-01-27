import network

from machine import Pin

from logger import Logger
from microwebserver import MicroWebServer, WebHelper
import uasyncio

from motorcontroller import MotorController

# onboard led
led = Pin(2, Pin.OUT)

# left
in1 = Pin(15, Pin.OUT)  # 1=0,2=1=forward, 1=1,2=0=backward
in2 = Pin(13, Pin.OUT)  # 1=1,2=0=forward, 1=0,2=1=backward
# right
in3 = Pin(5, Pin.OUT)
in4 = Pin(4, Pin.OUT)

# Configure Logger
logger = Logger()
logger.info("main", "start")

# Connect to Wi-Fi
ssid = 'SSID'
password = 'PASSWORD'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    pass

logger.info("main", "wlan Connection successful")
logger.info("main", "wlan configuration: {}".format(station.ifconfig()))

motor = MotorController(in1, in2, in3, in4)


def show_overview():
    response = WebHelper.get_content_type_html()
    content = WebHelper.get_web_content("website.html")
    response += content.replace("{{SRV-ADDR}}", station.ifconfig()[0])
    return response


def show_left():
    motor.left()
    response = WebHelper.get_content_type_html()
    response += "left"
    return response


def show_right():
    motor.right()
    response = WebHelper.get_content_type_html()
    response += "right"
    return response


def show_left_stop():
    motor.left_stop()
    response = WebHelper.get_content_type_html()
    response += "left_stop"
    return response


def show_right_stop():
    motor.right_stop()
    response = WebHelper.get_content_type_html()
    response += "right_stop"
    return response


def show_backwards():
    motor.backward()
    response = WebHelper.get_content_type_html()
    response += "back"
    return response


def show_forwards():
    motor.forward()
    response = WebHelper.get_content_type_html()
    response += "forward"
    return response


def show_stop():
    motor.stop()
    response = WebHelper.get_content_type_html()
    response += "stop"
    return response


webserver = MicroWebServer(station.ifconfig()[0], 80)
webserver.add_get_handler("/", show_overview)
webserver.add_get_handler("/forward", show_forwards)
webserver.add_get_handler("/backward", show_backwards)
webserver.add_get_handler("/left", show_left)
webserver.add_get_handler("/left_stop", show_left_stop)
webserver.add_get_handler("/right", show_right)
webserver.add_get_handler("/right_stop", show_right_stop)
webserver.add_get_handler("/stop", show_stop)

event_loop = uasyncio.get_event_loop()
uasyncio.run(webserver.start_server())
event_loop.run_forever()
