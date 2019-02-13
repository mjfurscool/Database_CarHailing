import	sqlite3
from datetime import datetime
def post(email,connection, cursor):
    while 1:
        try:
            date = str(input("Provide a date yyyy-mm-dd"))
            if check_valid("date", date) == True :
                break

        except:
            print("Invalid date")
    cursor.execute("SELECT rid FROM requests")
    requests_num = cursor.fetchall()
    rid = max(requests_num)[0] + 1
    while 1:
        pickup = str(input("Provide a pick up location code"))
        if check_valid("location", pickup, cursor) == True:
            break
    while 1:
        dropoff = str(input("Provide a drop off location code"))
        if check_valid("location", dropoff, cursor) == True:
            break
    while 1:
        try:
            amount = int(input("Provide the amount you'd like to pay per seat"))
            if check_valid("amount", amount)== True:
                break
        except:
            print("Amount should be integer")

    print("Success. Your rid is: ", rid)
    args = (rid, email, date, pickup, dropoff, amount)
    cursor.execute("insert into requests values (?,?,?,?,?,?);",args)
    #cursor.execute("INSERT INTO requests VALUES(:rid,:email,:rdate,:pickup,:dropoff,:amount)", {"rid": rid, "email": email,"rdate":date, "pickup": pickup, "dropoff":dropoff, "amount":amount})
    connection.commit()
    return
def check_valid(type, value, cursor = None):


    if type == "date":
        y, m , d = value.split("-")
        if datetime(int(y), int(m), int(d)) > datetime.today():
            print("valid date")
            return True
        else:
            print("invalid date")
            return False
    if type == "location":
        cursor.execute("SELECT lcode FROM locations;")
        lcodes = cursor.fetchall()
        if (value,) in lcodes:
            print("valid lcode")
            return True
        else:
            print("invalid lcode")
            return False
    if type == "amount":
        if(isinstance(value,int)== True):
            print("valid price")
            return True
        else:
            print("invalid price")
            return False



