import os
import paho.mqtt.client as mqtt

def main():
    try:
        irk = os.getenv("ES_PRESENSE_IRK", None)
        device_id = os.getenv("ES_PRESENSE_DEVICE_ID", None)
        device_name = os.getenv("ES_PRESENSE_DEVICE_NAME", None)
        if not irk and not device_id and not device_name:
            print(f"Missing env vars for ES_PRESENSE_IRK, ES_RESENSE_DEVICE_ID, or ES_PRESENSE_DEVICE_NAME")
            exit(1)

        mqtt_host = os.getenv("MQTT_HOST")
        mqtt_port = os.getenv("MQTT_PORT", 1883)
        if not mqtt_host:
            print("Missing env var for MQTT_PORT")
            exit(1)

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.connect(mqtt_host, mqtt_port, 60)

        response = client.publish(
            topic=f'espresense/settings/{irk}/config',
            payload=str({"id": device_id, "name": device_name})
        )
        client.disconnect()

        if response.rc == 0:
            print(f"Success!")
            exit(0)
        else:
            print(f"Failed to publish settings. Status: {response.rc}")
            exit(2)
    except Exception as e:
        print(f'Failed to publish settings due to error: {e}')
        exit(3)

if __name__ == "__main__":
    main()