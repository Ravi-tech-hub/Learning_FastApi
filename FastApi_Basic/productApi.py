from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from datetime import datetime

# product request model
class ProductCreate(BaseModel):
  name:str=Field(...,min_length=2,max_length=100)
  price:float=Field(...,gt=0)
  category:str=Field(...,min_length=2,max_length=50)
  description:Optional[str]=None

# product response
class ProductResponse(BaseModel):
  id:int
  name:str
  price:float
  category:str
  description:Optional[str]
  class Config:form_attributes=True

from fastapi import FastAPI,HTTPException
app=FastAPI()
product_db=[]

@app.get("/products",response_model=list[ProductResponse])
def get_products(
  skip:int =0,
  limit:int=10,
  search:Optional[str]=None,
  category:Optional[str]=None,
  min_price:Optional[float]=None,
  max_price:Optional[float]=None
):
  results=product_db.copy()
  if search:
    results=[product for product in results if search.lower() in product["name"].lower()]

  if category:
        results = [product for product in results if product["category"].lower() == category.lower()]
  if min_price is not None:
        results = [p for p in results if p["price"] >= min_price]

  if max_price is not None:
        results = [p for p in results if p["price"] <= max_price]

  return results[skip : skip + limit]

@app.get("/products/{product_id}",response_model=ProductResponse)
def get_product(product_id:int):
   for product in product_db:
      if product["id"]==product_id:
         return product
      raise HTTPException(status_code=404,detail="Product not found")

@app.post("/products",response_model=ProductResponse)
def create_product(product:ProductCreate):
    new_product={
        "id":len(product_db)+1,
        "name":product.name,
        "category":product.category,
        "price":product.price,
        "description":product.description
    }
    product_db.append(new_product)
    return new_product

@app.put("/products/{product_id}",response_model=ProductResponse)
def update_product(product_id:int,product:ProductCreate):
    for p in product_db:
        if p["id"]==product_id:
            p["name"]=product.name
            p["category"]=product.category
            p["price"]=product.price
            p["description"]=product.description
            return p
        raise HTTPException(status_code=404,detail="Product not found")
    

@app.delete("/products/{product_id}")
def delete_product(product_id:int):
    for p in product_db:
        if p["id"]==product_id:
            product_db.remove(p)
            return {"detail":"product deleted"}
        raise HTTPException(status_code=404,detail="Product not found")