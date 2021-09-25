import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user
    Run a while loop to collect valid data from the user through the input.
    Check if the data has 6 values and if they all are intengers.
    The data is split in a list separated by commas.
    The loop persist until the checks are True.
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,14,43,25,30,23\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try convert all strings into intergers
    Raises ValueError if strings cannot be converted into inte,
    or if there are not 6 exactly values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are expected, your provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    
    return True

# def update_sales_worksheet(data):
#     """
#     Updata worksheet sales in google sheet love_sandwiches
#     and add a new row with the data input from the user.
#     """

#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each of item type

    The surplus is defined as the sales figures subtracted from the stock:
    - Positive surplus indicate waste
    - Negative surplues indicates extra made when the stock was sold out.
    """

    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data
    
# def update_surplus_worksheet(data):
#     """
#     Updata worksheet surplus in google sheet love_sandwiches
#     and add a new row resulted of the calculation of stock numbers less sales number.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print(f"Surplus worksheet updated successfully with this data{data}\n")

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(f"{worksheet}")
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully with this data{data}\n")

def get_5_last_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting 5 of each of sandwiches and returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5::1])
    return columns
        

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome love sandwiches data automation\n")

# main()
sales_columns = get_5_last_entries_sales()