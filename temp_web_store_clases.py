class Product:

  __product_name: str = None
  __product_price: float = None  

  @property
  def product_name(self)->str:
    return self.__product_name
  
  @product_name.setter
  def product_name(self, name):
    if name:
      self.__product_name = name
    else:
      print("Product name not valid.") 

  @property
  def product_price(self)->float:
    return self.__product_price
  
  @product_price.setter
  def product_price(self, price):
    if price >= 0:
      self.__product_price = price
    else:
      print("Product price is not valid.")
  
  def __init__(self, name, price):
    self.product_name = name
    self.product_price = price
  


class Customer:
  __customer_name = "Guest"
  __customer_orders = []

  @property  
  def customer_name(self)->str:
    return self.__customer_name
  
  def 


