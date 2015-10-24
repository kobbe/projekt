#!/usr/bin/python -u
# -*- coding:utf-8 -*-

"""
Dokumentation:

Copyright Hans Koberg 920130, you can ask me for help!
    -Send an sms or email hans@koberg.nu

Special keywords    :
    exit program    :   exit or 0/0 or 1337/1337
    adminpanel      :   admin or 012345
    show statistics :   stats or 98765
    Interesting data:   datamining or 0258
    pressing enter  :   F10 or enter or KP_enter (small enter)
    sell things     :   "" or OK 
    
Notes:
    It is really important that the scanner does NOT press OK on error messages
    since users maybe wont see the error message if it is "scanned closed" by
    scanning another product. 
    To minimize this risk, the barcode scanner SHOULD end with F10 insted of
    ENTER. Enter will still work but if F10 is used by the skanner there
    is no way the scanner can acutally close error messages.

Reserved Barcodes: (need to add it manually as product)
    1337133713378: Inventering 
    6666666666666: Bankningar

On what is is built?
    -Python 2.7
    -Built on the built in standard Tkinter and ttk library.
    -Built with functions since they dont need "self" argument..

How to modify?
    -There are a bunch of global variables that can be changed, look there.
    -Otherwise just modify the source code

How is the database implemented?:
    -The database is sqlite3 which have to be installed seperately
    -The database is created automatically as:

    /*For each product, category is arbitrarily used*/
    CREATE TABLE products(
    barcode integer UNIQUE PRIMARY KEY,
    price integer NOT NULL,
    name TEXT,
    category TEXT
    );
    
    /*For each transaction/sale of a product*/
    CREATE TABLE transactions(
    id integer UNIQUE PRIMARY KEY AUTOINCREMENT,
    barcode integer REFERENCES products(barcode) NOT NULL,
    timestamp DATE DEFAULT (datetime('now','localtime')),
    price integer NOT NULL
    );

    /*This is a secret copy of all removed sales used
      in order to detect if someone removes sales*/
    CREATE TABLE transactionChanges(
    removedId integer PRIMARY KEY,
    removedBarcode integer,
    removedTimestamp DATE,
    removedPrice integer,
    timestamp DATE DEFAULT (datetime('now','localtime'))
    );

    /*This is when when we search for the exsistence of a sold product so
      we dont delete its product data.*/
    CREATE INDEX index_transactions_barcode on transactions (barcode);

    
    -Note that transactions references products, this is mabye not a nessesary condition to have.
    -Further comments:
        -con.commit() have to be used after modification of the database or nothing changes.
    
Backups:
    -There is probably a cron job making a copy to a remove server (Rasmus)
    -There should (!!!!) be a cron job that copies to the second hard drive
    -There can be a RAID system
    -There should probably be some more backups done regularly!

    
How to reset database after a year of sales:
    -Backup the database before!
    -Just delete the old one, a new is created automatically!
    
    
TODO:
    -(5/5) Tell everyone there is an physical help document 
    -(5/5) Transactions in sell stack are lost during a crash
    -(5/5) Fix an backup computer which can be used in case computer crashes completely
    -(5/5) Implement own popup error or modify existing one to remove BUGS 
    -(5/5) Add an "OK" barcode that can be used instead of regular enter.
           Make sure that you can not press ok on error messages!
    
    -(4/5) Log error handling messages to see if users ever encounter them and why
           You can have some indication (like a small text) on screen when this
           log is not empty
    -(4/5) Do the ground work for "kontantfaktura" if people use their
           access card to identify themself, possibly getting a discount.
           Table with info about them and how much they bougth for.
    -(4/5) Indicate if numlock is on or off, keypad does not work otherwise
           users dont detect this themself!
    -(4/5) Scanner presses OK on errors, it should not be able to!
    -(4/5) Add options as file -> easier to work on different computers etc
    -(4/5) Make sure all global options work propperly and maybe add more?

    -(3/5) Add barcode meny that can be access with scanner in order to
           list barcodes that are on the counter. code for exit and enter.
           Maybe dont cover the sell stack but everything else?
           Automatic exit after a while?
    -(3/5) Datamining with the ability to sort per product       
    -(3/5) Automatic enter after a while?
    
    -(2/5) Add help meny?
    -(2/5) Log all wrong barcodes and see what the problem usually is
    -(2/5) use WM_DELETE_WINDOW if a window is closed improperly to catch it
    -(2/5) Do we need to reset control to an old window (datamining) after plots?
    -(2/5) Admin page (and all input fields) can give feedback if barcode already used or values illegal.
    -(2/5) Make STACKTABLEHEIGHT changable
    
    -(1/5) Week in dataming could be wednesday to wednesday insted.
    -(1/5) Timepoint changed a product
    -(1/5) Log uptime to see how often computer is restarted/crashed
    -(1/5) Be able to change a barcode
    -(1/5) If barcode scanner can read on screen: Add page for all unusual barcodes
    
    

BUGS:
    -Users can resize GUI tables (treeview). It is restored on every clock tick.
    -There is a maximum of STACKTABLEHEIGHT products (size of stackTable) to be sold at the same time.
        This is because the remove buttons would be wierd if a scrollbox was introduced.
    -On UNIX small enter is not the same enter as big enter and can not close error boxes.
        A manual remapping in UNIX is required

        
Error handling:
    -When an error occurs, a popup is displayed. 
    -This is the only error indication, this handles both python and sql errors.
    -This does not handle error that occur before the mainloop is ran.

    
Possibilites:
    -The possibilites are endless but some features:
    -Full system. i.e inserting what we now do in google docs.
    -Insert amount of products when we buy them.
    -Insert price of bought items.
    -insert exactely what we inventerar
    -finally compute how much that have gone missing.
    -Could even insert kvitton and how much we have at the bank.
    -Online backup would be great. Do some "maintnance" like once a week at night where 
     no one can buy something where the database are uploaded online. need to close db first.
    -ultemately, if it could do image analysis of scanned receipt from axfood and load it automatically would be nice!
    
TODO at install:
    --Create databases (transactions,products,transactionchanges)
    --change explicit location of database
    --install tk?
    --computer needs automatic time update to ensure correct timestamps.
    -disable screensaver and power saving
    -Modifying the global variables so the program fits the screen
    -Auto mount usb for easier export of things.
    -Add autologin and automatic startup
    

Changelog:
    2014-03-02: Started the changelog to remember what was changed if something goes wrong sometime.
    2014-03-02: Selectmode="browse" in admin tables
    2014-03-02: Width of admin panel name increasted to 150
    2014-03-02: Added adminUpdateCopy button
    2014-03-02: added copySelected
    2014-03-04: Uploaded changes
    2014-03-17: getTransactionsBetweenIds choose strict ids, changed to inclusive
    2014-03-17: root.bind_all("<Button-1>",takeFocus) uses takeFocus insted of takeFocus2
    2014-03-17: function enter() changed to enter(*args)
    2014-04-08: Implemented export all products on stats page
    2014-04-08: Uploaded changes
    2014-05-13: Updated todo at install
    2014-09-30: Changed the manual a bit
    2014-11-28: Changed db setup to work properly with index.
    2014-11-29: Commented out a lot of disable() and enable() that was unnesessary
    2014-11-29: Fixed a bunch of small problems
    2014-12-03: fixed flashing backgrond on some error messages
    2014-12-03: Pushed new version
    2014-12-03: Reenabled disable() since it was needed on linux and pushed changes
    2014-12-05: Removed some unessecary code and added ESC key in admin and stats
    2014-12-11: Uploaded changes and removed disable() and enable()
    2015-02-26: Added a few fields to "stats" and make some sqlGets easier
    2015-02-07: Added sorting to product table
    2015-02-08: Added dataMining page
    2015-02-08: Uploaded changes
    2015-03-14: Added own plotter and can now plot last day,week,month, year etc.
    2015-03-14: uploaded changes
    2015-03-15: Fixed documentant to be nice

    
Old comments laying around..
    How is normal popup defined? How to keep focus at it? w.lift(aboveThis=None)?

    rebind the numpad enter to normal enter. -> xmodmap
    xmodmap have to be run every time keyboard is inserted into machine..
    run retcode = subprocess.call(["xmodmap", ".xmodmap"])

    #A bunch of implementational notes, not interesting to read:

    <toplevel>.wm_attributes("-topmost", 1)   # Make sure window remains on
    top of all others
    <toplevel>.focus() 

"""


from Tkinter import *
import tkSimpleDialog
import tkFileDialog
import tkMessageBox
import ttk
import math

import datetime
import sqlite3 as lite
import traceback #For traceback error

PATH = "/home/moebius/kassa/kassa.db" #Path to the database file
#PATH = "kassa.db"
BARLEN = [13,8]         #Allowed Barcode lengths, 13 and 8 is standard in EU.
BORDERPAD = 25          #To change the outer border padding
ADMINBORDERPAD = 15     #To change the outer border in admin panel (and padding)
STATSBORDERPAD = 15     #To change the outer border in stats panel (and padding)
DATAPAD = 15            #Sets the padding in dataMining
DRAWPAD = 15            #Sets the padding in plot window
STACK = []              #Sell stack
PRICE = 0               #Total Sell price
DATA = []               #What is on last transaction table
STACKTABLEHEIGHT = 13   #number of items that is the stack..NOT IMPLEMENTED enought to change it from 13..
TRANSNUMBER = 30        #Number of transaction to show in table
ADMINTRANSNUMBER = 15   #Number of transaction height in admin panel
CLOCKSIZE = 70          #Font size of clock
CONT = True #If flashing background should stop, DO NOT CHANGE!

#Gradient animation colours in colouring the last sold items.
GRADIENT = ["#FF9900","#FF9C07","#FF9F0F","#FFA217","#FFA51F","#FFA827",
"#FFAC2F","#FFAF37","#FFB23F","#FFB547","#FFB84F","#FFBC57","#FFBF5F",
"#FFC267","#FFC56F","#FFC877","#FFCC7F","#FFCF87","#FFD28F","#FFD597",
"#FFD89F","#FFDBA7","#FFDFAF","#FFE2B7","#FFE5BF","#FFE8C7",
"#FFEBCF","#FFEFD7","#FFF2DF","#FFF5E7","#FFF8EF","#FFFBF7","#FFFFFF"]
ORIGCOLOR = None; #saves the original color of the background.

def enable():
    root.bind("<Button-1>",takeFocus)
    root.bind("<Return>",addToStack)
    root.bind("<KP_Enter>",addToStack)
    root.bind('<F10>',addToStack)
    root.bind("<Delete>",removeLast)

#Defines the error messages popups
def show_error(*args):
    a = traceback.format_exception(*args)
    tkMessageBox.showerror("Python/sql fel, kontakta Tech!", "\nKontakta Tech!\n\n" + "\n".join(a))

#All modifikations to database bellow ----------------
def insertTransactionNoCommit(cur,con,barcode,price):
    cur.execute('insert into transactions(barcode,price) values(?,?)',(str(barcode), str(price)))
    
def insertProduct(cur,con,barcode,price,name,category):
    cur.execute('insert into products(barcode,price,name,category) values(?,?,?,?)', (barcode,price,name,category))
    con.commit()
    
def updateProduct(cur,con,barcode,price,name,category):
    cur.execute('update products set price=?,name=?,category=? where barcode=?', (price,name,category,barcode))
    con.commit()
    
def deleteTransactionById(cur,con,transId):
    data = getTransactionById(cur,transId)
    (removedId,name,removedTimestamp,removedPrice,removedBarcode) = data[0]
    cur.execute('insert into transactionChanges(removedId,removedBarcode,removedTimestamp,removedPrice) values (?,?,?,?)',
        (removedId,removedBarcode,removedTimestamp,removedPrice))
    cur.execute('delete from transactions where id=?',(transId,))
    con.commit()
    
def delteProducyByBarcode(cur,con,barcode):
    cur.execute('delete from products where barcode=?', (barcode,))
    con.commit()
    
def CreateTransactionsTable(cur,con):
    cur.execute("""
    /*For each transaction/sale of a product*/
    CREATE TABLE transactions(
    id integer UNIQUE PRIMARY KEY AUTOINCREMENT,
    barcode integer REFERENCES products(barcode) NOT NULL,
    timestamp DATE DEFAULT (datetime('now','localtime')),
    price integer NOT NULL
    ); 
    """)
    con.commit()
    
def CreateProductsTable(cur,con):
    cur.execute("""
    /*For each product, category is arbitrarily used*/
    CREATE TABLE products(
    barcode integer UNIQUE PRIMARY KEY,
    price integer NOT NULL,
    name TEXT,
    category TEXT
    );
    """)
    con.commit()
    
def CreateTransactionChangesTable(cur,con):
    cur.execute("""
    /*This is a secret copy of all removed sales used
      in order to detect if someone removes sales*/
    CREATE TABLE transactionChanges(
    removedId integer PRIMARY KEY,
    removedBarcode integer,
    removedTimestamp DATE,
    removedPrice integer,
    timestamp DATE DEFAULT (datetime('now','localtime'))
    );
    """)
    con.commit()
    
#All gets to database here -----------------
def getTableWithName(cur,name):
    cur.execute('SELECT name FROM sqlite_master WHERE type=\'table\' AND name=?;',(name,))
    data = cur.fetchall()
    return data

def getLast(cur,number):
    cur.execute('select id,name,timestamp,transactions.price,transactions.barcode from transactions,products\
                where transactions.barcode=products.barcode order by id desc limit ?',(number,))
    data = cur.fetchall()
    return data

def getTransactionById(cur,transId):
    cur.execute('select id,name,timestamp,transactions.price,transactions.barcode from transactions,products\
                where id=? and transactions.barcode=products.barcode',(transId,))
    data = cur.fetchall()
    return data

def getProductByBarcode(cur,barcode):
    cur.execute('select barcode,price,name,category from products where barcode=?',(barcode,))
    data = cur.fetchall()
    return data

def getPriceAndName(cur,barcode):
    barcode = str(barcode)
    cur.execute('select price,name from products where barcode= ? ', (barcode,))
    data = cur.fetchall()
    if len(data) == 0:
        return (-1,"Produkt med streckkod: " + barcode + " existerar inte")
    if len(data) == 1:
        (price,name) = data[0]
        return (price,name)
    else:
        return (-1,"Omöjligt! Två produkter med samma streckkod")

#Fetching is done in function row by row, fetchall is to dangerous.
def getTransactionsBetweenIds(cur,fromId,toId):
    cur.execute('select id,name,timestamp,transactions.price,transactions.barcode from transactions,products\
                where id>=? and id <=? and transactions.barcode=products.barcode order by id',(fromId,toId))

#Fetching is done in function row by row, fetchall is to dangerous.
def getTransactionsBetweenIdsByCategory(cur,fromId,toId):
    cur.execute('select category,count(*),sum(transactions.price) from transactions,products where\
                id>=? and id <=? and transactions.barcode=products.barcode group by category',(fromId,toId))
    
#Fetching is done in function row by row, fetchall is to dangerous.
def getTransactionsBetweenIdsByProducts(cur,fromId,toId):
    cur.execute('select name,transactions.barcode,count(transactions.barcode),sum(transactions.price)\
                from transactions,products where id>=? and id <=? and transactions.barcode=products.barcode\
                group by transactions.barcode',(fromId,toId))
    
def getSumBeweenIds(cur,fromId,toId):
    cur.execute('select sum(price) from transactions where id>=? and id<=?',(fromId,toId))
    data = cur.fetchall()
    (sum,) = data[0]
    if sum == None:
        sum = "0"
    return str(sum)
    
def getInventeringar(cur):
    cur.execute('select id,timestamp from transactions where barcode = 1337133713378 order by id desc')
    data = cur.fetchall()
    return data
    
def getBankningar(cur):
    cur.execute('select id,timestamp from transactions where barcode = 6666666666666 order by id desc')
    data = cur.fetchall()
    return data

def getCategories():
    cur.execute('select distinct category from products')
    data = cur.fetchall()
    return data
    
def getIdsByBarcode(cur,barcode):
    cur.execute('select id from transactions where barcode=? limit 10', (barcode,))
    data = cur.fetchall()
    return data
    
def getTransactionsByBarcode(cur,barcode,number):
    cur.execute('select id,price,timestamp from transactions\
    where barcode=? order by id desc limit ? ', (barcode,number))
    data = cur.fetchall()
    return data

def getAllProducts():
    cur.execute('select barcode,price,name,category from products')
    data = cur.fetchall()
    return data
    
def getNumberOfProducts(cur):
    cur.execute('select count(*) from products')
    data = cur.fetchall()
    (num,) = data[0]
    if num == None:
        num = "ERROR"
    return str(num)  
    
def getMeanSalePrice(cur):
    cur.execute('select avg(price) from transactions')
    data = cur.fetchall()
    (avg,) = data[0]
    if avg == None:
        avg = "ERROR"
    return str(avg)
    
def getMedianSalePrice(cur): #MIGHT BE EXPENSIVE!!
    cur.execute('SELECT AVG(price) FROM \
    (SELECT price FROM transactions ORDER BY price \
    LIMIT 2 - (SELECT COUNT(*) FROM transactions) % 2\
    OFFSET (SELECT (COUNT(*) - 1) / 2 FROM transactions))')
    data = cur.fetchall()
    (median,) = data[0]
    if median == None:
        median = "ERROR"
    return str(median)
    
def getNumberOfTransactions(cur):
    cur.execute('select count(*) from transactions')
    data = cur.fetchall()
    (num,) = data[0]
    if num == None:
        num = "ERROR"
    return str(num)    

def getCategoryStats(cur):
    cur.execute('select category,count(t.price),ifnull(sum(t.price),0),count(distinct p.barcode),ifnull(avg(t.price),0)\
                from products as p left outer join transactions as t \
                on t.barcode=p.barcode group by category')
    data = cur.fetchall()
    return data
    
def getTransactionsGroupedByBarcode(cur):
    cur.execute('select p.name,p.barcode,count(t.barcode),sum(t.price),p.price from transactions as t,products as p where\
                t.barcode=p.barcode group by p.barcode')
    data = cur.fetchall()
    return data
    
def getTransactionsChunks(cur):
    cur.execute('select count(*) from (select count(timestamp) from transactions group by timestamp)')
    data = cur.fetchall()
    (num,) = data[0]
    if num == None:
        num = "ERROR"
    return str(num) 
    
def getMeanChunkSize(cur):
    cur.execute('select avg(t) from (select count(timestamp) as t from transactions group by timestamp)')
    data = cur.fetchall()
    (num,) = data[0]
    if num == None:
        num = "ERROR"
    return str(num) 
     
def getTransactionsByDate(timeFrom,timeTo,cur):
    cur.execute('select sum(price),timestamp from transactions where timestamp between ? and ? group by timestamp',(timeFrom,timeTo))
    data = cur.fetchall()
    return data

#To update the information in root window
def rootUpdate():
    global DATA
    DATA = getLast(cur,TRANSNUMBER)
    for i,val in enumerate(transactionTableIds):
        #start with last row.
        if len(DATA) >  i:
            transactionTable.set(val,column="id",value=DATA[i][0])
            transactionTable.set(val,column="name",value=DATA[i][1])
            transactionTable.set(val,column="price",value=DATA[i][3])
            transactionTable.set(val,column="time",value=DATA[i][2])
        else:
            transactionTable.set(val,column="id",value="")
            transactionTable.set(val,column="name",value="")
            transactionTable.set(val,column="price",value="")
            transactionTable.set(val,column="time",value="")
    takeFocus()

#Animation when added to sold items.
def gradient(rows,index):
    if index >= len(GRADIENT):
        pass
    else:
        for i in rows:
            transactionTable.tag_configure(i,background=GRADIENT[index])
        root.after(70,lambda:gradient(rows,index+1))


def takeFocus(*args):
    streckkodEntry.focus_set()
    
def removeLast(*args):
    if len(STACK) == 0:
        pass
    else:
        removeFromStack(len(STACK)-1)

    #Sorting function for columns in a table. To use it, table needs the values lastCol
    #and lastReverse initialized as None.
def treeview_sort_column(tv, col, reverse, update):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    #Checks the type of the column, specidied manually in the name
    if col[0:2] == "I_":
        l.sort(reverse=reverse,key=lambda tup:int(tup[0]))
    elif col[0:2] == "F_":
        l.sort(reverse=reverse,key=lambda tup:float(tup[0]))
    else:
        l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
    if not update:
        # reverse sort next time
        tv.heading(col, command=lambda:treeview_sort_column(tv, col, not reverse,False))
        tv.lastCol = col
        tv.lastReverse = reverse
        
def makeLabelAndVar(owner,labelName,(column,row),font):
    dataBasicL = Label(owner,text=labelName, font=font)
    dataBasicL.grid(column=column,row=row,sticky=E)
    dataBasicVar = StringVar()
    dataBasicVar.set("")
    dataBasicValue = Label(owner,textvariable=dataBasicVar, font=font)
    dataBasicValue.grid(column=column+1,row=row)
    return (dataBasicL,dataBasicVar,dataBasicValue)
 
def makeLabelAndEntry(owner,labelName,(column,row),font,width):
    dataBasicL = Label(owner,text=labelName, font=font)
    dataBasicL.grid(column=column,row=row,sticky=E)
    dataBasicEntry = Entry(owner,width=width)
    dataBasicEntry.grid(column=column+1,row=row)
    return (dataBasicL,dataBasicEntry)
    
        
#The stats window
def stats():
    statsroot = Toplevel()
    statsroot.geometry("1024x900")
    statsroot.transient(root) #Does not seem to work in windows
    statsroot.grab_set() #Force all events to this window so it will be on top of the other one.
    #self.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def statsfullscreen():
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        #root.overrideredirect(1)
        statsroot.attributes('-fullscreen', True)
        statsroot.geometry("%dx%d+0+0" % (w, h))
        
    def statsUpdate():
        #update inventeringTable
        for i in statsInvTable.get_children():
            statsInvTable.delete(i)
        temp = getInventeringar(cur)
        for i in temp:
            statsInvTable.insert("",0,values=(i[0],i[1]))
            
        #update BakningTable
        for i in statsBankTable.get_children():
            statsBankTable.delete(i)
        temp = getBankningar(cur)
        for i in temp:
            statsBankTable.insert("",0,values=(i[0],i[1]))
            
        #Update last id
        data = getLast(cur,1)
        StatsLastId.set("Last ID: "+str(data[0][0]))
    
    def quitstats(*args):
        statsroot.destroy()
        
    def checkInput(fromId,toId):
        if not fromId.isdigit():
            tkMessageBox.showerror("Fel","Från id är ingen siffra",parent=statsroot)
            return False
        elif not toId.isdigit():
            tkMessageBox.showerror("Fel","Till id är ingen siffra",parent=statsroot)
            return False
        elif int(fromId) > int(toId):
            tkMessageBox.showerror("Fel","Till id är större än från id",parent=statsroot)
            return False
        else:
            return True
        
    def statsSum(*args):
        if checkInput(statsGenerateF.get(),statsGenerateT.get()):
            sum = getSumBeweenIds(cur,statsGenerateF.get(),statsGenerateT.get())
            statsSumVar.set(sum+" kr")
            
    def statsGenerateReport(type):
        fileToWrite = tkFileDialog.asksaveasfile(mode='w',defaultextension = ".csv",
            filetypes=[('comma seperated value', '.csv')],parent=statsroot )
        if fileToWrite:
            if type == "categories":
                getTransactionsBetweenIdsByCategory(cur,statsGenerateF.get(),statsGenerateT.get())
            elif type == "products":
                getTransactionsBetweenIdsByProducts(cur,statsGenerateF.get(),statsGenerateT.get())
            data = cur.fetchone()
            numberOfRecords = 0
            while data != None:
                numberOfRecords = numberOfRecords +1
                if type == "categories":
                    (category,count,sumPrice) = data
                    stringToWrite = category + ';' + str(count) + ';' + str(sumPrice) + '\n'
                    fileToWrite.write(stringToWrite.encode('utf8'))
                elif type == "products":
                    (name,barcode,count,sumPrice) = data
                    stringToWrite = name + ';' + str(barcode) + ';' + str(count) + ';' + str(sumPrice) + '\n'
                    fileToWrite.write(stringToWrite.encode('utf8'))
                data = cur.fetchone()
            tkMessageBox.showinfo("Lyckades"," Sparade " + str(numberOfRecords) +
                                  " transaktioner till: " + str(fileToWrite.name),parent=statsroot)
            fileToWrite.close()
        else:
            tkMessageBox.showerror("Fel","Inte en giltig fil, avbryter.",parent=statsroot)
    
    def statsExportProducts(*args):
        fileToWrite = tkFileDialog.asksaveasfile(mode='w',defaultextension = ".csv",
            filetypes=[('comma seperated value', '.csv')],parent=statsroot )
        if fileToWrite:
            allProducts = getAllProducts()
            for i in allProducts:
                (barcode,price,name,category) = i
                stringToWrite = str(barcode) + ';' + str(price) + ';' + name + ';' + category + '\n'
                fileToWrite.write(stringToWrite.encode('utf8'))
            tkMessageBox.showinfo("Lyckades"," Sparade " + str(len(allProducts)) +
                                  " produkter till: " + str(fileToWrite.name),parent=statsroot)
            fileToWrite.close()
        else:
            tkMessageBox.showerror("Fel","Inte en giltig fil, avbryter.",parent=statsroot)
    
    def statsGetTransById(*args):
        transId = statsGetTransEntry.get()
        if transId.isdigit():
            data = getTransactionById(cur,transId)
            if data != []:
                (id,name,timestamp,price,barcode) = data[0]
                statsIdVar.set(str(id))
                statsNameVar.set(str(name))
                statsTimeVar.set(str(timestamp))
                statsPriceVar.set(str(price))
                statsBarcodeVar.set(str(barcode))
                
            else:
                tkMessageBox.showerror("Fel","transaktion med id: " + transId + " finns inte",parent=statsroot)
                statsIdVar.set("")
                statsNameVar.set("")
                statsTimeVar.set("")
                statsPriceVar.set("")
                statsBarcodeVar.set("")
        else:
            tkMessageBox.showerror("Fel","id är ingen siffra",parent=statsroot)
        statsGetTransEntry.delete(0,END)
    
    def statsUpdateTransTable(*args):
        #Get the 100 last transactions by a barcode
        #Could be variable
        statsBarcode = statsGetTransTableEntry.get()
        statsGetTransTableEntry.delete(0,END)
        
        data = getTransactionsByBarcode(cur,statsBarcode,100)
        for i in statsGetTransTable.get_children():
            statsGetTransTable.delete(i)
        if data == []:
            tkMessageBox.showerror("Fel","Inga transaktioner funna med steeckkod: " +str(statsBarcode),parent=statsroot)
        else:
            for i in data:
                (id,price,time) = i
                statsGetTransTable.insert("",0,values=(i[0],i[2],i[1]))
            (price,name) = getPriceAndName(cur,int(statsBarcode))
            statsGetTransVar.set(name)
    
    #GUI here..
    statsroot.grid_rowconfigure(7,weight=1)
    statsroot.grid_columnconfigure(7,weight=1)
    
    #Table with inventeringar
    statsInvTableLF= LabelFrame(statsroot, text="Inventeringar")
    statsInvTableLF.grid(column=0,row=0,sticky=W,padx=(STATSBORDERPAD,0) ,pady=(STATSBORDERPAD,0))
    
    statsInvTableScroll = Scrollbar(statsInvTableLF)
    statsInvTableScroll.grid(column=1,row=0,sticky=N+S)
    
    statsInvTable = ttk.Treeview(statsInvTableLF,columns=("id","time"),height=8,yscrollcommand=statsInvTableScroll.set,selectmode="browse")
    statsInvTable['show'] = 'headings'
    statsInvTable.column("id",width=100,anchor="center")
    statsInvTable.column("time",width=150,anchor="center")
    statsInvTable.heading("0", text="Id")
    statsInvTable.heading("1", text="Tid")
    statsInvTable.grid(column=0,row=0,sticky=W)
    
    statsInvTableScroll.config(command=statsInvTable.yview)
    
    #Table with bankningar
    statsBankTableLF= LabelFrame(statsroot, text="Bankningar")
    statsBankTableLF.grid(column=1,row=0,sticky=W,padx=(STATSBORDERPAD,0) ,pady=(STATSBORDERPAD,0),columnspan=1)
    
    statsBankTableScroll = Scrollbar(statsBankTableLF)
    statsBankTableScroll.grid(column=1,row=0,sticky=N+S)
    
    statsBankTable = ttk.Treeview(statsBankTableLF,columns=("id","time"),height=8,yscrollcommand=statsBankTableScroll.set,selectmode="browse")
    statsBankTable['show'] = 'headings'
    statsBankTable.column("id",width=100,anchor="center")
    statsBankTable.column("time",width=150,anchor="center")
    statsBankTable.heading("0", text="Id")
    statsBankTable.heading("1", text="Tid")
    statsBankTable.grid(column=0,row=0,sticky=W)

    statsBankTableScroll.config(command=statsBankTable.yview)
    
    #Table with custom barcode insted of bankning or inventering
    statsGetTransactionsTableLF= LabelFrame(statsroot, text="Hämta sålda produkter, 100 senaste")
    statsGetTransactionsTableLF.grid(column=1,row=1,sticky=W+N,padx=(STATSBORDERPAD,0) ,pady=(STATSBORDERPAD,0),rowspan=2,columnspan=8)
    
    statsGetTransTableLFId = LabelFrame(statsGetTransactionsTableLF, text="barcode", padx=5,pady=5)
    statsGetTransTableLFId.grid(sticky=W,column=0,row=0)
    statsGetTransTableEntry = Entry(statsGetTransTableLFId,width=18)
    statsGetTransTableEntry.grid(column=0,row=0)
    statsGetTransTableEntry.bind('<Return>',statsUpdateTransTable)
    
    statsGetTransTableButton = Button(statsGetTransactionsTableLF, text="Hämta",height=2,command=statsUpdateTransTable)
    statsGetTransTableButton.grid(column=1,row=0,padx=(5,0),sticky=W)
    statsGetTransTableButton.bind('<Return>',statsUpdateTransTable)
    
    statsGetTransL = Label(statsGetTransactionsTableLF,text="Namn: ", font=("Helvetica",10))
    statsGetTransL.grid(column=2,row=0,sticky=W)
    statsGetTransVar = StringVar()
    statsGetTransVar.set("asd")
    statsGetTransValue = Label(statsGetTransactionsTableLF,textvariable=statsGetTransVar, font=("Helvetica",10))
    statsGetTransValue.grid(column=3,row=0,sticky=W)
    
    statsGetTransactionsTableScroll = Scrollbar(statsGetTransactionsTableLF)
    statsGetTransactionsTableScroll.grid(column=4,row=1,sticky=N+S)
    
    statsGetTransactionsTableLF.grid_columnconfigure(3,weight=1)
    
    statsGetTransTable = ttk.Treeview(statsGetTransactionsTableLF,columns=("id","time","price"),
        height=10,yscrollcommand=statsGetTransactionsTableScroll.set,selectmode="browse")
    statsGetTransTable['show'] = 'headings'
    statsGetTransTable.column("id",width=100,anchor="center")
    statsGetTransTable.column("time",width=150,anchor="center")
    statsGetTransTable.column("price",width=100,anchor="center")
    statsGetTransTable.heading("0", text="Id")
    statsGetTransTable.heading("1", text="Tid")
    statsGetTransTable.heading("2", text="Pris")
    statsGetTransTable.grid(column=0,row=1,sticky=W,columnspan=4)

    statsGetTransactionsTableScroll.config(command=statsGetTransTable.yview)
    
    #shows last used ID
    StatsLastId = StringVar()
    StatsLastId.set("Last ID: 0")
    statsIdLabel = Label(statsroot, textvariable=StatsLastId, font=("Helvetica",25))
    statsIdLabel.grid(column=0,row=1,sticky=W,padx=(STATSBORDERPAD,0))

    #select in which interval to produce results
    statsIntervalLF = LabelFrame(statsroot, text="Intervall att använda", padx=5,pady=5)
    statsIntervalLF.grid(sticky=W,column=0,row=2,padx=(STATSBORDERPAD,0))

    statsGenerateFLF = LabelFrame(statsIntervalLF, text="Från id", padx=5,pady=5)
    statsGenerateFLF.grid(sticky=W,column=0,row=0)
    statsGenerateF = Entry(statsGenerateFLF,width=18)
    statsGenerateF.grid(column=0,row=0)

    statsGenerateTLF = LabelFrame(statsIntervalLF, text="till id", padx=5,pady=5)
    statsGenerateTLF.grid(sticky=W,column=1,row=0)
    statsGenerateT = Entry(statsGenerateTLF,width=18)
    statsGenerateT.grid(column=0,row=0)
    statsGenerateT.bind('<Return>',statsSum)

    #sum totalt sold items value
    statsSumFrame = LabelFrame(statsIntervalLF, text="Summera sålda varor", padx=5,pady=5)
    statsSumFrame.grid(column=0,row=1,padx=(STATSBORDERPAD,0),sticky=W,columnspan=2)
    
    statsSumLabel = Label(statsSumFrame,text="Summa: ", font=("Helvetica",20))
    statsSumLabel.grid(column=0,row=0)
    
    statsSumVar = StringVar()
    statsSumVar.set("0 kr")
    statsSumLabelValue = Label(statsSumFrame,textvariable=statsSumVar, font=("Helvetica",20))
    statsSumLabelValue.grid(column=1,row=0)
    
    statsGenerateButton0 = Button(statsSumFrame, text="Summera",height=2,command=statsSum)
    statsGenerateButton0.grid(column=2,row=0,padx=(5,0))
    statsGenerateButton0.bind('<Return>',statsSum)
    
    #Generate a report per product
    statsGenerateLF = LabelFrame(statsIntervalLF, text="Exportera per produkt till excel", padx=5,pady=5)
    statsGenerateLF.grid(sticky=W,column=0,row=4,padx=(STATSBORDERPAD,0),columnspan=2)

    statsGenerateButton1 = Button(statsGenerateLF, text="Spara som..",height=2,command=lambda:statsGenerateReport("products"))
    statsGenerateButton1.grid(column=0,row=0,padx=(5,0))
    statsGenerateButton1.bind('<Return>',lambda x :statsGenerateReport("products"))
    
    #Generate a report per category
    statsGenerateLF2 = LabelFrame(statsIntervalLF, text="Exportera per kategori till excel", padx=5,pady=5)
    statsGenerateLF2.grid(sticky=W,column=0,row=5,padx=(STATSBORDERPAD,0),columnspan=2)

    statsGenerateButton2 = Button(statsGenerateLF2, text="Spara som..",height=2,command=lambda:statsGenerateReport("categories"))
    statsGenerateButton2.grid(column=0,row=0,padx=(5,0))
    statsGenerateButton2.bind('<Return>',lambda x:statsGenerateReport("categories"))
    
    #Export all products
    statsExportLF = LabelFrame(statsIntervalLF, text="Exportera alla produkter", padx=5,pady=5)
    statsExportLF.grid(sticky=W,column=0,row=6,padx=(STATSBORDERPAD,0),columnspan=2)

    statsExportButton = Button(statsExportLF, text="Spara som..",height=2,command=statsExportProducts)
    statsExportButton.grid(column=0,row=0,padx=(5,0))
    statsExportButton.bind('<Return>',statsExportProducts)
    
    #Get info from a id id,name,timestamp,transactions.price,transactions.barcode
    font = ("Helvetica",15)
    statsGetTransLF = LabelFrame(statsroot, text="Hämta transaktion", padx=5,pady=5)
    statsGetTransLF.grid(sticky=W,column=2,row=0,padx=(STATSBORDERPAD,0),pady=(STATSBORDERPAD,0))

    statsGetTransLFId = LabelFrame(statsGetTransLF, text="id", padx=5,pady=5)
    statsGetTransLFId.grid(sticky=W,column=0,row=0)
    statsGetTransEntry = Entry(statsGetTransLFId,width=18)
    statsGetTransEntry.grid(column=0,row=0)
    statsGetTransEntry.bind('<Return>',statsGetTransById)
    
    statsGetTransButton = Button(statsGetTransLF, text="Hämta",height=2,command=statsGetTransById)
    statsGetTransButton.grid(column=1,row=0,padx=(5,0))
    statsGetTransButton.bind('<Return>',statsGetTransById)
    
    statsGetTransLabel1 = Label(statsGetTransLF,text="Id: ", font=font)
    statsGetTransLabel1.grid(column=0,row=1,sticky=E)
    statsIdVar = StringVar()
    statsIdVar.set("")
    statsGetTransLabelValue1 = Label(statsGetTransLF,textvariable=statsIdVar, font=font)
    statsGetTransLabelValue1.grid(column=1,row=1)
    
    statsGetTransLabel2 = Label(statsGetTransLF,text="Namn: ", font=font)
    statsGetTransLabel2.grid(column=0,row=2,sticky=E)
    statsNameVar = StringVar()
    statsNameVar.set("")
    statsGetTransLabelValue2 = Label(statsGetTransLF,textvariable=statsNameVar, font=font)
    statsGetTransLabelValue2.grid(column=1,row=2)
    
    statsGetTransLabel3 = Label(statsGetTransLF,text="Steckkod: ", font=font)
    statsGetTransLabel3.grid(column=0,row=3,sticky=E)
    statsBarcodeVar = StringVar()
    statsBarcodeVar.set("")
    statsGetTransLabelValue3 = Label(statsGetTransLF,textvariable=statsBarcodeVar, font=font)
    statsGetTransLabelValue3.grid(column=1,row=3)
    
    statsGetTransLabel4 = Label(statsGetTransLF,text="Pris: ", font=font)
    statsGetTransLabel4.grid(column=0,row=4,sticky=E)
    statsPriceVar = StringVar()
    statsPriceVar.set("")
    statsGetTransLabelValue4 = Label(statsGetTransLF,textvariable=statsPriceVar, font=font)
    statsGetTransLabelValue4.grid(column=1,row=4)
    
    statsGetTransLabel5 = Label(statsGetTransLF,text="Tid: ", font=font)
    statsGetTransLabel5.grid(column=0,row=5,sticky=E)
    statsTimeVar = StringVar()
    statsTimeVar.set("")
    statsGetTransLabelValue5 = Label(statsGetTransLF,textvariable=statsTimeVar, font=font)
    statsGetTransLabelValue5.grid(column=1,row=5)
    
    #close button
    statsCloseButton = Button(statsroot, text="Stäng",height=2,width=10,command=quitstats)
    statsCloseButton.grid(column=10,row=10,padx=(0,STATSBORDERPAD),pady=(0,STATSBORDERPAD))
    statsCloseButton.bind('<Return>',quitstats)
    
    statsUpdate()
    statsfullscreen()
    statsroot.bind("<Escape>",quitstats)
    statsGenerateF.focus_set() #Set focus


      
def draw(x,y):
    drawrootTop = Toplevel()
    drawrootTop.geometry("1024x900")
    drawrootTop.transient(root) #Does not seem to work in windows
    drawrootTop.grab_set()
    drawrootCanvas = Canvas(drawrootTop)
    drawrootCanvas.grid(row=0,column=0,sticky=W+E+N+S)
    drawroot = Frame(drawrootCanvas)
    #drawroot.grid(row=0,column=0,sticky=W+E+N+S)
    
    drawrootTop.grid_rowconfigure(0,weight=1)
    drawrootTop.grid_columnconfigure(0,weight=1)
    
    drawrootCanvas.create_window((0,0),window=drawroot,anchor='nw')
    
    #drawroot.grid_rowconfigure(0,weight=1)
    #drawroot.grid_columnconfigure(0,weight=1)
    
    def OnFrameConfigure(event):
        '''Reset the scroll region to encompass the inner frame'''
        drawrootCanvas.configure(scrollregion=drawrootCanvas.bbox("all"))

    drawroot.bind("<Configure>", OnFrameConfigure) #Something scrollbox
        
    def quitdraw(*args):
       drawrootTop.destroy()
        
    def drawUpdate():
        drawCanvas.update_idletasks()
        drawCanvas.delete(ALL) #to delete everything before redraw
        
        #Update the option with what it actually is
        drawEntry0.delete(0, END)
        drawEntry0.insert(0, str(drawCanvas.yLabelWidth))
        drawEntry1.delete(0, END)
        drawEntry1.insert(0, str(drawCanvas.xLabelHeight))
        drawEntry2.delete(0, END)
        drawEntry2.insert(0, str(drawCanvas.xAxelDist))
        drawEntry3.delete(0, END)
        drawEntry3.insert(0, str(drawCanvas.yAxelDist))
        drawEntry4.delete(0, END)
        drawEntry4.insert(0, str(drawCanvas.padTop))
        drawEntry5.delete(0, END)
        drawEntry5.insert(0, str(drawCanvas.padLeft))
        drawEntry6.delete(0, END)
        drawEntry6.insert(0, str(drawCanvas.padRight))
        drawEntry7.delete(0, END)
        drawEntry7.insert(0, str(drawCanvas.width))
        drawEntry8.delete(0, END)
        drawEntry8.insert(0, str(drawCanvas.height))
        
        drawCanvas.config(width=drawCanvas.width, height=drawCanvas.height)
        
        drawHistogram()
        
    def drawUpdateButtonPress(*args):
        drawCanvas.yLabelWidth = int(drawEntry0.get())
        drawCanvas.xLabelHeight = int(drawEntry1.get())
        drawCanvas.xAxelDist = int(drawEntry2.get())
        drawCanvas.yAxelDist = int(drawEntry3.get())
        drawCanvas.padTop = int(drawEntry4.get())
        drawCanvas.padLeft = int(drawEntry5.get())
        drawCanvas.padRight = int(drawEntry6.get())
        drawCanvas.padLeft = int(drawEntry5.get())
        drawCanvas.padRight = int(drawEntry6.get())
        drawCanvas.width = int(drawEntry7.get())
        drawCanvas.height = int(drawEntry8.get())
        drawUpdate()
        
    #Sets the initial size of the canvas depending on screen size and
    #options widget size. 4/3
    def drawInit():
        #drawUpdate()
        drawCanvas.update_idletasks()
        drawrootCanvas.update_idletasks()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        settingWidth = drawLF.winfo_width()
        width = w-settingWidth-75
        proposedHeight = int(width*(float(3)/4))
        diff = h - proposedHeight
        if diff < 0:
            drawCanvas.config(width=width, height=(h-75))
            drawCanvas.width = width
            drawCanvas.height = (h-75)
        elif diff < 101:
            drawCanvas.config(width=width, height=proposedHeight-(75-diff))
            drawCanvas.width = width
            drawCanvas.height = proposedHeight-(75-diff)
        else:
            drawCanvas.config(width=width, height=proposedHeight)
            drawCanvas.width = width
            drawCanvas.height = proposedHeight
        drawUpdate()
    
    def drawfullscreen():
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        #root.overrideredirect(1)
        drawrootTop.attributes('-fullscreen', True)
        drawrootTop.geometry("%dx%d+0+0" % (w, h))
        
    def drawBase(widthUsed):
        drawCanvas.update_idletasks()
        drawCanvas.create_line(convertX(0-drawCanvas.padLeft), convertY(0), convertX(0-drawCanvas.padLeft), convertY(getH())) #Y axel
        drawCanvas.create_line(convertX(0-drawCanvas.padLeft), convertY(0), convertX(widthUsed), convertY(0)) #X axel
        
    #Covert from (0,0) being top left to (0,0) being 
    #(drawCanvas.xLabelWidth,drawCanvas.winfo_height()-drawCanvas.yLabelWidth)
    def convertX(coord):
        drawCanvas.update_idletasks()
        return drawCanvas.yLabelWidth+coord+drawCanvas.padLeft
    
    def convertY(coord):
        drawCanvas.update_idletasks()
        return drawCanvas.winfo_height()-drawCanvas.xLabelHeight-coord
    
    def getW():
        return getWidth()
        
    def getH():
        return getHeight()
    
    #Gets the width minus labls
    def getWidth():
        drawCanvas.update_idletasks()
        return drawCanvas.winfo_width()-drawCanvas.yLabelWidth-drawCanvas.padLeft-drawCanvas.padRight
        
    #gets the heigth minus labels
    def getHeight():
        drawCanvas.update_idletasks()
        return drawCanvas.winfo_height()-drawCanvas.xLabelHeight-drawCanvas.padTop
        
    def drawXLabel(widthUsed):
        #Take a sample every drawCanvas.xAxelDist of the X input and print it along with
        #vertical bars
        drawCanvas.update_idletasks()
        numberOfLegends = widthUsed/drawCanvas.xAxelDist
        distLegend = float(widthUsed)/numberOfLegends
        for i in range(numberOfLegends+1):
            part = float(i)/numberOfLegends
            index = part*(len(x))
            if part == 1.0:
                value2 = x[int(index)-1]
            else:
                value2 = x[int(index)]
            temp = Label(drawCanvas, text=str(value2))
            #TODO, each other is high and low, if space enougth, should use compact form if needed.
            if i % 2 == 0:
                drawCanvas.create_line(convertX(i*distLegend),convertY(0),convertX(i*distLegend),convertY(0-15))
                drawCanvas.create_window((convertX(i*distLegend),convertY(-25)),window=temp)
            else:
                drawCanvas.create_line(convertX(i*distLegend),convertY(0),convertX(i*distLegend),convertY(0-30))
                drawCanvas.create_window((convertX(i*distLegend),convertY(-40)),window=temp)
        
    def drawYLabel(maxValue):
        drawCanvas.update_idletasks()
        numberOfLegends = getH()/drawCanvas.yAxelDist
        distLegend = float(getH())/numberOfLegends
        for i in range(numberOfLegends+1):
            drawCanvas.create_line(convertX(0-drawCanvas.padLeft),convertY(i*distLegend),convertX(-15-drawCanvas.padLeft),convertY(i*distLegend))
            if isinstance(maxValue, int):
                if i == numberOfLegends:
                    value = maxValue
                else:
                    value = int(round(float(maxValue*i*distLegend)/getH()))
            elif isinstance(maxValue, float):
                if i == numberOfLegends:
                    value = maxValue
                    value = "%.3f" % value
                else:
                    value = maxValue*i*distLegend/getH()
                    value = "%.3f" % value
            else:
                tkMessageBox.showerror("Fel","Okänd in-typ",parent=drawrootTop)
            temp = Label(drawCanvas, text=str(value) )
            drawCanvas.create_window((convertX(-30),convertY(i*distLegend)),window=temp,anchor=E)
        
    #graph types: Histrogram (connected chart) , line chart, column chart (distance between entries)
    #Add labls when mouse on a bar.
    
    def drawHistogram():
        drawCanvas.update_idletasks()
        pixelsPerX,remainder = divmod(getWidth(),len(x))
        if pixelsPerX != 0:
            widthUsed = getW() - remainder
            maxValue = max(y)
            for i,value in enumerate(y):
                if maxValue==0:
                    fraction = 0
                else:
                    fraction = float(value)/maxValue
                iHeight = getH()*fraction
                temp = drawCanvas.create_rectangle(convertX(i*pixelsPerX), convertY(0), convertX(i*pixelsPerX+pixelsPerX), convertY(iHeight),fill="blue")
                #drawCanvas.tag_bind(temp, '<ButtonPress-1>', drawUpdateButtonPress)   
                #Can make a ditionary lookup of the value
                #Just print it somewhere easy..
                #Or put a label there? 
            drawYLabel(maxValue)
            drawXLabel(widthUsed)
            drawBase(widthUsed)
        else:
            widthask = len(x)+drawCanvas.yLabelWidth+drawCanvas.padLeft+drawCanvas.padRight
            if tkMessageBox.askyesno("Fel","Grafen är inte nog bred för antal input i X\n, vill du sätta bredden till %i pixlar?" % (widthask,),parent=drawrootTop):
                drawCanvas.width = widthask
                drawUpdate()
        
    font = ("Helvetica",15)
    width = 15
    
    scrollbarVertical = Scrollbar(drawrootTop,command=drawrootCanvas.yview)
    scrollbarVertical.grid(column=1,row=0,sticky=N+S,rowspan=1)
    scrollbarHorizontal = Scrollbar(drawrootTop, orient = HORIZONTAL,command=drawrootCanvas.xview)
    scrollbarHorizontal.grid(column=0,row=1,sticky=W+E+N+S)
    drawrootCanvas.configure(yscrollcommand=scrollbarVertical.set)
    drawrootCanvas.configure(xscrollcommand=scrollbarHorizontal.set)
        
    #GUI here...

    #Options
    
    #Canvas for graph, decide where to put labels and how.
        
    #Left is a settings panel
    drawLF = LabelFrame(drawroot, text="Inställningar", padx=5,pady=5)
    drawLF.grid(sticky=W+N,column=0,row=0,padx=(DRAWPAD,DRAWPAD),pady=(DRAWPAD,DRAWPAD))
    
    (drawL0,drawEntry0) = makeLabelAndEntry(drawLF,"Y label Bredd: ",(0,0),font,width)
    (drawL1,drawEntry1) = makeLabelAndEntry(drawLF,"X label Höjd: ",(0,1),font,width) 
    (drawL2,drawEntry2) = makeLabelAndEntry(drawLF,"x Label Distance: ",(0,2),font,width) 
    (drawL3,drawEntry3) = makeLabelAndEntry(drawLF,"y Label Distance: ",(0,3),font,width)
    (drawL4,drawEntry4) = makeLabelAndEntry(drawLF,"Pad Top: ",(0,4),font,width) 
    (drawL5,drawEntry5) = makeLabelAndEntry(drawLF,"Pad Left: ",(0,5),font,width) 
    (drawL6,drawEntry6) = makeLabelAndEntry(drawLF,"Pad Right: ",(0,6),font,width)
    (drawL7,drawEntry7) = makeLabelAndEntry(drawLF,"Bredd ",(0,7),font,width)
    (drawL8,drawEntry8) = makeLabelAndEntry(drawLF,"Höjd: ",(0,8),font,width)
    drawEntry0.bind('<Return>',drawUpdateButtonPress)
    drawEntry1.bind('<Return>',drawUpdateButtonPress)
    drawEntry2.bind('<Return>',drawUpdateButtonPress)
    drawEntry3.bind('<Return>',drawUpdateButtonPress)
    drawEntry4.bind('<Return>',drawUpdateButtonPress)
    drawEntry5.bind('<Return>',drawUpdateButtonPress)
    drawEntry6.bind('<Return>',drawUpdateButtonPress)
    drawEntry7.bind('<Return>',drawUpdateButtonPress)
    drawEntry8.bind('<Return>',drawUpdateButtonPress)
    
    #Update button
    drawUpdateButton = Button(drawLF,command=drawUpdateButtonPress,text="Uppdatera",height=1,width=10)
    drawUpdateButton.grid(column=1,row=10,padx=(0,0),pady=(0,0))
    drawUpdateButton.bind('<Return>',drawUpdateButtonPress)
    
    #Canvas to print graph on
    drawCanvas = Canvas(drawroot,width=400, height=300,highlightthickness=0, bd=0,relief='ridge')
    drawCanvas.grid(row=0,column=1,sticky=W+E+N+S,padx=(0,DRAWPAD),pady=(DRAWPAD,DRAWPAD))
    
    drawCanvas.yLabelWidth = 75
    drawCanvas.xLabelHeight = 75
    drawCanvas.xAxelDist = 75
    drawCanvas.yAxelDist = 50
    drawCanvas.padTop = 10
    drawCanvas.padLeft = 10
    drawCanvas.padRight = 10
    drawCanvas.width = 400
    drawCanvas.height = 300
        
    #close button
    drawCloseButton = Button(drawrootTop,command=quitdraw,image=photo)
    drawCloseButton.grid(column=1,row=1,padx=(0,0),pady=(0,0))
    drawCloseButton.bind('<Return>',quitdraw)
    
    drawfullscreen()
    drawInit()
    drawrootTop.bind("<Escape>",quitdraw)
    #drawroot.bind("<Escape>",quitdraw) #Do I need these two?
    #drawrootCanvas.bind("<Escape>",quitdraw)
    drawEntry0.focus_set() #Needs a focus before escape works
 

        
def dataMining():
    dataMiningroot = Toplevel()
    dataMiningroot.geometry("1024x900")
    dataMiningroot.transient(root) #Does not seem to work in windows
    dataMiningroot.grab_set()
    
    def quitdataMining(*args):
        dataMiningroot.destroy()
        
    def dataMiningupdate():
        getBasicStats()
        dataCategoryTableUpdate()
        if dataCategoryTable.lastCol != None:
            treeview_sort_column(dataCategoryTable, dataCategoryTable.lastCol, dataCategoryTable.lastReverse,True)
        dataProductTableUpdate()
        
    def getBasicStats(*args):
        ##Transactions Mining
        #Make all measurements sortable by id? #DO this! Use a scale slider?? slide on id bu show data for that id..
        
        #How many of each price, histogram of price from 0 to max price.
        #something with time: When on day most sold
        #Number of sales per day,
        #number of sales last day, week, month.
        #Select stats over different time periods.
        #hisogram over sales per day?
        
        #försäljning per dag per produkt
        
        #Set last ID
        lastID = getLast(cur,1)
        dataBasicVar1.set(str(lastID[0][0]))
        
        #Set Number of transactions
        numberOfTransactions = getNumberOfTransactions(cur)
        dataBasicVar2.set(numberOfTransactions)
        
        #Set Mean Sales price
        mean = getMeanSalePrice(cur)
        dataBasicVar3.set(mean)
        
        #Set median sales price
        median = getMedianSalePrice(cur)
        dataBasicVar4.set(median)
        
        #Set Number of products
        number = getNumberOfProducts(cur)
        dataBasicVar5.set(number)
        
        #set total sale number
        number = getSumBeweenIds(cur,0,int(lastID[0][0]))
        dataBasicVar6.set(number)
        
        #set number of deleted transactions
        number = int(lastID[0][0])-int(numberOfTransactions)
        dataBasicVar7.set(number)
        
        #set number of chunks of transactions
        number = getTransactionsChunks(cur)
        dataBasicVar8.set(number)
        
        #set mean chunk size
        number = getMeanChunkSize(cur)
        dataBasicVar9.set(number)
        
        
    def dataCategoryTableUpdate():
        for i in dataCategoryTable.get_children():
            dataCategoryTable.delete(i)
        temp = getCategoryStats(cur)
        for i in temp:
            dataCategoryTable.insert("",0,values=(i[0],i[1],i[2],i[3],i[4]))
        
    def dataProductTableUpdate():
        for i in dataProductTable.get_children():
            dataProductTable.delete(i)
        temp = getTransactionsGroupedByBarcode(cur)
        for i in temp:
            dataProductTable.insert("",0,values=(i[0],i[1],i[2],i[3],i[4]))
        
    def dataMiningfullscreen():
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        #root.overrideredirect(1)
        dataMiningroot.attributes('-fullscreen', True)
        dataMiningroot.geometry("%dx%d+0+0" % (w, h))
      
    
    #This function plots a given range and in resolution (seconds) time interval
    def dataMiningPlotter(timeFrom, timeTo, resolution, category = None, product = None):
        if (timeFrom > timeTo):
            tkMessageBox.showerror("Fel","starttid är mindre än sluttid",parent=dataMiningroot)
            return
            
        #Remove milliseconds to make everything start at even second.
        timeFrom = timeFrom.replace(microsecond=0)
        
        #Covert start and end time to string
        dateTimeNowS = timeTo.strftime("%Y-%m-%d %H:%M:%S")
        dateTimePastS = timeFrom.strftime("%Y-%m-%d %H:%M:%S")
        
        #Get data between times and grouped by time
        data = getTransactionsByDate(dateTimePastS,dateTimeNowS,cur)
        
        dateList = []
        tempTime = timeFrom
        
        #create dateList with dates that are resoltuions seconds apart
        while (tempTime < timeTo):
            dateList.append([tempTime,0])
            tempTime += datetime.timedelta(seconds = resolution)
        
        #Go through the data and put the data in right slot in dateList.
        for (price,time) in data:
            index = int((datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")-timeFrom).total_seconds())/resolution
            dateList[index][1] += price
        
        #Make strings in order to be printable nice
        if resolution >= 60*60*24*30:
            #Strip days
            x = [i[0].strftime("%Y-%m") for i in dateList]
        elif resolution >= 60*60*24:
            #Strip hours
            x = [i[0].strftime("%Y-%m-%d") for i in dateList]
        elif resolution >= 60*60:
            #strip of minutes
            x = [i[0].strftime("%Y-%m-%d %H") for i in dateList]
        elif resolution >=60:
            #Strip seconds
            x = [i[0].strftime("%Y-%m-%d %H:%M") for i in dateList]
        
        y = [i[1] for i in dateList]
        
        #plot it
        draw(x,y)
    
    def dataSpcialPlotter(*args):
        tkMessageBox.showerror("Fel","TODO, custom time",parent=dataMiningroot)
    
    #GUI here..
    font = ("Helvetica",15)
    dataMiningroot.grid_rowconfigure(8,weight=1)
    dataMiningroot.grid_columnconfigure(8,weight=1)
    
    #Basic stats
    dataBasicLF = LabelFrame(dataMiningroot, text="Grundläggande data", padx=5,pady=5)
    dataBasicLF.grid(sticky=W+N,column=0,row=0,padx=(DATAPAD,0),pady=(DATAPAD,0),rowspan=2)
    
    (dataBasicL1,dataBasicVar1,dataBasicValue1) = makeLabelAndVar(dataBasicLF,"Senaste ID: ",(0,0),font)
    (dataBasicL2,dataBasicVar2,dataBasicValue2) = makeLabelAndVar(dataBasicLF,"Antal köp: ",(0,1),font)
    (dataBasicL3,dataBasicVar3,dataBasicValue3) = makeLabelAndVar(dataBasicLF,"Medelpris: ",(0,2),font)
    (dataBasicL4,dataBasicVar4,dataBasicValue4) = makeLabelAndVar(dataBasicLF,"Medianpris: ",(0,3),font)
    (dataBasicL5,dataBasicVar5,dataBasicValue5) = makeLabelAndVar(dataBasicLF,"Antal Produkter: ",(0,4),font)
    (dataBasicL6,dataBasicVar6,dataBasicValue6) = makeLabelAndVar(dataBasicLF,"Summa sålt: ",(0,5),font)
    (dataBasicL7,dataBasicVar7,dataBasicValue7) = makeLabelAndVar(dataBasicLF,"Borttagna köp: ",(0,6),font)
    (dataBasicL8,dataBasicVar8,dataBasicValue8) = makeLabelAndVar(dataBasicLF,"Antal chunks av köp: ",(0,7),font)
    (dataBasicL9,dataBasicVar9,dataBasicValue9) = makeLabelAndVar(dataBasicLF,"Storlek på Medelchunk: ",(0,8),font)

    #Different plots
    dataPlotLF = LabelFrame(dataMiningroot, text="Grafer", padx=5,pady=2)
    dataPlotLF.grid(sticky=W+N,column=0,row=2,padx=(0,0),pady=(0,0))
    
    dataPlotLFDay = LabelFrame(dataPlotLF, text="Sista 24h", padx=5,pady=2)
    dataPlotLFDay.grid(sticky=W+N,column=0,row=0,padx=(0,0),pady=(0,0))
    
    dataPlotLFWeek = LabelFrame(dataPlotLF, text="Sista veckan", padx=5,pady=2)
    dataPlotLFWeek.grid(sticky=W+N,column=0,row=1,padx=(0,0),pady=(0,0))
    
    dataPlotLFMonth = LabelFrame(dataPlotLF, text="Sista månaden", padx=5,pady=2)
    dataPlotLFMonth.grid(sticky=W+N,column=0,row=2,padx=(0,0),pady=(0,0))
    
    dataPlotLFYear = LabelFrame(dataPlotLF, text="Sedan första sålda", padx=5,pady=2)
    dataPlotLFYear.grid(sticky=W+N,column=0,row=3,padx=(0,0),pady=(0,0))
    
    dataPlotLFCustom = LabelFrame(dataPlotLF, text="Custom", padx=5,pady=2)
    dataPlotLFCustom.grid(sticky=W+N,column=0,row=4,padx=(0,0),pady=(0,0))
    
    dateTimeNow = datetime.datetime.now()
    dateTime1Day = dateTimeNow - datetime.timedelta(days=1)
    dateTime1Week = dateTimeNow - datetime.timedelta(days=7)
    dateTime1Month = dateTimeNow - datetime.timedelta(days=30)
    
    #Get date of first sale!!! #TODO: 
    dateTimeSinceStart = dateTimeNow - datetime.timedelta(days=365)
    
    #To make row 1 as small as possible to make row 2 be able to strech upwards
    dataMiningroot.grid_rowconfigure(2,weight=1)
    
    #lastDaySecFunc = lambda: dataMiningPlotter(dateTime1Day,dateTimeNow,1)
    lastDayMinuteFunc = lambda: dataMiningPlotter(dateTime1Day,dateTimeNow,60)
    lastDayHourFunc = lambda: dataMiningPlotter(dateTime1Day,dateTimeNow,60*60)
    
    lastWeekHourFunc = lambda: dataMiningPlotter(dateTime1Week,dateTimeNow,60*60)
    lastWeekDayFunc = lambda: dataMiningPlotter(dateTime1Week,dateTimeNow,60*60*24)
    
    lastMonthHourFunc = lambda: dataMiningPlotter(dateTime1Month,dateTimeNow,60*60)
    lastMonthDayFunc = lambda: dataMiningPlotter(dateTime1Month,dateTimeNow,60*60*24)
    lastMonthWeekFunc = lambda: dataMiningPlotter(dateTime1Month,dateTimeNow,60*60*24*7)
    
    lastSinceStartDayFunc = lambda: dataMiningPlotter(dateTimeSinceStart,dateTimeNow,60*60*24)
    lastSinceStartWeekFunc = lambda: dataMiningPlotter(dateTimeSinceStart,dateTimeNow,60*60*24*7)
    lastSinceStartMonthFunc = lambda: dataMiningPlotter(dateTimeSinceStart,dateTimeNow,60*60*24*30)
    
    dataCloseButton1 = Button(dataPlotLFDay, text="Per minut",height=2,width=10,command= lastDayMinuteFunc)
    dataCloseButton1.grid(column=0,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton1.bind('<Return>',lastDayMinuteFunc)
    dataCloseButton2 = Button(dataPlotLFDay, text="Per timma",height=2,width=10,command= lastDayHourFunc)
    dataCloseButton2.grid(column=1,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton2.bind('<Return>',lastDayHourFunc)
    
    dataCloseButton3 = Button(dataPlotLFWeek, text="Per timma",height=2,width=10,command= lastWeekHourFunc)
    dataCloseButton3.grid(column=0,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton3.bind('<Return>',lastWeekHourFunc)
    dataCloseButton4 = Button(dataPlotLFWeek, text="Per dag",height=2,width=10,command= lastWeekDayFunc)
    dataCloseButton4.grid(column=1,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton4.bind('<Return>',lastWeekDayFunc)
    
    dataCloseButton5 = Button(dataPlotLFMonth, text="Per timma",height=2,width=10,command= lastMonthHourFunc)
    dataCloseButton5.grid(column=0,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton5.bind('<Return>',lastMonthHourFunc)
    dataCloseButton6 = Button(dataPlotLFMonth, text="Per dag",height=2,width=10,command= lastMonthDayFunc)
    dataCloseButton6.grid(column=1,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton6.bind('<Return>',lastMonthDayFunc)
    dataCloseButton7 = Button(dataPlotLFMonth, text="Per vecka",height=2,width=10,command= lastMonthWeekFunc)
    dataCloseButton7.grid(column=2,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton7.bind('<Return>',lastMonthWeekFunc)
    
    dataCloseButton8 = Button(dataPlotLFYear, text="Per dag",height=2,width=10,command= lastSinceStartDayFunc)
    dataCloseButton8.grid(column=0,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton8.bind('<Return>',lastSinceStartDayFunc)
    dataCloseButton9 = Button(dataPlotLFYear, text="Per vecka",height=2,width=10,command= lastSinceStartWeekFunc)
    dataCloseButton9.grid(column=1,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton9.bind('<Return>',lastSinceStartWeekFunc)
    dataCloseButton10 = Button(dataPlotLFYear, text="Per månad",height=2,width=10,command= lastSinceStartMonthFunc)
    dataCloseButton10.grid(column=2,row=0,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton10.bind('<Return>',lastSinceStartMonthFunc)
    
    dataCustomLF1 = LabelFrame(dataPlotLFCustom, text="från tid (YYYY-MM-DD HH:MM:SS)", padx=5,pady=5)
    dataCustomLF1.grid(sticky=W,column=0,row=0)
    dataCustomFE1 = Entry(dataCustomLF1,width=18)
    dataCustomFE1.grid(column=0,row=0)
    dataCustomLF2 = LabelFrame(dataPlotLFCustom, text="till tid", padx=5,pady=5)
    dataCustomLF2.grid(sticky=W,column=1,row=0)
    dataCustomFE2 = Entry(dataCustomLF2,width=18)
    dataCustomFE2.grid(column=0,row=0)
    dataCustomLF3 = LabelFrame(dataPlotLFCustom, text="intervallläng (sekunder)", padx=5,pady=5)
    dataCustomLF3.grid(sticky=W,column=0,row=1)
    dataCustomFE3 = Entry(dataCustomLF3,width=18)
    dataCustomFE3.grid(column=0,row=0)
    
    dataCloseButton11 = Button(dataPlotLFCustom, text="OK",height=2,width=10,command= dataSpcialPlotter)
    dataCloseButton11.grid(column=1,row=1,padx=(0,DATAPAD),pady=(0,0))
    dataCloseButton11.bind('<Return>',dataSpcialPlotter)
    
    #Do complete custom
    #12h?
    #1day: second (86k pixlar),minute (1440pixlar),hr (24 pixlar)
    #1week: second (>86k pixlar),minute (10k pixlar),hr (168 pixlar),day (7 pixlar)
    #1month: second,minute (44k),hr (744 pixlar),day (31 pixlar),week (5 pixlar)
    #since start: second,minute,hr (8k),day (365),week (52 pixlar),month (12 pixlar)
    
    #Be able to choose which day, hr, month etc to use..
    
    #Plot this:
        #sales last 24hrs, per minute, hour, or custom?.
        #Sales last week, per hr or something
        #Sales last month, per day sum
        #Sales since beginning, per day?
        #Plot specific category or product on each plot?
        #Need a fill function that assigns 0 to all empty slots of time.
        #Truncate time depending on what we show
        #How to smooth is out to see where most buy?
        
        #Can be sorted by product or category
        #Cut time to right digits.
        
        #Have buttons for most common options, aka 24hr, 1week, 1 monther, all etc.
    
    
    
    
    #dataSacleFrom = Scale(dataMiningroot,from_=0,to=20000,orient=HORIZONTAL)
    #dataSacleFrom.grid(column=0,row=1,sticky=E+W)
    
    #Make a table where we fill category, number of sales by category, total price by category and 
    #number of products in each category, mean price
    dataCategoryTableLF= LabelFrame(dataMiningroot, text="Kategoridata")
    dataCategoryTableLF.grid(column=1,row=0,sticky=W+N,padx=(DATAPAD,0) ,pady=(DATAPAD,0))
        
    dataCategoryTableScroll = Scrollbar(dataCategoryTableLF)
    dataCategoryTableScroll.grid(column=1,row=0,sticky=N+S)
    
    categories = ("S_category","I_num sales","I_tot price","I_num prod","F_mean price")
    dataCategoryTable = ttk.Treeview(dataCategoryTableLF,columns=categories,
                    height=10,yscrollcommand=dataCategoryTableScroll.set,selectmode="browse")
    dataCategoryTable['show'] = 'headings'
    dataCategoryTable.column(categories[0],width=120,anchor="center")
    dataCategoryTable.column(categories[1],width=100,anchor="center")
    dataCategoryTable.column(categories[2],width=120,anchor="center")
    dataCategoryTable.column(categories[3],width=100,anchor="center")
    dataCategoryTable.column(categories[4],width=100,anchor="center")
    dataCategoryTable.heading("0", text="Kategori",anchor="center",
                              command=lambda: treeview_sort_column(dataCategoryTable, categories[0], False,False))
    dataCategoryTable.heading("1", text="Antal Sålda",anchor="center",
                              command=lambda: treeview_sort_column(dataCategoryTable, categories[1], False,False))
    dataCategoryTable.heading("2", text="Totalt Pris",anchor="center",
                              command=lambda: treeview_sort_column(dataCategoryTable, categories[2], False,False))
    dataCategoryTable.heading("3", text="Ant Prod",command=lambda: treeview_sort_column(dataCategoryTable, categories[3], False,False))
    dataCategoryTable.heading("4", text="Medelpris",command=lambda: treeview_sort_column(dataCategoryTable, categories[4], False,False))
    dataCategoryTable.grid(column=0,row=0,sticky=W)
    dataCategoryTable.lastCol = None
    dataCategoryTable.lastReverse = None

    dataCategoryTableScroll.config(command=dataCategoryTable.yview)
    
    #Table of number of sold items per barcode, Name, sum of sold items, their total price,
    dataProductTableLF= LabelFrame(dataMiningroot, text="Produktdata")
    dataProductTableLF.grid(column=1,row=1,sticky=W+N,padx=(DATAPAD,0) ,pady=(DATAPAD,0),rowspan=2)
    
    dataProductTableScroll = Scrollbar(dataProductTableLF)
    dataProductTableScroll.grid(column=1,row=0,sticky=N+S)
    
    dataProductTable = ttk.Treeview(dataProductTableLF,columns=("S_name","I_barcode","I_num sold","I_tot price","I_price"),
        height=15,yscrollcommand=dataProductTableScroll.set,selectmode="browse")
    dataProductTable['show'] = 'headings'
    dataProductTable.column("S_name",width=120,anchor="center")
    dataProductTable.column("I_barcode",width=120,anchor="center")
    dataProductTable.column("I_num sold",width=100,anchor="center")
    dataProductTable.column("I_tot price",width=120,anchor="center")
    dataProductTable.column("I_price",width=100,anchor="center")
    dataProductTable.heading("0", text="Namn",anchor="center",command=lambda: treeview_sort_column(dataProductTable, "S_name", False,False))
    dataProductTable.heading("1", text="Steckkod",anchor="center",command=lambda: treeview_sort_column(dataProductTable, "I_barcode", False,False))
    dataProductTable.heading("2", text="Antal sålda",anchor="center",command=lambda: treeview_sort_column(dataProductTable, "I_num sold", False,False))
    dataProductTable.heading("3", text="Totalt pris",command=lambda: treeview_sort_column(dataProductTable, "I_tot price", False,False))
    dataProductTable.heading("4", text="Pris",command=lambda: treeview_sort_column(dataProductTable, "I_price", False,False))
    dataProductTable.grid(column=0,row=0,sticky=W)
    dataProductTable.lastCol = None
    dataProductTable.lastReverse = None
    
    dataProductTableScroll.config(command=dataProductTable.yview)
    
    #close button
    dataCloseButton = Button(dataMiningroot, text="Stäng",height=2,width=10,command=quitdataMining)
    dataCloseButton.grid(column=10,row=10,padx=(0,DATAPAD),pady=(0,DATAPAD))
    dataCloseButton.bind('<Return>',quitdataMining)
    
    dataMiningfullscreen()
    dataMiningupdate()
    dataMiningroot.bind("<Escape>",quitdataMining)
    dataBasicL1.focus_set()
        
        
#The admin window stuffs 
def admin():
    adminroot = Toplevel()
    adminroot.geometry("1024x900")
    adminroot.transient(root) #Does not seem to work in windows
    adminroot.grab_set() #Force all events to this window so it will be on top of the other one.
    
    def adminfullscreen():
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        #root.overrideredirect(1)
        adminroot.attributes('-fullscreen', True)
        adminroot.geometry("%dx%d+0+0" % (w, h))
    
    def adminupdate():
        #Update category boxes
        A = getCategories()
        for i in range(len(A)):
            (str,) = A[i]
            A[i] = str
        adminCatCombo.config(values=A)
        adminUpdateCategory.config(values=A)
        
        #Update product list
        for i in adminProductTable.get_children():
            adminProductTable.delete(i)
        temp = getAllProducts()
        for i in temp:
            adminProductTable.insert("",0,values=(i[0],i[1],i[2],i[3]))
        if adminProductTable.lastCol != None:
            treeview_sort_column(adminProductTable, adminProductTable.lastCol, adminProductTable.lastReverse,True)
            
        #Update transactions list
        for i in adminTransactionTable.get_children():
            adminTransactionTable.delete(i)
        temp = getLast(cur,100)
        for i in temp:
            adminTransactionTable.insert("",0,values=(i[0],i[1],i[4],i[3],i[2]))

        #update inventeringTable
        for i in adminInvTable.get_children():
            adminInvTable.delete(i)
        temp = getInventeringar(cur)
        for i in temp:
            adminInvTable.insert("",0,values=(i[0],i[1]))
            
        
    def insertNewProduct(*args):
        wrong = ""
        if len(adminbarcode.get()) not in BARLEN or not adminbarcode.get().isdigit():
            wrong = wrong + " Wrong barcode length or none digits,"
        if not adminprice.get().isdigit():
            wrong = wrong + " Price is none digits"
        if adminprice.get().isdigit() and int(adminprice.get()) < 0:
            wrong = wrong + " Price negative"
        if len(wrong) == 0:
            data = getProductByBarcode(cur,adminbarcode.get())
            if data == []:
                insertProduct(cur,con,adminbarcode.get(),adminprice.get(),adminname.get(),adminCatCombo.get())
                adminbarcode.delete(0,END)
                adminprice.delete(0,END)
                adminname.delete(0,END)
                adminCatCombo.set("")
                adminupdate()
            else:
                tkMessageBox.showerror("Fel","Produkten existerar redan",parent=adminroot)
        else:
            tkMessageBox.showerror("Fel",wrong,parent=adminroot)

    def updateAProduct(*args):
        temp = adminUpdateBarcode.get()
        if len(temp) in BARLEN and temp.isdigit():
            (price,name) = getPriceAndName(cur,temp)
            if (price !=-1):
                if adminUpdatePrice.get().isdigit() and int(adminUpdatePrice.get()) >=0:
                    if tkMessageBox.askyesno("Säker?","Updatera produkt\nStreckkod: " +
                            str(temp) +"\nPris: " + str(price) + "\nNamn: " + name + 
                            "\ntill\nStreckkod: " + str(temp) + "\nPris: " + 
                            str(adminUpdatePrice.get()) + "\nNamn: " + adminUpdateName.get() + 
                            "\nKategori:  " + adminUpdateCategory.get(),parent=adminroot):
                        updateProduct(cur,con,temp,adminUpdatePrice.get(),adminUpdateName.get(),adminUpdateCategory.get())
                        adminUpdatePrice.delete(0,END)
                        adminUpdateName.delete(0,END)
                        adminUpdateCategory.set("")
                        adminUpdateBarcode.delete(0,END)
                        adminupdate()
                else:
                    tkMessageBox.showerror("Fel","Fel pris",parent=adminroot)
            else:
                tkMessageBox.showerror("Fel",name,parent=adminroot)
        else:
            tkMessageBox.showerror("Fel","Ingen giltig Streckkod",parent=adminroot)

    def deleteAProduct(*args):
        temp = adminDeleteBarcode.get()
        if len(temp) in BARLEN and temp.isdigit():
            data = getIdsByBarcode(cur,temp)
            if len(data) == 0:
                data = getProductByBarcode(cur,temp)
                if len(data) != 0:
                    (barcode,price,name,category) = data[0]
                    if tkMessageBox.askyesno("Säker?","Ta bort produkt \nStreckkod: " + temp +
                                             "\nPris: " + str(price) + "\nNamn: " + name +
                                             "\nKategori: " + category,parent=adminroot):
                        delteProducyByBarcode(cur,con,temp)
                        adminDeleteBarcode.delete(0,END)
                        adminupdate()
                else:
                    tkMessageBox.showerror("Fel","ingen produkt med Streckkod: " + temp + " existerar",parent=adminroot)
            else:
                idString = ""
                for i in data:
                    (id,) = i
                    idString = idString + "," + str(id)
                tkMessageBox.showerror("Fel","Streckkod " + temp + " finns i transaktioner: " + 
                                        idString + ", kunde inte ta bort produkten",parent=adminroot)
        else:
            tkMessageBox.showerror("Fel","Ingen giltig Streckkod",parent=adminroot)

    def deleteTransaction(*args):
        transId = adminDeleteId.get()
        checkTrans = getTransactionById(cur,transId)
        if checkTrans != []:
            (id,name,timestamp,price,barcode) = checkTrans[0]
            if tkMessageBox.askyesno("Säker?","Ta bort transaktion:\nId: " + transId + "\nNamn:" +
                    name + "\nStreckkod:" + str(barcode) + "\nPris:" + str(price) + "\nTid:" + str(timestamp),parent=adminroot):
                deleteTransactionById(cur,con,id)
                adminDeleteId.delete(0,END)
                adminupdate()
        else:
            tkMessageBox.showerror("Fel","transaktion med id: " + transId + " finns inte",parent=adminroot)

    def generateReport(*args):
        fileToWrite = tkFileDialog.asksaveasfile(mode='w',defaultextension = ".csv",
            filetypes=[('comma seperated value', '.csv')],parent=adminroot )
        if fileToWrite:
            getTransactionsBetweenIds(cur,adminGenerateF.get(),adminGenerateT.get())
            data = cur.fetchone()
            numberOfRecords = 0
            while data != None:
                numberOfRecords = numberOfRecords +1
                (transId,name,timestamp,price,barcode) = data
                name
                toWrite = str(transId) + ';' + name + ';' + str(barcode) + ';' + str(price) + ';' + str(timestamp) + '\n'
                fileToWrite.write(toWrite.encode('utf8'))
                data = cur.fetchone()
            adminGenerateF.delete(0,END)
            adminGenerateT.delete(0,END)
            tkMessageBox.showinfo("Lyckades"," Sparade " + str(numberOfRecords) + 
                " transaktioner till: " + str(fileToWrite.name),parent=adminroot)
            fileToWrite.close()
        else:
            tkMessageBox.showerror("Fel","Inte en giltig fil, avbryter.",parent=adminroot)
    
    def quitadmin(*args):
        adminroot.destroy()
        
    def copySelected(*args):
        #how to get which thing is selected
        item = adminProductTable.focus()
        if not item == '':
            values = adminProductTable.item(item)
            values =  values['values']
            #barcode,price,name,category
        
            #How to update the fields
            adminUpdateBarcode.delete(0, END)
            adminUpdateBarcode.insert(0, str(values[0]))
        
            adminUpdatePrice.delete(0, END)
            adminUpdatePrice.insert(0, str(values[1]))
        
            adminUpdateName.delete(0, END)
            adminUpdateName.insert(0, values[2])
        
            adminUpdateCategory.set(values[3])
        else:
            tkMessageBox.showinfo("Fel"," Ingen produkt markerad")
        
    #GUI definitions bellow ------
    
    #Expanding row and columns
    adminroot.grid_rowconfigure(2,weight=1)
    adminroot.grid_columnconfigure(2,weight=1)

    #admin Products table
    adminProductFrame = Frame(adminroot)
    adminProductFrame.grid(column=0,row=1,columnspan=1,padx=(ADMINBORDERPAD,0),sticky=W)

    adminProductLabelFrame = LabelFrame(adminProductFrame, text="Produkter", padx=5,pady=5)
    adminProductLabelFrame.grid()

    adminProductScroll = Scrollbar(adminProductLabelFrame)
    adminProductScroll.grid(column=1,row=0,sticky=N+S)
    
    adminProductTable = ttk.Treeview(adminProductLabelFrame,columns=("S_barcode","I_price","S_name","S_category"),
        height=ADMINTRANSNUMBER,yscrollcommand=adminProductScroll.set,selectmode="browse")
    adminProductTable['show'] = 'headings'
    adminProductTable.column("I_price",width=75,anchor="center")
    adminProductTable.column("S_barcode",width=125,anchor="center")
    adminProductTable.column("S_name",width=200,anchor="center")
    adminProductTable.column("S_category",width=100,anchor="center")
    adminProductTable.heading("0", text="Streckkod",command=lambda: treeview_sort_column(adminProductTable, "S_barcode", False,False))
    adminProductTable.heading("1", text="Pris",command=lambda: treeview_sort_column(adminProductTable, "I_price", False,False))
    adminProductTable.heading("2", text="Namn",command=lambda: treeview_sort_column(adminProductTable, "S_name", False,False))
    adminProductTable.heading("3", text="Kategori",command=lambda: treeview_sort_column(adminProductTable, "S_category", False,False))
    adminProductTable.grid(column=0,row=0)
    adminProductTable.lastCol = None
    adminProductTable.lastReverse = None

    adminProductScroll.config(command=adminProductTable.yview)
    
    #admin transaction table
    adminTransactionFrame = Frame(adminroot)
    adminTransactionFrame.grid(column=2,row=1,pady=(ADMINBORDERPAD,),padx=(0,ADMINBORDERPAD),sticky=E)

    adminTransactionLF= LabelFrame(adminTransactionFrame, text="Transaktioner", padx=5,pady=5)
    adminTransactionLF.grid()

    adminTransactionTableScroll = Scrollbar(adminTransactionLF)
    adminTransactionTableScroll.grid(column=1,row=0,sticky=N+S)
    
    adminTransactionTable = ttk.Treeview(adminTransactionLF,columns=("id","name","barcode","price","time"),
        height=ADMINTRANSNUMBER,yscrollcommand=adminTransactionTableScroll.set,selectmode="browse")
    adminTransactionTable['show'] = 'headings'
    adminTransactionTable.column("id",width=75,anchor="center")
    adminTransactionTable.column("name",width=125,anchor="center")
    adminTransactionTable.column("barcode",width=125,anchor="center")
    adminTransactionTable.column("price",width=75,anchor="center")
    adminTransactionTable.column("time",width=150,anchor="center")
    adminTransactionTable.heading("0", text="Id")
    adminTransactionTable.heading("1", text="Namn")
    adminTransactionTable.heading("2", text="Strckkod")
    adminTransactionTable.heading("3", text="Pris")
    adminTransactionTable.heading("4", text="Tid")
    adminTransactionTable.grid(column=0,row=0,sticky=W)

    adminTransactionTableScroll.config(command=adminTransactionTable.yview)

    #admin product modification
    adminProductModificationFrame = Frame(adminroot)
    adminProductModificationFrame.grid(column=0,row=3,padx=(ADMINBORDERPAD,0),pady=(0,ADMINBORDERPAD),sticky=W)

    #Delete product        
    adminDeleteProductLF = LabelFrame(adminProductModificationFrame, 
        text="Ta bort en produkt, ingen sådan produkt kan vara såld!", padx=5,pady=5)
    adminDeleteProductLF.grid(sticky=W,column=0,row=0)

    adminDeleteLF = LabelFrame(adminDeleteProductLF, text="Streckkod, 13 siffror", padx=5,pady=5)
    adminDeleteLF.grid(sticky=W)
    adminDeleteBarcode = Entry(adminDeleteLF,width=18)
    adminDeleteBarcode.grid(column=0,row=0)

    adminDeleteOK = Button(adminDeleteProductLF, text="OK",height=1,command=deleteAProduct,font=("Helvetica",12))
    adminDeleteOK.grid(column=4,row=0,padx=(5,0))
    adminDeleteOK.bind('<Return>',deleteAProduct)
    
    #Copy button
    adminUpdateCopy = Button(adminProductModificationFrame, text="kopiera",height=1,command=copySelected,font=("Helvetica",12))
    adminUpdateCopy.grid(column=1,row=0,padx=(5,0))
    adminUpdateCopy.bind('<Return>',copySelected)
    
    #Update product
    adminUpdateProductLF = LabelFrame(adminProductModificationFrame, 
        text="Uppdatera befintlig produkt, skriv in befintlig streckkod, streckkod kan ej ändras", padx=5,pady=5)
    adminUpdateProductLF.grid(sticky=W,column=0,row=1,columnspan=2)

    uppLF = LabelFrame(adminUpdateProductLF, text="Streckkod, 13 siffror", padx=5,pady=5)
    uppLF.grid(sticky=W)
    adminUpdateBarcode = Entry(uppLF,width=15)
    adminUpdateBarcode.grid(column=0,row=0)

    uppLF2 = LabelFrame(adminUpdateProductLF, text="Nytt Pris", padx=5,pady=5)
    uppLF2.grid(column=1,row=0)
    adminUpdatePrice = Entry(uppLF2,width=5)
    adminUpdatePrice.grid(column=0,row=0)

    uppLF3 = LabelFrame(adminUpdateProductLF, text="Nytt Namn", padx=5,pady=5)
    uppLF3.grid(column=2,row=0)
    adminUpdateName = Entry(uppLF3,width=18)
    adminUpdateName.grid(column=0,row=0)

    uppLF4 = LabelFrame(adminUpdateProductLF, text="Ny Kategori", padx=5,pady=5)
    uppLF4.grid(column=3,row=0)
    adminUpdateCategory = ttk.Combobox(uppLF4,width=12)
    adminUpdateCategory.grid(column=0,row=0)

    adminUpdateOK = Button(adminUpdateProductLF, text="OK",height=1,command=updateAProduct,font=("Helvetica",12))
    adminUpdateOK.grid(column=4,row=0,padx=(5,0))
    adminUpdateOK.bind('<Return>',updateAProduct)
    
    #Add new product
    addproLF = LabelFrame(adminProductModificationFrame, text="Lägg till ny produkt", padx=5,pady=5)
    addproLF.grid(sticky=W,column=0,row=2,columnspan=2)

    pg3 = LabelFrame(addproLF, text="Streckkod, 13 siffror", padx=5,pady=5)
    pg3.grid(sticky=W)
    adminbarcode = Entry(pg3,width=15)
    adminbarcode.grid(column=0,row=0)

    pg4 = LabelFrame(addproLF, text="Pris", padx=5,pady=5)
    pg4.grid(column=1,row=0)
    adminprice = Entry(pg4,width=5)
    adminprice.grid(column=0,row=0)

    pg5 = LabelFrame(addproLF, text="Namn", padx=5,pady=5)
    pg5.grid(column=2,row=0)
    adminname = Entry(pg5,width=18)
    adminname.grid(column=0,row=0)

    pg6 = LabelFrame(addproLF, text="Kategori", padx=5,pady=5)
    pg6.grid(column=3,row=0)
    adminCatCombo = ttk.Combobox(pg6,width=12)
    adminCatCombo.grid(column=0,row=0)
    
    adminOK = Button(addproLF, text="OK",height=1,command=insertNewProduct,font=("Helvetica",12))
    adminOK.grid(row=0,column=4,padx=(5,0))
    adminOK.bind('<Return>',insertNewProduct)

    #More admin stuff
    adminStuffFrame = Frame(adminroot)
    adminStuffFrame.grid(column=2,row=3,padx=(0,ADMINBORDERPAD),pady=(0,ADMINBORDERPAD))

    #Delete transaction
    adminDeleteTransLF = LabelFrame(adminStuffFrame, text="Ta bort en transaktion", padx=5,pady=5)
    adminDeleteTransLF.grid(sticky=W,column=0,row=0)

    adminDeleteTLF = LabelFrame(adminDeleteTransLF, text="Transaktions Id", padx=5,pady=5)
    adminDeleteTLF.grid(sticky=W)
    adminDeleteId = Entry(adminDeleteTLF,width=18)
    adminDeleteId.grid(column=0,row=0)

    adminDeleteTOK = Button(adminDeleteTransLF, text="OK",height=1,command=deleteTransaction,font=("Helvetica",12))
    adminDeleteTOK.grid(column=4,row=0,pady=(0,0),padx=(5,0))
    adminDeleteTOK.bind('<Return>',deleteTransaction)

    #Table with inventeringar
    adminInvTableLF= LabelFrame(adminStuffFrame, text="Inventeringar", padx=5,pady=5)
    adminInvTableLF.grid(column=0,row=1,sticky=W)
    
    adminInvTableScroll = Scrollbar(adminInvTableLF)
    adminInvTableScroll.grid(column=1,row=0,sticky=N+S)
    
    adminInvTable = ttk.Treeview(adminInvTableLF,columns=("id","time"),height=5,yscrollcommand=adminInvTableScroll.set)
    adminInvTable['show'] = 'headings'
    adminInvTable.column("id",width=100,anchor="center")
    adminInvTable.column("time",width=150,anchor="center")
    adminInvTable.heading("0", text="Id")
    adminInvTable.heading("1", text="Tid")
    adminInvTable.grid(column=0,row=0,sticky=W)

    adminInvTableScroll.config(command=adminInvTable.yview)

    #Generate a report
    adminGenerateLF = LabelFrame(adminStuffFrame, text="Exportera till excel", padx=5,pady=5)
    adminGenerateLF.grid(sticky=W,column=0,row=2)

    adminGenerateFLF = LabelFrame(adminGenerateLF, text="Från id", padx=5,pady=5)
    adminGenerateFLF.grid(sticky=W,column=0,row=0)
    adminGenerateF = Entry(adminGenerateFLF,width=10)
    adminGenerateF.grid(column=0,row=0)

    adminGenerateTLF = LabelFrame(adminGenerateLF, text="till id", padx=5,pady=5)
    adminGenerateTLF.grid(sticky=W,column=1,row=0)
    adminGenerateT = Entry(adminGenerateTLF,width=10)
    adminGenerateT.grid(column=0,row=0)

    adminGenerateButton = Button(adminGenerateLF, text="Spara som..",height=2,command=generateReport)
    adminGenerateButton.grid(column=2,row=0,padx=(5,0))
    adminGenerateButton.bind('<Return>',generateReport)

    #close button
    adminCloseButton = Button(adminStuffFrame, text="Stäng",height=2,width=10,command=quitadmin)
    adminCloseButton.grid(column=4,row=1,padx=(5,0))
    adminCloseButton.bind('<Return>',quitadmin)

    adminfullscreen()
    adminupdate()
    adminroot.bind("<Escape>",quitadmin)
    adminDeleteBarcode.focus_set()
        
def addToTable(barcode,price,name):   
    global STACK
    global PRICE
    if len(STACK) != STACKTABLEHEIGHT:
        stackId = stack.insert("","end",values=(name,price))
        PRICE = PRICE + price
        rootPrice.set(str(PRICE) + "kr")
        STACK.append((barcode,name,price,stackId))
        saleButtonList[len(STACK)-1].lift()
        return True
    else:
        root.bell()
        showerror("Fel","max antal varor")
        return False
   
#The "main" entry box here
def addToStack(*args):
    global STACK
    global PRICE
    temp = streckkodEntry.get()
    streckkodEntry.delete(0,END)
    if len(temp) in BARLEN and temp.isdigit():
        (price,name) = getPriceAndName(cur,temp)
        if price != -1:
            addToTable(temp,price,name)
        else:
            root.bell()
            showerror("Fel",name)
    elif temp == "" or temp == "OK":
        gradientList = []
        for i in range(len(STACK)):
            gradientList.append(str(i))
            saleButtonList[i].lower()
        for i in STACK:
            (barcode,name,price,stackId) = i
            insertTransactionNoCommit(cur,con,barcode,price)
        con.commit()
        for i in stack.get_children():
            stack.delete(i)
        STACK = []
        PRICE = 0
        rootPrice.set(str(PRICE) + "kr")
        rootUpdate()
        gradient(gradientList,0)
    elif temp[0] == '*' or temp[0] == '+':
        sign = temp[0]
        temp = temp[1:]
        if temp.isdigit() and int(temp) <= STACKTABLEHEIGHT and int(temp) >0:
            if STACK != []:
                if sign == '*':
                    for i in range(int(temp)-1):
                        if not addToTable(STACK[-1][0],STACK[-1][2],STACK[-1][1]):
                            break
                elif sign == '+':
                    for i in range(int(temp)):
                        if not addToTable(STACK[-1][0],STACK[-1][2],STACK[-1][1]):
                            break
            else:
                root.bell()
                tkMessageBox.showerror("Fel","Finns ingen föregående produkt att lägga till")
        else:
            root.bell()
            tkMessageBox.showerror("Fel", '"' + temp + '"' + " är inte en siffra mindre än: " + str(STACKTABLEHEIGHT) )
    elif temp == "admin" or temp == "01234":
        admin()
    elif temp == "stats" or temp == "98765":
        stats()
    elif temp == "datamining" or temp == "0258":
        dataMining()
    elif temp == "exit" or temp == "0/0" or temp == "1337/1337":
        rootExit()
    elif temp.isdigit():
        root.bell()
        showerror("Fel", '"' + temp + '"' + " har fel antal siffror i streckkoden.")
    else:
        root.bell()
        showerror("Fel", '"' + temp + '"' + " är inte en giltig streckkod")

def rootExit():
    if STACK == []:
        root.destroy()
    elif tkMessageBox.askyesno("Säker?","Ska du avluta med produkter i stacken?"):
        root.destroy()
        
def showerror(header,text):
    global CONT
    CONT = True #start flash
    a = root.after(1,lambda:flash(True))
    tkMessageBox.showerror(header,text)
    CONT = False #Stop flashing here
        
def removeFromStack(index):
    global PRICE,STACK
    saleButtonList[len(STACK)-1].lower()
    PRICE = PRICE - STACK[index][2]
    rootPrice.set(str(PRICE)+"kr")
    stack.delete(STACK[index][3])
    STACK.pop(index)

def removeFromTransactions(index):
    if (index < len(DATA)):
        if tkMessageBox.askyesno("Säker?","Ska du ta bort: \n" + "Id: " +
                str(DATA[index][0]) + "\n Namn:" + DATA[index][1]+ "\nPris:  " +
                str(DATA[index][3]) + "\n Tid: " + str(DATA[index][2])):
            deleteTransactionById(cur,con,DATA[index][0])
            rootUpdate()
    else:
        tkMessageBox.showerror("Fel","Finns inget att ta bort")
        
        
def fullscreen():
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.overrideredirect(1)
    root.attributes('-fullscreen', True)
    root.geometry("%dx%d+0+0" % (w, h))
    #takeFocus()
  
#Flash background when error!
def flash(state):  
    global CONT
    if CONT:
        if state:
            root.configure(background = 'red')
        else:
            root.configure(background = ORIGCOLOR)
        root.after(500,lambda:flash(not state))
    else:
        root.configure(background = ORIGCOLOR)
    
#False on file does not exist or is sqlite3
#True on file exists and is not sqlite3
def isNotSQLite3(filename):
    from os.path import isfile

    if isfile(filename):
        with open(filename, 'rb') as fd:
            header = fd.read(100)
            if header[:16] == 'SQLite format 3\x00':
                return False
            else:
                return True
                
    return False
    
#creation of main window  
root = Tk()
root.geometry("1024x1000") #A initizial window size

#save original color
ORIGCOLOR = root['bg']

#Makes all exception appear in a popup insted of in terminal.
root.report_callback_exception = show_error

#------------------------    

if isNotSQLite3(PATH):
    raise IOError('The database file already exists and is not a Sqlite3 file')


#Open database
con = lite.connect(PATH)
cur = con.cursor()

#Turn on foreign keys check, not really necessary..
cur.execute('PRAGMA foreign_keys = ON') 
data = cur.fetchall()
con.commit()

#Check if some table does not exist inside, otherwise create it.
data = getTableWithName(cur,'products')
if data == []:
    CreateProductsTable(cur,con)
    
data = getTableWithName(cur,'transactions')
if data == []:
    CreateTransactionsTable(cur,con)
    
data = getTableWithName(cur,'transactionChanges')
if data == []:
    CreateTransactionChangesTable(cur,con)
    cur.execute("""/*This is when when we search for the exsistence of a sold product so
      we dont delete its product data.*/
    CREATE INDEX index_transactions_barcode on transactions (barcode);""")
    con.commit()
    


#------------------------

#The X buttons are images converted into base64 and saved here in source code
#Image to button: print "icon='''\\\n" + base64.encodestring(open("icon.gif").read(  )) + "'''"

#the X icon image
icon='''\
R0lGODlhDQAOAPcAAPDwq/oAAP8AAPqr8PDw8PDw8PDw8PDw8PDw8PDwzvc2AP8ANvfO8PDw8PDO
h/wAAP8AYPXw8PDw8PDw8PDw8PDw8PVgAP8AAPqr8PDw8PDw8PDw8PKHNv8AAP9gq/Dw8PDw8PDw
8PCrYP8AAP9gq/Dw8PDw8PDw8PDw8PDwzvc2AP8AAPqr8PDw8PDOh/wAAP82h/Lw8PDw8PDw8PDw
8PDw8PDw8PDwq/oAAP8AYPXwzvc2AP8ANvfO8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PCrYP8AAP8A
AP8AAPqr8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PVgAP8AAP9gq/Dw8PDw8PDw8PDw8PDw
8PDw8PDw8PDw8PDw8PDOh/wAAP8AAP8ANvfO8PDw8PDw8PDw8PDw8PDw8PDw8PDw8PDwzvc2AP8A
NveHYP8AAP8AYPXw8PDw8PDw8PDw8PDw8PDw8PDw8PVgAP8AAPyHzvDw8PKHNv8AAP9gq/Dw8PDw
8PDw8PDw8PDw8PCrYP8AAP82h/Lw8PDw8PDwzvc2AP8AAPqr8PDw8PDw8PDw8PDwq/oAAP8ANvfO
8PDw8PDw8PDw8PDOh/wAAP8ANvfO8PDw8PDwzvc2AP8AAPqr8PDw8PDw8PDw8PDw8PDw8PKHNv8A
AP82h/Lw8PKHNv8AAP9gq/Dw8PDw8PDw8PDw8PDw8PDw8PDwzvc2AP8AAPyHzgAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAAAALAAAAAANAA4A
AAjPAAEEEDCAQAEDBxAkULCAQQMHDyBEkDCBQgULFzBk0LCBQwcPH0CEEDGCRAkTJ1CkULGCRQsX
L2DEkDGDRg0bN3Dk0LGDRw8fP4AEETKESBEjR5AkUbKESRMnT6BEkTKFShUrV7Bk0bKFSxcvX8CE
ETOGTBkzZ9CkUbOGTRs3b+DEkTOHTh07d/Dk0bOHTx8/fwAFEjSIUCFDhxAlUrSIUSNHjyBFkjSJ
UiVLlzBl0rSJUydPn0CFEjWKVClTp1ClUrWKVStXr2DFkjWLVq2AADs=
'''
photo = PhotoImage(data=icon)

#Add expanding row and columns
root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(2,weight=1)
root.grid_columnconfigure(3,weight=1)
root.grid_columnconfigure(5,weight=1)

oldgroup = Frame()
oldgroup.grid(column=4,row=0,padx=(0,BORDERPAD),pady=(BORDERPAD,0),rowspan=5,sticky=N)

senaste = Label(oldgroup, text="Senaste köpen", font=("Helvetica",20))
senaste.grid(column=0,row=0,sticky=W)

#So we can acess the entry later on and delete it.
tagList = []
for i in range(TRANSNUMBER):
    tagList.append(str(i))

    
#Last transactions table
transactionTable = ttk.Treeview(oldgroup,columns=("id","name","price","time"),selectmode="none",height=TRANSNUMBER)
transactionTable['show'] = 'headings'
transactionTable.column("id",width=50,anchor="center")
transactionTable.column("name",anchor="center")
transactionTable.column("price",width=100,anchor="center")
transactionTable.column("time",anchor="center")
transactionTable.heading("0", text="Id",command=takeFocus)
transactionTable.heading("1", text="Namn",command=takeFocus)
transactionTable.heading("2", text="Pris",command=takeFocus)
transactionTable.heading("3", text="Tid",command=takeFocus)
transactionTableIds = []
#Fill it with empty things, modify these entries later.
for i in range(TRANSNUMBER):
    transactionTableIds.append(transactionTable.insert("",0,values=("","","",""),tag=tagList[i]))
transactionTable.grid(column=0,row=1,sticky=W,rowspan=TRANSNUMBER)

transactionButtonList = []
transactionButtonList.append(Button(oldgroup,image=photo,command=lambda:removeFromTransactions(TRANSNUMBER-1)))
transactionButtonList[0].grid(column=1,row=1,pady=(15,0),padx=(5,0),sticky=W+N)

#Create X buttons in transaction list
for i in range(1,TRANSNUMBER):
    index = TRANSNUMBER-i-1
    transactionButtonList.append(Button(oldgroup,image=photo,command=lambda index=index:removeFromTransactions(index)))
    transactionButtonList[i].grid(column=1,row=i+1,padx=(5,0),sticky=W+N)

salegroup = Frame()
salegroup.grid(column=0,row=4,padx=(BORDERPAD,0),pady=(0,BORDERPAD),sticky=W)

#Stack table
stack = ttk.Treeview(salegroup,columns=("name","price"),height=13,selectmode="none")
stack['show'] = 'headings'
stack.column("price",width=100,anchor="center")
stack.column("name",anchor="center")
stack.heading("0", text="Namn",command=takeFocus)
stack.heading("1", text="Pris",command=takeFocus)
stack.grid(column=0,row=0,columnspan=3,sticky=W,rowspan=13)

#Barcode entry
streckkodEntry = Entry(salegroup,width=27) #edit the number for barcode-field width
streckkodEntry.grid(column=1,row=13,sticky=E,columnspan=2)
streckkodEntry.focus()

streckkodLabel = Label(salegroup,text="Streckkod:")
streckkodLabel.grid(column=0,row=13,sticky=W)

betalaLabel = Label(salegroup, text="ATT BETALA:", font=("Helvetica",25))
betalaLabel.grid(column=0,row=14,sticky=W,columnspan=2)

rootPrice = StringVar()
rootPrice.set("0kr")
priceLabel = Label(salegroup, textvariable=rootPrice, font=("Helvetica",25),fg="blue")
priceLabel.grid(column=2,row=14,sticky=E,padx=(0,10))

#Cover to be able to hide X buttons on stack table
cover = Canvas(salegroup, width=50, height=295,selectborderwidth=0)
cover.create_rectangle(0,0,50,295, fill="",outline=salegroup.cget('bg'))
cover.grid(column=3,row=0,rowspan=14,sticky=W+N)


#Deletebuttons on stack table
saleButtonList = []
saleButtonList.append(Button(salegroup,image=photo,command=lambda:removeFromStack(0)))
saleButtonList[0].grid(column=3,row=0,pady=(15,0),padx=(5,0),sticky=W+N)
saleButtonList[0].lower()

#Delete X buttons on stack table
for i in range(1,13):
    saleButtonList.append(Button(salegroup,image=photo,command=lambda i=i:removeFromStack(i)))
    saleButtonList[i].grid(column=3,row=i,padx=(5,0),sticky=W+N)
    saleButtonList[i].lower()

betalaButton = Button(salegroup, text="BETALA",height=2,width=10,bg="#1fe01f",command=addToStack)
betalaButton.grid(column=3,row=14,sticky=E+W+N+S,padx=(5,0))
# if u want larget font:, font=("Helvetica",12)

#Time
rootTime = StringVar()
now = datetime.datetime.now().strftime("%H:%M:%S")
rootTime.set(now)
q = Label(root, textvariable=rootTime, font=("Helvetica",CLOCKSIZE),fg="red")
q.grid(column=0,row=1,columnspan=4)


#The clock update function (and gui reset)
def clock():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    rootTime.set(now)
    
    #Users dont mess with table size
    if transactionTable.column("name")["width"] != 200:
        transactionTable.column("name",width=200)
        takeFocus()
    if transactionTable.column("id")["width"] != 50:
        transactionTable.column("id",width=50)
        takeFocus()
    if transactionTable.column("price")["width"] != 100:
        transactionTable.column("price",width=100)
        takeFocus()
    if transactionTable.column("time")["width"] != 200:
        transactionTable.column("time",width=200)
        takeFocus()
    if stack.column("name")["width"] != 200:
        stack.column("name",width=200)
        takeFocus()
    if stack.column("price")["width"] != 100:
        stack.column("price",width=100)
        takeFocus()
    root.after(100,clock)
    
#A few functions that starts stuff
fullscreen()
enable()
rootUpdate()
clock()
takeFocus()
root.mainloop() #the thing that starts everything
#We can only view error messages after this have ran.




