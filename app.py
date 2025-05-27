import logging
import os
import sys
import time
from pathlib import Path

import schedule

from mqtt.publish_service import PublishService
from utils import file_utils

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def main():
    settings_file_str = os.getenv("SETTINGS_FILE", None)
    if not settings_file_str:
        logger.error(f"Failed to get env var SETTINGS_FILE")
        exit(1)

    settings_file = Path(settings_file_str)
    if not settings_file.exists() or not settings_file.is_file():
        logger.error(f"Invalid settings file: {settings_file}")
        exit(4)

    settings = file_utils.read_json_from_file(settings_file)

    if len(settings) < 1:
        logger.error(f"Invalid settings!")
        exit(4)

    logger.info("Start publishing settings...")
    service = PublishService()
    for setting in settings:
        service.publish(
            topic=f"espresense/settings/{setting['irk']}/config",
            message=str({"id":setting['id'], "name":setting['name']})
        )

def run_scheduler():
    schedule_minutes = os.getenv("SCHEDULE_MINUTES", 15)
    schedule.every(schedule_minutes).minutes.do(main)

    logger.info(f"Starting scheduler every {schedule_minutes} minutes...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()