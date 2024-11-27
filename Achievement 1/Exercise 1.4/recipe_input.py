import pickle

recipes_list = []
ingredients_list = []

# Function to take user input for a recipe and return it
def take_recipe():
    name = input("Enter the name of a recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients, separated by a comma: ").split(", ")
    
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": ""
    }
    
    return recipe

# Function to determine and assign difficulty to each recipe in recipes_list
def calc_difficulty(recipes_list):
    for recipe in recipes_list:
        if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
            recipe["difficulty"] = "Easy"
        elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
            recipe["difficulty"] = "Medium"
        elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
            recipe["difficulty"] = "Intermediate"
        elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
            recipe["difficulty"] = "Hard"

# Function to display recipe information
def display_recipes(recipes_list):
    for recipe in recipes_list:
        print("\nRecipe:", recipe["name"])
        print("Cooking time (minutes):", recipe["cooking_time"])
        print("Ingredients:")
        for ingredient in recipe["ingredients"]:
            print(ingredient)
        print("Difficulty:", recipe["difficulty"])

# Input user's file name
file_name = input("Enter a file name to open: ")

# Attempt to load the file
try:
    with open(file_name, "rb") as file:
        data = pickle.load(file)
        print("File is loaded.")
except FileNotFoundError:
    print("File with that name not found. Creating new file...")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
except Exception as e:
    print("An unexpected error occurred:", e)
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

# Extracts values from data dictionary
recipes_list = data["recipes_list"]
ingredients_list = data["all_ingredients"]

# Sorts through number of given recipes
n = int(input("How many recipes would you like to enter? "))
for i in range(n):
    recipe = take_recipe()
    
    # Add new ingredients to ingredients_list if not already present
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    # Append the recipe to recipes_list
    recipes_list.append(recipe)
    print("Added recipe.")

# Calculate difficulty for each recipe
calc_difficulty(recipes_list)

# Display all recipes
display_recipes(recipes_list)

# Update data dictionary with new recipes and ingredients
data = {
    "recipes_list": recipes_list,
    "all_ingredients": ingredients_list
}

# Save updated data to file
with open(file_name, "wb") as updated_file:
    pickle.dump(data, updated_file)
    print("File updated.")
