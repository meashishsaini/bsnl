## BSNL Scripts
Some scripts to help me in managing daily BSNL broadband things like declining FUP, activating promotional packs, etc.

## Requirements
* _requests_
* _beautifulsoup4_

## Installation
1. Clone the repository.
2. Change directory to 'bsnl'
3. Install using `pip install .`

## Usage
```
usage: bsnl [-h]
			[-d {FUPDetails,RouterDetails,DataUsage} [{FUPDetails,RouterDetails,DataUsage} ...]]
			[-e]
			[-a {Daily_4GB_Promotional,Monthly_10GB_Promotional} [{Daily_4GB_Promotional,Monthly_10GB_Promotional} ...]]
			[-r {DSLW200}] [-t] [-j] [-f REFRESH] [-u USERNAME] [-p PASSWORD]

optional arguments:
  -h, --help			show this help message and exit
  -d {FUPDetails,RouterDetails,DataUsage} [{FUPDetails,RouterDetails,DataUsage} ...], --display {FUPDetails,RouterDetails,DataUsage} [{FUPDetails,RouterDetails,DataUsage} ...]
						display details
  -e, --decline			decline fup
  -a {Daily_4GB_Promotional,Monthly_10GB_Promotional} [{Daily_4GB_Promotional,Monthly_10GB_Promotional} ...], --activate {Daily_4GB_Promotional,Monthly_10GB_Promotional} [{Daily_4GB_Promotional,Monthly_10GB_Promotional} ...]
						activate plans
  -r {DSLW200}, --router {DSLW200}
						select router
  -t, --restart			restart router
  -j, --json			output json
  -f REFRESH, --refresh REFRESH
						refresh display every some seconds
  -u USERNAME, --username USERNAME
						username for the router
  -p PASSWORD, --password PASSWORD
						password for the router
```
