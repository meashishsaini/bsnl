import urllib3
import logging
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(filename=__package__ + ".log",
						filemode="a",
						format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
						datefmt="%Y-%m-%d %H:%M:%S",
						level=logging.DEBUG)