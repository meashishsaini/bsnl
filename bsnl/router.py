import requests
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
from bs4 import BeautifulSoup
from bsnl import data

logger = logging.getLogger(__name__)

@dataclass
class Details:
	model_number: str = ""
	software_version: str = ""
	hardware_version: str = ""
	serial_number: str = ""
	mac_address: str = ""
	lan_ip_address: str = ""
	lan_subnet_mask: str = ""
	lan_dhcp_server: str = ""
	wan_status: str = ""
	wan_connection_type: str = ""
	wan_ip_address: str = ""
	wan_subnet_mask: str = ""
	wan_default_gateway: str = ""
	wan_primary_dns: str = ""
	wan_secondary_dns: str = ""
	wan_nat: str = ""
	wan_ppp_connection_time: str = ""
	ipv6_status: str = ""
	ipv6_ip_address: str = ""
	ipv6_prefix_length: str = ""
	ipv6_default_gateway: str = ""
	ipv6_dns_server: str = ""
	ipv6_prefix_delegation: str = ""
	adsl_firmware_version: str = ""
	adsl_line_state: str = ""
	adsl_modulation: str = ""
	adsl_annex_mod: str = ""
	adsl_snr_margin_downstream: str = ""
	adsl_snr_margin_upstream: str = ""
	adsl_line_attenuation_downstream: str = ""
	adsl_line_attenuation_upstream: str = ""
	adsl_data_rate_downstream: str = ""
	adsl_data_rate_upstream: str = ""

class Router(ABC):
	def __init__(self, address = None):
		self._router_address = address
	@property
	def router_address(self):
		return self._router_address
	@router_address.setter
	def router_address(self, address):
		self._router_address = address
	@abstractmethod
	def restart(self):
		pass
	@abstractmethod
	def authenticate(self, username, password):
		pass
	@abstractmethod
	def details(self):
		pass

class DSLW200(Router):
	def __init__(self, address = "http://192.168.1.1/"):
		super().__init__(address)
		self._username = None
		self._password = None
		self._session = requests.Session()

	def authenticate(self, username, password) -> data.Status:
		status = data.Status()
		response = None
		try:
				response = self._session.get(self.router_address, auth=(username, password))
				response.raise_for_status()
				self._username = username
				self._password = password
				status.message = "Authentication Successful."
				status.success = True
		except requests.exceptions.RequestException as request_exception:
			logger.exception("Error in making request.")
			status.code = response.status_code
			if response.status_code == 401:
				status.message = "Invalid username or password."
			else:
				status.message = str(request_exception)
		except Exception as error:
			logger.exception("General error occurred.")
			status.message = str(error)
		return status

	def restart(self) -> data.Status:
		status = data.Status()
		if self._username and self._password:
			payload = "restoreFlag=0"
			url = self.router_address + "Forms/tools_system_1"
			response = None
			try:
				response = requests.request("POST", url, data=payload, auth=(self._username, self._password))
				response.raise_for_status()
				status.message = "Router Restarted."
				status.success = True
			except requests.exceptions.RequestException as request_exception:
				logger.exception("Error in making request.")
				status.code = response.status_code
				status.message = str(request_exception)
			except Exception as error:
				logger.exception("General error occurred.")
				status.message = str(error)
		else:
			status.message = "Login details not provided"
		return status

	def details(self):
		status = data.Status()
		response = None
		try:
			response = self._session.get(self.router_address + "status/status_deviceinfo.htm", auth=(self._username, self._password))
			response.raise_for_status()
			dt = Details()
			soup = BeautifulSoup(response.content, features="html.parser")
			cells = soup.findAll("td")
			dt.model_number = cells[10].get_text().strip()
			dt.software_version = cells[15].get_text().strip()
			dt.hardware_version = cells[20].get_text().strip()
			dt.serial_number = cells[25].get_text().strip()
			dt.mac_address = cells[30].get_text().strip()
			dt.lan_ip_address = cells[40].get_text().strip()
			dt.lan_subnet_mask = cells[45].get_text().strip()
			dt.lan_dhcp_server = cells[50].get_text().strip()
			dt.wan_status = cells[65].get_text().strip()
			dt.wan_connection_type = cells[70].get_text().strip()
			dt.wan_ip_address = cells[76].get_text().strip()
			dt.wan_subnet_mask = cells[82].get_text().strip()
			dt.wan_default_gateway = cells[87].get_text().strip()
			dt.wan_primary_dns = cells[92].get_text().strip()
			dt.wan_secondary_dns = cells[97].get_text().strip()
			dt.wan_nat = cells[102].get_text().strip()
			dt.wan_ppp_connection_time = cells[107].get_text().strip()
			dt.ipv6_status = cells[117].get_text().strip()
			dt.ipv6_ip_address = cells[122].get_text().strip()
			dt.ipv6_prefix_length = cells[127].get_text().strip()
			dt.ipv6_default_gateway = cells[132].get_text().strip()
			dt.ipv6_dns_server = cells[137].get_text().strip()
			dt.ipv6_prefix_delegation = cells[142].get_text().strip()
			dt.adsl_firmware_version = cells[152].get_text().strip()
			dt.adsl_line_state = cells[157].get_text().strip()
			dt.adsl_modulation = cells[162].get_text().strip()
			dt.adsl_annex_mod = cells[167].get_text().strip()
			dt.adsl_snr_margin_downstream = cells[184].get_text().strip() + " db"
			dt.adsl_snr_margin_upstream = cells[185].get_text().strip() + " db"
			dt.adsl_line_attenuation_downstream = cells[191].get_text().strip() + " db"
			dt.adsl_line_attenuation_upstream = cells[192].get_text().strip() + " db"
			dt.adsl_data_rate_downstream = cells[198].get_text().strip() + " kbps"
			dt.adsl_data_rate_upstream = cells[199].get_text().strip() + " kbps"
			status.data = dt
			status.success = True
			status.message = "Success"
		except requests.exceptions.RequestException as request_exception:
			logger.exception("Error in making request.")
			status.code = response.status_code
			status.message = str(request_exception)
		except Exception as error:
			logger.exception("General error occurred.")
			status.message = str(error)
		return status