import uuid
from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import Ride



class RideAPI(MethodView):

    def __init__(self):

        if request.method != 'GET' and not request.json:
            abort(400)

    def get(self, ride_id): #get request
        if ride_id:
            try:
                ride_id = uuid.UUID(ride_id)
                rides = Ride.view_all_rides()
                for ride in rides:
                    if ride_id == ride['Id']:
                        return jsonify(ride), 200
                    return jsonify({'msg': "Ride not found "}), 404
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

        else:
            try:
                rides = Ride.view_all_rides()
                if rides == []:
                    response= {"msg": " No rides"}
                    return make_response(jsonify(response)), 200
                return jsonify(rides), 200
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 500

    def post(self): #post request
        data = request.json
        if not "drivername" and not "start" and not "end" and not "date" and not "time" and not "price"in data:
            abort(400)
        drivername = data["drivername"]
        start = data["start"]
        end = data["end"]
        date = data["date"]
        time = data["time"]
        price = data["price"]
        try:
            res = Ride.offer_ride(drivername, start, end, date, time, price)
            if res == "Ride offered":
                return jsonify({'msg': res}), 201
            return jsonify({'msg': res}), 409
        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500
