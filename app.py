from flask import Flask, request, jsonify, make_response
import requests
import re

weatherApiKey = "5bf558ca91a0459cabd104740242904"
weatherBaseUrl = "http://api.weatherapi.com/v1/current.json"

stocksApiKey = "cb8b1362ef2cff2ca1fabfafa349fbd282a83bc5"



app = Flask(__name__)

@app.route('/', methods=['GET'])
def service():
    if 'queryAirportTemp' in request.args:
        airport_code = request.args['queryAirportTemp']
        temperature = get_airport_temperature(airport_code)
        return make_response(jsonify(temperature), 200, {'Content-Type': 'application/json'})
    
    elif 'queryStockPrice' in request.args:
        stock_id = request.args['queryStockPrice']
        price = get_stock_price(stock_id)
        return make_response(jsonify(price), 200, {'Content-Type': 'application/json'})

    elif 'queryEval' in request.args:
        expression = request.args['queryEval']
        result = evaluate_expression(expression)
        return make_response(jsonify(result), 200, {'Content-Type': 'application/json'})

    else:
        return make_response(jsonify({"error": "Undefined"}), 400)

def get_airport_temperature(airport_code):
    full_url = f"{weatherBaseUrl}?key={weatherApiKey}&q={airport_code}&aqi=no"
    
    try:
        response = requests.get(full_url)
        
        if response.status_code == 200:
            data = response.json()
            temperature = data['current']['temp_c']
            return temperature
        else:
            return f"Error: Received response code {response.status_code}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def get_stock_price(stock_id):

    stocksBaseUrl = f"https://api.tiingo.com/tiingo/daily/{stock_id}/prices"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {stocksApiKey}'
    }

    try:
        response = requests.get(stocksBaseUrl, headers=headers)
        

        if response.status_code == 200:
            data = response.json()
            if data:
                latest_price = data[0]['close']
                return latest_price
            else:
                return "No data available for this ticker"
        else:
            return f"Error: Received response code {response.status_code}"
    except requests.RequestException as e:
        return f"Error: {str(e)}"
    
def evaluate_expression(expression):
    expression = expression.replace(" ", "+")
    if re.fullmatch(r'[0-9\+\-\*/\(\) ]+', expression):
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return result
        except Exception as e:
            return str(e)
    else:
        return "Invalid expression"

if __name__ == '__main__':
    app.run(debug=True, port=44444)