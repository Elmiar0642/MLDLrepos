#Libraries Used.......................
from customer_analysis import *
from tkinter import *

def delphi_gen():
        pred_res=str(delphi())
        
def delphi_res(): 
        pred_res=str(delphi_on_id(entry.get()))
        
        
        

root = Tk() 

root.title("DELPHI")

customer_id = Label(root, text="ENTER CUSTOMER ID", borderwidth=2, background="goldenrod1") 
customer_id.grid(row=0,column=1)
'''
Server_name = Label(root, text="ENTER SERVER NAME", borderwidth=2, background="goldenrod1") 
Server_name.grid(row=0)

Database_name = Label(root, text="ENTER DATABASE NAME", borderwidth=2, background="goldenrod1") 
Database_name.grid(row=1)

customer_id = Label(root, text="ENTER CUSTOMER ID", borderwidth=2, background="goldenrod1") 
customer_id.grid(row=0)

customer_id = Label(root, text="ENTER CUSTOMER ID", borderwidth=2, background="goldenrod1") 
customer_id.grid(row=0)
'''

entry = Entry(root,background="LightBlue1") 
entry.grid(row=0, column=1) 
entry.config(highlightbackground="LightBlue1",highlightthickness=2)

predict_button = Button(root, text="PREDICT", command=delphi_res, bg="goldenrod1") 
predict_button.grid(row=0, column=2)
predict_button.config(highlightbackground="LightBlue1",highlightthickness=2)


predict_all_button = Button(root, text="PREDICT ALL", command=delphi_gen, bg="goldenrod1") 
predict_all_button.grid(row=1)
predict_all_button.config(highlightbackground="LightBlue1",highlightthickness=2)

root.mainloop() 
