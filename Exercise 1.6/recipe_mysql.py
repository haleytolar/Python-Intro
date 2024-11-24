import sys
import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'cf-python',
    'passwd': 'password',
    'database': 'task_database'
}

# Custom exit function
def quit():
    print("Exiting the script. Goodbye!")
    sys.exit()

# Helper function for calculating difficulty
def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients.split(', '))
    if cooking_time < 10:
        return 'Easy' if num_ingredients < 4 else 'Medium'
    else:
        return 'Intermediate' if num_ingredients < 4 else 'Hard'

# Helper function for sanitizing ingredients
def sanitize_ingredients(ingredients):
    return ', '.join(ingredient.strip() for ingredient in ingredients.split(','))

# Create recipe functionality
def create_recipe(cursor):
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients (separate with comma): ")

    sanitized_ingredients = sanitize_ingredients(ingredients)
    difficulty = calculate_difficulty(cooking_time, sanitized_ingredients)

    cursor.execute("""
        INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
        VALUES (%s, %s, %s, %s)
    """, (name, sanitized_ingredients, cooking_time, difficulty))
    print("Recipe added successfully!")

# Search recipe functionality
def search_recipe(cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = {ingredient for row in results for ingredient in row[0].split(', ')}
    print("\nAvailable ingredients:")
    for idx, ingredient in enumerate(sorted(all_ingredients), start=1):
        print(f"{idx}. {ingredient}")

    choice = int(input("Choose an ingredient by number to search: ")) - 1
    search_ingredient = sorted(all_ingredients)[choice]

    cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ('%' + search_ingredient + '%',))
    results = cursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("No recipes found with that ingredient.")

# Update recipe functionality
def update_recipe(cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    print("\nExisting recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to update: "))
    column_to_update = input("Enter the column to update (name, ingredients, cooking_time): ")

    if column_to_update in ['name', 'ingredients', 'cooking_time']:
        new_value = input(f"Enter the new value for {column_to_update}: ")
        if column_to_update == 'cooking_time':
            new_value = int(new_value)
        elif column_to_update == 'ingredients':
            new_value = sanitize_ingredients(new_value)

        cursor.execute(f"UPDATE Recipes SET {column_to_update} = %s WHERE id = %s", (new_value, recipe_id))

        # Recalculate difficulty if necessary
        if column_to_update in ['ingredients', 'cooking_time']:
            cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
            row = cursor.fetchone()
            difficulty = calculate_difficulty(row[0], row[1])
            cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))

        print("Recipe updated successfully!")
    else:
        print("Invalid column.")

# Delete recipe functionality
def delete_recipe(cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()

    print("\nExisting recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = int(input("Enter the ID of the recipe to delete: "))
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    print("Recipe deleted successfully!")

# Database and table initialization
def create_database_and_table(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    cursor.execute("USE task_database")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Recipes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            ingredients VARCHAR(255),
            cooking_time INT,
            difficulty VARCHAR(20)
        )
    """)

# Main menu
def main_menu(cursor):
    options = {
        '1': ("Create a new recipe", create_recipe),
        '2': ("Search for recipes by ingredient", search_recipe),
        '3': ("Update an existing recipe", update_recipe),
        '4': ("Delete a recipe", delete_recipe),
        '5': ("Exit", quit)
    }

    while True:
        print("\nMain Menu:")
        for key, (desc, _) in options.items():
            print(f"{key}. {desc}")

        choice = input("Enter your choice (or type 'quit' to exit): ").strip().lower()
        
        if choice == 'quit':  # Allow 'quit' to exit
            quit()
        elif choice in options:
            options[choice][1](cursor)
        else:
            print("Invalid choice. Please try again.")

# Database connection
def connect_to_database():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    return conn, cursor

# Main entry point
if __name__ == "__main__":
    conn, cursor = connect_to_database()
    create_database_and_table(cursor)
    try:
        main_menu(cursor)
    finally:
        conn.commit()
        cursor.close()
        conn.close()
