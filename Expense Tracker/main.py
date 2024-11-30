from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkcalendar import DateEntry
from datetime import date
import datetime
import sqlite3
from tkcalendar import DateEntry

def listAllExpenses():
    global dbconnector,data_table
    data_table.delete(*data_table.get_children())
    all_data = dbconnector.execute('SELECT * FROM ExpenseTracker') 
    data=all_data.fetchall()
    for val in data:
        data_table.insert('',END,values=val)

def viewExpenseInfo():
    global data_table
    global dataField,payee,description,amount,modeOfPayment
    if not data_table.selection():
        mb.showerror('No expense selected','Please select van expense from the table to view its details')
    currentSelectedExpense=data_table.item(data_table.focus())
    val = currentSelectedExpense['values']
    expenditureDate=datetime.date(int(val[1][:4]),int(val[1][5:7]),int(val[1][8:]))
    dataField.set_data(expenditureDate); payee.set(val[2]);description.set(val[3]);amount.set(val[4]);modeOfPayment.set(val[5])

def clearFields():
    global description,payee,amount,modeOfPayment,dataField,data_table
    todayDate=datetime.datetime.now().date()
    description.set('');payee.set('');amount.set(0.0);modeOfPayment.set('Cash');dateField.set_date(todayDate)
    data_table.selection_remove(*data_table.selection())

def removeExpense():
    if not data_table.selection():
        mb.showerror('No record selected!','Please select a record to delete')
        return
    currentSelectedExpense=data_table.item(data_table.focus())
    valuesSelected=currentSelectedExpense['values']
    confirmation=mb.askyesno('Are you sure?',f'Are you sure that you want to delete the record of {valuesSelected[2]}')
    if confirmation:
        dbconnector.execute('DELETE FROM ExpenseTracker WHERE ID=%d'%valuesSelected[0])
        dbconnector.commit()
        listAllExpenses()
        mb.showinfo('Record deleted successfully!','The record you wanted to delete has been delected successfully')

def removeAllExpenses():
    confirmation=mb.askyesno('Are you sure?','Are you sure that you want to delete all the expense items from the database?',icon='warning')
    if confirmation:
        data_table.delete(*data_table.get_children())
        dbconnector.execute('DELETE FROM ExpenseTracker')
        dbconnector.commit()
        clearFields()
        listAllExpenses()
        mb.showinfo('All Expenses deleted','All the expenses were successfully deleted')
    else:
        mb.showinfo('Ok then','The task was aborted and no expense was deleted!')

def addAnotherExpense():
    global dateField,payee,description,amount,modeOfPayment
    global dbconnector
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():
        mb.showerror('Fields empty!',"Please fill all the missing fields before pressing the add button!")
        dbconnector.execute('INSERT INTO ExpenseTracker(Date,Payee,Description,Amount,ModeOfPayment)VALUES(?,?,?,?,?)',(dateField.get_date(),payee.get(),description.get(),amount.get(),modeOfPayment.get())
        )
        dbconnector.commit()
        clearFields()
        listAllExpenses()
        mb.showinfo('Expense added','The expense whose details you just entered has been added to the database')

def editExpense():
    global data_table
    def editExistingExpense():
        global dateField,amount,description,payee,modeOfPayment
        global dbconnector,data_table
        currentSelectedExpense=data_table.item(data_table.focus())
        content=currentSelectedExpense['values']
        dbconnector.execute('UPDATE ExpenseTracker SET Date=?,Payee=?,Description=?,Amount=?,ModeOfPayment=? WHEREID=?',(dateField.get_date(),payee.get(),description.get(),modeOfPayment.get(),content[0]))
        dbconnector.commit()
        clearFields()
        listAllExpenses()
        mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')  
        editSelectedButton.destroy()  
          
    if not data_table.selection():  
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')  
        return  
          
    viewExpenseInfo()  
    editSelectedButton = Button(  
        frameL3,  
        text = "Edit Expense",  
        font = ("Helvetica", "13"),  
        width = 30,  
        bg = "#90EE90",  
        fg = "#000000",  
        relief = GROOVE,  
        activebackground = "#008000",  
        activeforeground = "#98FB98",  
        command = editExistingExpense  
        )  
    editSelectedButton.grid(row = 0, column = 0, sticky = W, padx = 50, pady = 10)

def selectedExpenseToWords():    
    global data_table  
    if not data_table.selection():  
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')  
        return  
    currentSelectedExpense = data_table.item(data_table.focus())  
    val = currentSelectedExpense['values']  
    msg = f'Your expense can be read like: \n"You paid {val[4]} to {val[2]} for {val[3]} on {val[1]} via {val[5]}"'  
    mb.showinfo('Here\'s how to read your expense', msg)

def expenseToWordsBeforeAdding():    
    global dateField, description, amount, payee, modeOfPayment  
    if not dateField.get() or not payee.get() or not description.get() or not amount.get() or not modeOfPayment.get():  
        mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')  
    else:  
        msg = f'Your expense can be read like: \n"You paid {amount.get()} to {payee.get()} for {description.get()} on {dateField.get_date()} via {modeOfPayment.get()}"'     
    addQuestion = mb.askyesno('Read your record like: ', f'{msg}\n\nShould I add it to the database?')  
    if addQuestion:  
        addAnotherExpense()  
    else:  
        mb.showinfo('Ok', 'Please take your time to add this record')  

if __name__ == "__main__":  
    dbconnector = sqlite3.connect("Expense_Tracker.db")  
    dbcursor = dbconnector.cursor()  
    dbconnector.execute(  
        'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT)'  
    )  
    dbconnector.commit()  

main_win = Tk()  
main_win.title("EXPENSE TRACKER")  
main_win.geometry("1415x650+400+100")  
main_win.resizable(0, 0)  
main_win.config(bg = "#FFFAF0")  
#main_win.iconbitmap("./piggyBank.ico")
frameLeft = Frame(main_win, bg = "#FFF8DC")  
frameRight = Frame(main_win, bg = "#DEB887")  
frameL1 = Frame(frameLeft, bg = "#FFF8DC")  
frameL2 = Frame(frameLeft, bg = "#FFF8DC")  
frameL3 = Frame(frameLeft, bg = "#FFF8DC")  
frameR1 = Frame(frameRight, bg = "#DEB887")  
frameR2 = Frame(frameRight, bg = "#DEB887")  
frameLeft.pack(side=LEFT, fill = "both")  
frameRight.pack(side = RIGHT, fill = "both", expand = True)  
frameL1.pack(fill = "both")  
frameL2.pack(fill = "both")  
frameL3.pack(fill = "both")  
frameR1.pack(fill = "both")  
frameR2.pack(fill = "both", expand = True)

headingLabel = Label(  
    frameL1,  
    text = "EXPENSE TRACKER",  
    font = ("Helvetica", "25"),  
    width = 20,  
    bg = "#8B4513",  
    fg = "#FFFAF0"  
    )  
  
subheadingLabel = Label(  
    frameL1,  
    text = "Data Entry Frame",  
    font = ("Helvetica", "15"),  
    width = 20,  
    bg = "#F5DEB3",  
    fg = "#000000"  
    )  
  
headingLabel.pack(fill = "both")  
subheadingLabel.pack(fill = "both")

dateLabel = Label(  
    frameL2,  
    text = "Date:",  
    font = ("Helvetica", "11", "bold"),  
    bg = "#FFF8DC",  
    fg = "#000000"  
    )  
  
descriptionLabel = Label(  
    frameL2,  
    text = "Description:",  
    font = ("Helvetica", "11", "bold"),  
    bg = "#FFF8DC",  
    fg = "#000000"  
    )  
  
amountLabel = Label(  
    frameL2,  
    text = "Amount:",  
    font = ("Helvetica", "11", "bold"),  
    bg = "#FFF8DC",  
    fg = "#000000"  
    )  
  
payeeLabel = Label(  
    frameL2,  
    text = "Payee:",  
    font = ("Helvetica", "11", "bold"),  
    bg = "#FFF8DC",  
    fg = "#000000"  
    )  
  
modeLabel = Label(  
    frameL2,  
    text = "Mode of \nPayment:",  
    font = ("Helvetica", "11", "bold"),  
    bg = "#FFF8DC",  
    fg = "#000000"  
    )  
  
dateLabel.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)      
descriptionLabel.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)      
amountLabel.grid(row = 2, column = 0, sticky = W, padx = 10, pady = 10)      
payeeLabel.grid(row = 3, column = 0, sticky = W, padx = 10, pady = 10)      
modeLabel.grid(row = 4, column = 0, sticky = W, padx = 10, pady = 10)      
  
description = StringVar()  
payee = StringVar()  
modeOfPayment = StringVar(value = "Cash")  
amount = DoubleVar()  
  
dateField = DateEntry(  
    frameL2,  
    date = datetime.datetime.now().date(),  
    font = ("Helvetica", "11"),  
    relief = GROOVE  
    )  
  
descriptionField = Entry(  
    frameL2,  
    text = description,  
    width = 20,  
    font = ("Helvetica", "11"),  
    bg = "#FFFFFF",  
    fg = "#000000",  
    relief = GROOVE  
    )  
  
amountField = Entry(  
    frameL2,  
    text = amount,  
    width = 20,  
    font = ("Helvetica", "11"),  
    bg = "#FFFFFF",  
    fg = "#000000",  
    relief = GROOVE  
    )  
  
payeeField = Entry(  
    frameL2,  
    text = payee,  
    width = 20,  
    font = ("Helvetica", "11"),  
    bg = "#FFFFFF",  
    fg = "#000000",  
    relief = GROOVE  
    )  
  
modeField = OptionMenu(  
    frameL2,  
    modeOfPayment,  
    *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'UPI', 'Paytm', 'Google Pay', 'PhonePe', 'Razorpay']  
    )  
modeField.config(  
    width = 15,  
    font = ("Helvetica", "10"),  
    relief = GROOVE,  
    bg = "#FFFFFF"  
    )  
  
dateField.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)  
descriptionField.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10)  
amountField.grid(row = 2, column = 1, sticky = W, padx = 10, pady = 10)  
payeeField.grid(row = 3, column = 1, sticky = W, padx = 10, pady = 10)  
modeField.grid(row = 4, column = 1, sticky = W, padx = 10, pady = 10)  

insertButton = Button(  
    frameL3,  
    text = "Add Expense",  
    font = ("Helvetica", "13"),  
    width = 30,  
    bg = "#90EE90",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#008000",  
    activeforeground = "#98FB98",  
    command = addAnotherExpense  
    )  
  
convertButton = Button(  
    frameL3,  
    text = "Convert to Text before Adding",  
    font = ("Helvetica", "13"),  
    width = 30,  
    bg = "#90EE90",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#008000",  
    activeforeground = "#98FB98",  
    command = expenseToWordsBeforeAdding  
    )  
  
resetButton = Button(  
    frameL3,  
    text = "Reset the fields",  
    font = ("Helvetica", "13"),  
    width = 30,  
    bg = "#FF0000",  
    fg = "#FFFFFF",  
    relief = GROOVE,  
    activebackground = "#8B0000",  
    activeforeground = "#FFB4B4",  
    command = clearFields  
    )  
  
insertButton.grid(row = 0, column = 0, sticky = W, padx = 50, pady = 10)  
convertButton.grid(row = 1, column = 0, sticky = W, padx = 50, pady = 10)  
resetButton.grid(row = 2, column = 0, sticky = W, padx = 50, pady = 10)

viewButton = Button(  
    frameR1,  
    text = "View Selected Expense\'s Details",  
    font = ("Helvetica", "13"),  
    width = 35,  
    bg = "#FFDEAD",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#A0522D",  
    activeforeground = "#FFF8DC",  
    command = viewExpenseInfo  
    )  
  
editButton = Button(  
    frameR1,  
    text = "Edit Selected Expense",  
    font = ("Helvetica", "13"),  
    width = 35,  
    bg = "#FFDEAD",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#A0522D",  
    activeforeground = "#FFF8DC",  
    command = editExpense  
    )  
  
convertSelectedButton = Button(  
    frameR1,  
    text = "Convert Selected Expense to a Sentence",  
    font = ("Helvetica", "13"),  
    width = 35,  
    bg = "#FFDEAD",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#A0522D",  
    activeforeground = "#FFF8DC",  
    command = selectedExpenseToWords  
    )  
  
deleteButton = Button(  
    frameR1,  
    text = "Delete Selected Expense",  
    font = ("Helvetica", "13"),  
    width = 35,  
    bg = "#FFDEAD",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#A0522D",  
    activeforeground = "#FFF8DC",  
    command = removeExpense  
    )  
  
deleteAllButton = Button(  
    frameR1,  
    text = "Delete All Expense",  
    font = ("Helvetica", "13"),  
    width = 35,  
    bg = "#FFDEAD",  
    fg = "#000000",  
    relief = GROOVE,  
    activebackground = "#A0522D",  
    activeforeground = "#FFF8DC",  
    command = removeAllExpenses  
    )  
  
viewButton.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)  
editButton.grid(row = 0, column = 1, sticky = W, padx = 10, pady = 10)  
convertSelectedButton.grid(row = 0, column = 2, sticky = W, padx = 10, pady = 10)  
deleteButton.grid(row = 1, column = 0, sticky = W, padx = 10, pady = 10)  
deleteAllButton.grid(row = 1, column = 1, sticky = W, padx = 10, pady = 10) 

data_table = ttk.Treeview(  
    frameR2,  
    selectmode = BROWSE,  
    columns = ('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment')  
    )  
  
Xaxis_Scrollbar = Scrollbar(  
    data_table,  
    orient = HORIZONTAL,  
    command = data_table.xview  
    )  
  
Yaxis_Scrollbar = Scrollbar(  
    data_table,  
    orient = VERTICAL,  
    command = data_table.yview  
    )  
  
Xaxis_Scrollbar.pack(side = BOTTOM, fill = X)  
Yaxis_Scrollbar.pack(side = RIGHT, fill = Y)  
  
data_table.config(yscrollcommand = Yaxis_Scrollbar.set, xscrollcommand = Xaxis_Scrollbar.set)  
  
data_table.heading('ID', text = 'S No.', anchor = CENTER)  
data_table.heading('Date', text = 'Date', anchor = CENTER)  
data_table.heading('Payee', text = 'Payee', anchor = CENTER)  
data_table.heading('Description', text = 'Description', anchor = CENTER)  
data_table.heading('Amount', text = 'Amount', anchor = CENTER)  
data_table.heading('Mode of Payment', text = 'Mode of Payment', anchor = CENTER)  
  
data_table.column('#0', width = 0, stretch = NO)  
data_table.column('#1', width = 50, stretch = NO)  
data_table.column('#2', width = 95, stretch = NO)  
data_table.column('#3', width = 150, stretch = NO)  
data_table.column('#4', width = 450, stretch = NO)  
data_table.column('#5', width = 135, stretch = NO)  
data_table.column('#6', width = 140, stretch = NO)  
  
data_table.place(relx = 0, y = 0, relheight = 1, relwidth = 1)

main_win.mainloop()
