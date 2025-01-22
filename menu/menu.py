class Menu:
    def __init__(self):
        self.items = {}

    def add_item(self, item, price):
        self.items[item] = price
        print(f"Added {item} with price {price} to menu")

    def remove_item(self, item):
        if item in self.items:
            del self.items[item]
            print(f"Removed {item} from menu")
        else:
            print(f"{item} not found in menu")