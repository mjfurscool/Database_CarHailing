import	sqlite3
from datetime import datetime
from display import display


def book(email,connection, cursor):
    while 1:
        print("1.List the bookings you offer or cancel a booking\n")
        print("2.List the rides you offer or book a member on your rides\n")
        print("3.Quit\n")
        option = input("Enter your option:")
        if option == '1':
            list_bookings(email,connection, cursor)
        elif option == '2':
            list_rides(email,connection, cursor)

        elif option == '3':
            break
        else:
            print("invalide option")
    return




def list_bookings(email,connection, cursor): #The member should be able to list all bookings on rides s/he offers and cancel any booking
    cursor.execute("SELECT DISTINCT bookings.bno, bookings.email, bookings.rno, bookings.cost, bookings.seats, bookings.pickup, bookings.dropoff FROM bookings, rides WHERE bookings.rno = rides.rno and rides.driver = ? GROUP BY  bookings.bno, bookings.email, bookings.rno, bookings.cost, bookings.seats, bookings.pickup, bookings.dropoff;", (email, ))
    rows = cursor.fetchall()
    print("bno/ email/ rno/ cost/ seats/ pickup/ dropoff")
    for b in rows:
        print(b)
    option = input("Do you want to cancel a booking? -y/n")
    if option == 'y' or option == 'Y':

        try:
            deleted_bno = input("Enter the bno you want to cancel")
            #cursor .execute("DELETE FROM bookings WHERE bno = ?;",(deleted_bno,))
            cursor.execute("SELECT bookings.email, rides.driver, bookings.rno FROM bookings,rides WHERE bookings.rno = rides.rno and bookings.bno = ?;",(deleted_bno,))
            row = cursor.fetchone()
            msg = "Your booking ( bno=" + str(deleted_bno) + " ) is canceled by the driver"
            args = (row[0],datetime.now() ,row[1],msg, row[2], 'n')
            cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", args)
            print("Success! Your message has been sent to "+row[0])
        except:
            print("You have no related booking ")
            return

    elif option == 'n' or option == 'N':
        return
    else:
        print("invalide input")


def list_rides(email,connection, cursor):
    cursor.execute("SELECT DISTINCT rides.rno, rides.price, rides.rdate, rides.seats, rides.lugDesc, rides.src, rides.dst, rides.driver, rides.cno, rides.seats - ifnull(sum(bookings.seats),0) FROM rides, bookings WHERE rides.driver = ? and rides.rno = bookings.rno group by rides.rno, rides.price, rides.rdate, rides.seats, rides.lugDesc, rides.src, rides.dst, rides.driver, rides.cno;", (email,))
    rows = cursor.fetchall()
    print("rno, price, rdate, seats, lugDesc, src, dst, driver, cno, available seats")
    display(rows)
    option = input("Do you want to book a member on your rides from the above list? -y/n")
    if option == 'y' or option == 'Y':
        try:
            ride_no = int(input("select a ride by entering a rno"))
            for row in rows:
                if int(row[0]) == ride_no:
                    avalable_seats = row[9]
            print("The list of people who need the ride from you:")# They have sent a message to the driver in part2
            cursor.execute("SELECT inbox.sender FROM inbox WHERE inbox.email = ? and rno = ?;",(email,ride_no,))
            senders = cursor.fetchall()
            display(senders)
            try:
                book_member, booked_seats, cps, pk_lcode, dp_lcode = input("Enter a email, the number of seats booksed, the cost per seat, pick up location code and drop off location code to make a book(plesae split by a space)").split()
            except:
                print("Please follow the format/n")
                book_member, booked_seats, cps, pk_lcode, dp_lcode = input(
                    "Enter a email, the number of seats booksed, the cost per seat, pick up location code and drop off location code to make a book(plesae split by a space)").split()
            booked_seats = int(booked_seats)
            cps = int(cps)
            check_valid("location", pk_lcode,cursor)
            check_valid("location", dp_lcode,cursor)
            check_valid("amount", cps)

            if booked_seats > avalable_seats:#overbooking
                print("The book will be overbooked!")
                option = input("Do you still want to continue? - y/n")
                if option == 'y' or option == 'Y':
                    cursor.execute("SELECT bno FROM bookings")
                    booking_num = cursor.fetchall()
                    booking_no = max(booking_num)[0] + 1
                    args = (booking_no, book_member, ride_no, cps, booked_seats, pk_lcode, dp_lcode)
                    cursor.execute("INSERT INTO bookings VALUES (?,?,?,?,?,?,?)", args)
                    print("Successful booking! A message will send to your customer!")
                    msg = "Your request of rides (rno is " + str(ride_no) + " ) is confirmed (bno is" + str(
                        booking_num) + " )."
                    args = (book_member, datetime.now(), email, msg, ride_no, 'n')
                    cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", args)
                elif option == 'n' or option == 'N':
                    print("Your operation is canceled")
                else:
                    print("Invalide input")
            else: #not overbooking
                cursor.execute("SELECT bno FROM bookings")
                booking_num = cursor.fetchall()
                booking_no = max(booking_num)[0] + 1
                args = (booking_no, book_member, ride_no, cps, booked_seats, pk_lcode, dp_lcode)
                cursor.execute("INSERT INTO bookings VALUES (?,?,?,?,?,?,?)", args)
                print("Successful booking! A message will send to your customer!")
                msg = "Your request of rides (rno is " + str(ride_no) + " ) is confirmed (bno is" + str(booking_num) + " )."
                args = (book_member, datetime.now(), email, msg, ride_no, 'n')
                cursor.execute("INSERT INTO inbox VALUES(?,?,?,?,?,?)", args)
        except:
            print("invalid input. You may have no related information.")
            return
    elif option == 'n' or option == 'N':
        return
    else:
        print("invalide input")




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



