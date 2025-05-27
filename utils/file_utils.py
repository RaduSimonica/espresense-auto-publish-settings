import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def read_json_from_file(json_file: Path):
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read JSON file from: {json_file}", exc_info=True)