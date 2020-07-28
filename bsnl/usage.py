import requests
import os
import sys
from datetime import datetime
import logging
from bsnl import data

logger = logging.getLogger(__name__)
headers = data.common_headers
payload = {
  'location': 'NOID',
  'actionName': 'manual',
  '_search': 'false',
  'nd': '1588301203519',
  'rows': '4',
  'page': '1',
  'sidx': '',
  'sord': 'asc'
}

def fetch(session: requests.Session) -> data.Status:
	status = data.Status()
	response = None
	try:
		response = session.post(
		'https://fuptopup.bsnl.co.in/fetchUserQuotaPM.do',
		headers=headers,
		data=payload,
		verify=False)
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
