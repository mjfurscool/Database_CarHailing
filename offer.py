import	sqlite3	
import re
from datetime import datetime
global connection, cursor

def offer(email,connection, cursor):

    while 1:
        try:
            date = str(input("Provide a date yyyy-mm-dd"))
            if check_valid("date", date) == True :
                break
        except:
            print("Invalid date")

    number=input(" Provide the number of seats")
    while(number.isdigit() is False):
        number=input("Error.Provide the number per seat")   
    price=input("Provide the price per seat")
    while(price.isdigit() is False):
        price=input("Error.Provide the price per seat")
    luggage=str(input("Provide a luggage description"))
    source=str(input("Provide  a source location"))
    
    while (check(source,connection,cursor) is False):
        print("Invalid keyword")
        cursor.execute("SELECT * FROM locations WHERE city like ? union SELECT * FROM locations WHERE prov like ? union SELECT * FROM locations WHERE address like ?;",			
	 				('%{}%'.format(source),'%{}%'.format(source),'%{}%'.format(source),) )  
        result=cursor.fetchall()
        ls=[]
        for row in result:
            ls.append(row)
        l=len(ls) 
        i=0
        m=0        
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
                if (se!="y" and se!="Y"):
                    break   
            if se=='y' or se== 'Y' and l>0:
                se=str(input("see more?")) 
                if (se=="y" or se=="Y"):
                    for row in range(m,len(ls)):
                        print(ls[row])          
            
        source=str(input("Provide  a source location"))
        
    dest=str(input("Provide a destination location"))
    
    while (check(dest,connection,cursor) is False):
        print("Invalid keyword")
        cursor.execute("SELECT * FROM locations WHERE city like ? union SELECT * FROM locations WHERE prov like ? union SELECT * FROM locations WHERE address like ?;",			
	 				('%{}%'.format(dest),'%{}%'.format(dest),'%{}%'.format(dest),) )        
        result=cursor.fetchall()
        ls=[]
        for row in result:
            ls.append(row)
        l=len(ls) 
        i=0
        m=0        
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
                       
        dest=str(input("Provide  a destination location"))    
        
    cursor.execute("select max(rno) from rides;")
    res=cursor.fetchall()    
    r=[] 
    for i in res:  
        r.append(i[0])   
    rno=r[0]+1
    ask=input("Enter cno?")
    while (ask!= 'Y' and ask!= 'y' and ask!= 'N' and ask!= 'n'):
        ask=input("Enter cno?")
    if ask== 'Y' or ask== 'y':
        cn=input("Enter a cno")
        while(cn.isdigit() is False):
            cn=input("Error.Provide the cno")      
        while (car(cn,email,connection,cursor) is False):
            print("It's not your car")
            cn=input("Enter a cno")      
        cursor.execute("INSERT INTO rides VALUES(:rno,:price,:rdate,:seats,:lugDesc,:src,:dst,:driver,:cno)",{"rno":rno,"price":price,"rdate":date,"seats":number, "lugDesc":luggage, "src":source, "dst":dest, "driver":email, "cno":cn})
    else:
        cursor.execute("INSERT INTO rides (rno,price,rdate,seats,lugDesc,src,dst,driver) VALUES(:rno,:price,:rdate,:seats,:lugDesc,:src,:dst,:driver)",{"rno":rno,"price":price,"rdate":date,"seats":number, "lugDesc":luggage, "src":source, "dst":dest, "driver":email})    
    en=input("Enter enroute?")
    while(more(en,connection,cursor)is False):
        en=input("Enter enroute?")
    while( en=='Y' or en=='y'):
        code=str(input("Enter a lcode"))
        while (check (code,connection,cursor)is False):
            code=str(input("Wrong lcode. Enter a lcode again"))
        cursor.execute("INSERT INTO enroute VALUES(:rno,:lcode)",{"rno":rno,"lcode":code}) 
        en=input("Enter more?")
        while(more(en,connection,cursor)is False):
            en=input("Enter more?")  
    connection.commit()
    
    return

def check (location,connection,cursor):
    
    cursor.execute("SELECT * FROM locations" )	
     
    result=cursor.fetchall()
     
    locats=[]
     
    for i in result:
        
        locats.append(i[0])	
	    
    if location in locats:
	    
        return True
       
    else: 
	    
        return False
     
    connection.commit()    
    return
def car(cn,email,connection,cursor):
    
    cursor.execute("SELECT cno FROM cars where owner=:cowner",{"cowner": email})	
    
    result=cursor.fetchall()
     
    car=[]
    carn=int(cn) 
    
    for i in result:
        
        car.append(int(i[0]))	

    if carn in car:
	
        return True
       
    else: 
	    
        return False
     
    connection.commit()        
    return
def more(enter,connection,cursor):
    if enter=='Y' or enter== 'y' or enter=='N' or enter== 'n':
        return True    
    else:
        return False   
    
def check_valid(type, value, cursor = None):


    if type == "date":
        y, m , d = value.split("-")
        if datetime(int(y), int(m), int(d)) > datetime.today():
            print("valid date")
            return True
        else:
            print("invalid date")
            return False