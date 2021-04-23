from flask import Flask, request, jsonify
import util
from flask_pymongo import PyMongo
from flask_cors import CORS
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://yash:yash1234@collab.g1ws0.mongodb.net/house?retryWrites=true&w=majority"
mongo = PyMongo(app)
CORS(app)

@app.route('/sell',methods=['POST'])
def add_home():
    request_data = request.get_json()
    price=float(request_data['price'])
    total_sqft = float(request_data['sqft'])
    location = request_data['location']
    bhk = int(request_data['bhk'])
    desc=request_data['desc']
    mongo.db.home.insert_one({
        'location':location,
        'price':price,
        'bhk':bhk,
        'sqft':total_sqft,
        'desc':desc
    })


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()  # Populate locations to the frontend
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    request_data = request.get_json()
    total_sqft = float(request_data['sqft'])
    location = request_data['location']
    bhk = int(request_data['bhk'])
    bath = int(request_data['nobath'])
    response = jsonify({
        # populate the estimated price to the frontend
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/getproperty', methods=['GET'])
def propertydetails():
    data = mongo.db.home.find()
    result = [{
        'location': home['location'],
        'price':home['price'],
        'bhk':home['bhk']} 
        for home in data]
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()
