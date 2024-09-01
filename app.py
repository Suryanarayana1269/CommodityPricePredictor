from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Example data
bikes = [
    {'Brand': 'Yamaha', 'Model-Year': 2020, 'Fuel-Type': 'Petrol', 'Gears': 6, 'Top-Speed': 180, 'Price': 8000},
    {'Brand': 'Honda', 'Model-Year': 2019, 'Fuel-Type': 'Petrol', 'Gears': 5, 'Top-Speed': 160, 'Price': 7500},
    {'Brand': 'Tesla', 'Model-Year': 2022, 'Fuel-Type': 'Electric', 'Gears': 0, 'Top-Speed': 250, 'Price': 12000},
    {'Brand': 'Harley-Davidson', 'Model-Year': 2021, 'Fuel-Type': 'Petrol', 'Gears': 6, 'Top-Speed': 200, 'Price': 15000}
]

cars = [
    {'Brand': 'Toyota', 'ModelYear': 2020, 'FuelType': 'Petrol', 'Gears': 'Automatic', 'TopSpeed': 180, 'Mileage': 15, 'Price': 20000},
    {'Brand': 'Honda', 'ModelYear': 2019, 'FuelType': 'Gas', 'Gears': 'Manual', 'TopSpeed': 160, 'Mileage': 20, 'Price': 18000},
    {'Brand': 'Tesla', 'ModelYear': 2022, 'FuelType': 'Electric', 'Gears': 'Automatic', 'TopSpeed': 250, 'Mileage': 350, 'Price': 35000},
    {'Brand': 'Ford', 'ModelYear': 2021, 'FuelType': 'Petrol', 'Gears': 'Automatic', 'TopSpeed': 200, 'Mileage': 12, 'Price': 25000}
]

laptops = [
    {'Brand': 'Dell', 'Type': 'Ultrabook', 'RAM': 8, 'Weight': 1.5, 'Touchscreen': 'No', 'IPS': 'Yes', 'ScreenSize': 13.3, 'ScreenResolution': '1920x1080', 'CPU': 'Intel Core i5', 'HDD': 0, 'SSD': 256, 'GPU': 'Intel UHD Graphics', 'OS': 'Windows 10', 'Price': 999},
    {'Brand': 'HP', 'Type': 'Notebook', 'RAM': 4, 'Weight': 2.1, 'Touchscreen': 'No', 'IPS': 'No', 'ScreenSize': 15.6, 'ScreenResolution': '1366x768', 'CPU': 'Intel Core i3', 'HDD': 1000, 'SSD': 0, 'GPU': 'Intel HD Graphics', 'OS': 'Windows 10', 'Price': 459},
    {'Brand': 'Lenovo', 'Type': 'Gaming', 'RAM': 16, 'Weight': 2.3, 'Touchscreen': 'No', 'IPS': 'Yes', 'ScreenSize': 15.6, 'ScreenResolution': '1920x1080', 'CPU': 'AMD Ryzen 7', 'HDD': 0, 'SSD': 512, 'GPU': 'NVIDIA GTX 1650', 'OS': 'Windows 10', 'Price': 1199},
    {'Brand': 'Apple', 'Type': 'Ultrabook', 'RAM': 8, 'Weight': 1.4, 'Touchscreen': 'No', 'IPS': 'Yes', 'ScreenSize': 13.3, 'ScreenResolution': '2560x1600', 'CPU': 'Apple M1', 'HDD': 0, 'SSD': 256, 'GPU': 'Apple M1 GPU', 'OS': 'macOS', 'Price': 1299}
]

mobiles = [
    {'Brand': 'Samsung', 'Model-Year': 2023, 'RAM': 8, 'Storage': 256, 'Price': 900},
    {'Brand': 'Samsung', 'Model-Year': 2022, 'RAM': 8, 'Storage': 128, 'Price': 799},
    {'Brand': 'Apple', 'Model-Year': 2021, 'RAM': 6, 'Storage': 64, 'Price': 699},
    {'Brand': 'OnePlus', 'Model-Year': 2023, 'RAM': 12, 'Storage': 256, 'Price': 999},
    {'Brand': 'Google', 'Model-Year': 2023, 'RAM': 8, 'Storage': 128, 'Price': 599}
]

# Model training functions
def train_model(data, feature_names):
    X = []
    y = []
    for item in data:
        features = [item.get(f, 0) for f in feature_names]
        X.append(features)
        y.append(item['Price'])
    X = np.array(X)
    y = np.array(y)
    
    model = LinearRegression()
    model.fit(X, y)
    return model

# Define feature names for each model
bike_features = ['Model-Year', 'Top-Speed', 'Gears']
car_features = ['ModelYear', 'TopSpeed', 'Mileage']
laptop_features = ['RAM', 'Weight', 'ScreenSize', 'SSD']
mobile_features = ['RAM', 'Storage']

# Train models
bike_model = train_model(bikes, bike_features)
car_model = train_model(cars, car_features)
laptop_model = train_model(laptops, laptop_features)
mobile_model = train_model(mobiles, mobile_features)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/<predictor>', methods=['GET'])
def get_data(predictor):
    if predictor == 'bike':
        data = bikes
    elif predictor == 'car':
        data = cars
    elif predictor == 'laptop':
        data = laptops
    elif predictor == 'mobile':
        data = mobiles
    else:
        return jsonify({'error': 'Invalid predictor type'}), 400
    
    return jsonify(data)

@app.route('/predict/<predictor>', methods=['POST'])
def predict(predictor):
    data = request.json
    
    if predictor == 'bike':
        features = [data.get('Model-Year', 0), data.get('Top-Speed', 0), data.get('Gears', 0)]
        model = bike_model
    elif predictor == 'car':
        features = [data.get('ModelYear', 0), data.get('TopSpeed', 0), data.get('Mileage', 0)]
        model = car_model
    elif predictor == 'laptop':
        features = [data.get('RAM', 0), data.get('Weight', 0), data.get('ScreenSize', 0), data.get('SSD', 0)]
        model = laptop_model
    elif predictor == 'mobile':
        features = [data.get('RAM', 0), data.get('Storage', 0)]
        model = mobile_model
    else:
        return jsonify({'error': 'Invalid predictor type'}), 400

    features = np.array([features])
    prediction = model.predict(features)
    
    return jsonify({'price': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
