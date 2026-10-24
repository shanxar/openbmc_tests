import pytest

from utils.logger import get_logger
from utils.ipmi_utils import run_ipmi_command
from utils.constants import *
logger=get_logger(__name__)

@pytest.mark.ipmi 
@pytest.mark.smoke 

def test_ipmi_mc_info():
    logger.info(f"Starting {__name__}")

    result=run_ipmi_command(mc_info_command)

    if result.returncode!=0 :
        assert False,(f"{__name__} is failed; {result.stderr}")

    logger.info(f"\n {result.stdout}")

    assert "Device ID" in result.stdout,("Property 'Device ID not found")
    logger.info("IPMI device information test passed")
