#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_nobinobi-core
------------

Tests for `nobinobi-core` models module.
"""

from django.test import TestCase
from django.utils import timezone

from nobinobi_core.models import Holiday, Organisation, OrganisationClosure


class TestNobinobiCoreModels(TestCase):

    def setUp(self):
        self.holiday = Holiday(name="My entry title", date=timezone.localdate())
        self.organisation = Organisation(name="Prolibre", short_code="PRO")
        self.organisation_closure = OrganisationClosure(from_date=timezone.localdate(), end_date=timezone.localdate(),
                                              organisation=self.organisation)

    def test_str_representation_holiday(self):
        self.assertEqual(str(self.holiday), "{} - {}".format(self.holiday.name, self.holiday.date))

    def test_str_representation_organisation(self):
        self.assertEqual(str(self.organisation), "{} - {}".format(self.organisation.name, self.organisation.short_code))

    def test_str_representation_organisation_closure(self):
        self.assertEqual(str(self.organisation_closure),
                         "{} ({} | {})".format(self.organisation.name, self.organisation_closure.from_date,
                                               self.organisation_closure.end_date))

    def tearDown(self):
        pass
