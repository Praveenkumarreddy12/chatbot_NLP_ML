import joblib
import re
from fastapi import FastAPI
from src.db_connector import (
    get_user_details,
    get_order_details,
    get_order_status,
    get_refund_status,
    update_user_phone,
    cancel_order
)

model = joblib.load("src/model.pkl")
vectorizer = joblib.load("src/vectorizer.pkl")
app =FastAPI()




@app.get("/")
def home():
    return {"message": "E-commerce chatbot API is running"}

@app.get("/chatbot")
def chatbot(): #user_id: int, message: str

    message = "i received a damaged product and want a refund my order id 1 and user id 1"
    request = predict_intent(message)

    intent_handler = {
    "account" : get_user_details,
    "order_status" : get_order_status,
    "cancellation" : cancel_order,
    "refund" : get_refund_status,
    "order_details" : get_order_details,
    "update" : update_user_phone

    }

    intent = request["intent"] #need to upgrade like dist
    parameters = request['parameters']


    return intent_handler[intent](parameters)  




def predict_intent(text) :

    text_vectorizer = vectorizer.transform([text])
    predictions = model.predict(text_vectorizer)

    intent = predictions[0]

    # -------------------------
    #  Extract parameters
    # -------------------------

    parameters = {}


    # Extract order ID
    order_match = re.search(
        r"\b(?:order|order\s*id|order\s*number|order\s*#)\s*(?:id\s*)?#?\s*(\d+)\b",
        text.lower()
    )

    if order_match:
        parameters["order_id"] = int(order_match.group(1))


    # Extract product ID
    product_match = re.search(
        r"\b(?:product|product\s*id|product\s*number|product\s*#)\s*(?:id\s*)?#?\s*(\d+)\b",
        text.lower()
    )

    if product_match:
        parameters["product_id"] = int(product_match.group(1))


    # Extract user ID
    user_match = re.search(
        r"\b(?:user(?:\s*id)?|my(?:\s*user)?(?:\s*id)?)\s*#?\s*(\d+)\b",
        text.lower()
    ) 

    if user_match:
        parameters["user_id"] = int(user_match.group(1))

    # Extract Phone number
    phone_match = re.search(
        r"\b(?:phone|phone\s*number|mobile|mobile\s*number|contact|contact\s*number)\s*#?\s*(\d{10})\b",
        text.lower()
    )

    if phone_match :
        parameters["phone_number"] = str(phone_match.group(1))


    print("Parameters : ",parameters)
    return {
        "intent" : intent,
        "parameters" : parameters
    }

# lst = [
#     "Cancel my order 3",
#     "my order has not arrived",
#     "can i return this item",
#     "i am not happy with my purchase and want a refund",
#     "i received a damaged product and want a refund",
#     "my account is locked"
# ]

# for i in lst :
#     print(predict_intent(i))

# print(predict_intent("i want to cancel my subscription order 3"))