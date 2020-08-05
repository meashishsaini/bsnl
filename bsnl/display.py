from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax
from bsnl import data, helpers, router
import json

console = Console()

def data_usage(usage_data):
	table = Table(title="[red]Data Usage")
	style = "green"
	table.add_column("Name", style=style)
	table.add_column("Type", style=style)
	table.add_column("Today Used", style=style)
	table.add_column("Total Used", style=style)
	table.add_column("Total DL", style=style)
	table.add_column("Total UP", style=style)
	for row in usage_data["rows"]:
		table.add_row(row["serviceName"], row["serviceType"], row["dailyUsedOctets"], row["totalOctets"],
		row["downloadOctets"], row["uploadOctets"])
	console.print(table)

def create_grid() -> Table.grid:
	grid = Table.grid(expand=True, padding=(0,1,0,0))
	grid.add_column(style="bold blue")
	grid.add_column(style="green")
	return grid

def fup_details(combined_fup_data: data.FUPDetails):
	console.print("FUP Details", style="red")
	grid = create_grid()
	grid.add_row("Username", combined_fup_data.username)
	grid.add_row("Phone number", combined_fup_data.phone_number)
	grid.add_row("Redirecting to FUP page", str(combined_fup_data.is_fup_redirect) + 
					((" [yellow](" + combined_fup_data.redirect_to + ")") if combined_fup_data.is_fup_redirect else ""))
	grid.add_row("FUP option received", combined_fup_data.fup_option)
	grid.add_row("Equivalent option message", combined_fup_data.equivalent_fup_message)
	grid.add_row("Promotional daily 4GB activated", str(combined_fup_data.is_daily_4gb_activated))
	grid.add_row("Promotional monthly 10GB activated", str(combined_fup_data.is_monthly_10gb_activated))
	console.print(grid)

def a_dict(data: dict, title: str = ""):
	# rich library print doesn't render bool
	data = {key:(str(value) if isinstance(value, bool) else value) for (key, value) in data.items()}
	if title:
		console.print(title, style="red")
	grid = create_grid()
	for key in data.keys():
		grid.add_row(key, data[key])
	console.print(grid)

def router_details(data: router.Details):
	a_dict(data.__dict__, "Router Details")

def a_status(status: data.Status, title: str = ""):
	a_dict(status.__dict__, title)

def errors(statuses: dict):
	for key in statuses.keys():
		if not statuses[key].success:
			console.print(key, style="red")
			console.print(statuses[key].message)

def as_json(statuses: list):
	syntax = Syntax(json.dumps(statuses, cls=data.ClassToDictEncoder), lexer_name="json")
	console.print(syntax)