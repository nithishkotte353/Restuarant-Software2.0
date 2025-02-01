from azure.cosmos import CosmosClient,PartitionKey, exceptions

class Inventory:
    def __init__(self):
        self.items = {}
        self.cosmos_client = self.init_cosmos_client()
        self.database_name = 'RestaurantDatabase'
        self.container_name = 'InventoryContainer'
        self.container = self.create_container(self.database_name, self.container_name)

    def init_cosmos_client(self):
        # Replace with your actual connection string
        connection_string = "AccountEndpoint=https://restuarant-cosmosdb.documents.azure.com:443/;AccountKey=BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"
        return CosmosClient.from_connection_string(connection_string)
    
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

    def add_inventory_item(self, item_id, category_id, item_name, quantity):
        item = {
            'id': item_id,
            'categoryId': category_id,
            'name': item_name
        }
        self.add_item(item, quantity)
        self.container.upsert_item(item)
        print(f"Added item {item_name} and quantity {quantity} to inventory and Cosmos DB")

    def remove_inventory_item(self, item_id, category_id, quantity):
        item = {
            'id': item_id,
            'categoryId': category_id
        }
        self.remove_item(item, quantity)
        
        # Assuming you want to remove the item from Cosmos DB as well
        self.container.delete_item(item, partition_key=category_id)
        print(f"Removed item with ID {item_id} and quantity {quantity} from inventory and Cosmos DB")

    def add_item(self, item, quantity):
        self.items[item] = self.items.get(item, 0) + quantity
        print(f"Added {quantity} of {item} to inventory")

    def remove_item(self, item, quantity):
        if item in self.items and self.items[item] >= quantity:
            self.items[item] -= quantity
            print(f"Removed {quantity} of {item} from inventory")
        else:
            print(f"Not enough {item} in inventory")