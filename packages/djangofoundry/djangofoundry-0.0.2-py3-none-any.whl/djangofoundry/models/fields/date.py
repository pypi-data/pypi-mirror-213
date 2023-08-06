"""


	Metadata:

		File: date.py
		Project: Django Foundry
		Created Date: 18 Aug 2022
		Author: Jess Mann
		Email: jess.a.mann@gmail.com

		-----

		Last Modified: Wed Apr 26 2023
		Modified By: Jess Mann

		-----

		Copyright (c) 2022 Jess Mann

"""
# Generic imports
from __future__ import annotations

# Django Imports
from django.db import models
# Lib Imports
# App Imports

class DateField(models.DateField):
	'''
	Override the default django field
	'''

class DateGroupField(models.JSONField):
	"""
	Accepts a single date, or a list of dates, or a range of dates, stored in a json field.
	"""

class DateTimeField(models.DateTimeField):
	'''
	Override the default django field
	'''

class InsertedNowField(DateTimeField):
	'''
	Override the default django field to customize typical init options
	'''
	def __init__(self, *_args, **kwargs):
		# Default is not allowed. Accept it as an arg (thus pulling it from kwargs) and then ignore it.
		super().__init__(auto_now_add=True, null = False, blank = False, **kwargs)


class UpdatedNowField(DateTimeField):
	'''
	Override the default django field to customize typical init options
	'''
	def __init__(self, *_args, **kwargs):
		# Default is not allowed. Accept it as an arg (thus pulling it from kwargs) and then ignore it.
		super().__init__(auto_now=True, null = False, blank = False, **kwargs)
