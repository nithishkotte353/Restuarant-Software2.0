class Recipe:
    def __init__(self):
        self.recipes = {}

    def add_recipe(self, name, ingredients):
        self.recipes[name] = ingredients
        print(f"Added recipe: {name}")

    def remove_recipe(self, name):
        if name in self.recipes:
            del self.recipes[name]
            print(f"Removed recipe: {name}")
        else:
            print(f"Recipe {name} not found")

    def get_recipe(self, name):
        if name in self.recipes:
            return self.recipes[name]
        else:
            print(f"Recipe {name} not found")
            return None