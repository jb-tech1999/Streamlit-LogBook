import requests
import datetime


# create class with methods

class Api:

    def __init__(self, username, password):
        self.base_url = 'http://0.0.0.0:8000/'
        self.username = username
        self.password = password

    def get_token(self):
        url = f'{self.base_url}login'
        payload = {'username': self.username, 'password': self.password}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def get_cars(self, token):
        url = f'{self.base_url}cars'
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
        response = requests.get(url, headers=headers)
        return response.json()


    def get_logs(self, token, car):
        url = f'{self.base_url}logs/{car}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)
        return response.json()       
    
    def add_log(self,token, car_choice, date, speedometer, distance, totalcost, garage, liters):
        url = f'{self.base_url}addlog'
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