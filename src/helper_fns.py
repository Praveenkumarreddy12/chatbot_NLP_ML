import random
import re

def get_greating_welcome(text : str):
    lst = [
        "Hello! 👋 How can I help you today?",
        "Hi there! 😊 What can I do for you?",
        "Hey! 👋 How may I assist you?",
        "Hello! Nice to hear from you. How can I help?",
        "Hi! 😊 What would you like help with?",
        "Hey there! How can I assist you today?",
        "Good morning! ☀️ How can I help you?",
        "Good afternoon! 😊 What can I do for you?",
        "Good evening! 🌆 How may I assist you?",
        "Welcome! 👋 How can I help you today?",
        "Hi! I'm here to help. What do you need?",
        "Hello! 😊 Feel free to ask me anything.",
    ]

    return {
        "error" : str(random.choice(lst))
    }



def get_parameters(text : str, waiting_intent : str) :
    # -------------------------
    #  Extract parameters
    # -------------------------

    parameters = {}

    print("Text : ", text)
    print("Text : ",type(text))
    print(waiting_intent)
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


    print("get_parameters are running.................", phone_match,text)
    return {
        "intent" : waiting_intent,
        "parameters" : parameters
    }