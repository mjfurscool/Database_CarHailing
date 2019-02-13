import sqlite3	
import re
from datetime import datetime
global connection, cursor

def search(email,connection, cursor):
    key=str(input("Enter 1-3 location keywords"))
    lst = key.split(" ")
    while len(lst)>3:
        key=str(input("Enter 1-3 location keywords"))
        lst = key.split(" ")
    l=len(lst)
    i = 0
    k=0
    ls=[]
    ck=[]
    lis=[]
    fin=[]
    cursor.execute("select lcode from locations")
    result = cursor.fetchall()
    ck.append(result)
    for i in lst:
        k=0
        for l in ck[0]:
            if l[0]==i:
                k=1

        if k==1:

            cursor.execute(" select rides.rno from rides,enroute where enroute.rno=rides.rno and (lcode like ?) union select rno from rides where (src like ? or dst like ? ); ",
                           ('%{}%'.format(i), '%{}%'.format(i), '%{}%'.format(i),))
            result = cursor.fetchall()
            if result == []:
                ls.append([])
            else:
                ls.append(result)

        else:

            cursor.execute(" select rides.rno from rides,locations where (src=lcode or dst=lcode) and (city like ? or prov like ? "
                           "or address like ? )union select rno from locations l, enroute e where e.lcode=l.lcode "
                           "and (city like ? or prov like ? or address like ?) ;",
                           ('%{}%'.format(i),'%{}%'.format(i),'%{}%'.format(i),'%{}%'.format(i),'%{}%'.format(i),'%{}%'.format(i),))
            result=cursor.fetchall()
            if result==[]:
                ls.append([])
            else:
                ls.append(result)

    if len(ls)==1:
        lis=ls[0]
    elif len(ls)==2:
        lis=list(set(ls[0])&set(ls[1]))
    elif len(ls)==3:
        lis=list(set(ls[0])&set(ls[1])& set(ls[2]))
    for i in lis:
        cursor.execute(" select rides.*,make,model,year,owner from rides left outer join cars on cars.cno=rides.cno where rno= ?;",			
                                            ('{}'.format(i[0]), ))        
        result=cursor.fetchall()
        fin.append(result)


    i=0
    m=0
    l=len(fin)
    if l<=5:
        for row in fin:
            print(row)        
                
    else:
        while(l>5):
                m+=5
                for row in range(i,m):
                    print (fin[row])	   
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
                        for row in range(m,len(fin)):
                            print(fin[row])
                        break
                else:
                    break   
                    
    again=str(input("search again?"))
    while more(again,connection,cursor) is False:
        again=str(input("search again?"))    
    if again=='y' or again=='Y':
        search(email,connection, cursor)
    else:
        select(email,connection, cursor) 
    connection.commit()	
def select(email,connection, cursor):

    choice=input("Select a ride")
    while( choice.isdigit() is False) :
        choice=input("Select a ride")
    cursor.execute("select driver from rides where rno=?;", (choice,))
    result=cursor.fetchall()
    name=result[0][0]
    content=str(input("Enter a message content"))
    #time=str(datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))
    time=datetime.now()
    seen='n'
    cursor.execute("INSERT INTO inbox VALUES(:email,:msgTimestamp,:sender,:content,:rno,:seen)",{"email":name,"msgTimestamp":time,"sender":email,"content":content,"rno":choice,"seen":seen})
    connection.commit()	
    print("Message sent!")
def more(enter,connection,cursor):
    if enter=='Y' or enter== 'y' or enter=='N' or enter== 'n':
        return True    
    else:
        return False   
    
    connection.commit()	