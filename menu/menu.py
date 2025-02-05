from azure.cosmos import exceptions, PartitionKey
from utils.cosmos_utils import init_cosmos_client

class Menu:
    
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"

    def __init__(self, cosmos_endpoint, cosmos_key):
        self.items = {}
        self.cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)
        self.database_name = 'RestaurantDatabase'
        self.container_name = 'MenuContainer'
        self.database = self.create_database(self.database_name)
        self.container = self.create_container(self.database, self.container_name)

    def create_database(self, database_name):
        try:
            database = self.cosmos_client.create_database_if_not_exists(id=database_name)
            print(f"Database '{database_name}' created successfully.")
            return database
        except exceptions.CosmosResourceExistsError:
            print(f"Database '{database_name}' already exists.")
            return self.cosmos_client.get_database_client(database_name)

    def create_container(self, database, container_name):
        try:
            partition_key_path = PartitionKey(path="/categoryId")
            container = database.create_container_if_not_exists(
                id=container_name,
                partition_key=partition_key_path
            )
            print(f"Container '{container_name}' created successfully.")
            return container
        except exceptions.CosmosResourceExistsError:
            print(f"Container '{container_name}' already exists.")
            return self.cosmos_client.get_database_client(self.database_name).get_container_client(container_name)

    def add_item(self, item_id, category_id, item_name, price):
        item = {
            'id': item_id,
            'categoryId': category_id,
            'name': item_name,
            'price': price
        }
        self.container.upsert_item(item)
        print(f"Added item {item_name} with price {price} to menu")

    def remove_item(self, item_id, category_id):
        try:
            self.container.delete_item(item_id, partition_key=category_id)
            print(f"Removed item with ID {item_id} from menu")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Item with ID {item_id} not found in menu")

