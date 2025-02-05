from pos.pos import POS
from inventory.inventory import Inventory
from menu.menu import Menu
from reporting.reporting import Reporting
from recipe.recipe import Recipe
from utils.cosmos_utils import init_cosmos_client

from ui.main_ui import RestaurantSoftwareApp

def add_inventory_item(inventory):
    item_id = input("Enter item ID: ").strip()
    item_name = input("Enter item name: ").strip()
    quantity = int(input("Enter quantity: ").strip())
    inventory.add_item(item_id, item_name, quantity)
    print(f"Added {quantity} of {item_name} to inventory")

def remove_inventory_item(inventory):
    item_id = input("Enter item ID to remove: ").strip()
    inventory.remove_item(item_id)
    print(f"Removed item with ID {item_id} from inventory")

def main():
    # Define Cosmos DB endpoint and key
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"

    # Initialize modules
    cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)

    pos = POS()
    inventory = Inventory(cosmos_endpoint, cosmos_key)
    menu = Menu(cosmos_endpoint, cosmos_key)
    reporting = Reporting()
    recipe = Recipe(cosmos_endpoint, cosmos_key)

    # Example usage
    pos.create_order("Order 1")
    pos.process_payment("Order 1", 100)

    while True:
        action = input("Enter 'add' to add an item, 'remove' to remove an item from inventory, 'menu' to manage menu items, 'recipe' to manage recipes, or 'exit' to quit: ").strip().lower()
        if action == 'exit':
            break
        elif action == 'inventory':
            inventory_action = input("Enter 'add' to add an item to inventory or 'remove' to remove an item from inventory: ").strip().lower()
            inventory_item_id = input("Enter item ID: ").strip()
            inventory_category_id = input("Enter category ID: ").strip()
            if inventory_action == 'add':
                inventory_item_name = input("Enter item name: ").strip()
                inventory_quantity = int(input("Enter quantity: ").strip())
                inventory.add_inventory_item(inventory_item_id, inventory_category_id, inventory_item_name, inventory_quantity)
                print(f"Added item {inventory_item_name} in inventory")
            elif inventory_action == 'remove':
                inventory.remove_inventory_item(inventory_item_id, inventory_category_id, inventory_quantity)
                print(f"Removed item with ID {inventory_item_name} from inventory")
            else:
                print("Invalid inventory action. Please enter 'add' or 'remove'.")
        elif action == 'menu':
            menu_action = input("Enter 'add' to add an item to the menu or 'remove' to remove an item from the menu: ").strip().lower()
            item_id = input("Enter item ID: ").strip()
            category_id = input("Enter category ID: ").strip()
            if menu_action == 'add':
                item_name = input("Enter item name: ").strip()
                price = float(input("Enter item price: ").strip())
                menu.add_item(item_id, category_id, item_name, price)
                print(f"Added item {item_name} with price {price} to menu")
            elif menu_action == 'remove':
                menu.remove_item(item_id, category_id)
                print(f"Removed item with ID {item_id} from menu")
            else:
                print("Invalid menu action. Please enter 'add' or 'remove'.")
        elif action == 'recipe':
            recipe_action = input("Enter 'add' to add a recipe or 'remove' to remove a recipe: ").strip().lower()
            name = input("Enter recipe name: ").strip()
            if recipe_action == 'add':
                ingredients = input("Enter ingredients (comma-separated): ").strip().split(',')
                recipe.add_recipe(name, ingredients)
            elif recipe_action == 'remove':
                recipe.remove_recipe(name)
            else:
                print("Invalid recipe action. Please enter 'add' or 'remove'.")
        else:
            print("Invalid action. Please enter 'add', 'remove', 'menu', 'recipe', or 'exit'.")

if __name__ == "__main__":
    app = RestaurantSoftwareApp()
    app.run()
    main()