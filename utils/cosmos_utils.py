from azure.cosmos import CosmosClient

cosmos_endpoint = "https://restuarant-cosmosdb.documents.azure.com:443/"
cosmos_key = "BfgdJzuIq6DKgvvEEJAfxaXrUZiZL2D6rzt7MoRC2tHwLVcD2zPCj9E1Lush577j62Y4dqH3FVcIACDbaLJ68A==;"

def init_cosmos_client(cosmos_endpoint, cosmos_key):
    return CosmosClient(cosmos_endpoint, cosmos_key)