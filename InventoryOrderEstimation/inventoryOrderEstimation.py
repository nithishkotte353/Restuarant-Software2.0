import pandas as pd
import numpy as np

def calculate_orders(inventory, menu):
    """
    Calculate maximum orders for each menu item and profit/loss using generative AI techniques for optimization.

    Parameters:
        inventory (dict): Dictionary of ingredients and their available quantities.
        menu (list): List of menu items with their ingredient requirements and prices.

    Returns:
        pd.DataFrame: DataFrame showing menu items, max orders, and profit/loss.
    """
    def calculate_max_orders(ingredients, inventory):
        """Calculate the maximum number of orders that can be fulfilled."""
        max_orders = float('inf')
        total_cost = 0

        for ingredient, required_qty in ingredients.items():
            if ingredient not in inventory:
                return 0, 0
            max_orders = min(max_orders, inventory[ingredient]['quantity'] // required_qty)
            total_cost += required_qty * inventory[ingredient]['cost']

        return max_orders, total_cost

    results = []

    for item in menu:
        name = item['name']
        price = item['price']
        ingredients = item['ingredients']

        # Calculate max orders and cost
        max_orders, total_cost = calculate_max_orders(ingredients, inventory)

        # Calculate profit per order and total profit
        profit_per_order = price - total_cost
        total_profit = max_orders * profit_per_order if max_orders > 0 else 0

        results.append({
            'Menu Item': name,
            'Max Orders': max_orders,
            'Profit per Order': round(profit_per_order, 2),
            'Total Profit': round(total_profit, 2)
        })

    return pd.DataFrame(results)

# Example Input Data
inventory = {
    'rice': {'quantity': 100, 'cost': 1.0},  # in kg
    'chicken': {'quantity': 50, 'cost': 5.0},  # in kg
    'spices': {'quantity': 10, 'cost': 2.0},  # in kg
    'yogurt': {'quantity': 20, 'cost': 3.0},  # in liters
    'onion': {'quantity': 30, 'cost': 1.5},  # in kg
}

menu = [
    {
        'name': 'Chicken Biryani',
        'price': 170.0,
        'ingredients': {
            'rice': 0.3,  # per serving
            'chicken': 0.2,
            'spices': 0.05,
            'yogurt': 0.1,
            'onion': 0.1
        }
    }
]

# Calculate and display results
results = calculate_orders(inventory, menu)
print(results)
