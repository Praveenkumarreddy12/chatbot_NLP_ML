import joblib
import re
from fastapi import FastAPI
from fastapi.responses import FileResponse

from src.db_connector import (
    get_user_details,
    get_order_details,
    get_order_status,
    get_refund_status,
    update_user_phone,
    cancel_order,
    get_connection
)

from src.helper_fns import (
    get_greating_welcome,
    get_parameters,
    predict_intent
)


app =FastAPI()

conversation = {
    "intent" : None,
    "waiting_intent" : None,
    "parameters" : {}
}

def reset_conversaton(intent, value, para):

    global conversation

    if intent == "parameters":
        conversation = {
                "intent" : None,
                "waiting_intent" : value,
                "parameters" : para
            }
    else :
        conversation = {
            "intent" : None,
            "waiting_intent" : value,
            "parameters" : {}
        }

    


@app.get("/")
def home():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                product_id,
                product_name,
                category,
                price,
                stock_quantity,
                description,
                brand,
                image_url
            FROM products
        """)

        products = cursor.fetchall()

        return {
            "message": "E-commerce chatbot API is running",
            "products": products
        }

    finally:
        cursor.close()
        # connection.close()

@app.get("/chatbot")
def chatbot(text : str): #user_id: int, message: str

    # message = "i received a damaged product and want a refund my order id 1 and user id 1"
    
    global conversation


    intent_handler = {
    "account" : get_user_details,   
    "delivery" : get_order_status,  
    "cancellation" : cancel_order,  
    "refund" : get_refund_status,   
    "order_details" : get_order_details,
    "update" : update_user_phone,   
    "greatings" : get_greating_welcome, 
    "parameters" : get_parameters   

    }


    request = predict_intent(text)


    intent = request["intent"] 
    waiting_intent = request.get("waiting_intent")
 
    parameters = request["parameters"]





    if intent != conversation["intent"]:
        reset_conversaton(intent, conversation["waiting_intent"], conversation["parameters"])
        print("Reset Done.")


    # check previous intent
    if conversation["intent"] is not None :
        # If current message contains useful parameters
        # but does not contain a meaningful new intent,
        # continue with previous intent.

        # if intent not in intent_handler :
        #     intent = conversation["intent"]

        if intent == "parameters" :
            intent = conversation["intent"]
            waiting_intent = conversation["waiting_intent"]

    conversation["intent"] = intent
    if waiting_intent is not None :
        conversation["waiting_intent"] = waiting_intent

    # merge parameters
    if intent == "parameters":
        res_parameters = intent_handler[intent](text, conversation["waiting_intent"])
        parameters = res_parameters.get("parameters")
        intent = res_parameters.get("intent")
        pass
    conversation["parameters"].update(parameters)
    conversation["intent"] = intent
    parameters = conversation["parameters"]
    intent = conversation["intent"]


    result =intent_handler[intent](parameters) 

    return result


@app.get("/frontend")
def frontend():
    return FileResponse("templates/home.html")


