from django.test import TestCase
from django.test import SimpleTestCase

class ApiTests(SimpleTestCase):
    
    def test_feedGetHttpStatus_200(self):
        response = self.client.get('/api/feed')
        self.assertEqual(response.status_code, 200)

    def test_feedItemGetHttpStatus_404(self):
        response = self.client.get('/api/feed/123')
        self.assertEqual(response.status_code, 404)