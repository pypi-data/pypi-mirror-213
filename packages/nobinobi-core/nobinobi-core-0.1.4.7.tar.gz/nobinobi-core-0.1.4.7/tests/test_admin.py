#      Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from nobinobi_core.admin import OrganisationAdmin, delete_selected
from nobinobi_core.models import Organisation


class MockSuperUser:
    def has_perm(self, perm):
        return True

    def is_active(self):
        return True

    def is_staff(self):
        return True

    pk = 1


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

# If you need to test something using messages
setattr(request, 'session', 'session')
messages = FallbackStorage(request)
setattr(request, '_messages', messages)


class TestNobinobiCoreAdmin(TestCase):

    def setUp(self):
        site = AdminSite()
        self.admin = OrganisationAdmin(Organisation, site)

    @classmethod
    def setUpTestData(cls):
        cls.organisation = Organisation.objects.create(name="Prolibre", short_code="PRO")

    def test_delete_model_organisation(self):
        obj = Organisation.objects.get(name="Prolibre")
        self.admin.delete_model(request, obj)

        deleted = Organisation.objects.filter(name="Prolibre").first()
        self.assertEqual(deleted, None)

    def test_delete_model_with_deleted_method(self):
        obj = Organisation.objects.filter(name="Prolibre")
        user = User.objects.create(id=1, username="Test", is_active=True, is_staff=True, is_superuser=True)
        request.POST = request.POST.copy()
        request.user = user
        request.POST['post'] = True
        self.request = request
        delete_selected(self.admin, request, obj)

        deleted = Organisation.objects.filter(name="Prolibre").first()
        self.assertEqual(deleted, None)
