import	sqlite3	
import re
import sys
import getpass
from offer import*
from search import*
from requests import*
from post import*
from book import*
connection = None
cursor = None
def main():
	
	global connection, cursor
	
	p=input("Enter a database's name")
	path=str("./"+p)
	connect(path)
	
	welcome_screen()
	
	connection.commit()
	connection.close()
	return
def connect(path):
	
	global connection, cursor

	connection = sqlite3.connect(path, timeout=10)
	
	cursor = connection.cursor()
	
	cursor.execute('PRAGMA foreign_keys=ON; ')

	connection.commit()
	return	
def welcome_screen():
	
	global connection,cursor

	while(1):

		status=input("Enter log in(l), register(r), quit(q)? ")
		
		if status == "l" or status == "L":
			log_in()
			break		
		elif status == "r" or status == "R":
			sign_up()
			break
		elif status == "q" or status == "Q":
			sys.exit()		
		else:
			print("Invalid, enter again.")
			continue
					
	connection.commit()
	return
def sign_up():
	
	global connection,cursor
	

	
	email=input("Enter an e-mail ")
	
	while (validateEmail(email) is False):
		
		print("This is an invalid email")
		
		email=str(input("Enter an e-mail "))	
		
	while( check_email(email) is True):
		
		print("This is an existing email")
		
		email=str(input("Enter an e-mail "))
		
	name=str(input("Enter a name"))
	
	phone=str(input("Enter a phone"))
	
	pwd=getpass.getpass('Enter your password')
	
	insert_members="INSERT INTO members VALUES(:email,:name,:phone,:pwd)"
	
	cursor.execute(insert_members,{"email":email,"name":name,"phone":phone,"pwd":pwd})
	
	menu(email)	
	
	connection.commit()
	



	return
def log_in():
	
	global connection,cursor
	
	email=str(input("Enter your e-mail"))
	
	while (validateEmail(email) is False):
		
		print("This is an invalid email")
		
		email=str(input("Enter an e-mail "))		
	
	while(check_email(email) is False):
		
		print("This is not a vaild e-mail")
		
		email=str(input("Enter your e-mail"))	
	
	pwd=getpass.getpass('Enter your password')
		
	while(check_log(email,pwd) is False):
		
		print("This is not a vaild password")
		
		pwd=getpass.getpass('Enter your password')
		
	menu(email)	
	
	return

def check_email(email):
	
	global connection,cursor

	cursor.execute("select email from members ;")

	result=cursor.fetchall()

	emails=[]

	for i in result:
		emails.append(i[0])

	if email in emails:

		return True

	else:

		return False
	
def check_log(email,pwd):
	
	global connection,cursor
	
	
	cursor.execute("SELECT * FROM members WHERE email=:email and pwd=:pwd",			
	 				{"email":email, "pwd":pwd} )	
	
	result=cursor.fetchall()
	
	pwds=[]

	for i in result:
		pwds.append(i[3])	
		
	if pwd in pwds:
		
		return True
	
	else:
		
		return False
	
	connection.commit()
	
def menu(email):
	
	global connection,cursor
	
	mail(email)
	
	select=input("Select what you want to do.\n1.Offer a ride.\n2.Search for rides.\n3.Book members or cancel bookings.\n4.Post ride requests.\n5.Search and delete ride requests.\n6.Quit")
	
	if select=="1":
		
		offer(email,connection,cursor)
		
	elif select=="2":
		
		search(email,connection,cursor)
		
	elif select=="3":
		
		book(email,connection,cursor)
		
	elif select=="4":
		
		post(email,connection,cursor)
		
	elif select=="5":
		
		search_delete_requests(email,connection,cursor)
		
	elif select=="6":	
		
		welcome_screen()
	else:
		
		print("Invalid input")
		
	menu(email)
	
	connection.commit()
	
	return
def mail(email):
	
	global connection,cursor
	
	cursor.execute("SELECT * FROM inbox WHERE email=:email and seen='n'",			
	 				{"email":email} )	
	result=cursor.fetchall()
	
	for row in result:
		
		print (row)	
		
	cursor.execute("UPDATE inbox SET seen = 'y' WHERE email=:email",			
	                                {"email":email} )	

	connection.commit()	
	return

def validateEmail(email):

	if len(email) > 5:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return True
	return False

main()