import logging
import os

import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class PublishService(object):

    def __init__(self):
        self.host = os.getenv("MQTT_HOST", None)
        self.port = os.getenv("MQTT_PORT", 1883)

        if not self.host:
            logger.error("Cannot find MQTT_HOST env var.")
            exit(1)

    def publish(self, topic: str, message: str):
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            client.connect(self.host, self.port, 60)

            response = client.publish(topic=topic, payload=message)
            client.disconnect()

            if response.rc == 0:
                logger.info(f"Successfully published message: {message} on topic: {topic}.")
            else:
                logger.error(f"Failed to publish message {message} on topic: {topic}. Status: {response.rc}")
                exit(2)
        except Exception as e:
            logger.error(f"Error occurred while trying to send an MQTT message", exc_info=True)
            exit(3)