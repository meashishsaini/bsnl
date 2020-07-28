from bsnl import usage, helpers, display, data, router
import requests
import argparse
import json
import signal
import time
import sys

def add_parser_arg(parser):
	display_choices = data.DisplayChoices()
	router_choices = data.RouterChoices()
	activate_choices = data.ActivateChoices()
	parser.add_argument("-d", "--display", type=str, choices=display_choices.arguments(), help="display details", nargs="+")
	parser.add_argument("-e", "--decline", help="decline fup", action='store_true')
	parser.add_argument("-a", "--activate", type=str, choices=activate_choices.arguments(), help="activate plans", nargs="+")
	parser.add_argument("-r", "--router", type=str, choices=router_choices.arguments(), help="select router")
	parser.add_argument("-t", "--restart", help="restart router", action='store_true')
	parser.add_argument("-j", "--json", help="output json", action='store_true')
	parser.add_argument("-f", "--refresh", type=float, help="refresh display every some seconds")
	parser.add_argument("-u", "--username", type=str, help="username for the router")
	parser.add_argument("-p", "--password", type=str, help="password for the router")

def switch(args):
	display_choices = data.DisplayChoices()
	router_choices = data.RouterChoices()
	activate_choices = data.ActivateChoices()
	statuses = {}
	session = requests.Session()
	if args.display:
		for choice in args.display:
			if choice == display_choices.fup_details:
				usage_data = usage.fetch(session)
				statuses[choice] = usage_data
				if usage_data.success:
					fup_redirect_data = helpers.fup_redirect(session)
					statuses[choice] = fup_redirect_data
					if fup_redirect_data.success:
						fup_param = helpers.fetch_fup_param(session)
						statuses[choice] = fup_param
						if fup_param.success:
							combined_fup_data = helpers.map_fup_details(fup_redirect_data.data, fup_param.data, usage_data.data)
							if not args.json:
								display.fup_details(combined_fup_data)
							status = data.Status()
							status.success = True
							status.message = "Success"
							status.data = combined_fup_data
							statuses[choice] = status
			if choice == display_choices.router_details:
				if args.router:
					cls = getattr(router, args.router)
					router_instance = cls()
					status = router_instance.authenticate(args.username, args.password)
					if status.success:
						status = router_instance.details()
						if status.success:
							if not args.json:
								display.display_dict(status.data.__dict__, choice)
					statuses[choice] = status
				else:
					status = data.Status()
					status.message = "Please add router model."
					statuses[choice] = status
			if choice == display_choices.data_usage:
				usage_data = usage.fetch(session)
				statuses[choice] = usage_data
				if usage_data.success:
					if not args.json:
						display.data_usage(usage_data.data)
	if args.decline:
		status = helpers.decline_fup(session)
		statuses["decline"] = status
		if status.success and not args.json:
			display.display_dict(status.data, "decline")
	if args.activate:
		for choice in args.activate:
			status = helpers.activate_plan(session, choice)
			statuses[choice] = status
			if status.success and not args.json:
				display.display_dict(status.data, choice)
	if args.restart:
		if args.router:
			cls = getattr(router, args.router)
			router_instance = cls()
			status = router_instance.authenticate(args.username, args.password)
			if status.success:
				status = router_instance.restart()
				if status.success and not args.json:
					display.display_dict(status.__dict__, "restart")
			statuses["restart"] = status
		else:
			status = data.Status()
			status.message = "Please add router model."
			statuses[choice] = status
	if args.json:
		print(json.dumps(statuses, cls=data.ClassToDictEncoder))
	else:
		display.errors(statuses)

def parse():
	signal.signal(signal.SIGINT, exit_gracefully)
	parser = argparse.ArgumentParser()
	add_parser_arg(parser)
	args = parser.parse_args()
	switch(args)
	if args.refresh:
		while True:
			time.sleep(args.refresh)
			helpers.cls()
			switch(args)

def exit_gracefully(signum, frame):
	sys.exit(0)

if __name__ == "__main__":
	parse()