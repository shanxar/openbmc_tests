import os

#redfish tests
HOST_HTTPS_PORT="2443"

#reboot test
MANAGER_URI = "/redfish/v1/Managers/bmc"
SERVICE_ROOT_URI = "/redfish/v1/"
RESET_URI = f"{MANAGER_URI}/Actions/Manager.Reset"
BMC_RECOVERY_TIMEOUT=180

#service_root test
BMC_HOST=os.getenv("BMC_HOST")
BMC_USERNAME=os.getenv("BMC_USERNAME")
BMC_PASSWORD=os.getenv("BMC_PASSWORD")


#IPMI Test constants
mc_info_command=["mc","info"]
HOST_UDP_PORT="2623"