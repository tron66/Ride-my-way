import unittest
import json
from data import*
from app import create_app


class RideTestCase(unittest.TestCase): #this represents the ride testcase

    def setup(self):
        self.app = create_app(config_name = "testing")
        self.client = self.app.test_client
        self.ride1 = {"drivername": "jessy"}
        self.app.app_context()


    def test_ride(self): #testing post requests api
        response = self.client().post('/api/v1/rides/',
                                    content_type='application/json',
                                    data=json.dumps(ride1))

        self.assertEqual(response.status_code, 201)
        self.assertIn('Ride offered', str(response.data))

    def test_all_rides(self): #testing get requests api
        response = self.client().post('/api/v1/rides/',
                                    content_type='application/json',
                                    data=json.dumps(ride2))

        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/rides/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("end", str(response.data))

    def test_ride_by_id(self): #testing for a single id
        response = self.client().post('/api/v1/rides/',
                                    content_type='application/json',
                                    data=json.dumps(ride3))
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/rides/')
        self.assertEqual(response.status_code, 200)

        results = json.loads(response.data.decode())
        for ride in results:
            result = self.client.get(
                '/api/v1/rides/{}'.format(ride['Id']))
            self.assertEqual(result.status_code, 200)
            self.assertIn(ride['Id'], str(result.data))

    def test_join_request_issuccesful(self): #testing api to send a request
        response = self.client().post('/api/v1/rides/',
                                    content_type='application/json',
                                    data=json.dumps(ride4))

        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/rides/')
        self.assertEqual(response.status_code, 200)

        results = json.loads(response.data.decode())

        for ride in results:
            response = self.client.post('/api/v1/rides/{}/requests'
                                        .format(ride['Id']),
                                        content_type='application/json',
                                        data=json.dumps({'join': 'True'}))
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                " request sent",
                str(response.data))
