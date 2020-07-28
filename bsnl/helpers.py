import requests
import logging
from urllib.parse import urlparse
from bsnl import data
from bs4 import BeautifulSoup
import os

logger = logging.getLogger(__name__)

def fetch_fup_param(session: requests.Session) -> data.Status:
	url = data.server_base_address + data.location_by_ip
	status = data.Status()
	payload = {
		"actionName": "dailyFupPlan",
		"location": ""}
	response = None
	headers = data.common_headers
	try:
		response = session.post(url, data=payload, headers= headers)
		response.raise_for_status()
		status.data = response.json()
		status.success = True
		status.message = "Success"
	except requests.exceptions.RequestException as request_exception:
		logger.exception("Error in making request.")
		if response:
			status.code = response.status_code
		status.message = str(request_exception)
	except Exception as error:
		logger.exception("General error occurred.")
		status.message = str(error)
	return status

def get_fup_option(json_data):
	return json_data.get("dailyFupPlanParam1", "")

def decline_fup(session: requests.Session) -> data.Status:
	url = data.server_base_address + data.update_subscriber_profile
	headers = data.common_headers
	status = data.Status()
	payload = {
		"operation": "dailyDecline",
		"location": "NOID",
		"actionName": "dailyFupPlan"
		}
	response = None
	try:
		response = session.post(url, headers=headers, data=payload, verify=False)
		response.raise_for_status()
		response_json = response.json()
		if response_json["resultCode"] == "200":
			status.data = response_json
			status.success = True
			status.message = "Success"
		else:
			status.message = "Plan upgrade declined failed with message: {}".format(response_json["msg"])
			logger.warn(status.message)
			status.code = int(response_json["resultCode"])
	except requests.exceptions.RequestException as request_exception:
		logger.exception("Error in making request.")
		status.message = str(request_exception)
		if response:
			status.code = response.status_code
	except Exception as error:
		logger.exception("General error occurred.")
		status.message = str(error)
	return status

def fup_redirect(session: requests.Session) -> data.Status:
	status = data.Status()
	response = None
	try:
		response = session.get("http://www.msftconnecttest.com/redirect")
		response.raise_for_status()
		is_fup_redirect = data.normal_redirect_netloc != urlparse(response.url).netloc
		soup = BeautifulSoup(response.content, 'html.parser')
		url = ""
		if soup:
			soup = soup.find("meta")
			if soup:
				content = soup.get("content")
				if content:
					content = content.split(";")
					if len(content) > 1:
						content = content[1].split("=")
						if len(content) > 1:
							url = content[1]
		status.data = {
			"is_fup_redirect" : is_fup_redirect,
			"redirect_to": url
			}
		status.success = True
		status.message = "Success"
	except requests.exceptions.RequestException as request_exception:
		logger.exception("Error in making request.")
		if response:
			status.code = response.status_code
		status.message = str(request_exception)
	except Exception as error:
		logger.exception("General error occurred.")
		status.message = str(error)
	return status

def get_all_services(usage_data):
	services = []
	for row in usage_data["rows"]:
		services.append({
			"service_name": row["serviceName"],
			"service_type": row["serviceType"]
		})
	return services

def map_fup_details(fup_redirect_data, fup_param, usage_data) -> data.FUPDetails:
	fup_details = data.FUPDetails()
	is_daily_4gb_activated = False
	is_monthly_10gb_activated = False
	all_services = get_all_services(usage_data)
	for service in all_services:
		if service["service_name"] == data.promotional_daily_4gb:
			is_daily_4gb_activated = True
		if service["service_name"] == data.promotional_monthly_10gb:
			is_monthly_10gb_activated = True
	fup_details.username = fup_param.get("username", "")
	fup_details.phone_number = fup_param.get("phoneNumber", "")
	fup_details.is_fup_redirect = fup_redirect_data["is_fup_redirect"]
	fup_details.redirect_to = fup_redirect_data["redirect_to"]
	fup_details.fup_option = get_fup_option(fup_param)
	fup_details.equivalent_fup_message = data.fup_plan_params.get(get_fup_option(fup_param),"")
	fup_details.is_daily_4gb_activated = is_daily_4gb_activated
	fup_details.is_monthly_10gb_activated = is_monthly_10gb_activated
	
	return fup_details

def activate_plan(session: requests.Session, plan_name: str) -> data.Status:
	activate_choices = data.ActivateChoices()
	headers = data.common_headers
	status = data.Status()
	if plan_name == activate_choices.promotional_daily_4gb:
		url = data.server_base_address + data.promotional_daily_4gb_url
		payload = {
			'planId': '-1',
			'location': 'NOID',
			'actionName': 'dailyFupPlan'
		}
	elif plan_name == activate_choices.promotional_monthly_10gb:
		url = data.server_base_address + data.promotional_monthly_10gb_url
		payload = {
			'location': 'NOID',
			'actionName': 'manual'
			}
	else:
		status.message = "Unknown plan selected."
		logger.warn(status.message)
		return status
	response = None
	try:
		response = session.post(url, headers=headers, data=payload, verify=False)
		response.raise_for_status()
		response_json = response.json()
		status.data = response_json
		if response_json["resultCode"] == "200":
			status.message = "Plan '{}' activated with message: {}".format(response_json["planName"], response_json["msg"])
			status.success = True
		else:
			status.code = int(response_json["resultCode"])
			status.message = "Plan activation failed with message: {}".format(response_json["msg"])
			logger.warn(status.message)
	except requests.exceptions.RequestException as request_exception:
		logger.exception("Error in making request.")
		status.message = str(request_exception)
		if response:
			status.code = response.status_code
	except Exception as error:
		logger.exception("General error occurred.")
		status.message = str(error)
	return status

def cls():
	os.system('cls' if os.name=='nt' else 'clear')