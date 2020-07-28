from dataclasses import dataclass
from json import JSONEncoder

# These values from http://172.30.136.25:8090/ssssportal/js/custome-bsnl.js
fup_plan_params = {
	"option1": "Dear Esteemed Customer,\nYou have exhausted your daily usage limit (as per your existing plan) and hereafter will be able to browse internet at reduced speed for the day. Being a Premium Broadband Customer of BSNL, a free TOP UP for today is being offered to enable you to continue to browse internet at higher speed.",
	"option2": "Dear Esteemed Customer,\nYou have exhausted your daily usage limit (as per your existing plan) again in this month, therefore you will be able to browse internet at reduced speed today. You may like to continue to enjoy browsing at Higher speed by availing upgraded but economical broadband plan with higher daily usage limit.",
	"option3": "Dear Esteemed Customer,\nAs you are a premium Broadband user of BSNL, We are sure you have already enjoyed complementary TOPUP and you have also changed Base plan in current month. Please click on Decline button to continue browsing with FUP speed as per your Base Plan. \nNote : Base Plan change is only allowed once in month.",
	"option4": "Dear Esteemed Customer,\nAs you are a premium Broadband user of BSNL, We are sure you have already enjoyed complementary TOPUP and also visited Base Plan change detail. Please continue browsing with High/FUP speed as per your Plan. \nKind regards \nBSNL Broadband",
	"option5": "Dear Esteemed Customer,\nAs you are a premium Broadband user of BSNL, We are sure you have already enjoyed complementary TOPUP and also upgraded Base Plan when you have visited Base Plan change for upgraded Base Plan. Please continue browsing with High/FUP speed as per your Plan. Note : Base Plan change is only allowed once in month. Kind regards BSNL Broadband",
	"option6": "Dear Esteemed Customer,\nAs you are a premium Broadband user of BSNL, We are sure you have already enjoyed complementary TOPUP and opted to continue browsing with FUP speed. Please continue browsing with FUP speed as per your Plan. \nKind regards \nBSNL Broadband",
	"defaultError": "Dear Esteemed Customer,\nThere is some technical issue. Please contact BSNL Support Team. \nKind regards \nBSNL Broadband",
}
server_base_address = "http://172.30.136.25:8090/ssssportal/"
location_by_ip = "getLocationByIP.do"
update_subscriber_profile = "updateSubscriberProfile.do"
promotional_daily_4gb_url = "topUpConfirmation.do"
promotional_monthly_10gb_url = "promotionalAction.do"
promotional_daily_4gb = "Daily_4GB"
promotional_monthly_10gb = "Daily_10GB"
normal_redirect_netloc = "www.msn.com"
common_headers = {
		"connection": "keep-alive",
		"accept": "application/json, text/javascript, */*; q=0.01",
		"x-requested-with": "XMLHttpRequest",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
		"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
	}

@dataclass
class FUPDetails:
	username: str = ""
	phone_number: str = ""
	is_fup_redirect: bool = False
	redirect_to: str = ""
	fup_option: str = ""
	equivalent_fup_message: str = ""
	is_daily_4gb_activated: bool = False
	is_monthly_10gb_activated: bool = False

@dataclass
class DisplayChoices:
	fup_details: str = "FUPDetails"
	router_details: str = "RouterDetails"
	data_usage: str = "DataUsage"
	def arguments(self) -> list:
		choices = []
		as_dict = self.__dict__
		for key in as_dict:
			choices.append(as_dict[key])
		return choices
@dataclass
class RouterChoices:
	dslw200: str = "DSLW200"
	def arguments(self) -> list:
		choices = []
		as_dict = self.__dict__
		for key in as_dict:
			choices.append(as_dict[key])
		return choices
@dataclass
class ActivateChoices:
	promotional_daily_4gb: str = "Daily_4GB_Promotional"
	promotional_monthly_10gb: str = "Monthly_10GB_Promotional"
	def arguments(self) -> list:
		choices = []
		as_dict = self.__dict__
		for key in as_dict:
			choices.append(as_dict[key])
		return choices
@dataclass
class Status:
	code: int = None
	message: str = ""
	success: bool = False
	data: any = None
	def __repr__(self):
	 return self.message + (" With code: " + str(self.code) if self.code else "")

class ClassToDictEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__