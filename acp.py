from flask import Flask, jsonify, request
import json
import pprint
import base64
import requests
from datetime import datetime


# Define app, ip address, and port number
app = Flask(__name__)
# ip_addr = "192.168.10.87"
# port = 4444

# Central Access Control System details
cacs_ip = "192.168.10.66"
cacs_port = 4040


# Function to log to `all.log` and a specific file of the user's choosing
# Requires:         filename:string - the filename of the user-chosen log
# 					request:string - the request that is being processed,
#                                       use `ip_addr` (this machine's IP if it's just an internal method call)
# 					src_ip:string - the source ip address that made the request - can be 127.0.0.1 if an internal call (e.g. auth.log)
# 					log_type:int - a number representing the type of log, 0=INFO, 1=ERROR, 2=FATAL
# 					content:string - data to be written to the file
# Returns:          return_code:int - a return code for the logging attempt, 0=FAIL, 1=SUCCESS
# Expected Action:  Open log file, write JSON data, close file
def log(filename, request, src_ip, log_type, content):
    filename = "log/" + filename

    return_code = 0  # Default = FAIL

    # Get timestamp
    date_time = datetime.now()
    timestamp = date_time.strftime("%d-%m-%Y @ %H:%M:%S")

    # Set the string for the log_type

    # log_type = 0 # info - information including authentication success and failure
    # log_type = 1 # error - errors in program execution
    # log_type = 2 # fatal - fatal errors that cause the program to exit/shutdown
    if log_type == 0:
        str_log_type = "INFO"
    elif log_type == 1:
        str_log_type = "ERROR"
    elif log_type == 2:
        str_log_type = "FATAL"
    else:
        print("[ERROR] Error writing to log file!")
        return return_code

    req = str(request)
    ip = str(src_ip)
    log_content = content

    log_entry = {
        "timestamp": timestamp,
        "request": req,
        "source_ip": ip,
        "log_type": str_log_type,
        "log_content": log_content,
    }
    log_entry_dump = json.dumps(log_entry, indent=4)

    # Write to master log
    try:
        with open("log/all.log", "a") as file:
            file.write(log_entry_dump)
            file.close()
            return_code = 1
    except:
        print("[ERROR] Error writing to log file!")

    # Write to individual log
    try:
        with open(filename, "a") as file:
            file.write(log_entry_dump)
            file.close()
            return_code = 1
    except:
        print("[ERROR] Error writing to log file!")

    pprint.pprint(log_entry)

    return return_code


# Route for default request @ http://{ip_addr}:{port}/
# Requires:         None
# Returns:          message:JSON - Information message identifying the program.
# Expected Action:  Returns a fairly standard default JSON message to the request
@app.route("/")
def hello():
    return jsonify(message="Access Control Panel 2.1.4.")


# Route to accept and forward requests to the Central Access Control System.
# Requires:			employee_id:int - the ID of the employee attempting to gain access
#                   pin:int - the pin of the employee attempting to gain access
#                   image:b64(*.jpg) - base64-encoded bytestring of face image of the employee attempting to gain access
# Returns:			JSON(auth_result:int,message:str) - the JSON encoded integer authentication result, 0=FAIL, 1=SUCCESS, and a message explaining the reason for the result
# Expected Action:	Receive ID, PIN, and Image, lookup the ID in the database, sned image to the Facial Recognition System (FRS), ensure FRS ID returns matching ID, check PIN, return result and/or open door
@app.route("/input", methods=["GET", "POST"])
def input():
    req = str(request)
    src_ip = str(request.remote_addr)
    print(f"{req} from {src_ip}")

    data = request.json
    employee_id = data["employee_id"]
    employee_pin = data["pin"]
    encoded_string = base64.b64decode(data["image"])
    # Decode and store face temporarily
    with open("tmp_face.jpg", "wb") as fh:
        fh.write(encoded_string)

    msg = f"[INFO] Forwarding {employee_id}:{employee_pin}:<image>."
    with open("tmp_face.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    data = {"employee_id": employee_id, "pin": employee_pin, "image": encoded_image}
    url = "http://" + str(cacs_ip) + ":" + str(cacs_port) + "/access_request"
    response = requests.post(url, json=data)
    resp = response.json()
    print(resp)

    return jsonify(resp)


# Main Program!
if __name__ == "__main__":
    print("[START] Program started.")
    flask_msg = "[FLASK] Starting Flask Server..."
    log("system_state.log", "__main__", "localhost", 0, flask_msg)
    app.run()
