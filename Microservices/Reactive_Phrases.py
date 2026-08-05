import random
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:6423")

#Phrases:
good_short = ("Great", "Nice", "Bravo", "Congratulations", "Good", "Kudos", "Amazing", "Congrats", "Hooray", "Hurrah", "Splendid", "Lucky")
good_long = ("You did Great", "Well done", "Good job", "That was amazing", "Well played", "Nice Work", "Nice going", "Nicely done", "Good for you", "Way to go", "Great job", "Good game", "Super duper", "You made that look easy", "You got this down", "You were just lucky")
bad_short = ("Ouch", "Oof", "Uh-oh", "Bummer", "Failure", "Sorry", "Poor", "Pity", "Aww", "Shame", "Unfortunate", "Unlucky")
bad_long = ("Better luck next time", "That didn't go well", "That's too bad", "How unfortunate", "What a shame", "That could've gone better", "That was rough", "Tough luck", "Give it another try", "That was disappointing", "That was a bummer")

def goodPhrase(length = None):
    #Determine length of response:
    if length == None:
        gList = random.randint(1,3)
        if gList == 1: gList = good_short
        else: gList = good_long

    elif length == "short": gList = good_short
    else: gList = good_long

    #select response
    selection = random.choice(gList)
    return selection


def badPhrase(length=None):
    # Determine length of response:
    if length == None:
        bList = random.randint(1, 3)
        if bList == 1:
            bList = bad_short
        else:
            bList = bad_long

    elif length == "short":
        bList = bad_short
    else:
        bList = bad_long

    # select response
    selection = random.choice(bList)
    return selection

while True:
    message = socket.recv_string()
    message = message.lower()
    reply = ""
    length = None

    if message.find("reactphrase") >= 0:
        if message.find("good") >= 0:
            if message.find("long") >= 0:
                length = "long"
            if message.find("short") >= 0:
                length ="short"
            reply = goodPhrase(length)

        elif message.find("bad") >= 0:
            if message.find("long") >= 0:
                length = "long"
            if message.find("short") >= 0:
                length = "short"
            reply = badPhrase(length)

    socket.send_string(str(reply))