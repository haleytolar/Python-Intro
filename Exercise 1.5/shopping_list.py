class ShoppingList:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    
    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f"'{item}' is successfully added to the list.")
        else:
            print(f"'{item}' is already in the list.")
    
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f"'{item}' is successfully removed.")
        else:
            print(f"'{item}' is not in the list.")
    
    def view_list(self):
        if self.shopping_list:
            print(f"Shopping List '{self.list_name}':")
            for index, item in enumerate(self.shopping_list, 1):
                print(f"{index}. {item}")
        else:
            print(f"Shopping List '{self.list_name}' is empty.")
    
    def merge_lists(self, obj):
        # Creating a name for our new, merged shopping list
        merged_lists_name = 'Merged List - ' + str(self.list_name) + " + " + str(obj.list_name)

        # Creating an empty ShoppingList object
        merged_lists_obj = ShoppingList(merged_lists_name)

        # Adding the first shopping list's items to our new list
        merged_lists_obj.shopping_list = self.shopping_list.copy()

        # Adding the second shopping list's items to our new list -
        # we're doing this so that there won't be any repeated items
        # in the final list, if both source lists contain common
        # items between each other
        for item in obj.shopping_list:
            if item not in merged_lists_obj.shopping_list:
                merged_lists_obj.shopping_list.append(item)

        # Returning our new, merged object
        return merged_lists_obj


# Creating the shopping list objects
pet_store_list = ShoppingList('Pet Store List')
grocery_store_list = ShoppingList('Grocery Store List')

# Adding items to the pet store list
for item in ['dog food', 'frisbee', 'bowl', 'collars', 'flea collars']:
    pet_store_list.add_item(item)

# Removing an item
pet_store_list.remove_item('flea collars')

# Adding a duplicate item
pet_store_list.add_item('frisbee')  # Duplicate item

# Adding items to the grocery store list
for item in ['fruits', 'vegetables', 'bowl', 'ice cream']:
    grocery_store_list.add_item(item)

# Merging the lists
merged_list = pet_store_list.merge_lists(grocery_store_list)

# Displaying the merged list
merged_list.view_list()
