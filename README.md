# A System Data Publisher to MQTT

## Overview

This Python script is designed to publish system data, such as CPU usage, memory usage, and disk space, to an MQTT broker at regular intervals. It retrieves system metrics, formats them as JSON, and publishes them to a specified MQTT topic. This README provides instructions for setting up and using the script effectively.

## Prerequisites

Before using this script, ensure you have the following prerequisites installed/available to you:

- Python 3.x
- Paho MQTT Client (`paho-mqtt`)
- YAML Parser (`pyyaml`)
- psutil
- An MQTT broker (e.g., Mosquitto)

You can install the required Python libraries using pip:

```bash
pip install paho-mqtt pyyaml psutil
```

## Configuration

1. Clone this repository to your local machine or download the script and configuration file (`mqtt_config.yaml`) to your project directory.

2. Edit the `mqtt_config.yaml` file to configure your MQTT broker and topic settings:

   - `broker_address`: The address of your MQTT broker.
   - `port`: The MQTT broker port.
   - `username`: Your MQTT broker username (if required).
   - `password`: Your MQTT broker password (if required).
   - `wait_seconds`: The interval (in seconds) between data publications.
   - `run_verbose`: Set to `true` if you want to print data to the console as it is published.
   
   Example `mqtt_config.yaml` file:

   ```yaml
   mqtt:
     broker_address: "mqtt.example.com"
     port: 1883
     username: "your_username"
     password: "your_password"
     wait_seconds: 30
     run_verbose: true
   ```

3. Ensure you have an MQTT broker running and accessible with the provided configuration.

## Usage

1. Run the script using Python:

   ```bash
   python mqtt_publisher.py
   ```

   The script will connect to the MQTT broker, publish system data in JSON format to the specified topic, and continue doing so at the defined interval.

2. Monitor the MQTT topic `tele/<server_name>/SENSOR` to access the published data.

## MQTT Topics

- `tele/<server_name>/LWT`: The Last Will and Testament (LWT) topic indicating the status of the script. It will show "Online" when the script is running and "Offline" when it disconnects.

- `tele/<server_name>/SENSOR`: The topic where the system data is published in JSON format.

## Customization

You can customize the script to publish additional system metrics or modify the data format as needed. Edit the code within the "Publish data" section of the script.

## License

This script is provided under the MIT License. Feel free to modify and use it in your projects.

## Acknowledgments

This script uses the Paho MQTT library for MQTT communication and psutil for system data retrieval.
