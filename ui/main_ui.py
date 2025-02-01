import streamlit as st
from pos.pos import POS
from inventory.inventory import Inventory
from menu.menu import Menu
from reporting.reporting import Reporting
from recipe.recipe import Recipe

class RestaurantSoftwareApp:
    def __init__(self):
        # Initialize modules
        self.pos = POS()
        self.inventory = Inventory()
        self.menu = Menu()
        self.reporting = Reporting()
        self.recipe = Recipe()

    def run(self):
        st.title("Restaurant Software")

        # Create navigation
        menu = ["POS", "Inventory", "Menu", "Reservation", "Customer", "Reporting", "Employee", "Recipe"]
        choice = st.sidebar.selectbox("Select Module", menu)

        #dummmy comment

        if choice == "POS":
            self.pos_ui()
        elif choice == "Inventory":
            self.inventory_ui()
        elif choice == "Menu":
            self.menu_ui()
        elif choice == "Reporting":
            self.reporting_ui()
        elif choice == "Recipe":
            self.recipe_ui()

    def pos_ui(self):
        st.header("POS System")
        order_id = st.text_input("Order ID")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        if st.button("Create Order"):
            self.pos.create_order(order_id)
        if st.button("Process Payment"):
            self.pos.process_payment(order_id, amount)

    def inventory_ui(self):
        st.header("Inventory Management")
        item_id = st.text_input("Item ID")
        category_id = st.text_input("Category ID")
        item = st.text_input("Item")
        quantity = st.number_input("Quantity", min_value=0)
        if st.button("Add Item"):
            self.inventory.add_inventory_item(item_id, category_id, item, quantity)
        if st.button("Remove Item"):
            self.inventory.remove_item(item, quantity)

    def menu_ui(self):
        st.header("Menu Management")
        item_id = st.text_input("Item ID")
        category_id = st.text_input("Category ID")
        item_name = st.text_input("Item Name")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        
        if st.button("Add Item"):
            self.menu.add_item(item_id, category_id, item_name, price)
            st.success(f"Added item {item_name} with price {price}")
        
        if st.button("Remove Item"):
            self.menu.remove_item(item_id, category_id)
            st.success(f"Removed item with ID {item_id} ")

    def reporting_ui(self):
        st.header("Reporting and Analytics")
        if st.button("Generate Sales Report"):
            self.reporting.generate_sales_report(self.pos.orders)

    def recipe_ui(self):
        st.header("Recipe Management")
        name = st.text_input("Recipe Name")
        ingredients = st.text_input("Ingredients (comma separated)")
        if st.button("Add Recipe"):
            self.recipe.add_recipe(name, ingredients.split(','))
        if st.button("Remove Recipe"):
            self.recipe.remove_recipe(name)
        if st.button("Get Recipe"):
            recipe = self.recipe.get_recipe(name)
            st.write(recipe)

if __name__ == "__main__":
    app = RestaurantSoftwareApp()
    app.run()