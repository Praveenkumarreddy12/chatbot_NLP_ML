import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="chatbot_nlp"
    )

# print("MySQL connected successfully!")

# -------------------------
# ACCOUNT INTENTS
# -------------------------

def get_user_details(request):

    connection = get_connection()

    user_id = request.get('user_id')

    if user_id is None:
        return {
            "Success" : False,
            "error" : "Please provide user id with out this i can't proced further steps."
        }

    cursor =connection.cursor(dictionary=True)

    query = """
        SELECT id, user_name, email, phone, created_at
        FROM users
        WHERE id = %s
    """

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def update_user_phone(request):

    connection = get_connection()

    user_id = request.get('user_id')
    phone = request.get('phone_number')
    
    if user_id is None:
        return {
            "Success" : False,
            "error" : "Please provide user id with out this i can't proced further steps."
        }

    if phone is None:
        return {
            "Success" : False,
            "error" : "Please provide phone number ex: my number 990XXXXX or phone number : 8843XXX with 10 digit correct number with out this i can't proced further steps."
        }

    cursor = connection.cursor()

    query = """
        UPDATE users
        SET phone = %s
        WHERE user_id = %s
    """

    cursor.execute(query, (phone, user_id))
    connection.commit()

    cursor.close()
    connection.close()

    return "Phone number updated successfully."


def get_order_status(request):

    connection = get_connection()

    user_id = request.get('user_id')

    if user_id is None:
        return {
            "Success" : False,
            "error" : "Please provide user id with out this i can't proced further steps."
        }
    
    cursor = connection.cursor()

    query = """
        SELECT order_id, order_status, total_amount
        FROM orders
        WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))

    results = cursor.fetchall()

    cursor.close()

    lst_result = []
    for order_id, status, amount in results:
         lst_result.append({
              "order_id" : order_id,
              "status" : status,
              "amount" : amount
         })
         


    return lst_result
# {
#         "order_id": results[0],
#         "status":results[0],
#         "amount": results[0]
#     }


# -------------------------
# ORDER DETAILS
# -------------------------

def get_order_details(request):

    connection = get_connection()

    order_id = request.get('order_id')
    user_id = request.get('user_id')
    
    if order_id is None:
        return {
            "Success" : False,
            "error" : "Please provide order id and user id at Once. with out this i can't proced further steps1."
        }
    if user_id is None:
            return {
                "Success" : False,
                "error" : "Please provide user id and order id at Once. with out this i can't proced further steps."
            }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            o.order_id,
            p.product_name,
            oi.quantity,
            oi.price
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE o.order_id = %s
        AND o.user_id = %s
    """

    cursor.execute(query, (order_id, user_id))
    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results



# -------------------------
# CANCELLATION
# -------------------------

def cancel_order(request):

    connection = get_connection()

    order_id = request.get('order_id')
    user_id = request.get('user_id')

    if order_id is None:
        return {
            "Success" : False,
            "error" : "Please provide order id and user id at once. with out this i can't proced further steps2."
        }
    if user_id is None:
            return {
                "Success" : False,
                "error" : "Please provide user id and order id at once. with out this i can't proced further steps."
            }

    cursor = connection.cursor()

    # First check current status
    query = """
        SELECT order_status
        FROM orders
        WHERE order_id = %s
        AND user_id = %s
    """

    cursor.execute(query, (order_id, user_id))
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        connection.close()
        return "Order not found."

    current_status = result[0]

    if current_status in ("Delivered", "Cancelled"):
        cursor.close()
        connection.close()
        return f"Order cannot be cancelled because it is already {current_status}."

    # Cancel order
    update_query = """
        UPDATE orders
        SET order_status = 'Cancelled'
        WHERE order_id = %s
        AND user_id = %s
    """

    cursor.execute(update_query, (order_id, user_id))
    connection.commit()

    cursor.close()
    connection.close()

    return f"Order #{order_id} has been cancelled successfully."


# -------------------------
# REFUND STATUS
# -------------------------

def get_refund_status(request):

    connection = get_connection()

    order_id = request.get('order_id')
    user_id = request.get('user_id')

    if order_id is None:
        return {
            "Success" : False,
            "error" : "Please provide order id and user id at once. without this i can't proced further steps."
        }
    if user_id is None:
            return {
                "Success" : False,
                "error" : "Please provide user id and order id at once. with out this i can't proced further steps."
            }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT order_id, order_status, total_amount
        FROM orders
        WHERE order_id = %s
        AND user_id = %s
    """

    cursor.execute(query, (order_id, user_id))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result is None:
        return None

    if result["order_status"] == "Cancelled":
        return {
            "order_id": result["order_id"],
            "refund_status": "Refund initiated",
            "amount": result["total_amount"]
        }

    return {
        "order_id": result["order_id"],
        "refund_status": "No refund available",
        "amount": result["total_amount"]
    }