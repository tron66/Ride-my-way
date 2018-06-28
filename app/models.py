import uuid
from datetime import date, datetime

rides = []
requests = []

class Ride(object): #ride classmethod

    def __init__(self, ride_id, drivername, start, end, date,
                 time, price):
        self.ride_id = ride_id
        self.drivername = drivername
        self.start = origin
        self.end = destination
        self.date = date
        self.time = time
        self.price = price

    @classmethod #checks if the ride exits
    def existing_ride(self, start, end):
        for ride in rides:
            if ride['start'] == start and ride['end'] == end:
                return True
        else:
            return False

    @classmethod #checks to see the date doesnt exceed the current date
    def valid_date(self, date):
        date = datetime.strptime(edate, '%Y-%m-%d').date()
        if date <= date.today():
            return False
        return True

    @classmethod #offering a ride
    def offer_ride(self, drivername, start, end, date, time,
                  price):
        self.data = {}
        if self.existing_ride(drivername, start, end, date,
                             time, price):
            return "ride offer exists"
        else:
                self.data['Id'] = uuid.uuid1()
                self.data["drivername"] = drivername
                self.data['start'] = start
                self.data['end'] = end
                self.data["date"] = date
                self.data["time"] = time
                self.data["price"] = price

                rides.append(self.data)
                return "Ride offered"

    @classmethod #displays all rideoffers
    def view_all_rides(self):
        return rides

    @classmethod #sending request to join a ride
    def join_ride(self, ride_id):
        for ride in rides:
            if ride['Id'] == ride_id:
                requests.append(ride)
                return "request sent"
