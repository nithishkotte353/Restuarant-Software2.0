import streamlit as st
from pos.pos import POS
from inventory.inventory import Inventory
from menu.menu import Menu
from reporting.reporting import Reporting
from recipe.recipe import Recipe
from utils.cosmos_utils import init_cosmos_client

class RestaurantSoftwareApp:
    def __init__(self):
        # Define Cosmos DB endpoint and key
        cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
        cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"

        # Initialize modules
        self.pos = POS()
        self.inventory = Inventory(cosmos_endpoint, cosmos_key)
        self.menu = Menu(cosmos_endpoint, cosmos_key)
        self.reporting = Reporting()
        self.recipe = Recipe(cosmos_endpoint, cosmos_key)

    def run(self):
        st.title("Restaurant Software")

        # Create navigation
        menu = ["POS", "Inventory", "Menu", "Reservation", "Customer", "Reporting", "Employee", "Recipe"]
        choice = st.sidebar.selectbox("Select Module", menu)

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
        st.header("POS Management")
        order_id = st.text_input("Order ID")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        
        if st.button("Create Order"):
            self.pos.create_order(order_id)
            st.success(f"Order {order_id} created")
        
        if st.button("Process Payment"):
            self.pos.process_payment(order_id, amount)
            st.success(f"Processed payment of {amount} for order {order_id}")

    def inventory_ui(self):
        st.header("Inventory Management")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=0)
        
        if st.button("Add Item"):
            self.inventory.add_inventory_item(item_name, quantity)
            st.success(f"Added item {item_name} and quantity {quantity} to inventory")
        
        if st.button("Remove Item"):
            self.inventory.remove_inventory_item(item_name, quantity)
            st.success(f"Removed item with ID {item_name} and quantity {quantity} from inventory")

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
            st.success(f"Removed item with ID {item_id}")

    def reporting_ui(self):
        st.header("Reporting and Analytics")
        if st.button("Generate Sales Report"):
            self.reporting.generate_sales_report(self.pos.orders)

    def recipe_ui(self):
        st.header("Recipe Management")
        name = st.text_input("Recipe Name")
        ingredients = st.text_area("Ingredients (comma-separated)")
        
        if st.button("Add Recipe"):
            ingredients_list = ingredients.split(',')
            self.recipe.add_recipe(name, ingredients_list)
            st.success(f"Added recipe {name}")
        
        if st.button("Remove Recipe"):
            self.recipe.remove_recipe(name)
            st.success(f"Removed recipe {name}")
        if st.button("Get Recipe"):
            recipe = self.recipe.get_recipe(name)
            st.write(recipe)

if __name__ == "__main__":
    app = RestaurantSoftwareApp()
    app.run()