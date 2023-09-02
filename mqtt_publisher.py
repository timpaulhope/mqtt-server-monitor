import paho.mqtt.client as mqtt
import yaml
import psutil
import os
import json
import time
from datetime import datetime, timezone
import socket

def get_hostname():
    # Get hostname for local machine
    return socket.gethostname()

def publish_system_data(config_file_path):
    # Load MQTT configuration from the YAML file
    with open(config_file_path, 'r') as config_file:
        mqtt_config = yaml.safe_load(config_file)["mqtt"]

    # Extract MQTT configuration values
    broker_address = mqtt_config["broker_address"]
    port = mqtt_config["port"]
    username = mqtt_config["username"]
    password = mqtt_config["password"]
    wait_seconds = mqtt_config["wait_seconds"]
    run_verbose =  mqtt_config["run_verbose"]
    # Topic settings
    server_name = get_hostname()
    lwt_topic = f"tele/{server_name}/LWT"  # Define the LWT topic
    lwt_message = "Offline"  # Define the LWT message
    sensor_topic = f"tele/{server_name}/SENSOR"  # Change to the desired topic
    BytesPerGB = float(1024.0 ** 3) ## <- A Factor to convert Bytes to Gb
    
        # Create an MQTT client
    client = mqtt.Client("python_publisher")

    # Set the username and password
    client.username_pw_set(username, password)

    # Set the LWT message and topic
    client.will_set(lwt_topic, lwt_message, 0, retain=True)

    # Connect to the MQTT broker
    client.connect(broker_address, port)

    # Initiate the LWT to "Online" when connected
    client.publish(lwt_topic, "Online", 0, retain=True)
    
    if run_verbose:
        print(f"Script Running\nSensors publishing to: {sensor_topic}\nLWT publishing to:     {lwt_topic}\n")

    while True:
        # Set data you want to publish
        cpu_pc = psutil.cpu_percent()  # Get CPU usage
        mem = psutil.virtual_memory()  ## get memory use
        rootFolder = psutil.disk_usage('/')
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

        # Create a dictionary of data to publish
        message_data = {
            "Time": current_time,
            "CpuPc": cpu_pc,
            "MemPc": round(100 * (float(mem.used) / float(mem.total)),2),
            "Root": {"TotalGB" : round(float(rootFolder.total) / BytesPerGB ,1),
                     "UsedPc" : round(100*(float(rootFolder.total - rootFolder.free) / float(rootFolder.total)) ,1),
                     "FreeGB" : round(float(rootFolder.free) / BytesPerGB ,1)}}

        # Serialize the dictionary to a JSON string
        message_json = json.dumps(message_data)

        # Publish the message to the MQTT topic
        client.publish(sensor_topic, message_json)

        if run_verbose:
            print(message_json)
            
        # Wait for the specified number of seconds before publishing the next message
        time.sleep(wait_seconds)

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Define the relative path to the YAML configuration file
    config_file_path = os.path.join(script_dir, "mqqt_config.yaml")
    
    # Call the function to start publishing data
    publish_system_data(config_file_path)

#==EoF==