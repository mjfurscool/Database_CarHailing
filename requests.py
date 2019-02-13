import sqlite3
import datetime
global connection, cursor

def search_delete_requests(email,connection,cursor):

    all_requests(email,connection,cursor)
    request2 = input("Do you want to delete? Y/N")
    while(more(request2,connection,cursor) is False):
        request2 = input("Do you want to delete? Y/N")
    if request2 == "y" or request2 == "Y":
        request3 = input("Which request do you want to delete? Please enter a rid")
        while(request3.isdigit() is False):
            request3 = input("Which request do you want to delete? Please enter a rid?")
        cursor.execute("select * from requests where rid = :rid and email = :email;",{"rid":request3,"email":email}) 
        while(cursor.fetchone() == None):
            request3 = input("Error. Which request do you want to delete? Please enter a rid?")
            cursor.execute("select * from requests where rid = :rid and email = :email;",{"rid":request3,"email":email}) 
        cursor.execute("delete from requests where rid = :rid and email = :email ;",{"rid":request3,"email":email}) 

    request4 = input("Do you want to message a member? Y/N")
    if request4 == "y" or request4 == "Y":
        search_request(email,connection,cursor)
    connection.commit()    

def all_requests(email,connection,cursor):
    cursor.execute("select * from requests where email = :member;",{"member":email})
    result = cursor.fetchall()
    ride_requests=[]
    l=len(result)
    for i in range (len(result)):
        ride_requests.append(result[i])
    for i in ride_requests:
        print(i)
    connection.commit()
 
def search_request(email,connection,cursor):
    sr = input("Enter a location code or city to see the matched ride requests")
    if sr != '':

        cursor.execute("SELECT requests.* FROM requests, locations WHERE requests.pickup=locations.lcode and city like ? union SELECT * FROM requests WHERE pickup= ? ;",			
	 				('%{}%'.format(sr),'{}'.format(sr),) )    
        while(cursor.fetchone() == None):
            sr = input("Error. Enter location code or city to see ride requests")
            cursor.execute("SELECT requests.* FROM requests, locations WHERE requests.pickup=locations.lcode and city like ? union SELECT * FROM requests WHERE pickup= ? ;",			
	 				('%{}%'.format(sr),'{}'.format(sr),) )
        
        cursor.execute("SELECT requests.* FROM requests, locations WHERE requests.pickup=locations.lcode and city like ? union SELECT * FROM requests WHERE pickup= ? ;",			
                                        ('%{}%'.format(sr),'{}'.format(sr),) )         
        result=cursor.fetchall()
        ls=[]
        for row in result:
            ls.append(row)
        print(len(ls))
        l=len(ls) 
        i=0
        m=0        
        con=0
        if l<=5:
            for row in ls:
                print(row)                  
        else:
            while(l>5):
                m+=5
                for row in range(i,m):
                    print (ls[row])	   
                l-=5
                i+=5
                if l>5:
                    se=str(input("see more?"))
                    while more(se,connection,cursor) is False:
                        se=str(input("see more?"))
                    if (se!="y" and se!="Y"):
                        break 
                elif l<=5 and l>0:    
                    se=str(input("see more?"))
                    while more(se,connection,cursor) is False:
                        se=str(input("see more?"))
                    if (se=="y" or se=="Y"):
                        for row in range(m,len(ls)):
                            print(ls[row])
                        break
                else:
                    break
    while 1:
        try:
            choice=input("Select a ride")
            if choice.isdigit() :
                break
        except:
            print("Invalid input")
    cursor.execute("select email from requests where rid=?;", (choice,)) 
    while(cursor.fetchone() == None):
        while 1:
            try:
                choice=input("Select a ride")
                if choice.isdigit() :
                    break
            except:
                print("Invalid input")
        cursor.execute("select email from requests where rid=?;", (choice,)) 
    cursor.execute("select email from requests where rid=?;", (choice,))     
    result=cursor.fetchall()
    name=result[0][0]
    
    content=str(input("Enter your message content"))
    time=str(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))
    seen='n'
    cursor.execute("INSERT INTO inbox VALUES(:email,:msgTimestamp,:sender,:content,:rno,:seen)",{"email":name,"msgTimestamp":time,"sender":email,"content":content,"rno":choice,"seen":seen})
       
    connection.commit()

def more(enter,connection,cursor):
    if enter=='Y' or enter== 'y' or enter=='N' or enter== 'n':
        return True    
    else:
        return False   
    connection.commit()