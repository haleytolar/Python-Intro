import pickle

# Function to display recipe details
def display_recipe(recipe):
    print("\nRecipe: " + recipe["name"])
    print("Cooking Time (minutes): " + str(recipe["cooking_time"]))
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print("- " + ingredient)
    print("Difficulty: " + recipe["difficulty"])

# Function to search for an ingredient in all data
def search_ingredient(data):
    if not data.get("all_ingredients"):
        print("No ingredients available in the data.")
        return

    # Use enumerate with a start value of 1
    all_ingredients = list(enumerate(data["all_ingredients"], start=1))
    
    # Display each ingredient with a number starting at 1
    print("\nIngredients available across all recipes:")
    print("-----------------------------------------")
    for index, ingredient in all_ingredients:
        print(f"{index}. {ingredient}")

    # Attempt to search for a user-defined ingredient number
    try:
        n = int(input("Enter the number of an ingredient to search: "))
        
        # Check if the ingredient number is within range
        if n < 1 or n > len(all_ingredients):
            print("Invalid number. Please select a number from the list.")
            return
        
        ingredient_searched = all_ingredients[n - 1][1]  # Adjust index for 1-based numbering
        print(f"\nSearching for recipes with '{ingredient_searched}'...\n")

        # Print each recipe that contains the specified ingredient
        found = False
        for recipe in data.get("recipes_list", []):
            if ingredient_searched in recipe.get("ingredients", []):
                display_recipe(recipe)
                found = True
        if not found:
            print(f"No recipes found with the ingredient '{ingredient_searched}'.")

    except ValueError:
        print("Invalid input. Please enter a number.")

# Load data from a file and handle potential errors
file_name = input("Enter the filename that contains recipe data: ")

try:
    with open(file_name, "rb") as file:
        data = pickle.load(file)
        print("File loaded successfully.")
except FileNotFoundError:
    print("File with that name not found.")
except pickle.UnpicklingError:
    print("Error: The file could not be read as a pickle file.")
else:
    file.close()
    search_ingredient(data)
