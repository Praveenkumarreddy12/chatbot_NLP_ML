# Chatbot NLP ML for (E-Commerc Website)

A basic **customer-support chatbot** built using **Python, NLP, Machine Learning, FastAPI, and MySQL**.

The main purpose of this project is to understand how an NLP-based chatbot can identify a user's intention, extract required information, connect with a database, and provide an appropriate response.

## Technologies Used

* Python
* NLP
* TF-IDF Vectorizer
* LinearSVC
* FastAPI
* MySQL
* HTML, CSS, JavaScript

## How It Works

The chatbot follows this flow:

```text
User Message
     ↓
NLP Processing
     ↓
TF-IDF Vectorizer
     ↓
LinearSVC
     ↓
Intent Detection
     ↓
Parameter Extraction
     ↓
Python Function
     ↓
MySQL Database
     ↓
Chatbot Response
```

## Intents

The chatbot currently supports the following intents:

| Intent          | Function               | Purpose                               |
| --------------- | ---------------------- | ------------------------------------- |
| `account`       | `get_user_details`     | Get user account details              |
| `delivery`      | `get_order_status`     | Check order delivery/status           |
| `cancellation`  | `cancel_order`         | Cancel an order                       |
| `refund`        | `get_refund_status`    | Check refund status                   |
| `order_details` | `get_order_details`    | Get order information                 |
| `update`        | `update_user_phone`    | Update user's phone number            |
| `greatings`     | `get_greating_welcome` | Handle greetings and welcome messages |

## NLP and Machine Learning

### TF-IDF Vectorizer

TF-IDF is used to convert the user's text into numerical features that can be understood by the machine learning model.

For example:

```text
"I want to cancel my order"
            ↓
      TF-IDF Vectorizer
            ↓
     Numerical Features
```

### LinearSVC

The **LinearSVC** machine learning algorithm is used for **intent classification**.

For example:

```text
User:
"I want to cancel my order"

        ↓

TF-IDF

        ↓

LinearSVC

        ↓

Intent:
cancellation
```

## Database

The application uses **MySQL** to store and retrieve e-commerce-related information such as:

* Users
* Products
* Orders
* Order items
* Delivery/order status
* Refund information

The chatbot uses the extracted parameters such as `user_id` and `order_id` to retrieve or update the required information.

## Important Project Note

This is a **basic chatbot application created mainly for learning and testing NLP, Machine Learning, API integration, and database connectivity**.

This application **does not contain shopping features such as a Buy button, Add to Cart functionality, payment processing, or a complete e-commerce checkout system**.

The main focus of this project is the **customer-support chatbot** and how it can:

* Understand user messages
* Identify the correct intent
* Extract information such as user ID and order ID
* Call the appropriate Python function
* Retrieve or update information in MySQL
* Return the result to the user

### Test Data Note

The database contains sample data created mainly for testing the chatbot.

In some test cases, the **user ID and order ID may appear to be the same**, for example:

```text
User ID: 1
Order ID: 1
```

This is only because of the simplified sample data used for testing.

In a real e-commerce application, a user can have **multiple orders**, so the same user ID can be associated with different order IDs:

```text
User ID: 1 → Order ID: 1
User ID: 1 → Order ID: 5
User ID: 1 → Order ID: 8
```

Therefore, the chatbot is designed to treat `user_id` and `order_id` as **two different parameters**, even when their values happen to be the same in the test data.

## Example

User:

```text
Can I cancel my order?
```

Chatbot:

```text
Please provide your user ID and order ID.
```

User:

```text
User ID 2 and Order ID 5
```

The application extracts:

```python
{
    "user_id": 2,
    "order_id": 5
}
```

Then it identifies the intent as:

```text
cancellation
```

and calls:

```python
cancel_order(user_id=2, order_id=5)
```

The function communicates with MySQL and returns the result to the chatbot.

## Project Goal

The goal of this project is to learn and demonstrate the complete flow of a simple NLP/ML chatbot:

```text
NLP
 ↓
Machine Learning
 ↓
Intent Classification
 ↓
Parameter Extraction
 ↓
FastAPI
 ↓
MySQL
 ↓
Chatbot Response
```

This project can be further extended with more intents, better NLP models, real e-commerce APIs, authentication, larger datasets, and more advanced conversational capabilities.

Setup
1. Create virtual environment
python -m venv venv
2. Activate environment
Windows PowerShell:

venv\Scripts\activate
Mac/Linux:

source venv/bin/activate
3. Install requirements
pip install -r requirements.txt
4. Add Groq API key
Create a .env file:

GROQ_API_KEY=your_groq_api_key_here
5. Run app
streamlit run app.py