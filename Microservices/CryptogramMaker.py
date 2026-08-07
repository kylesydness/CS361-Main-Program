import random
import zmq
import string

# initialize socket for zmq
context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://localhost:4454")

# cryptogram maker function
def cryptogram_maker(start_string: str, category: str = "letter"):

    #arrays to pull from for replacement
    char_array = list(string.ascii_lowercase)

    num_array = []
    for i in range(1, 27):
        num_array.append(i)

    #new array to append to
    new_string = ""

    # append new symbols based on category
    if category == "letter":
        # shuffle character array and map starting string to new letters
        random.shuffle(char_array)
        for letter in start_string:
            if letter.isalpha():
                new_letter = char_array[(ord(letter.lower()) - 97)]
                new_string += new_letter
            else:
                new_string += letter

    elif category == "number":
        # shuffle number array and map starting string to new numbers separated by lines
        random.shuffle(num_array)
        for letter in start_string:
            if letter.isalpha():
                new_number = str(num_array[(ord(letter.lower()) - 97)])
                new_string += "|" + new_number + "|"
            else:
                new_string += letter

    return new_string

# zmq pipeline, receiver, function call, and return

while True:
    message = socket.recv()

    cryptogram_request = message.decode()

    request_params = cryptogram_request.split("#")

    # no parameter
    if len(request_params) == 1:
        encoded_string = cryptogram_maker(request_params[0])
    # 1 parameter, check for 'letter' or 'number'
    elif len(request_params) == 2:
        if request_params[1] == "number":
            encoded_string = cryptogram_maker(request_params[0], "number")
        elif request_params[1] == "letter":
            encoded_string = cryptogram_maker(request_params[0])
        else:
            encoded_string = "Second parameter must be 'letter' or 'number'"
    else:
        encoded_string = "Please send String to encode, and optional parameter 'letter' or 'number' separated by #"

    # return string with either encoded string or error message
    socket.send_string(encoded_string)