import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit = False): #changes will not be saved by default.
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    if connection.is_connected():
        print("Connection Successful")
    else:
        print("Failed in connecting to database")


    cursor = connection.cursor(dictionary=True) #query results are returned as dictionaries
    yield cursor

    if commit: #Save changes if requested
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching expenses for date called with{expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s",(expense_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"Insert expenses for date called with{expense_date}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute(("INSERT into expenses (expense_date,amount,category,notes) VALUES(%s,%s,%s,%s)"),
        (expense_date, amount, category, notes)
                       )

def delete_expenses_for_date(expense_date):
    logger.info(f"Delete expenses for date called with{expense_date}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s",(expense_date,))


def fetch_expense_summary(start_date, end_date):
    logger.info(f" Fetching expense summary for date called with{start_date} and {end_date}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute('''SELECT category ,SUM(amount) as total FROM expenses
                                   WHERE expense_date BETWEEN %s AND %s
                                   GROUP BY Category;''', (start_date, end_date))
        data = cursor.fetchall()
        return data

def fetch_monthly_expense_summary():
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT MONTH(expense_date) AS month_number,
                      MONTHNAME(expense_date) AS month_name,
                      SUM(amount) AS total
               FROM expenses
               GROUP BY MONTH(expense_date), MONTHNAME(expense_date)
               ORDER BY month_number'''
        )
        data = cursor.fetchall()
        return data

if __name__ =="__main__":
    expenses = fetch_expenses_for_date("2024-08-01")
    print(expenses)
    insert_expense("2024-09-30", 40, "Food", "Eat tasty samosa chat")
    # delete_expenses_for_date("2024-08-25")
    summary = fetch_expense_summary("2024-08-01","2024-08-05")
    for record in summary:
        print(record)





