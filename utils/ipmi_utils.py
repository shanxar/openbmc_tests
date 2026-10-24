import subprocess
from utils.logger import get_logger
import os
from utils.constants import *

logger=get_logger(__name__)

def run_ipmi_command(arguments):
    bmc_host=BMC_HOST
    bmc_username=BMC_USERNAME
    bmc_password=BMC_PASSWORD

    ipmi_command=["ipmitool","-I","lanplus","-C","17","-H", bmc_host, 
                  "-p", HOST_UDP_PORT ,"-U",bmc_username,"-P",bmc_password]+ arguments

    logger.info(f"EXecuting IPMI command {" ".join(ipmi_command)}")
    result=subprocess.run(ipmi_command,capture_output=True,text=True,timeout=30)

    if result.returncode !=0:
        logger.error(f"IPMI command {" ".join(ipmi_command)} failed")

    return result

    