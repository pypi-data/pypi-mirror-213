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
from enum import Enum
import subprocess
from typing import Any, Callable, Optional
# Our imports
from utils.action import EnumAction
from utils.exceptions import *
from utils.settings import Settings
from db import Db

logger = Settings.getLogger(__name__)

class Actions(Enum):
	"""
	Defines the commands that can be used to interact with django.

	Attributes:
		start:
			start the django server
		test:
			runs our unit/integration tests
	"""
	start = "runserver"
	test = "test"
	#stop = "not-implemented"
	#restart = "not-implemented"
	#status = "not-implemented"

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

	@property
	def command(self) -> Actions:
		"""
		Get the currently executing command. This is typically set by self.perform()
  		"""
		if self._command is None:
			raise ValueError('Command has not been set yet')
		return self._command

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
		# Combine our additional arguments into a single string.
		#additional_args = ' '.join(option for option in args)

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
		return self.run_typical_command(Actions.start)

	def test(self) -> str:
		"""
		Run our unit and integration tests.

		Returns:
			str: The output returned by django
		"""
		return self.run_typical_command(Actions.test, None, '--noinput', '--verbosity=0')

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
		if self.command == Actions.start:
			self.sync_browser()

	def handle_output(self, line : str) -> None:
		"""
		Called for each line of input from django.

		Args:
			line (str):
				A line of output printed by django.

		Returns:
			None
		"""
		# Sanitize the value so we have something simple to compare to.
		value = re.sub(r'[\n\r\\]+', '', line or '')

		# Append the line to our output buffer.
		self._output_buffer += f'\n{value}'

		# Show the output to the console (if it's not empty)
		if (value) != '':
			print(value)

		# For each line, fire appropriate events.
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
			case Actions.start:
				# Start our entire app
				return app.start()
			case Actions.test:
				# Run tests
				return app.test()
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

if __name__ == '__main__':
	"""
	This code is only run when this script is called directly (i.e. python bin/app.py)
	"""
	try:
		# Setup the basic configuration for the parser
		parser = argparse.ArgumentParser(
				formatter_class=argparse.RawTextHelpFormatter,
				description=textwrap.dedent("""
					Interact with the django application (similar to manage.py)
				"""),
				epilog="",
		)

		# Define the arguments we will accept from the command line.
		parser.add_argument('action',
						type=Actions,
						action=EnumAction,
						help=textwrap.dedent("""\
							start: Start the django application, and any other tools it depends on.
							test: Run our unit and integration tests
						"""))

		# Parse the arguments provided to our script from the command line
		# These are used as attributes. For example: options.action
		options = parser.parse_args()

		try:
			# Instantiate a new DB object based on our arguments
			app = App()
		except ValueError as ve:
			# One of the options contains bad data. Print the message and exit.
			logger.error(f'Bad option provided: {ve}')
			sys.exit(0)
		except FileNotFoundError as fnf:
			# The options were okay, but we can't find a necessary file (probably the executable)
			logger.error(f'Unable to find a necessary file: {fnf}')
			sys.exit(0)

		try:
			result = app.perform(options.action)
			if result is not None:
				logger.debug(f'App returned ({result})')
		except UnsupportedCommandError as e:
			logger.error("Error: Unknown action. Try --help to see how to call this script.")
			sys.exit(0)

	except KeyboardInterrupt as e:
		logger.info(f'Shutting down server...')
		sys.exit(0)
	except DbStartError as e:
		logger.error('Could not start DB. Cannot continue')
		sys.exit(0)
