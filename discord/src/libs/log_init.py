
import logging

class LogSetting:
	def __init__(self, log_filename):
		if log_filename == "":
			raise ValueError("log_filename is empty.")
		#--- end of if ---
		self.log_filename = log_filename
	#--- end of def __init__ ---

	def log_init(self):
		# logging setting
		logging.basicConfig(
			level=logging.INFO,
			format="[%(asctime)s] - %(levelname)s - %(filename)s(func:%(funcName)s, line:%(lineno)d) %(message)s",
			datefmt="%Y-%m-%d %H:%M:%S",
			encoding="utf-8",
			filename=self.log_filename,
		)

		logger = logging.getLogger(__name__)
		return logger
	#--- end of def log_init ---
#--- end of class LogSetting ---