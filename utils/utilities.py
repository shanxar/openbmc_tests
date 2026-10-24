from utils.logger import get_logger
import requests
import time

logger = get_logger(__name__)

def assert_validator(data,key):

    logger.info(f"Validating {key} value")

    if key not in data:
        message = f"Missing key property : {key}"
        logger.error(message)
        raise AssertionError(message)

    logger.info("Property found: %s", key)


def check_bmc_is_up(bmc,deadline=5):
        recovered = False
        while time.monotonic() <= deadline:
            try:
                response=bmc.get(MANAGER_URI)
                if response.status_code == 200:
                    logger.info("Connection established post reboot")
                    manager_after = response.json()
                    current_reset_time = manager_after.get("LastResetTime")

                    if current_reset_time != previous_reset_time:
                        recovered=True
                        break
            
            except:
                logger.info("Connection not established post reboot. Retrying....")

        return recovered


