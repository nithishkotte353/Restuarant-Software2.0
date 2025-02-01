from pos.pos import POS
from inventory.inventory import Inventory
from menu.menu import Menu
from reporting.reporting import Reporting
from recipe.recipe import Recipe

from ui.main_ui import RestaurantSoftwareApp

if __name__ == "__main__":
    app = RestaurantSoftwareApp()
    app.run()

def main():
    # Initialize modules
    pos = POS()
    inventory = Inventory()
    menu = Menu()
    reporting = Reporting()
    recipe = Recipe()

    # Example usage
    pos.create_order("Order 1")
    pos.process_payment("Order 1", 100)

  
    inventory_itemid = input("Enter inventory item ID: ")
    inventory_categoryid = input("Enter inventory category ID: ")
    inventory_item = input("Enter inventory item: ")    
    quantity = input("Enter quantity: ")
    inventory.add_inventory_item(inventory_itemid, inventory_categoryid, inventory_item, quantity)
    inventory.remove_inventory_item(inventory_itemid, inventory_categoryid, quantity)

    # Add and remove items from the menu
    item_id = input("Enter item ID: ")
    category_id = input("Enter category ID: ")
    item_name = input("Enter item name: ")
    price = float(input("Enter item price: "))
    menu.add_item(item_id, category_id, item_name, price)
    menu.remove_item(item_id, category_id)

    reporting.generate_sales_report(pos.orders)

    recipe.add_recipe("Pasta", ["Tomato", "Basil", "Garlic"])
    recipe.remove_recipe("Pasta")
    print(recipe.get_recipe("Pasta"))

if __name__ == "__main__":
    main()