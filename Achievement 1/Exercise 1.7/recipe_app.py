# Import required packages
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_

# Database setup
engine = create_engine("mysql+mysqlconnector://cf-python:password@localhost/task_database")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define Recipe model
class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe {self.id}: {self.name}, Difficulty: {self.difficulty}>"

    def __str__(self):
        return (
            f"\n{'-'*40}\n"
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Ingredients: {self.ingredients}\n"
            f"Difficulty: {self.difficulty}\n"
            f"{'-'*40}\n"
        )

    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(', '))
        if self.cooking_time < 10:
            self.difficulty = 'Easy' if num_ingredients < 4 else 'Medium'
        else:
            self.difficulty = 'Intermediate' if num_ingredients < 4 else 'Hard'

Base.metadata.create_all(engine)

# Function to create a new recipe
def create_recipe():
    name = input("Enter the name of the recipe (max 50 chars): ").strip()
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    
    ingredients = []
    ingredient_count = int(input("How many ingredients does the recipe have? "))
    for i in range(ingredient_count):
        ingredients.append(input(f"Enter ingredient {i + 1}: ").strip())
    
    recipe = Recipe(
        name=name[:50],
        cooking_time=cooking_time,
        ingredients=', '.join(ingredients)
    )
    recipe.calculate_difficulty()
    session.add(recipe)
    session.commit()
    print("Recipe created successfully!")

# Function to view all recipes
def view_all_recipes():
    recipes = session.query(Recipe).all()
    if recipes:
        for recipe in recipes:
            print(recipe)
    else:
        print("No recipes found.")

# Function to search recipes by ingredients
def search_by_ingredients():
    all_ingredients = set()
    for recipe in session.query(Recipe.ingredients):
        all_ingredients.update(recipe.ingredients.split(', '))

    if not all_ingredients:
        print("No ingredients found in recipes.")
        return

    print("Available ingredients:")
    ingredient_list = sorted(all_ingredients)
    for i, ingredient in enumerate(ingredient_list, start=1):
        print(f"{i}. {ingredient}")

    Index = input("Enter ingredient numbers to search (separated by spaces): ").split()
    try:
        selected_ingredients = [ingredient_list[int(i) - 1] for i in Index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in selected_ingredients]
    results = session.query(Recipe).filter(and_(*conditions)).all()

    if results:
        for recipe in results:
            print(recipe)
    else:
        print("No matching recipes found.")

# Function to edit a recipe
def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("No recipes available to edit.")
        return

    print("Available recipes:")
    for recipe in recipes:
        print(f"{recipe.id}: {recipe.name}")

    try:
        recipe_id = int(input("Enter the ID of the recipe to edit: "))
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            print("Recipe not found.")
            return
    except ValueError:
        print("Invalid input.")
        return

    print(f"Editing recipe: {recipe}")
    print("1. Name\n2. Ingredients\n3. Cooking Time")
    choice = input("Choose the field to update: ")

    if choice == '1':
        recipe.name = input("Enter the new name (max 50 chars): ").strip()[:50]
    elif choice == '2':
        new_ingredients = []
        count = int(input("How many ingredients does the recipe have? "))
        for i in range(count):
            new_ingredients.append(input(f"Enter ingredient {i + 1}: ").strip())
        recipe.ingredients = ', '.join(new_ingredients)
    elif choice == '3':
        recipe.cooking_time = int(input("Enter the new cooking time (in minutes): "))
    else:
        print("Invalid choice.")
        return

    recipe.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")

# Function to delete a recipe
def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("No recipes available to delete.")
        return

    print("Available recipes:")
    for recipe in recipes:
        print(f"{recipe.id}: {recipe.name}")

    try:
        recipe_id = int(input("Enter the ID of the recipe to delete: "))
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()
        if not recipe:
            print("Recipe not found.")
            return
    except ValueError:
        print("Invalid input.")
        return

    session.delete(recipe)
    session.commit()
    print("Recipe deleted successfully!")

# Main Menu
def main_menu():
    while True:
        print("\nRecipe Manager")
        print("1. Create a Recipe")
        print("2. View All Recipes")
        print("3. Search Recipes by Ingredients")
        print("4. Edit a Recipe")
        print("5. Delete a Recipe")
        print("6. Exit")

        choice = input("Choose an option: ").strip()
        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
    session.close()
    engine.dispose()
