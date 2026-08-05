import zmq
import json
from pathlib import Path

# Colors:
BG_COLOR = "#000000"
HEADER_COLOR = "#FF2600"
BUTTON_COLOR = "#941100"
SELECTED_COLOR = "#FF2600"
BODY_COLOR = "#FFFFFF"
SETTING_COLOR = "#111111"
SETTING_SEL = "#222222"

# Font styles:
HEADER_FONT = "Herculanum"
BODY_FONT = "Bodoni 72"

small_size = 20
medium_size = 25
large_size = 30

slow_speed = 33
medium_speed = 15
fast_speed = 1

FONT_SIZE = medium_size

FONT_SPEED = medium_speed

# Name:
PLAYER = ""

def change_size(new_size):
    global FONT_SIZE
    FONT_SIZE = new_size

def change_speed(new_speed):
    global FONT_SPEED
    FONT_SPEED = new_speed


# MICROSERVICES:
context = zmq.Context()

# Random Name Generator:
RNG = context.socket(zmq.REQ)
RNG.connect("tcp://localhost:5555")

def get_r_name():
    RNG.send_string("RandomName")
    return RNG.recv().decode()

# Data Manager:
RECAP = context.socket(zmq.REQ)
RECAP.connect("tcp://localhost:54631")
step = 0
cwd = Path(__file__).resolve().parent

def set_step(data):
    global step
    request = {
        "command": "set",
        "data": {"recap": {step: data}},
        "cwd": str(cwd)
    }
    step += 1
    RECAP.send_json(request)
    response = RECAP.recv_string()
    return response

def get_recap():
    global step
    choices = ""
    request = {
        "command": "get",
        "data": ["recap"],
        "cwd": str(cwd)
    }
    RECAP.send_json(request)
    response = RECAP.recv_string()
    recap = json.loads(response)["recap"]
    if not recap is None:
        for x in range(0, step):
            choices += recap[str(x)]
    else: choices = "Your choices will display here"
    return choices

def clear_recap():
    request = {
        "command": "set",
        "data": {"recap":None},
        "cwd": str(cwd)
    }
    global step
    step = 0
    RECAP.send_json(request)
    response = RECAP.recv_string()
    return response

# Timer:
TMR = context.socket(zmq.REQ)
TMR.connect("tcp://localhost:8463")

def timer(command):
    TMR.send_string(command)
    return TMR.recv_string()

# Reactive Phrases:
RP = context.socket(zmq.REQ)
RP.connect("tcp://localhost:6423")

def react(command):
    RP.send_string("reactphrase" + command)
    return RP.recv_string()
