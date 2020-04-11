import time
from django.test import TestCase

class MovieListTests(TestCase):

    def test_cache_refresh(self):
        """
        Call the moves endpoint fist time, get the time refreshed
        Wait 30 seconds
        Call the endoint a second time, data should be taken from cache - so no context data in response
        Wait 31 seconds
        Call the endpoint a 3rd time, cache has expired, so time refreshed value should be different
        """
        response1 = self.client.get('/movies/')
        self.assertEqual(response1.status_code, 200)
        context1 = response1.context_data
        first_time = context1['last_refresh']

        time.sleep(30)  # wait 30 seconds

        response2 = self.client.get('/movies/')
        self.assertEqual(response2.status_code, 200)
        try:
            context2 = response2.context_data
            second_time = context2['last_refresh']
            self.assertEqual(second_time, first_time)
        except AttributeError:
            # get_context_data won't be called as it is retrieved from cache.
            # context data not added to response
            # Note, we could always compare the HTML output, where I have added the time at the bottom.
            pass

        time.sleep(31)  # wait another 31 seconds, so cache is refreshed, taking us past 60 seconds
        response3 = self.client.get('/movies/')
        self.assertEqual(response3.status_code, 200)
        context3 = response3.context_data
        third_time = context3['last_refresh']

        self.assertNotEqual(third_time, first_time)
