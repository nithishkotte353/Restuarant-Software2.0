from azure.cosmos import exceptions, CosmosClient, PartitionKey
from utils.cosmos_utils import init_cosmos_client

class Reporting:
    # Define Cosmos DB endpoint and key
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A=="
    
    def __init__(self, cosmos_endpoint, cosmos_key):
        self.cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)
        self.database_name = 'RestaurantDatabase'
        self.orders_container_name = 'OrdersContainer'
        self.orders_container = self.get_container(self.orders_container_name)

    def get_container(self, container_name):
        try:
            database = self.cosmos_client.get_database_client(self.database_name)
            container = database.get_container_client(container_name)
            print(f"Connected to container '{container_name}' successfully.")
            return container
        except exceptions.CosmosResourceNotFoundError:
            print(f"Container '{container_name}' not found.")
            return None

    def generate_sales_report(self):
        query = "SELECT c.orderId, c.amount FROM c"
        items = list(self.orders_container.query_items(query=query, enable_cross_partition_query=True))
        report = {}
        for item in items:
            order_id = item['orderId']
            amount = item.get('amount', 0)
            report[order_id] = amount
        return report

    def generate_inventory_report(self):
        query = "SELECT c.id, c.name, c.quantity FROM c"
        items = list(self.orders_container.query_items(query=query, enable_cross_partition_query=True))
        report = {}
        for item in items:
            item_id = item['id']
            name = item['name']
            quantity = item['quantity']
            report[item_id] = {'name': name, 'quantity': quantity}
        return report