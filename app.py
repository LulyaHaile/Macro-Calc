from flask import Flask, render_template, request, redirect, url_for, flash
import requests


app = Flask(__name__)
app.secret_key = 'clAkvcBeeoygBXhdBOXE1T4zRK4P0TyHXzKvCjxf'  # Replace with your own secret key


# Initialize variables to store user profile and food log data
user_profile = {}
food_log = []
macros = ""


# USDA API endpoint and your API key
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
USDA_API_KEY = "clAkvcBeeoygBXhdBOXE1T4zRK4P0TyHXzKvCjxf"  # Replace with your USDA API key


def get_food_nutrition(food_item):
    """Fetch nutritional information from the USDA API."""
    params = {
        'api_key': USDA_API_KEY,
        'query': food_item,
        'pageSize': 50  # Get a limited number of results
    }
    response = requests.get(USDA_API_URL, params=params)
   
    if response.status_code == 200:
        return response.json().get('foods', [])  # Return the list of foods or empty list if not found
    return []


@app.route('/')
def home():
    return render_template('index.html', profile=user_profile, food_log=food_log, macros=macros)


@app.route('/save_profile', methods=['POST'])
def save_profile():
    age = request.form.get('age')
    sex = request.form.get('sex')
    activity_level = request.form.get('activity_level')  # Get activity level from the form
   
    if age and sex in ['male', 'female'] and activity_level in ['none', 'light', 'active']:
        user_profile['age'] = age
        user_profile['sex'] = sex
        user_profile['activity_level'] = activity_level  # Save activity level
        flash('Profile saved successfully!', 'success')
    else:
        flash('Please provide valid age, sex, and activity level!', 'error')
   
    return redirect(url_for('home'))




@app.route('/calculate_macros', methods=['POST'])
def calculate_macros():
    weight = request.form.get('weight_for_calc', type=float)
    activity_level = user_profile.get('activity_level')  # Get the user's activity level from their profile


    if weight is not None and activity_level:
        # Protein goals based on activity level
        if activity_level == 'none':
            user_profile['protein_goal'] = weight * 0.36
        elif activity_level == 'light':
            user_profile['protein_goal'] = weight * 0.6
        elif activity_level == 'active':
            user_profile['protein_goal'] = weight * 0.8


        # Fiber goals based on activity level
        if activity_level == 'none':
            user_profile['fiber_goal'] = weight * 0.10
        elif activity_level == 'light':
            user_profile['fiber_goal'] = weight * 0.14
        elif activity_level == 'active':
            user_profile['fiber_goal'] = weight * 0.18


        # Carbs goals based on activity level
        if activity_level == 'none':
            user_profile['carbs_goal'] = weight * 2.0
        elif activity_level == 'light':
            user_profile['carbs_goal'] = weight * 3.0
        elif activity_level == 'active':
            user_profile['carbs_goal'] = weight * 4.0


        # Sugar goals based on activity level
        if activity_level == 'none':
            user_profile['sugar_goal'] = weight * 0.05
        elif activity_level == 'light':
            user_profile['sugar_goal'] = weight * 0.1
        elif activity_level == 'active':
            user_profile['sugar_goal'] = weight * 0.15


        flash('Macronutrients calculated successfully!', 'success')
    else:
        flash('Please provide a valid weight and ensure your activity level is set!', 'error')


    return redirect(url_for('home'))




@app.route('/search_food', methods=['POST'])
def search_food():
    food_item = request.form.get('food_item')
    food_results = get_food_nutrition(food_item)
   
    return render_template('index.html', profile=user_profile, food_log=food_log, food_results=food_results)


@app.route('/log_food', methods=['POST'])
def log_food():
    food_item = request.form.get('food_item')
    protein = request.form.get('protein', type=float)
    fiber = request.form.get('fiber', type=float)
    carbs = request.form.get('carbs', type=float)
    sugar = request.form.get('sugar', type=float)
   
    if food_item:
        food_log.append({
            'item': food_item,
            'protein': protein,
            'fiber': fiber,
            'carbs': carbs,
            'sugar': sugar
        })
        flash('Food logged successfully!', 'success')
    else:
        flash('Please provide a food item to log!', 'error')


    return redirect(url_for('home'))




@app.route('/calculate_totals')
def calculate_totals():
    total_protein = sum(item['protein'] for item in food_log)
    total_fiber = sum(item['fiber'] for item in food_log)
    total_carbs = sum(item['carbs'] for item in food_log)
    total_sugar = sum(item['sugar'] for item in food_log)


    return total_protein, total_fiber, total_carbs, total_sugar


if __name__ == '__main__':
    app.run(debug=True)




