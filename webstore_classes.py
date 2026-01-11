class Product:
  
  def __init__(self, product_name, product_price):
    self.product_name = product_name
    self.product_price = product_price


class Customer:
  orders = []
  def __init__(self, customer_name):
    self.customer_name = customer_name
    
  def add_order(self, order: Order):
    self.orders.append(order)


class Order:
  
  products = []

  def add_pruduct(self, product: Product):
    self.products.append(product)


class Discount:

  def __init__(self, discount_description, discount_percent):
    self.description = discount_description
    self.discount_percent = discount_percent

