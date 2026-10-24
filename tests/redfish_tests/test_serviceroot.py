import pytest
from utils.logger import get_logger 
from utils.utilities import assert_validator
from utils.constants import *

logger=get_logger(__name__)

@pytest.mark.redfish
@pytest.mark.smoke
def test_redfish_serviceroot(bmc):

    logger.info("Starting test_service_root")

    response=bmc.get(SERVICE_ROOT_URI)

    data=response.json()

    assert data.get("Id") == "RootService", (
        f"Expected Id='RootService', got {data.get('Id')!r}"
    )

    assert_validator(data, "Systems")
    assert_validator(data, "Chassis")
    assert_validator(data, "Managers")
