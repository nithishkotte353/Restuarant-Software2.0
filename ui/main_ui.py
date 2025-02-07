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
        cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A=="

        # Initialize Cosmos DB client
        cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)

        # Initialize modules
        self.pos = POS(cosmos_endpoint, cosmos_key)
        self.inventory = Inventory(cosmos_endpoint, cosmos_key)
        self.menu = Menu(cosmos_endpoint, cosmos_key)
        self.reporting = Reporting(cosmos_endpoint, cosmos_key)
        self.recipe = Recipe(cosmos_endpoint, cosmos_key)

    def run(self):
        st.title("Restaurant Software")

        # Create navigation
        menu = ["POS", "Inventory", "Menu", "Reporting", "Recipe"]
        choice = st.sidebar.selectbox("Select Module", menu)

        if choice == "POS":
            self.pos_ui()
        elif choice == "Inventory":
            self.inventory_ui()
        elif choice == "Menu":
            self.menu_ui()
        elif choice == "Recipe":
            self.recipe_ui()
        elif choice == "Reporting":
            self.reporting_ui()

    @st.cache_data
    def fetch_pos_data(self):
        # Fetch POS data from Cosmos DB or other sources
        return self.pos.get_all_orders()

    @st.cache_data
    def fetch_inventory_data(self):
        # Fetch inventory data from Cosmos DB or other sources
        return self.inventory.get_all_items()

    @st.cache_data
    def fetch_menu_data(self):
        # Fetch menu data from Cosmos DB or other sources
        return self.menu.get_all_items()

    @st.cache_data
    def fetch_reporting_data(self):
        # Fetch reporting data from Cosmos DB or other sources
        return self.reporting.generate_sales_report(), self.reporting.generate_inventory_report()

    def pos_ui(self):
        st.header("POS Management")
        order_id = st.text_input("Order ID")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        
        if st.button("Create Order"):
            self.pos.create_order(order_id)
            st.success(f"Order {order_id} created in POS")
        
        if st.button("Process Payment"):
            self.pos.process_payment(order_id, amount)
            st.success(f"Processed payment of {amount} for order {order_id}")

    def inventory_ui(self):
        st.header("Inventory Management")
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=0)
        
        if st.button("Add Item"):
            self.inventory.add_inventory_item(item_name, quantity)
            st.success(f"Added item {item_name} with quantity {quantity} to inventory")
        
        if st.button("Remove Item"):
            self.inventory.remove_inventory_item(item_name, quantity)
            st.success(f"Removed item {item_name} with quantity {quantity} from inventory")

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

    def reporting_ui(self):
        st.header("Reporting")
        
        if st.button("Generate Sales Report"):
            sales_report, _ = self.fetch_reporting_data()
            st.write(sales_report)
        
        if st.button("Generate Inventory Report"):
            _, inventory_report = self.fetch_reporting_data()
            st.write(inventory_report)

if __name__ == "__main__":
    app = RestaurantSoftwareApp()
    app.run()