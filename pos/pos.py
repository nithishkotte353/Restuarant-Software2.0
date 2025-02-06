from azure.cosmos import PartitionKey, exceptions
from utils.cosmos_utils import init_cosmos_client

class POS:
     # Define Cosmos DB endpoint and key
    cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
    cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A=="
    def __init__(self, cosmos_endpoint, cosmos_key):
        self.orders = []
        self.cosmos_client = init_cosmos_client(cosmos_endpoint, cosmos_key)
        self.database_name = 'RestaurantDatabase'
        self.container_name = 'OrdersContainer'
        self.container = self.create_container()

    def create_container(self):
        try:
            database = self.cosmos_client.create_database_if_not_exists(id=self.database_name)
            partition_key_path = PartitionKey(path="/orderId")
            container = database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=partition_key_path
            )
            print(f"Container '{self.container_name}' created successfully.")
            return container
        except exceptions.CosmosResourceExistsError:
            print(f"Container '{self.container_name}' already exists.")
            return self.cosmos_client.get_database_client(self.database_name).get_container_client(self.container_name)

    def create_order(self, order_id):
        order = {
            'id': order_id,  # Ensure 'id' is used as the unique identifier
            'orderId': order_id
        }
        self.orders.append(order)
        self.container.upsert_item(order)
        print(f"Order created: {order}")

    def process_payment(self, order_id, amount):
        try:
            order = self.container.read_item(item=order_id, partition_key=order_id)
            order['amount'] = amount
            self.container.upsert_item(order)
            print(f"Processed payment for order {order_id} with amount {amount}")
        except exceptions.CosmosResourceNotFoundError:
            print(f"Order {order_id} not found in Cosmos DB")