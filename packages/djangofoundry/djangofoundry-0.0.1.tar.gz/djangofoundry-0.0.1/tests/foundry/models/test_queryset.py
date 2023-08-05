"""

	Metadata:

		File: test_queryset.py
		Project: Django Foundry
		Created Date: 09 Apr 2023
		Author: Jess Mann
		Email: jess.a.mann@gmail.com

		-----

		Last Modified: Wed May 10 2023
		Modified By: Jess Mann

		-----

		Copyright (c) 2023 Jess Mann
"""
from math import sqrt
from django.test import TestCase
from model_bakery import baker
from models.abstract import QuerySet
from django.db.models import Q
from unittest.mock import MagicMock

# Create a mock model using model_bakery
class Case:
	objects = QuerySet.as_manager()

class QuerySetTestCase(TestCase):
	model = Case
	app = 'django-foundry'
	model_name = 'Case'

	@classmethod
	def setUpClass(cls):
		super().setUpClass()

		# Assign the mock model to a class attribute
		cls.model = Case
		cls.model._meta = type(
			'Meta', (), {'app_label': cls.app, 'model_name': cls.model_name})

	@classmethod
	def setUpTestData(cls):
		super().setUpTestData()

		cls.queryset = cls.model.objects.all()

		# Store case attributes in a dict so we can reference them in tests.
		cls.model_attributes = [
			{
				'case_type': 'test_case_1',
				'case_id': 5,
				'summary': 'test',
				'category': 'value1',
			},
			{
				'case_type': 'test_case_2',
				'case_id': 100,
				'summary': 'test2',
				'category': 'value2',
			},
			{
				'case_type': 'test_case_3',
				'case_id': -5,
				'summary': '',
				'category': 'value_3',
				'status': 'open',
				'processing_ms': 9,
			},
			{
				'case_type': 'test_case_4',
				'status': 'open',
				'location': '10023',
				'processing_ms': 1,
				'summary': None,
			},
			{
				'case_type': 'test_case_5',
				'status': 'closed',
				'location': '52312',
				'processing_ms': 2,
			},
			{
				'case_type': 'test_case_6',
				'status': '',
				'location': '',
				'processing_ms': 3,
			}
		]

		cls.models : list[cls.model] = []
		for attribs in cls.model_attributes:
			model = baker.make(f'{cls.app}.{cls.model_name}', **attribs)
			cls.models.append(model)

	def _create_sample_cases(self):
		# Create a list of cases to test with
		cases = []
		for attribs in self.model_attributes:
			cases.append(self.model(**attribs))
		return cases

	def _create_sample_documents(self, cases : list):
		# Create a list of documents to test with
		document_attributes = [
			{
				'case_type': 'test_document_1',
				'document_type': 'invoice',
			},
			{
				'case_type': 'test_document_2',
				'document_type': 'recalc',
			},
			{
				'case_type': 'test_document_3',
				'document_type': 'invoice',
			},
			{
				'case_type': 'test_document_4',
				'document_type': 'recalc',
			},
			{
				'case_type': 'test_document_5',
				'document_type': 'invoice',
			},
			{
				'case_type': 'test_document_6',
				'document_type': 'recalc',
			},
		]

		documents = []

		for i in range(len(cases)):
			doc = baker.make(f'{self.app}.Document', case=cases[i], **document_attributes[i])
			documents.append(doc)

		return documents

	def test_is_evaluated(self):
		qs = self.model.objects.all()
		self.assertFalse(qs.is_evaluated())
		list(qs)
		self.assertTrue(qs.is_evaluated())

	def test_field_is_numeric(self):
		self.assertTrue(self.model.objects.field_is_numeric("case_id"))
		self.assertFalse(self.model.objects.field_is_numeric("summary"))

	def test_latest_value(self):
		latest_value = self.model.objects.latest_value("category")
		self.assertEqual(latest_value, self.models[-1].category)

	def test_has_smallest(self):
		qs = self.model.objects.has_smallest("id")
		self.assertTrue(qs.exists())
		self.assertEqual(qs.first().id, 1)

	def test_has_largest(self):
		qs = self.model.objects.has_largest("id")
		self.assertTrue(qs.exists())
		self.assertEqual(qs.first().id, self.models[-1].id)

	def test_has_blank(self):
		qs = self.model.objects.has_blank("summary", include_null=False)
		self.assertTrue(qs.exists())
		for model in qs:
			self.assertEqual(model.summary, '')
		self.assertEqual(qs.count(), 1)

	def test_has_blank_or_null(self):
		qs = self.model.objects.has_blank("summary", include_null=True)
		self.assertTrue(qs.exists())
		for model in qs:
			# assert it is a blank string or null
			self.assertTrue(model.summary == '' or model.summary is None)
		self.assertEqual(qs.count(), 4)

	def test_have_blanks(self):
		qs = self.model.objects.have_blanks(number_of_blank_fields=1, include_null=False)
		self.assertTrue(qs.exists())
		for model in qs:
			# test that at least one field of the property (any field) is blank
			blank = False
			for field in model._meta.get_fields():
				if getattr(model, field.name) == '':
					blank = True
					break
			self.assertTrue(blank)
		self.assertEqual(qs.count(), 2)

	def test_have_multiple_blanks(self):
		total_blanks = 2
		qs = self.model.objects.have_blanks(number_of_blank_fields=total_blanks, include_null=False)
		self.assertTrue(qs.exists())
		for model in qs:
			# count the blanks
			blank_count = 0
			for field in model._meta.get_fields():
				if getattr(model, field.name) == '':
					blank_count += 1
			self.assertEqual(blank_count, total_blanks)
		self.assertEqual(qs.count(), 1)

	def test_total(self):
		total = self.model.objects.total("case_id")
		# sum the values of all case_id
		expected_total = 0
		for model in self.models:
			expected_total += model.case_id

		self.assertEqual(total, expected_total)

	def test_request(self):
		# Register a filter for testing
		def example_filter(queryset):
			return queryset.filter(category="value1")

		QuerySet.filters["example_filter"] = example_filter

		qs = self.model.objects.request("example_filter")
		self.assertTrue(qs.exists())
		self.assertEqual(qs.first().category, self.models[0].category)

	def test_apply_filter(self):
		# Register a filter for testing
		def example_filter(queryset):
			return queryset.filter(category="value1")

		QuerySet.filters["example_filter"] = example_filter

		qs = self.model.objects.apply_filter("example_filter")
		self.assertTrue(qs.exists())
		self.assertEqual(qs.first().category, self.models[0].category)

	def test_apply_filter_raises_error(self):
		with self.assertRaises(NotImplementedError):
			self.model.objects.apply_filter("non_existent_filter")

	def test_filter_by_related(self):
		cases = self._create_sample_cases()
		documents = self._create_sample_documents(cases)
		result = self.model.objects.filter_by_related('documents', Q(document_type='invoice'))
		self.assertEqual(len(result), 3)
		# compare results set to our expected cases
		self.assertCountEqual(result, [cases[0], cases[2], cases[4]])

	def test_group_report(self):
		result = self.model.objects.group_report('status')
		expected_result = {'open': 2, 'closed': 1}
		self.assertEqual(result, expected_result)

	def test_group_total(self):
		result = self.model.objects.group_total('status', 'open')
		self.assertEqual(result, 10)
		result = self.model.objects.group_total('status', 'closed')
		self.assertEqual(result, 1)

	def test_summarize_x_by_average_y(self):
		result = self.model.objects.summarize_x_by_average_y('status', 'processing_time')
		expected_result = {'open': 5.0, 'closed': 1.0}
		self.assertEqual(result, expected_result)

	def test_summarize_x_by_sum_y(self):
		result = self.model.objects.summarize_x_by_sum_y('status', 'processing_time')
		expected_result = {'open': 10.0, 'closed': 1.0}
		self.assertEqual(result, expected_result)

	def test_summarize_x_by_high_y(self):
		cases = self.create_sample_cases()
		result = self.model.objects.summarize_x_by_high_y('status', 'processing_time')
		expected_result = {'open': 1, 'closed': 0}
		self.assertEqual(result, expected_result)

	def test_summarize_x_by_low_y(self):
		cases = self.create_sample_cases()
		result = self.model.objects.summarize_x_by_low_y('status', 'processing_time')
		expected_result = {'open': 0, 'closed': 1}
		self.assertEqual(result, expected_result)

	def test_anomalies_in(self):
		cases = self.create_sample_cases()
		result = self.model.objects.anomalies_in('processing_time', deviations=1)
		self.assertEqual(len(result), 1)
		self.assertCountEqual(result, [cases[1]])

	def test_summarize_distribution(self):
		cases = self.create_sample_cases()
		result = self.model.objects.summarize_distribution('processing_time', bins=5)
		expected_result = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0}
		self.assertEqual(result, expected_result)

	def test_summarize_x_by_y_distribution(self):
		cases = self.create_sample_cases()
		result = self.model.objects.summarize_x_by_y_distribution('status', 'processing_time', bins=5)
		expected_result = {
			'open': {0: 1, 1: 0, 2: 1, 3: 0, 4: 0},
			'closed': {0: 0, 1: 1, 2: 0, 3: 0, 4: 0}
		}
		self.assertEqual(result, expected_result)

	def test_count_unique(self):
		cases = self.create_sample_cases()
		result = self.model.objects.count_unique('status')
		self.assertEqual(result, 2)

	def test_count_x_by_unique_y(self):
		expected = {'open': 1, 'closed': 0}
		actual = self.model.objects.count_x_by_unique_y('status', 'location')
		self.assertEqual(actual, expected)

	def test_median(self):
		expected = 2.5
		actual = self.model.objects.median('processing_time')
		self.assertAlmostEqual(actual, expected)

	def test_percentile(self):
		expected = 2
		actual = self.model.objects.percentile('processing_time', 0.5)
		self.assertEqual(actual, expected)

	def test_mode(self):
		expected = 'open'
		actual = self.model.objects.mode('status')
		self.assertEqual(actual, expected)

	def test_variance(self):
		expected = 1.25
		actual = self.model.objects.variance('processing_time')
		self.assertAlmostEqual(actual, expected)

	def test_standard_deviation(self):
		expected = sqrt(1.25)
		actual = self.model.objects.standard_deviation('processing_time')
		self.assertAlmostEqual(actual, expected)

	def test_covariance(self):
		expected = 1.25
		actual = self.model.objects.covariance('processing_time', 'processing_time')
		self.assertAlmostEqual(actual, expected)

	def test_correlation(self):
		expected = 1.0
		actual = self.model.objects.correlation('processing_time', 'processing_time')
		self.assertAlmostEqual(actual, expected)

	def test_linear_regression(self):
		expected = (0.0, 1.0)
		actual = self.model.objects.linear_regression('processing_time', 'processing_time')
		self.assertAlmostEqual(actual[0], expected[0])
		self.assertAlmostEqual(actual[1], expected[1])
