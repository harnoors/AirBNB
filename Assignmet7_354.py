#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


# importing module
import pyodbc

#connection creation
connection = pyodbc.connect('driver={SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes;')
cur = connection.cursor()

cont=1
while cont==1 :
    print("Home:\n")
    print("What would you like to do in this session?")
    print("\t 1.Search a Listing ")
    print("\t 2.Book a Listing (Only if you know the listing ID)  ")
    print("\t 3.Write a Review ")
    print("\t ENTER YOUR CHOICE (1 , 2 or 3) ")
    a=int (input())
    
    while(a!=1 and a!=2 and a!=3):
        print("INVALID CHOICE !")
        print("\t ENTER YOUR CHOICE (1 , 2 or 3) ")
        a=int (input())
    
    while (a==1 or a==2 or a==3 or a==4):

        if a==1:
            print("Input the filters of your search:\n")
            print("\t1.Start Date And End Date\n")
            print("\t2.Start And End Date + Minimum And Maximum Price.\n")
            print("\t3.Start And End Date + number of bedrooms.\n")
            print("\t4.Start And End Date + number of bedrooms +  Minimum And Maximum Price.\n")
            print("\tplease enter your choice from 1 , 2 , 3 or 4")
            searchCriteria=int(input())
            
            #start and end date
            if(searchCriteria==1):
                StartDate=input("Enter the start date in the format (YYYY-MM-DD) : \n")
                EndDate=input("Enter the end date in the format (YYYY-MM-DD) : \n")
                SQL_Command=("SELECT DISTINCT id,name,number_of_bedrooms,SUBSTRING(description,1,25),MAX(price) FROM Listings,Calendar WHERE id=listing_id AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ?  AND date <= ?) AND (available = 0)) GROUP BY id,name,SUBSTRING(description,1,25),number_of_bedrooms")
                cur.execute(SQL_Command,StartDate,EndDate,StartDate,EndDate)
                
            #START AND END DATE+PRICE
            elif(searchCriteria==2):
                StartDate=input("Enter the start date in the format (YYYY-MM-DD) : \n")
                EndDate=input("Enter the end date in the format (YYYY-MM-DD) : \n")
                mini=int(input("Enter the minimum price : \n"))
                maxi=int(input("Enter the maximum price : \n"))
                SQL_Command=("SELECT DISTINCT id,name,number_of_bedrooms,SUBSTRING(description,1,25),MAX(price) FROM Listings,Calendar WHERE id=listing_id AND (date >= ? AND date <= ? )AND (price >= ? AND price <= ?) AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND (price >= ? AND price <= ? AND available = 0)) GROUP BY id,name,SUBSTRING(description,1,25),number_of_bedrooms")
                cur.execute(SQL_Command,StartDate,EndDate,mini,maxi,StartDate,EndDate,mini,maxi);
               
                
            #START AND END DATE+bedrooms
            elif(searchCriteria==3):
                StartDate=input("Enter the start date in the format (YYYY-MM-DD) : \n")
                EndDate=input("Enter the end date in the format (YYYY-MM-DD) : \n")
                Count=int(input("Enter the number of bedrooms : \n"))
                SQL_Command="SELECT DISTINCT id,name,number_of_bedrooms,LEFT(description,25),MAX(price) FROM Listings,Calendar WHERE number_of_bedrooms= ? AND id=listing_id AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND available = 0) GROUP BY id,name,LEFT(description,25),number_of_bedrooms"
                cur.execute(SQL_Command,Count,StartDate,EndDate,StartDate,EndDate);
                
            #START AND END DATE+PRICE+BEDROOMS
            elif (searchCriteria==4):
                StartDate = input('Enter a Startdate in YYYY-MM-DD format:\n')
                EndDate = input('Enter a Enddate in YYYY-MM-DD format:\n')
                mini= int(input('Please enter minimum price\n'))
                maxi= int(input('Please enter maximum price\n'))
                Count= int(input("Please Enter Number of Bedrooms:\n"))
                SQL_Command="SELECT DISTINCT id,name,number_of_bedrooms,LEFT(description,25),MAX(price) FROM Listings,Calendar WHERE number_of_bedrooms= ? AND price >= ? AND price <= ? and id=listing_id AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND (price >= ? AND price <= ? AND available = 0)) GROUP BY id,name,LEFT(description,25),number_of_bedrooms"
                cur.execute(SQL_Command,Count,mini,maxi,StartDate,EndDate,StartDate,EndDate,mini,maxi)

            results = cur.fetchall()
            print("\nSearch result are : \n")
            if len(results) == 0:
                print("\n ERROR! \n\t NO DATA FOUND.\n")
            else:
                print("\nSearch result is : \n")
                for i in results:  
                    print ("Listings ID        :" ,  i[0]) 
                    print ("Name               : " , i[1])
                    print ("Number of bedrooms : " , i[2]) 
                    print ("Discription        : " , i[3])
                    print ("Price              : " , i[4]) 
                    print("\n") 
            
            print("Enter 1 to Search again, 2 to book a listing or 0 to go to home.\n")
            a=int(input())
            
               
        #book listing
        if a==2:
            #input-lid,name,stayfrom and stay to
            
            Lid=int(input("Enter the listing ID"))
            name=input("please enter your name.")
            Noguests=int(input("Enter the number of Guests."))
            
            #genrating BID
            SQL=("SELECT MAX(id),COUNT(id) FROM Bookings")
            cur.execute(SQL)
            results=cur.fetchall()
            if results[0][1]==0:
                    Bid=1
            elif results[0][1]==1:
                    Bid=2
            else:
                Bid= int(results[0][0])+1
                             
            #SQL to insert inputed data
            SQL = ("INSERT INTO Bookings(id,listing_id,guest_name,stay_from,stay_to,number_of_guests) VALUES (?,?,?,?,?,?)")  
            Values = [Bid,Lid,name,StartDate,EndDate,Noguests] 
            cur.execute(SQL,Values)
            
            print("Thank you for your reservation.\n Your Booking ID is : ",Bid)
            connection.commit()
            print("\n\nEnter 2 to Book another listing or 0 to go to home.\n")
            a=int(input())
            
            
        #write review
        if a==3:
            name=input("please enter your name : ")
            SQL=(" SELECT * FROM Bookings WHERE guest_name=? ")
            cur.execute(SQL,name)
            results=cur.fetchall()
            if len(results)==0:
                print("Error!\n\tNo Data Found with this name.\nEnter 3 try again or 0 to exit to home")
                a=int(input())
            else:
                itr=1
                print("\n\n")
                for i in results:
                    print("Booking - ",itr)
                    print ("Booking ID         :" ,i[0])  
                    print ("Listing ID         : " ,i[1])  
                    print ("Guest name         : " ,i[2]) 
                    print ("Stay from          : " ,i[3])
                    print ("Stay to            : " ,i[4]) 
                    print("\n")
                    itr=itr+1 
                Bid=int(input("For which Booking would you like to submit a review ? (please enter the booking Id from above list) "))
                Lid=int(input("please enter the Listing id Id from above list:"))
                comment=input('Enter your review')

                #genrating Review id
                SQL=("SELECT MAX(id),COUNT(id) FROM Reviews")
                cur.execute(SQL)
                
                results=cur.fetchall()
                if results[0][1]==0:
                    Rid=1
                elif results[0][1]==1:
                    Rid=2
                else:
                    Rid= int(results[0][0])+1

                #if date>stayTo:
                SQL=("INSERT INTO Reviews (id,listing_id,comments,guest_name) VALUES (?,?,?,?);")
                Values = [Rid,int(Lid),comment,name] 
                cur.execute(SQL,Values)
            connection.commit()
            print("Enter 3 to add another review or 0 to go to home")
            a=int(input())
                         
   

    print("Enter 1 to continue or 0 to end you session.")
    cont=int(input())
connection.commit()
connection.close()


# ### 

# In[ ]:




