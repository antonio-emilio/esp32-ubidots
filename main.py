import requests
import random
import time
import paho.mqtt.publish as publish

TOKEN = "BBFF-6NwFfOYeg91z0monEscR42kSPRjNnB" # Assign your Ubidots Token
DEVICE = "esp32-teste" # Assign the device label to obtain the variable
VARIABLE = "temperatura" # Assign the variable label to obtain the variable value
DELAY = 1  # Delay in seconds
MQTT_BROKER = "mqtt.ubidots.com"
MQTT_PORT = 1883

def get_var(device, variable):
    try:
        url = "http://industrial.api.ubidots.com/"
        url = url + \
            "api/v1.6/devices/{0}/{1}/".format(device, variable)
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        req = requests.get(url=url, headers=headers)
        return req.json()['last_value']['value']
    except:
        pass

def build_payload(variable_1):
    # Creates two random values for sending data
    value_1 = random.randint(-10, 50)
    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

if __name__ == "__main__":
    while True:
        received_value = get_var(DEVICE, VARIABLE)
        if received_value is not None:
            incremented_value = received_value + 10
            print("Received Value:", received_value)
            print("Incremented Value:", incremented_value)
            # Send the incremented value to another topic, e.g., "temperatura-2"
            payload = build_payload("temperatura-2")

            print("[INFO] Attemping to send data")
            post_request(payload)
            print("[INFO] finished")
        time.sleep(DELAY)
