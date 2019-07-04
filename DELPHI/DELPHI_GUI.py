from customer_analysis import *
from tkinter import *
#from tkinter.ttk import *

def filename(): 
        cust_id = entry.get()
        
        if (cust_id==None):
                pred_res=str(delphi())
                entryx.insert("file created successfully!")

        else:
                pred_res=str(delphi_on_id(cust_id))
                entryx.insert(," predicted successfully!")


root = Tk() 

root.title("DELPHI")

customer_id = Label(root, text="ENTER CUSTOMER ID", borderwidth=2, background="goldenrod1") 
customer_id.grid(row=0)


entry = Entry(root,background="LightBlue1") 
entry.grid(row=0, column=1) 
entry.config(highlightbackground="LightBlue1",highlightthickness=2)

entryx = Entry(root,background="LightBlue1") 
entryx.grid(row=1) 
entryx.config(highlightbackground="LightBlue1",highlightthickness=2)


predict_button = Button(root, text="PREDICT", command=filename, bg="goldenrod1") 
predict_button.grid(row=0, column=2)
predict_button.config(highlightbackground="LightBlue1",highlightthickness=2)

root.mainloop() 
