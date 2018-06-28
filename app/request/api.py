from flask.views import MethodView
from flask import jsonify, request, abort, make_response
from app.models import Ride
import uuid


class RequestAPI(MethodView): #requesting a ride

    def post(self, ride_id):
        ride_id = uuid.UUID(ride_id)
        try:
            res = Ride.join_ride(ride_id)
            if res == "request to join sent":
                return jsonify({'msg': res}), 201

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500
