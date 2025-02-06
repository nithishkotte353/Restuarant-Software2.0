from azure.cosmos import CosmosClient,PartitionKey, exceptions
from utils.cosmos_utils import init_cosmos_client

class Inventory:
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"

    def __init__(self, cosmos_endpoint, cosmos_key):
        self.items = {}
        self.cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)
        self.database_name = 'RestaurantDatabase'
        self.container_name = 'InventoryContainer'
        self.container = self.create_container(self.database_name, self.container_name)
    
    def create_container(self, database, container_name):
        try:
            database = self.cosmos_client.get_database_client(self.database_name)
            partition_key_path = PartitionKey(path="/categoryId")
            container = database.create_container_if_not_exists(
                id=container_name,
                partition_key=partition_key_path
            )
            print(f"Container '{self.container_name}' created successfully.")
            return container
        except exceptions.CosmosResourceExistsError:
            print(f"Container '{self.container_name}' already exists.")
            return self.cosmos_client.get_database_client(self.database_name).get_container_client(self.container_name)

    def add_inventory_item(self, item_name, quantity):
        item = {
            'id': item_name,
            'name': item_name,
            'quantity': quantity
        }
        self.items[item_name] = self.items.get(item_name, 0) + quantity
        self.container.upsert_item(item)
        print(f"Added item {item_name} with quantity {quantity} to inventory and Cosmos DB")

    def remove_inventory_item(self, item_name, quantity):
        if item_name in self.items and self.items[item_name] >= quantity:
            self.items[item_name] -= quantity
            if self.items[item_name] == 0:
                del self.items[item_name]
                self.container.delete_item(item_name, partition_key=item_name)
                print(f"Removed item {item_name} from inventory and Cosmos DB")
            else:
                item = {
                    'id': item_name,
                    'name': item_name,
                    'quantity': self.items[item_name]
                }
                self.container.upsert_item(item)
                print(f"Updated item {item_name} with new quantity {self.items[item_name]} in inventory and Cosmos DB")
        else:
            print(f"Not enough of item {item_name} in inventory to remove {quantity}")

    def add_item(self, item, quantity):
        self.items[item['id']] = self.items.get(item['id'], 0) + quantity
        print(f"Added {quantity} of item {item['id']} to inventory")

    def remove_item(self, item, quantity):
        if item['id'] in self.items and self.items[item['id']] >= quantity:
            self.items[item['id']] -= quantity
            print(f"Removed {quantity} of item {item['id']} from inventory")
        else:
            print(f"Not enough of item {item['id']} in inventory to remove {quantity}")