class Recipe:
    all_ingredients = []

    def __init__(self, name, cooking_time, ingredients):
        self.name = name
        self.cooking_time = cooking_time
        self.ingredients = ingredients
        self.difficulty = None
        self.calculate_difficulty()
        self.update_all_ingredients()

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time 

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *new_ingredients):
        for ingredient in new_ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)

        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time > 10 and num_ingredients > 4:
            self.difficulty = "Hard"

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()  
        return self.difficulty  

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    @classmethod
    def get_all_ingredients(cls):
        return cls.all_ingredients
    
    def __str__(self):
        ingredients_list = "\n".join(self.ingredients)
        return (f"Recipe: {self.name}\n"
                f"Cooking Time: {self.cooking_time} minutes\n"
                f"Difficulty: {self.get_difficulty()}\n"
                f"Ingredients:\n{ingredients_list}")
    
    @staticmethod
    def recipe_search(data, search_term):
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)
                print("-" * 30)


tea = Recipe("Tea", 5, ["Tea Leaves", "Sugar", "Water"])
coffee = Recipe("Coffee", 5, ["Coffee Powder", "Sugar", "Water"])
cake = Recipe("Cake", 50, ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"])
smoothie = Recipe("Banana Smoothie", 5, ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"])


recipes_list = [tea, coffee, cake, smoothie]


for recipe in recipes_list:
    print(recipe)
    print("=" * 40)


for ingredient in ["Water", "Sugar", "Bananas"]:
    print(f"Searching for recipes with the ingredient: {ingredient}")
    Recipe.recipe_search(recipes_list, ingredient)
    print("=" * 40)
