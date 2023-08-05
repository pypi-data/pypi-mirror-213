"""

	Metadata:

		File: db.py
		Project: Django Foundry
		Created Date: 06 Sep 2022
		Author: Jess Mann
		Email: jess.a.mann@gmail.com

		-----

		Last Modified: Fri Apr 21 2023
		Modified By: Jess Mann

		-----

		Copyright (c) 2022 Jess Mann
"""
#!/usr/bin/env python

# Generic imports
import argparse, textwrap, os, re
import sys
from enum import Enum
import subprocess
from shutil import which
import time
# Our imports
from .utils.action import EnumAction

# Default path to the data directory, which we pass directly to postgres
DEFAULT_DATA_PATH = os.environ.get('django_foundry_db_data_path', './pgsql/data')
# Default path to the logfile we want to use.
DEFAULT_LOG_PATH = os.environ.get('django_foundry_log_path', './pgsql/pgsql.log')
# Command to use to interact with the DB. This must be in our path.
EXE = os.environ.get('django_foundry_postgres_bin', "pg_ctl")

class Db:
	"""
	Manages a database instance. This class is responsible for starting, stopping, and restarting the database.

	Attributes:
		data_path (str):
			The path to the data directory for the database.
		log_path (str):
			The path to the logfile for the database.
		user (str):
			The user to run the database as.
		database (str):
			The name of the database to use.
	"""
	_data_path : str
	_log_path : str
	_user : str
	_database : str

	@property
	def log_path(self) -> str:
		return self._log_path

	@property
	def data_path(self) -> str:
		return self._data_path

	@property
	def user(self) -> str:
		return self._user

	@property
	def database(self) -> str:
		return self._database

	@log_path.setter
	def log_path(self, user_input_path : str) -> None:
		"""
		Sets the log path. Assumes that input_path is user input and sanitizes it accordingly.

		Args:
			user_input_path (str): The path provided via user input to sanitize and set.

		Returns:
			None
  		"""
		self._log_path = self.sanitize_path(user_input_path)

	@data_path.setter
	def data_path(self, user_input_path : str) -> None:
		"""
		Sets the data directory path. Assumes that input_path is user input and sanitizes it accordingly.

		Args:
			user_input_path(str): The path provided via user input to sanitize and set.

		Returns:
			None
  		"""
		self._data_path = self.sanitize_path(user_input_path)

	def __init__(self, data_path: str = DEFAULT_DATA_PATH, log_path: str = DEFAULT_LOG_PATH):
		"""
		Sets up our Db object with config options we'll use for this run.

		Args:
			data_path (str, optional):
				The data directory path to use, which is passed directly to Postgres.
				Note: This is sanitized and only accepts these characters: a-zA-Z0-9/_.-
				On windows, this also accepts colons and backslashes.
				Defaults to the DEFAULT_DATA_PATH constant.
			log_path
				The logfile we want Postgres to use.
				Note: This is sanitized and only accepts these characters: a-zA-Z0-9/_.-
				On windows, this also accepts colons and backslashes.
				Defaults to the DEFAULT_LOG_PATH constant.

		Raises:
			ValueError: If the config options provided are not valid, or the files they reference are not found.
			FileNotFoundError: If the postgres executable cannot be found.
  		"""
		# Validation
		if not os.path.isdir(data_path):
			raise ValueError(f'Data path not found: "{data_path}"')
		if not os.path.isfile(log_path):
			raise ValueError(f'Log path not found: "{log_path}"')
		if which(EXE) is None:
			raise FileNotFoundError(f'DB executable not found. Is "{EXE}" in your path?')

		# Set our paths. Note: This calls the property setter, which sanitizes them.
		self.data_path = data_path
		self.log_path = log_path

		self._user = os.environ.get('django_foundry_db_user', 'postgres')
		self._database = os.environ.get('django_foundry_db_database', 'DjangoFoundry')

	def start(self) -> int:
		"""
		Starts the PostgresSQL server (if it is not running) and prints all output to stdout.

		If the server is already running, prints a message indicating so, but does NOT attempt to restart.

		Returns:
			int: The exit code returned from executing the postgres command (pg_ctl), or -1 if the server is already running.
  		"""
		# If we're already running, then just return right away.
		if self.is_running():
			print("Postgres server already running")
			return -1

		# Okay, not running. Try starting it with subprocess.run
		return subprocess.run([EXE, '-D', self.data_path, '-l', self.log_path, 'start'], check=True).returncode

	def restart(self) -> int:
		"""
		Restarts the PostgresSQL server and prints all output to stdout.

		Returns:
			int: The exit code returned from executing the postgres command (pg_ctl)
  		"""
		return subprocess.run([EXE, '-D', self.data_path, '-l', self.log_path, 'restart'], check=True).returncode

	def stop(self) -> int:
		"""
		Stops the PostgresSQL server and prints all output to stdout.

		Returns:
			int: The exit code returned from executing the postgres command (pg_ctl)
  		"""
		return subprocess.run([EXE, '-D', self.data_path, '-l', self.log_path, 'stop'], check=True).returncode

	def status(self) -> int:
		"""
		Checks the status of the postgres server and prints all output to stdout.

		Returns:
			int: The exit code returned from executing the postgres command (pg_ctl)
  		"""
		return subprocess.run([EXE, '-D', self.data_path, '-l', self.log_path, 'status'], check=True).returncode

	def check_errors(self) -> int:
		"""
		Checks the postgres server for errors and prints all output to stdout.
		"""
		cmd = ['psql', '-U', self.user, '-d', self.database, '-c', "SELECT * FROM pg_stat_database_conflicts WHERE datname = current_database();"]
		return subprocess.call(cmd)

	def analyze(self) -> int:
		"""
		Runs an ANALYZE VERBOSE on the database.
		"""
		cmd = ['psql', '-U', self.user, '-d', self.database, '-c', "ANALYZE VERBOSE;"]
		return subprocess.call(cmd)

	def repair_errors(self) -> int:
		"""
		Runs a REINDEX DATABASE on the database.
		"""
		cmd = ['psql', '-U', self.user, '-d', self.database, '-c', "REINDEX DATABASE current_database;"]
		return subprocess.call(cmd)

	def dead_rows(self) -> int:
		"""
		Checks for dead rows in the database.
		"""
		cmd = ['psql', '-U', self.user, '-d', self.database, '-c', "SELECT relname, n_dead_tup FROM pg_stat_user_tables WHERE n_dead_tup > 0;"]
		return subprocess.call(cmd)

	def long_queries(self) -> int:
		"""
		Checks for long running queries in the database.
		"""
		cmd = ['psql', '-U', self.user, '-d', self.database, '-c', "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';"]
		return subprocess.call(cmd)

	def locks(self) -> int:
		"""
		Checks for locks in the database.
		"""
		cmd = ['psql', '-U', self.user, '-d', self.database, '-c', "SELECT pid, relation::regclass, mode, granted FROM pg_locks WHERE NOT granted;"]
		return subprocess.call(cmd)


	def manage(self) -> None:
		"""
		Manages the postgres server, restarting it if it is not running.
		"""
		while True:
			if not self.is_running():
				print("Postgres is not running. Starting it up...")
				self.start()
			else:
				print("Postgres is running.")
			time.sleep(5)

	def is_running(self) -> bool:
		"""
		Determines if the postgres server is running, without printing anything to stdout.

		Returns:
			bool: True if the server is running, False otherwise.

		Raises:
			FileNotFoundError: If postgres is not able to find the data directory
  		"""
		# Create a child process, supressing output
		child = subprocess.run([EXE, '-D', self.data_path, 'status'], stdout = subprocess.PIPE, check=True)

		"""
  		Postgres returns exit code 3 if the server is NOT running, and 4 on error. It returns 0 otherwise.

		See here: https://www.postgresql.org/docs/current/app-pg-ctl.html
			status mode checks whether a server is running in the specified data directory. If it is,
	  		the server's PID and the command line options that were used to invoke it are displayed.
			If the server is not running, pg_ctl returns an exit status of 3.
		 	If an accessible data directory is not specified, pg_ctl returns an exit status of 4.
		"""
		if child.returncode == 4:
			raise FileNotFoundError(f'Postgres is not able to find the data directory: {self.data_path}')
		return not child.returncode

	def sanitize_path(self, user_input_path : str) -> str:
		"""
		Takes arbitrary user input, and sanitizes it to prevent injection attacks.

		NOTE: The return value from this function will generally be passed directly to the command line,
  		so we must be especially careful with what we return.

		Args:
			user_input_path (str): The user input to turn into a path

		Returns:
			str: The sanitized path
		"""
		# Whitelist "good" characters and remove all others

		if os.name == 'nt':
			# If we're running on windows, we must accept colons and backslashes
			return re.sub(r'[^a-zA-Z0-9:/\\_.-]', '', user_input_path)

		# If we're running on a sane operating system, don't allow colons or backslashes.
		return re.sub(r'[^a-zA-Z0-9/_.-]', '', user_input_path)

class Actions(Enum):
	"""
	Defines the options we allow to be passed in from the command line when this script is run.

	Attribues:
		status:
			check the DB status
		start:
			start the DB (if it is not already running)
		restart:
			stop the DB (if it is running) and start it again.
		stop:
			stop the DB (if it is running)
	"""
	START = 'start'
	RESTART = 'restart'
	STATUS = 'status'
	STOP = 'stop'
	CHECK_ERRORS = 'check_errors'
	ANALYZE = 'analyze'
	REPAIR_ERRORS = 'repair_errors'
	MANAGE = 'manage'
	DEAD_ROWS = 'dead_rows'
	LONG_QUERIES = 'long_queries'
	LOCKS = 'locks'

	def __str__(self):
		"""
		Turns an option into a string representation
		"""
		return self.value


if __name__ == '__main__':
	"""
 		This code is only run when this script is called directly (i.e. python bin/db.py)
   	"""

	# Setup the basic configuration for the parser
	parser = argparse.ArgumentParser(
			formatter_class=argparse.RawTextHelpFormatter,
	 		description=textwrap.dedent("""
				Interact with the application's local DB
			"""),
			epilog="",
	)

	# Define the arguments we will accept from the command line.
	parser.add_argument('action',
					 type=Actions,
					 action=EnumAction,
					 help=textwrap.dedent("""\
						Start the local application DB

						status: check the DB status
						start: start the DB (if it is not already running)
						restart: stop the DB (if it is running) and start it again.
						stop: stop the DB (if it is running)
						check_errors: check for errors in the DB
						repair_errors: repair errors in the DB
						analyze: analyze the DB
						dead_rows: check for dead rows in the DB
						long_queries: check for long running queries in the DB
						locks: check for locks in the DB
						manage: manage the DB, restarting it if it is not running
					 """))
	parser.add_argument('-l', '--log',
					 	type=str,
						metavar='path',
						default=DEFAULT_LOG_PATH,
	  					help="Path to the log file for the DB.")
	parser.add_argument('-d', '--data',
					 	type=str,
						metavar='path',
						default=DEFAULT_DATA_PATH,
	  					help="Path to the data directory for postgres.")

	# Parse the arguments provided to our script from the command line
	# These are used as attributes. For example: options.action
	options = parser.parse_args()

	try:
		# Instantiate a new DB object based on our arguments
		db = Db(data_path=options.data, log_path=options.log)
	except ValueError as ve:
		# One of the options contains bad data. Print the message and exit.
		print(f'Bad option provided: {ve}')
		sys.exit()
	except FileNotFoundError as fnf:
		# The options were okay, but we can't find a necessary file (probably the executable)
		print(f'Unable to find a necessary file: {fnf}')
		sys.exit()

	match options.action:
		case Actions.START:
			# Check the status and start the server if it isn't running, and print output to stdout.
			result = db.start()
		case Actions.STOP:
			# Stop the server and print output to stdout.
			result = db.stop()
		case Actions.RESTART:
			# Restart the server and print output to stdout.
			result = db.restart()
		case Actions.STATUS:
			# Check the server status and print output to stdout.
			result = db.status()
		case Actions.CHECK_ERRORS:
			result = db.check_errors()
		case Actions.ANALYZE:
			result = db.analyze()
		case Actions.REPAIR_ERRORS:
			result = db.repair_errors()
		case Actions.DEAD_ROWS:
			result = db.dead_rows()
		case Actions.LONG_QUERIES:
			result = db.long_queries()
		case Actions.LOCKS:
			result = db.locks()
		case Actions.MANAGE:
			db.manage()
		case _:
			print("Error: Unknown action. Try --help to see how to call this script.")

	sys.exit()