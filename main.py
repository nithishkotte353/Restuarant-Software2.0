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

    inventory.add_item("Tomato", 50)
    inventory.remove_item("Tomato", 20)

    menu.add_item("Pasta", 12.99)
    menu.remove_item("Pasta")

    reporting.generate_sales_report(pos.orders)

    recipe.add_recipe("Pasta", ["Tomato", "Basil", "Garlic"])
    recipe.remove_recipe("Pasta")
    print(recipe.get_recipe("Pasta"))

if __name__ == "__main__":
    main()