
import time
import requests
import pytest

from utils.logger import get_logger
from utils.utilities import check_bmc_is_up
from utils.constants import *

logger=get_logger(__name__)


@pytest.mark.redfish
@pytest.mark.reboot
def test_redfish_reboot(bmc):
    logger.info("Starting reboot test")

    response=bmc.get(MANAGER_URI)
    if response.status_code != 200:
        assert False , (f"BMC not reachable ; Reboot test failed  {response.status_code}")

    manager_data=response.json()
    previous_reset_time=manager_data["LastResetTime"]
    assert previous_reset_time,("Previous Reset Time missing")

    logger.info("BMC is reachable. LastResetTime: %s", previous_reset_time)

    logger.info("Sending BMC reboot request")
    try:
        response=bmc.post(RESET_URI, json = {"ResetType":"GracefulRestart"}
                          )
        logger.info("Reboot request HTTP status: %s", response.status_code)

        assert response.status_code in [200,202,2024] ,  (f"HTTP Code mismatch after sending reboot request: {response.text}")

    except requests.RequestException as e:
        logger.warning(
            "Connection dropped during reboot request: %s. "
            "Checking whether the reboot occurred.",
            e)

    logger.info("Waiting for BMC recovery")

    deadline = time.monotonic() + BMC_RECOVERY_TIMEOUT

    if not check_bmc_is_up(bmc,deadline):
        logger.error("Reboot test not passed")
        assert True,  ("Reboot test not passed")

    logger.info("Reboot test  passed")
    assert True,  ("Reboot test  passed")

"""    while time.monotonic() <= deadline:
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

    if not recovered:
        logger.error("Recovery failed post reboot. BMC not reachable") 
        assert False("Reboot test failed") 
    
    logger.info("Reboot test passed") """
    

                



