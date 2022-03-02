import requests
import datetime as dt
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']

SHEET_ENDPOINT = os.environ['SHEET_ENDPOINT']

TOKEN = os.environ['TOKEN']

GENDER = 'male'
WEIGHT_KG = 92
HEIGHT_CM = 175
AGE = 24

# ------------- Get user input ----------- #

user_query = input('Tell me what you did today: ')


# ------------- Set up the nutritionix ----------- #

exercise_endpoint = 'https://trackapi.nutritionix.com/v2/natural/exercise'
headers = {
    'x-app-id': APP_ID,
    'x-app-key': API_KEY
}

parameters = {
 "query": user_query,
 "gender": GENDER,
 "weight_kg": WEIGHT_KG,
 "height_cm": HEIGHT_CM,
 "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
data = response.json()
print(data)

# --------------- Adding data to my sheet ------------------ #

today = dt.datetime.today().strftime('%d/%m/%Y')
time = dt.datetime.now().strftime('%H:%M')

sheety_header = {
    "Authorization": f"Bearer {TOKEN}",
    'Content-Type': 'application/json'
}

for exercise in data['exercises']:
    sheety_parameters = {
        'workout': {
            'date': today,
            'time': time,
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }

    sheety_response = requests.post(SHEET_ENDPOINT, json=sheety_parameters, headers=sheety_header)
    print(sheety_response.json())