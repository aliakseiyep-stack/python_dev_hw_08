class Product:

  product_name: str = None
  __product_price: str = None

  def __init__(self, name, price):
    
    
    

  @property
  def product_name(self)->str:
    return self.__product_name
  
  @product_name.setter
  def product_name(self, name):
    if name:
      self.__product_name = name
    else:
      print("Product name is blank.") 

  @property
  def product_price(self)->float:
    return self.__product_price
  
  @product_price.setter
  def product_price(self, price):
    if price >= 0:
      self.__product_price = price
    else:
      print("Product price must be >=0.")
      
      
      
  


class Customer:
  __name = "Guest"
  __orders = []