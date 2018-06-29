# importing "copy" for copy operations
from copy import deepcopy # allows to deep copy or shallow copy mutable objects
import unittest
import json

import app

BASE_URL = 'http://127.0.0.1:5000//ridemyway/api/v1/rides'
BAD_RIDE_URL = '{}/5'.format(BASE_URL)
GOOD_RIDE_URL = '{}/3'.format(BASE_URL)


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.backup_rides = deepcopy(app.rides)
        self.app = app.app.test_client()
        self.app.testing = True

    def test_get_all(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['rides']), 3)

    def test_get_one(self):
        response = self.app.get(BASE_URL)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['rides'][0]['drivername'], 'sam')

    def test_ride_not_exist(self):
        response = self.app.get(BAD_RIDE_URL)
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        # missing value field = bad
        ride = {"drivername": "some_ride"}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        ride = {"drivername": "costa", "From": "kla", "to": "mask", "depaturedate": 'string', "price": 'string'}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        ride = {"drivername": "costa", "From": "kla", "to": "mask", "depaturedate": 2/3/2018, "price": 20000}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data())
        ride = {"drivername": "costa", "From": "kla", "to": "mask", "depaturedate": 2/3/2018, "price": 20000}
        response = self.app.post(BASE_URL,
                                 data=json.dumps(ride),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        ride = {"price": 30}
        response = self.app.put(GOOD_RIDE_URL,
                                data=json.dumps(ride),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['ride']['price'], 30)
        self.assertEqual(self.backup_rides[2]['price'], 60000)

    def test_update_error(self):
        ride = {"price": 30}
        response = self.app.put(BAD_RIDE_URL,
                                data=json.dumps(ride),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        ride = {"price": 'string'}
        response = self.app.put(GOOD_RIDE_URL,
                                data=json.dumps(ride),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.app.delete(GOOD_RIDE_URL)
        self.assertEqual(response.status_code, 204)
        response = self.app.delete(BAD_RIDE_URL)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        app.rides = self.backup_rides


if __name__ == "__main__":
    unittest.main()
