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
import platform
import shutil
from enum import Enum
import subprocess
from typing import Any, Callable, Optional
import json
import getpass
import logging
import psutil
from jinja2 import Environment, FileSystemLoader

# Our imports
from djangofoundry.scripts.utils.exceptions import DbStartError, UnsupportedCommandError
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
	PAGE = 'page'
	MODEL = 'model'

	def __str__(self):
		"""
		Turns an option into a string representation
		"""
		return self.value

	def __repr__(self):
		return self.value

class App:
	"""
	Our main application class. This script allows us to start, stop, and restart our django server.
	"""
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

		Note: This is a work in progress.

		Returns:
			A string indicating the status of the setup.
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

		Returns:
			A string indicating the status of the setup.
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
		data['scripts'] = { 'test': 'echo "Error: no test specified" && exit 1' }
		data['author'] = getpass.getuser()
		data['license'] = 'BSD-3-Clause'

		with open('package.json', 'w') as f:
			json.dump(data, f, indent=2)

		self.run_subprocess(["npm", "install"])
		self.run_subprocess(["npm", "install", "@angular/cli"])
		self.run_subprocess(["ng", "new", self.project_name, "--skip-git", "--skip-install"])
		os.chdir(self.directory) # Switch back to the original directory
		return f"Angular setup completed for {self.project_name}"

	def install_dependencies(self) -> None:
		"""
		Check if npm is installed and call install_npm() if it's not.

		Returns:
			None
		"""
		if not shutil.which('npm'):
			logger.info('NPM not found. Attempting to install...')
			self.install_npm()

	def install_npm(self) -> str:
		"""
		Attempt to install npm on the system.

		Returns:
			A string indicating the status of the installation.
		"""
		os_name = platform.system()

		if os_name == 'Linux' or os_name == 'Darwin':
			try:
				self.run_subprocess(['curl', 'https://www.npmjs.com/install.sh', '|', 'sh'])
				return "npm installed successfully on Linux or macOS"
			except subprocess.CalledProcessError as process_e:
				raise EnvironmentError(f"Error installing npm on Linux or macOS: {process_e}")
		elif os_name == 'Windows':
			try:
				self.run_subprocess(['powershell', '-Command', 'iex (New-Object Net.WebClient).DownloadString("https://www.npmjs.com/install.ps1")'])
				return "npm installed successfully on Windows"
			except subprocess.CalledProcessError as process_e:
				raise EnvironmentError(f"Error installing npm on Windows: {process_e}")
		else:
			raise EnvironmentError("Unsupported operating system")


	def check_environment(self) -> None:
		"""
		Check the environment to make sure the setup will run smoothly.

		Returns:
			None

		Raises:
			EnvironmentError: If the environment is not suitable for running the setup.
			OSError: If the operating system is not supported.
		"""
		# Check Python version
		if sys.version_info < (3, 10):
			raise EnvironmentError("Python 3.10 or above is required.")
		logger.debug("Python version check passed.")

		# Check directory permissions
		if not os.access(self.directory, os.W_OK):
			raise EnvironmentError("The provided directory does not have write permissions.")
		logger.debug("Directory permissions check passed.")

		# Check disk space
		disk_usage = psutil.disk_usage('/')
		if disk_usage.free < 10**9:  # less than 1GB
			raise EnvironmentError("Insufficient disk space. At least 1GB is required.")
		logger.debug("Disk space check passed.")

		# Check RAM
		ram_usage = psutil.virtual_memory()
		if ram_usage.available < 10**6:  # less than 1MB
			raise EnvironmentError("Insufficient RAM. At least 1MB is required.")
		logger.debug("RAM check passed.")

		logger.info("All environment checks passed.")

	def confirm_setup(self) -> None:
		"""
		Confirm the setup has been completed successfully.
		
		Returns:
			None
			
		Raises:
			EnvironmentError: If the setup was not completed successfully.
		"""
		# Check for package dependencies
		dependencies = ["npm"]
		for dependency in dependencies:
			if not shutil.which(dependency):
				raise EnvironmentError(f"The {dependency} command isn't available. Please install it.")
		logger.debug("npm dependency check passed.")

		# Check for pip dependencies via imports
		dependencies = ["django", "psutil"]
		for dependency in dependencies:
			try:
				__import__(dependency)
			except ImportError:
				raise EnvironmentError(f"The {dependency} package isn't available. Please install it.")
		logger.debug("python dependency check passed.")

	def setup(self) -> None:
		"""
		Setup both Django and Angular projects and apps with given names.

		Returns:
			None
		"""
		os.makedirs(self.directory, exist_ok=True)

		self.check_environment()
		self.install_dependencies()
		self.django_setup()
		self.angular_setup()
		self.confirm_setup()

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

		Raises:
			ValueError: If the subprocess doesn't return any output.
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

		except KeyboardInterrupt:
			# Allow terminating the dev server from the command line.
			logger.info('Stopping server...')

		return self._output_buffer

	def run_subprocess(self, cmd_list: list[str], print_output: bool = True) -> None:
		"""
		Run the subprocess with the given command list.

		Args:
			cmd_list (list[str]):
				A list of strings to pass to the subprocess.
			print_output (bool):
				Whether to print the output of the subprocess to the console.

		Raises:
			ValueError: If the subprocess has no output.
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
			**kwargs:
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
	def status(self) -> bool:
		"""
		Determine the status of our application.
		"""
		server_process_names = ["runserver", "gunicorn", "daphne"]
		for process in psutil.process_iter(['name']):
			if process.info['name'] in server_process_names:
				return True

		return False

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

		Args:
			line (str):
				A line of output from django.
			print_output (bool):
				Whether to print the output of the subprocess to the console.

		Raises:
			ValueError: If the subprocess has no output.
		"""
		value = re.sub(r'[\n\r\\]+', '', line or '')
		self._output_buffer += f'\n{value}'
		if (value) != '' and print_output:
			print(value)

		match value.lower():
			case 'quit the server with ctrl-break.':
				logger.debug('Django started successfully')
				self.on_django_started()

	def perform(self, command: Actions, page_name: str = None, model_name: str = None) -> Any:
		"""
		Perform an action given a (string) command

		Args:
			command (Actions): The action to perform.
			page_name (str): The name of the page to create.
			model_name (str): The name of the model to create.

		Returns:
			Any: The result of the action.
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
			case Actions.STOP:
				# Stop our app
				return self.stop()
			case Actions.STATUS:
				# Determine the status of our app
				return self.status
			case Actions.PAGE:
				if page_name:
					return self.create_new_page(page_name)
				else:
					raise ValueError("Page name is required for 'page' action.")
			case Actions.MODEL:
				if model_name:
					return self.create_django_model(model_name, model_name.capitalize())
				else:
					raise ValueError("Model name is required for 'model' action.")
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


	def create_new_page(self, page_name: str) -> None:
		"""
		Create a new page in Django and Angular.

		Args:
			page_name (str): The name of the page to create.

		Returns:
			None
		"""
		try:
			self.create_angular_component(page_name)
			self.setup_routing(page_name)
			self.create_django_controller(page_name)
			logging.info(f"Successfully created new page '{page_name}' in Django and Angular.")
		except Exception as e:
			logging.error(f"Failed to create new page '{page_name}': {e}")

	def create_angular_component(self, page_name: str) -> None:
		"""
		Create a new Angular component.

		Args:
			page_name (str): The name of the page to create.

		Returns:
			None
		"""
		try:
			subprocess.run(["ng", "generate", "component", page_name], check=True)
		except subprocess.CalledProcessError as process_e:
			logging.error(f"Failed to create Angular component '{page_name}': {process_e}")
			raise

	def setup_routing(self, page_name: str) -> None:
		"""
		Set up routing for the new Angular component.

		Args:
			page_name (str): The name of the page to create.

		Returns:
			None
		"""
		routing_file = "src/app/app-routing.module.ts"
		try:
			with open(routing_file, "r", encoding="utf-8") as file:
				lines = file.readlines()

			# Add import statement for the new component
			import_statement = f"import {{ {page_name.capitalize()}Component }} from './{page_name}/{page_name}.component';\n"
			lines.insert(-1, import_statement)

			# Add new route for the new component
			new_route = f"  {{ path: '{page_name}', component: {page_name.capitalize()}Component }},\n"
			for index, line in enumerate(lines):
				if "routes: Routes" in line:
					lines.insert(index + 1, new_route)
					break

			with open(routing_file, "w") as file:
				file.writelines(lines)

		except FileNotFoundError as fnf:
			logging.error(f"Failed to set up routing for '{page_name}': {fnf}")
			raise

	def create_django_controller(self, page_name: str) -> None:
		"""
		Create a new Django controller.

		Args:
			page_name (str): The name of the page to create.

		Returns:
			None
		"""
		controllers_dir = "backend/controllers"
		os.makedirs(controllers_dir, exist_ok=True)

		controller_file = os.path.join(controllers_dir, f"{page_name}.py")
		try:
			with open(controller_file, "w") as file:
				file.write(f"from django.shortcuts import render\n\n")
				file.write(f"def {page_name}_view(request):\n")
				file.write(f"    return render(request, '{page_name}.html')\n")
		except IOError as ioe:
			logging.error(f"Failed to create Django controller '{page_name}': {ioe}")
			raise

	def create_new_model(self, model_name: str) -> None:
		"""
		Create a new Django model using Jinja2 templates.

		Args:
			model_name (str): The name of the model to create.

		Returns:
			None
		"""
		env = Environment(loader=FileSystemLoader("templates/jinja/model"))

		model_dir = f"backend/models/{model_name}"
		os.makedirs(model_dir, exist_ok=True)

		for template_name in env.list_templates():
			template = env.get_template(template_name)
			rendered_template = template.render(model_name=model_name)
			output_file = os.path.join(model_dir, template_name.replace(".jinja", ".py"))
			with open(output_file, "w") as file:
				file.write(rendered_template)


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
	parser.add_argument('--page-name', help='The name of the page to create.')
	parser.add_argument('--model-name', help='The name of the model to create.')
	args = parser.parse_args()

	# Load settings
	settings = Settings(args.settings)

	app = App(args.project_name, args.author_name, settings, args.directory, args.frontend_dir, args.backend_dir)
	command = Actions(args.action)

	result = app.perform(command, args.page_name, args.model_name)
	if result is not None:
		print(f'App returned ({result})')

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		logger.info(f'Shutting down server...')
		sys.exit(0)
	except DbStartError:
		logger.error('Could not start DB. Cannot continue')
		sys.exit(0)
	except EnvironmentError as env_error:
		logger.error(f'Cannot run script in the current environment. {env_error}')
		sys.exit(0)
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(0)
