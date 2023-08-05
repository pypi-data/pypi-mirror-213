"""

	Metadata:

		File: manager.py
		Project: Django Foundry
		Created Date: 18 Aug 2022
		Author: Jess Mann
		Email: jess.a.mann@gmail.com

		-----

		Last Modified: Sat Dec 03 2022
		Modified By: Jess Mann

		-----

		Copyright (c) 2022 Jess Mann
"""
# Generic imports
from __future__ import annotations
# Django extensions
import auto_prefetch
from psqlextra.manager import PostgresManager as PGManager
# App Imports

class Manager(auto_prefetch.Manager):
	'''
	A custom query manager. This creates QuerySets and is used in all models interacting with the db.
	'''

class PostgresManager(PGManager):
	'''
	A custom query manager. This creates querysets and is used in all models interacting with the db (when that db is postgres)
	'''
