class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item, quantity):
        self.items[item] = self.items.get(item, 0) + quantity
        print(f"Added {quantity} of {item} to inventory")

    def remove_item(self, item, quantity):
        if item in self.items and self.items[item] >= quantity:
            self.items[item] -= quantity
            print(f"Removed {quantity} of {item} from inventory")
        else:
            print(f"Not enough {item} in inventory")