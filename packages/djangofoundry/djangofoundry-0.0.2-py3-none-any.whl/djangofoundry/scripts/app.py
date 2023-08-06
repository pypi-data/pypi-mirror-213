"""

	Metadata:

		File: app.py
		Project: Django Foundry
		Created Date: 06 Sep 2022
		Author: Jess Mann
		Email: jess.a.mann@gmail.com

		-----

		Last Modified: Sat Dec 03 2022
		Modified By: Jess Mann

		-----

		Copyright (c) 2022 Jess Mann
"""
#!/usr/bin/env python

# Generic imports
from __future__ import annotations
import argparse, textwrap, os, re, sys
import shutil
from enum import Enum
import subprocess
from typing import Any, Callable, Optional
import json
import getpass
import logging
import psutil

# Our imports
from djangofoundry.scripts.utils.action import EnumAction
from djangofoundry.scripts.utils.exceptions import *
from djangofoundry.scripts.utils.settings import Settings
from djangofoundry.scripts.db import Db

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

class Actions(Enum):
	"""
	Defines the commands that can be used to interact with django.

	Attributes:
		start:
			start the django server
		test:
			runs our unit/integration tests
	"""
	START = "runserver"
	TEST = "test"
	STOP = "stop"
	RESTART = "restart"
	STATUS = "status"
	SETUP = 'setup'

	def __str__(self):
		"""
		Turns an option into a string representation
		"""
		return self.value

	def __repr__(self):
		return self.value

class App:
	_command : Actions
	_output_buffer : str = ''
	project_name : str
	directory : str
	frontend_dir : str
	backend_dir : str
	settings : Settings | None = None

	def __init__(self, project_name='myproject', author_name=None, settings = None, directory : str = '.', frontend_dir='frontend', backend_dir='backend'):
		self.project_name = project_name
		self.directory = directory
		self.frontend_dir = directory + '/' + frontend_dir
		self.backend_dir = directory + '/' + backend_dir
		self.author_name = author_name or getpass.getuser()
		self.settings = settings

	@property
	def command(self) -> Actions:
		"""
		Get the currently executing command. This is typically set by self.perform()
  		"""
		if self._command is None:
			raise ValueError('Command has not been set yet')
		return self._command
	
	def django_setup(self) -> str:
		"""
		Setup the Django project and app with given names.
		"""
		os.makedirs(self.backend_dir, exist_ok=True)
		os.chdir(self.backend_dir) # Switch to the backend directory before running Django commands
		self.run_subprocess(["pip", "install", "django"])
		self.run_subprocess(["django-admin", "startproject", self.project_name, '.'])
		self.run_subprocess(["python", "manage.py", "startapp", self.project_name])
		os.chdir(self.directory) # Switch back to the original directory
		return f"Django setup completed for {self.project_name}"

	def angular_setup(self) -> str:
		"""
		Setup the Angular project and app with given names.
		"""
		os.makedirs(self.frontend_dir, exist_ok=True)
		os.chdir(self.frontend_dir) # Switch to the frontend directory before running Angular commands
		self.run_subprocess(["npm", "init", "-y"])

		with open('package.json') as f:
			data = json.load(f)

		data['name'] = self.project_name
		data['version'] = '1.0.0'
		data['description'] = f'{self.project_name} - an Angular-Django project'
		data['main'] = 'index.js'
		data['scripts'] = {
			'test': 'echo "Error: no test specified" && exit 1'
		}
		data['author'] = getpass.getuser()
		data['license'] = 'BSD-3-Clause'

		with open('package.json', 'w') as f:
			json.dump(data, f, indent=2)

		self.run_subprocess(["npm", "install"])
		self.run_subprocess(["npm", "install", "@angular/cli"])
		self.run_subprocess(["ng", "new", self.project_name, "--skip-git", "--skip-install"])
		os.chdir(self.directory) # Switch back to the original directory
		return f"Angular setup completed for {self.project_name}"
	
	def check_environment(self):
		"""
		Check the environment to make sure the setup will run smoothly.
		"""
		# Check Python version
		if sys.version_info < (3, 10):
			raise EnvironmentError("Python 3.10 or above is required.")
		logger.debug("Python version check passed.")
		
		# Check directory permissions
		if not os.access(self.directory, os.W_OK):
			raise EnvironmentError("The provided directory does not have write permissions.")
		logger.debug("Directory permissions check passed.")
		
		# Check for Django and Angular dependencies
		dependencies = ["django", "npm"]
		for dependency in dependencies:
			if not shutil.which(dependency):
				raise EnvironmentError(f"The {dependency} command isn't available. Please install it.")
		logger.debug("Dependencies check passed.")
		
		# Check disk space
		disk_usage = psutil.disk_usage('/')
		if disk_usage.free < 10**9:  # less than 1GB
			raise EnvironmentError("Insufficient disk space. At least 1GB is required.")
		logger.debug("Disk space check passed.")

		# Check RAM
		ram_usage = psutil.virtual_memory()
		if ram_usage.available < 10**9:  # less than 1GB
			raise EnvironmentError("Insufficient RAM. At least 1GB is required.")
		logger.debug("RAM check passed.")
		
		logger.info("All environment checks passed.")

	def setup(self):
		"""
		Setup both Django and Angular projects and apps with given names.
		"""
		os.makedirs(self.directory, exist_ok=True)

		self.check_environment()
		self.django_setup()
		self.angular_setup()

	def run(self, command : Actions, callback : Optional[Callable] = None, *args, **kwargs) -> str:
		"""
		Run a django command in a similar way to manage.py

		Args:
			command (str):
				A command that django will accept. For example: runserver
			callback (Callable):
				A function to call after the command completes.
			*args:
				positional arguments to pass to django
			**kwargs:
				named arguments to pass to django

		Returns:
			str: The output returned by django.
		"""
		# Run the django dev server in a subprocess, and pipe output to the command.stdout property.
		try:
			# Clear the output buffer for this run
			self._output_buffer = ''

			# Subprocess wants each arg as a separate entry in a list... combine args into our known command string.
			script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../manage.py')
			input_str = ['python', script_path, f'{command}'] + [arg for arg in args]
			process = subprocess.Popen(input_str, stdout=subprocess.PIPE, encoding="utf-8")

			if not process.stdout:
				raise ValueError('No output from subprocess')

			# Stdout is a stream, so this acts like a while() loop as long as django is running.
			for line in process.stdout:
				# Pass all output to our handler, which may trigger events.
				self.handle_output(line)

			# Wait for output that may not have hit the stream yet. (TODO: This may not be necessary?)
			process.wait()

			# Issue our callback, as we're now finished.
			if callback is not None:
				logger.debug('Issuing callback on completion')
				callback(process)

		except KeyboardInterrupt as ki:
			# Allow terminating the dev server from the command line.
			logger.info('Stopping server...')

		return self._output_buffer
	
	def run_subprocess(self, cmd_list: list[str], print_output: bool = True) -> None:
		"""
		Run the subprocess with the given command list.
		"""
		process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, encoding="utf-8")
		if not process.stdout:
			raise ValueError('No output from subprocess')

		for line in process.stdout:
			self.handle_output(line, print_output)
		process.wait()


	def run_typical_command(self, command : Actions, callback : Optional[Callable] = None, *args, **kwargs) -> str:
		"""
		Runs a command that requires our normal tool suite (such as the DB) to be running.

		Args:
			command (str):
				A command that django will accept. For example: runserver
			callback (Callable):
				A function to call after the command completes.
			*args:
				positional arguments to pass to django
			**options:`
				named arguments to pass to django

		Returns:
			str: The output returned by django
		"""
		# Attempt to start the db first. If it fails, this will print output and exit.
		self._start_db()

		# Pass any command we asked for over to django.
		return self.run(command, callback, *args, **kwargs)

	def start(self) -> str:
		"""
		Start the django app, and any other tools it depends on.

		Returns:
			str: The output returned by django
		"""
		return self.run_typical_command(Actions.START)

	def test(self) -> str:
		"""
		Run our unit and integration tests.

		Returns:
			str: The output returned by django
		"""
		return self.run_typical_command(Actions.TEST, None, '--noinput', '--verbosity=0')

	def stop(self):
		"""
		Stop any tools that were started via start(), including the django app.
		"""
		raise NotImplementedError()

	@property
	def status(self):
		"""
		Determine the status of our application.
		"""
		raise NotImplementedError()

	def sync_browser(self):
		"""
		Start a process to sync the browser with the application state.

		We currently use browser-sync for this. When our app files change, the browser will automatically refresh the page.
  		"""
		# Subprocess wants each arg as a separate entry in a list... combine args into our known command string.
		input_str = ['npm', 'run', 'serve']
		logger.debug('Starting browsersync')
		process = subprocess.Popen(input_str, stdout=subprocess.PIPE, encoding="utf-8", shell=True)

		if not process.stdout:
			raise ValueError('No output from subprocess')

		# Stdout is a stream, so this acts like a while() loop as long as django is running.
		for line in process.stdout:
			# Pass all output to our handler, which may trigger events.
			self.handle_output(line)

		# Wait for output that may not have hit the stream yet. (TODO: This may not be necessary?)
		process.wait()

	def on_django_started(self) -> None:
		"""
		Called when the django dev server is fully started.
  		"""
		# If we're trying to start our app, then run our next action
		if self.command == Actions.START:
			self.sync_browser()

	def handle_output(self, line : str, print_output: bool = True) -> None:
		"""
		Called for each line of input from django.
		"""
		value = re.sub(r'[\n\r\\]+', '', line or '')
		self._output_buffer += f'\n{value}'
		if (value) != '' and print_output:
			print(value)

		match value.lower():
			case 'quit the server with ctrl-break.':
				logger.debug('Django started successfully')
				self.on_django_started()

	def perform(self, command : Actions) -> Any:
		"""
		Perform an action given a (string) command

		Args:
			command (Actions): The action to perform.
  		"""
		# Save the command for later
		self._command = command

		# Determine what method to run.
		match command:
			case Actions.START:
				# Start our entire app
				return self.start()
			case Actions.TEST:
				# Run tests
				return self.test()
			case Actions.SETUP:
				# Setup our app
				return self.setup()
			case _:
				raise UnsupportedCommandError(f"Unknown command {command}.")

	def _start_db(self) -> None:
		"""
		Call db.py to start the DB. This prints output and (under certain circumstances) exits.

		Returns:
			None
		"""
		db = Db()
		if db.is_running():
			logger.debug('DB is already running')
		else:
			logger.info('Starting DB...')
			_result = db.start()

			if not db.is_running():
				raise DbStartError('DB not running after start')

def main():
	"""
	This code is only run when this script is called directly (i.e. python bin/app.py)
	"""
	parser = argparse.ArgumentParser(description='Setup and manage the Django application.')
	parser.add_argument('action', choices=[e.value for e in Actions], help='The action to perform.')
	parser.add_argument('-p', '--project-name', default='myproject', help='The name of the project.')
	parser.add_argument('-a', '--author-name', help='The name of the author.')
	parser.add_argument('-d', '--directory', default='.', help='The directory for the project.')
	parser.add_argument('-f', '--frontend-dir', default='frontend', help='The directory for the frontend (relative to -d).')
	parser.add_argument('-b', '--backend-dir', default='backend', help='The directory for the backend (relative to -d).')
	parser.add_argument('-s', '--settings', default='conf/settings.yaml', help='The settings file to use.')
	args = parser.parse_args()

	# Load settings
	settings = Settings(args.settings)

	app = App(args.project_name, args.author_name, settings, args.directory, args.frontend_dir, args.backend_dir)
	command = Actions(args.action)

	result = app.perform(command)
	if result is not None:
		print(f'App returned ({result})')

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt as e:
		logger.info(f'Shutting down server...')
		sys.exit(0)
	except DbStartError as e:
		logger.error('Could not start DB. Cannot continue')
		sys.exit(0)
	except EnvironmentError as e:
		logger.error(f'Cannot run script in the current environment. {e}')
		sys.exit(0)
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(0)
