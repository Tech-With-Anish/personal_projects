import tkinter as tk
from tkinter import messagebox
import requests
from sklearn.linear_model import LinearRegression
import numpy as np

# Nutritionix API Configuration (replace with your API key)
NUTRITIONIX_API_KEY = 'your_api_key_here'
NUTRITIONIX_API_URL = 'https://trackapi.nutritionix.com/v2/natural/nutrients'

# Function to fetch nutritional data using Nutritionix API
def fetch_nutritional_data(food_item):
    headers = {
        'x-app-id': 'none', # use your own api fetched from the website
        'x-app-key': NUTRITIONIX_API_KEY,
    }
    payload = {'query': food_item}
    response = requests.post(NUTRITIONIX_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        food_data = data['foods'][0]
        nutrition_info = {
            'food_name': food_data['food_name'],
            'calories': food_data['nf_calories'],
            'protein': food_data['nf_protein'],
            'carbs': food_data['nf_total_carbohydrate'],
            'fat': food_data['nf_total_fat']
        }
        return nutrition_info
    else:
        messagebox.showerror("Error", "Failed to fetch data from Nutritionix API.")
        return None

# Machine Learning Model to suggest diet based on goals
def suggest_diet(user_goal, calories_needed):
    # For simplicity, we are using a basic model to suggest calories for weight loss or muscle gain
    # Sample training data (you can expand it)
    goals = {'weight_loss': -500, 'muscle_gain': 500, 'maintain': 0}
    
    # Simulate the machine learning model prediction (simple logic here for illustration)
    goal_offset = goals.get(user_goal, 0)
    suggested_calories = calories_needed + goal_offset

    return suggested_calories

# Function to create the personalized plan
def generate_plan():
    # Get user inputs
    user_goal = goal_var.get()
    daily_calories = int(calories_entry.get())
    food_item = food_entry.get()

    # Fetch nutritional data for the food item
    nutrition_data = fetch_nutritional_data(food_item)

    if nutrition_data:
        # Calculate suggested calories based on goal
        suggested_calories = suggest_diet(user_goal, daily_calories)

        # Display the personalized plan
        result_text = (
            f"Goal: {user_goal.capitalize()}\n"
            f"Suggested Calories: {suggested_calories} kcal/day\n\n"
            f"Food Item: {nutrition_data['food_name']}\n"
            f"Calories: {nutrition_data['calories']} kcal\n"
            f"Protein: {nutrition_data['protein']} g\n"
            f"Carbs: {nutrition_data['carbs']} g\n"
            f"Fat: {nutrition_data['fat']} g\n"
        )

        # Show the results in the text box
        result_label.config(text=result_text)

# Function to reset the input fields
def reset_fields():
    food_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)
    goal_var.set('maintain')
    result_label.config(text="")

# Create the GUI window
root = tk.Tk()
root.title("Personalized Diet & Exercise Planner")
root.geometry("600x500")

# Goal Label and Options
goal_label = tk.Label(root, text="Select your goal:", font=("Arial", 12))
goal_label.pack(pady=10)

goal_var = tk.StringVar(value="maintain")
goal_options = tk.OptionMenu(root, goal_var, "weight_loss", "muscle_gain", "maintain")
goal_options.pack(pady=5)

# Calories Entry
calories_label = tk.Label(root, text="Enter your daily calorie requirement:", font=("Arial", 12))
calories_label.pack(pady=10)

calories_entry = tk.Entry(root, font=("Arial", 12))
calories_entry.pack(pady=5)

# Food Item Entry
food_label = tk.Label(root, text="Enter a food item:", font=("Arial", 12))
food_label.pack(pady=10)

food_entry = tk.Entry(root, font=("Arial", 12))
food_entry.pack(pady=5)

# Generate Plan Button
generate_button = tk.Button(root, text="Generate Plan", font=("Arial", 12), command=generate_plan)
generate_button.pack(pady=20)

# Reset Button
reset_button = tk.Button(root, text="Reset", font=("Arial", 12), command=reset_fields)
reset_button.pack(pady=5)

# Results Display
result_label = tk.Label(root, text="", font=("Arial", 12), justify=tk.LEFT)
result_label.pack(pady=20)

# Run the GUI
root.mainloop()
