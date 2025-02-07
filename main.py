from pos.pos import POS
from inventory.inventory import Inventory
from menu.menu import Menu
from reporting.reporting import Reporting
from recipe.recipe import Recipe
from utils.cosmos_utils import init_cosmos_client

def main():
    # Define Cosmos DB endpoint and key
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A=="

    # Initialize modules
    cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)

    pos = POS(cosmos_endpoint, cosmos_key)
    inventory = Inventory(cosmos_endpoint, cosmos_key)
    menu = Menu(cosmos_endpoint, cosmos_key)
    reporting = Reporting(cosmos_endpoint, cosmos_key)
    recipe = Recipe(cosmos_endpoint, cosmos_key)

    while True:
        action = input("'pos' to manage POS, 'inventory' to manage inventory, 'menu' to manage menu items, 'recipe' to manage recipes, or 'exit' to quit: ").strip().lower()
        if action == 'exit':
            break
        elif action == 'pos':
            pos_action = input("Enter 'create' to create an order or 'process' to process a payment: ").strip().lower()
            if pos_action == 'create':
                order_id = input("Enter order ID: ").strip()
                pos.create_order(order_id)
                print(f"Created order {order_id} in POS")
            elif pos_action == 'process':
                order_id = input("Enter order ID: ").strip()
                amount = float(input("Enter payment amount: ").strip())
                pos.process_payment(order_id, amount)
                print(f"Processed payment of {amount} for order {order_id}")
            else:
                print("Invalid POS action. Please enter 'create' or 'process'.")
        elif action == 'inventory':
            inventory_action = input("Enter 'add' to add an item to inventory or 'remove' to remove an item from inventory: ").strip().lower()
            if inventory_action == 'add':
                item_name = input("Enter item name: ").strip()
                quantity = int(input("Enter quantity: ").strip())
                inventory.add_inventory_item(item_name, quantity)
                print(f"Added item {item_name} with quantity {quantity} to inventory")
            elif inventory_action == 'remove':
                item_name = input("Enter item name: ").strip()
                quantity = int(input("Enter quantity: ").strip())
                inventory.remove_inventory_item(item_name, quantity)
                print(f"Removed item {item_name} with quantity {quantity} from inventory")
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
                print(f"Added recipe {name} with ingredients {ingredients}")
            elif recipe_action == 'remove':
                recipe.remove_recipe(name)
                print(f"Removed recipe {name}")
            else:
                print("Invalid recipe action. Please enter 'add' or 'remove'.")
        elif action == 'reporting':
            report_action = input("Enter 'sales' to generate sales report or 'inventory' to generate inventory report: ").strip().lower()
            if report_action == 'sales':
                report = reporting.generate_sales_report()
                print("Sales Report:")
                for order_id, amount in report.items():
                    print(f"Order ID: {order_id}, Amount: {amount}")
            elif report_action == 'inventory':
                report = reporting.generate_inventory_report()
                print("Inventory Report:")
                for item_id, details in report.items():
                    print(f"Item ID: {item_id}, Name: {details['name']}, Quantity: {details['quantity']}")
            else:
                print("Invalid reporting action. Please enter 'sales' or 'inventory'.")
        else:
            print("Invalid action. Please enter 'pos', 'inventory', 'menu', 'recipe', 'reporting', or 'exit'.")

if __name__ == "__main__":
    main()