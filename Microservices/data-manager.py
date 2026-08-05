import zmq
import json
from pathlib import Path


# defs should return 1 if successful (or the JSON data if getdata was
# called) or error message if unsuccessful

# helper function for setData
def update_dict(existing_dict, new_dict):
    for key, value in new_dict.items():
        # checking if we need to dig deeper to set variables
        if (isinstance(value, dict)
                and key in existing_dict
                and isinstance(existing_dict[key], dict)):
            update_dict(existing_dict[key], value)
        # we do not need to dig any deeper
        else:
            existing_dict[key] = value


# helper function for removeData
def remove_dict(existing_dict, key_list):
    # checking if list is empty
    if not key_list:
        return

    current_key = key_list[0]

    # if we still have a path to traverse
    if len(key_list) > 1:
        # checking if we need to dig deeper
        if (current_key in existing_dict
                and isinstance(existing_dict[current_key], dict)):
            remove_dict(existing_dict[current_key], key_list[1:])
        else:
            # path doesn't exist
            pass
    else:
        try:
            del existing_dict[current_key]
        except KeyError:
            # trying to remove a key that doesn't exist, nothing to do.
            pass


def setData(data, cwd):
    data_file = cwd / "data.json"

    # file exists
    try:
        with open(data_file, "r") as file:
            try:
                existing_json = json.load(file)
            # the file has invalid json
            except json.JSONDecodeError:
                return "*Err6"
    except PermissionError:
        return "*Err7"
    # no file detected, writing everything to file
    except FileNotFoundError:
        try:
            with open(data_file, "w") as file:
                json.dump(data, file, indent=4)
            return str(1)
        except PermissionError:
            return "*Err7"

    # checking if loaded json is dictionary
    if not isinstance(existing_json, dict):
        return "*Err6"

    update_dict(existing_json, data)
    try:
        with open(data_file, "w") as file:
            json.dump(existing_json, file, indent=4)
        return str(1)
    except PermissionError:
        return "*Err7"


def getData(data_list, cwd):
    data_file = cwd / "data.json"

    #read the data file
    try:
        with open(data_file, "r") as file:
            try:
                existing_json = json.load(file)
            except json.JSONDecodeError:
                return "*Err6"
    except PermissionError:
        return "*Err7"
    except FileNotFoundError:
        return "*Err0"

    # stored JSON must be a dictionary
    if not isinstance(existing_json, dict):
        return "*Err6"

    requested_data = {}

    for data in data_list:
        # each requested value must be a string such as "property.city"
        if not isinstance(data, str):
            return "*Err5"

        keys = data.split(".")
        current_value = existing_json

        # follow  path through the stored JSON
        for key in keys:
            if isinstance(current_value, dict) and key in current_value:
                current_value = current_value[key]
            else:
                current_value = None
                break

        # rebuild the requested path in the response
        current_result = requested_data

        for key in keys[:-1]:
            if key not in current_result:
                current_result[key] = {}

            if not isinstance(current_result[key], dict):
                current_result[key] = {}

            current_result = current_result[key]

        current_result[keys[-1]] = current_value

    return json.dumps(requested_data)


def removeData(data_list, cwd):
    data_file = cwd / "data.json"

    # file exists
    try:
        with open(data_file, "r") as file:
            try:
                existing_json = json.load(file)
            # the file has invalid json
            except json.JSONDecodeError:
                return "*Err6"
    except PermissionError:
        return "*Err7"
    except FileNotFoundError:
        return "*Err0"

    # checking if loaded json is dictionary
    if not isinstance(existing_json, dict):
        return "*Err6"

    # deleting items
    for data in data_list:
        try:
            current_data = data.split(".")
            remove_dict(existing_json, current_data)
        except AttributeError:
            return "*Err5"
    # saving changes to data file
    try:
        with open(data_file, "w") as file:
            json.dump(existing_json, file, indent=4)
        return str(1)
    except PermissionError:
        return "*Err7"


# setting up socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:54631")
# listening for messages
while True:
    message = socket.recv()
    # check if message is valid JSON
    try:
        message = json.loads(message)
    # sending error message for invalid JSON
    except json.JSONDecodeError:
        socket.send_string("*Err1")
        continue
    # checking if message has the valid file structure
    if not isinstance(message, dict):
        socket.send_string("*Err2")
        continue
    required_keys = {"command", "data", "cwd"}
    # checking if all the required keys were sent
    if not required_keys.issubset(message.keys()):
        socket.send_string("*Err2")
        continue

    command = message["command"]
    data = message["data"]

    # checking if cwd is valid
    try:
        cwd = Path(message["cwd"])
    except TypeError:
        socket.send_string("*Err3")
        continue
    if not cwd.is_dir():
        socket.send_string("*Err3")
        continue

    # checking if data is in list format
    if command == "get" or command == "remove":
        if not isinstance(data, list):
            socket.send_string("*Err5")
            continue

    # checking if data is in dict format for set
    if command == "set":
        if not isinstance(data, dict):
            socket.send_string("*Err5")
            continue

    if command == "set":
        return_message = setData(data, cwd)
    elif command == "get":
        return_message = getData(data, cwd)
    elif command == "remove":
        return_message = removeData(data, cwd)
    else:
        socket.send_string("*Err4")
        continue
    socket.send_string(return_message)
