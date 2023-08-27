from fastapi import FastAPI
from item_model import Item


app = FastAPI()

@app.get("/")
# def root(): # or with async preferably
async def root():
    return {"message": "Heya Devs!!!"}

@app.get("/items/{item_id}")
# async def read_item(item_id): # or with type hint preferably
async def read_item(item_id: int):
    return {"item_id": item_id}

"""

    Order Matters: Put Fixed Paths First
    Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}
    Otherwise, the path for /users/{user_id} would also match for /users/me, thinking that it’s receiving the parameter user_id with a value of "me".

"""

@app.get("/users/me") # fixed path/endpoint/route
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}") # dynamic path/endpoint/route
async def read_user(user_id: str):
    return {"user_id": user_id}

# Create Item

@app.post("/items/")
async def create_item(item: Item):
    # return item # v1
    item_dict = item.model_dump()
    # item.tax = float(input('Enter the tax: ')) * .90 / 100
    # item.tax = item.price * 0.90 / 100
    if item.tax:
        price_with_tax = item.price * item.tax / 100
        calculated_percentage = item.price + price_with_tax
        f_price_with_tax = f"{f'${calculated_percentage:0.2f}'}"
        item_dict.update({"price_with_tax": f_price_with_tax})
    return item_dict