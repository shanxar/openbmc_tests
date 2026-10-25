import pytest 
import os
from utils.bmc_client import BMCClient
import urllib3
from utils.constants import *

@pytest.fixture
def bmc():
    host=BMC_HOST+":"+HOST_HTTPS_PORT
    username=BMC_USERNAME
    password=BMC_PASSWORD

    urllib3.disable_warnings(
        urllib3.exceptions.InsecureRequestWarning
    )
    client=BMCClient(host,username,password)

    yield client


    client.close()