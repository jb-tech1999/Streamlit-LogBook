import requests
import datetime

base_url = 'http://0.0.0.0:8000/'

def get_token(username, password):
    url = f'{base_url}login'
    payload = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['token']


def get_cars(token):
    url = f'{base_url}cars'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_logs(token, car):
    url = f'{base_url}logs/{car}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def add_log(token, car_choice, date, speedometer, distance, totalcost, garage, liters):
    url = f'{base_url}addlog'
    payload = {
        'carRegistration': car_choice,
        'date': str(date),
        'odometer': speedometer,
        'distance': distance,
        'totalcost': totalcost,
        'garage': garage,
        'litersPurchase': liters
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def str_to_date(date):
    #return date
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    return d.date()