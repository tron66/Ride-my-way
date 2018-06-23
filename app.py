from flask import Flask, jsonify, request, abort, make_response, url_for, abort, make_response
from flask_httpauth import HTTPBasicAuth

#define app using flask
app = Flask(__name__)
#auth = HTTPBasicAuth()

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


rides = [{
'id':1,
'drivername':'sam',
'From':'kaweme',
'to':'masaka',
'depaturedate':2/3/2018,
'price':40000
},
{
'id':2,
'drivername':'mathew',
'From':'mbarara',
'to':'singiro',
'depaturedate':5/6/2018,
'price':30000
},
{
'id':3,
'drivername':'grace',
'From':'jinja',
'to':'nakawa',
'depaturedate':7/8/2018,
'price':60000
}
]

@app.route('/')
def index():
    return 'here'
    
def _record_exists(drivername):
    return [ride for ride in rides if ride["drivername"] == drivername]

@app.route('/ridemyway/api/v1/rides',methods=['GET'])
def get_rides():
    return jsonify({'rides':rides})

@app.route('/ridemyway/api/v1/rides/<int:ride_id>',methods=['GET'])
def get_ride(ride_id):
    ride = [ride for ride in rides if ride['id'] == ride_id]
    if len(ride) == 0:
        abort(404)
    return jsonify({'rides':ride})

@app.route('/ridemyway/api/v1/rides',methods=['POST'])
def create_ride():
    if not request.json or 'drivername' not in request.json or 'price' not in request.json:
        abort(400)
    ride_id = rides[-1].get("id") + 1
    drivername = request.json.get('drivername')
    if _record_exists(drivername):
        abort(400)
    From = request.json.get('From')
    to = request.json.get('to')
    depaturedate = request.json.get('depaturedate')
    if type(depaturedate) is not int:
        abort(400)
    price = request.json.get('price')
    if type(price) is not int:
        abort(400)
    ride = {"id": ride_id,
    "drivername": drivername,
    "From":From,
    "to": to,
    "depaturedate": depaturedate,
    "price": price}
    rides.append(ride)
    return jsonify({'ride': ride}), 201

@app.route('/ridemyway/api/v1/rides/<int:ride_id>/requests',methods=['POST'])
def request_ride(ride_id):
    if not request.json or 'drivername' not in request.json:
        abort(400)
    drivername = request.json.get('drivername')
    ride = {"id": ride_id,
    "drivername": drivername}
    ride = [ride for ride in rides if ride["drivername"] == drivername]
    return jsonify({'ride':ride}), 201

@app.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['PUT'])
def update_ride(ride_id):
    ride = [ride for ride in rides if ride['id'] == ride_id]
    if len(ride) == 0:
        abort(404)
    if not request.json:
        abort(400)
    drivername = request.json.get('drivername', ride[0]['drivername'])
    From = request.json.get('From', ride[0]['From'])
    to = request.json.get('to', ride[0]['to'])
    depaturedate = request.json.get('depaturedate', ride[0]['depaturedate'])
    #if type(depaturedate) is not int:
    #    abort(400)
    price = request.json.get('price', ride[0]['price'])
    #if type(price) is not int:
    #    abort(400)
    ride[0]['drivername'] = drivername
    ride[0]['From'] = From
    ride[0]['to'] = to
    ride[0]['depaturedate'] = depaturedate
    ride[0]['price'] = price
    return jsonify({'ride': ride[0]}), 200

@app.route('/ridemyway/api/v1/rides/<int:ride_id>', methods=['DELETE'])
def delete_ride(ride_id):
    ride = [ride for ride in rides if ride['id'] == ride_id]
    if len(ride) == 0:
        abort(404)
    rides.remove(ride[0])
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(debug=True)
