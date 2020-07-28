from datetime import datetime
import colorful as cf
from bsnl import data, helpers

def data_usage(usage_data):
	print(cf.red("Data Usage:"))
	out_str = "{:<30} {:<15} {:<12} {:<12} {:<12} {:<12}"
	print (cf.bold & cf.blue | out_str.format("Name" , "Type", "Today Used", "Total Used", "Total DL", "Total UP"))
	print (cf.bold & cf.blue | out_str.format("====" , "====", "==========", "==========", "========", "========"))
	for row in usage_data["rows"]:
		print (cf.green | out_str.format(row["serviceName"], row["serviceType"], row["dailyUsedOctets"], row["totalOctets"],
		row["downloadOctets"], row["uploadOctets"]))
	print(cf.italic & cf.yellow | "\nUpdated at: %s" % datetime.now())

def heading(string):
	return cf.bold(cf.blue(string))

def subtext(string):
	return cf.green(string)

def fup_details(combined_fup_data: data.FUPDetails):
	print(cf.red("FUP Details:"))
	separator = ":"
	out_str = "{:<60} {:<2} {}"
	print(out_str.format(heading("⇛ Username"), separator, subtext(combined_fup_data.username)))
	print(out_str.format(heading("⇛ Phone number"), separator, subtext(combined_fup_data.phone_number)))
	print(out_str.format(heading("⇛ Redirecting to FUP page"), separator,
					subtext(str(combined_fup_data.is_fup_redirect)) + 
					(cf.yellow(" (" + combined_fup_data.redirect_to + ")") if combined_fup_data.is_fup_redirect else "")))
	print(out_str.format(heading("⇛ FUP option received"), separator, subtext(combined_fup_data.fup_option)))
	print(out_str.format(heading("⇛ Equivalent option message"), separator, subtext(combined_fup_data.equivalent_fup_message)))
	print(out_str.format(heading("⇛ Promotional daily 4GB activated"), separator, subtext(str(combined_fup_data.is_daily_4gb_activated))))
	print(out_str.format(heading("⇛ Promotional monthly 10GB activated"), separator, subtext(str(combined_fup_data.is_monthly_10gb_activated))))

def display_dict(data: dict, title: str = ""):
	if title:
		print(cf.red(title + ":"))
	for key in data.keys():
		separator = ":"
		out_str = "{:<60} {:<2} {}"
		print(out_str.format(heading("⇛ " + key), separator, subtext(data[key])))

def errors(statuses: dict):
	for key in statuses.keys():
		if not statuses[key].success:
			print(cf.red(key + ":"))
			print(statuses[key].message)