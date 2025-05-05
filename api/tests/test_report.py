from unittest import TestCase

from rest_framework.test import APITestCase

from api import BASE_URL
from api.serializers.report import ReportSerializer
from api.services.report import ReportService
from api.tests.utils import Utils


class ReportSerializerTestCase(APITestCase):
    pass

class ReportServiceTestCase(TestCase):
    def test_selling_resume(self):
        c = ReportService.get_most_active_customers()
        print(c)
        print(c[0].orders_count)
        print(getattr(c[0], 'bababbababa', None))
        self.assertTrue(True)
