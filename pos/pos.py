class POS:
    def __init__(self):
        self.orders = []

    def create_order(self, order):
        self.orders.append(order)
        print(f"Order created: {order}")

    def process_payment(self, order_id, amount):
        print(f"Processing payment for order {order_id} with amount {amount}")