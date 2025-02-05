from azure.cosmos import PartitionKey, exceptions
from utils.cosmos_utils import init_cosmos_client

class Recipe:
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"

    def __init__(self, cosmos_endpoint, cosmos_key):
        self.recipes = {}
        self.cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)
        self.database_name = 'RestaurantDatabase'
        self.container_name = 'RecipeContainer'
        self.container = self.create_container()

    def create_container(self):
        try:
            database = self.cosmos_client.create_database_if_not_exists(id=self.database_name)
            partition_key_path = PartitionKey(path="/name")
            container = database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=partition_key_path
            )
            print(f"Container '{self.container_name}' created successfully.")
            return container
        except exceptions.CosmosResourceExistsError:
            print(f"Container '{self.container_name}' already exists.")
            return self.cosmos_client.get_database_client(self.database_name).get_container_client(self.container_name)

    def add_recipe(self, name, ingredients):
        recipe = {
            'id': name,  # Ensure 'id' is used as the unique identifier
            'name': name,
            'ingredients': ingredients
        }
        self.recipes[name] = ingredients
        self.container.upsert_item(recipe)
        print(f"Added recipe: {name}")

    def remove_recipe(self, name):
        try:
            self.container.delete_item(name, partition_key=name)
            del self.recipes[name]
            print(f"Removed recipe: {name}")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Recipe {name} not found in Cosmos DB")

    def get_recipe(self, name):
        try:
            recipe = self.container.read_item(item=name, partition_key=name)
            return recipe
        except exceptions.CosmosResourceNotFoundError:
            print(f"Recipe {name} not found in Cosmos DB")
            return None