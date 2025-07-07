import random

def restock_product(product, min_qty=5, max_qty=20):
    additional = random.randint(min_qty, max_qty)
    product.quantity += additional