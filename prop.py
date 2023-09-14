
'''
import tkinter as tk
import pymysql as sql

def add_table(table_name):
    connection = sql.connect(host="localhost",user="root",database="thrilok",password="")
    cur=connection.cursor()
    qry="CREATE TABLE {table_name} ( id int(3) primary , name varchar(20) not null)"
    cur.execute(qry)
    return 



app=tk.Tk()       #creating an instance for Tk
app.title("My first app")     #title for window



# Create a button 
button1 = tk.Button(app, text="Hi!").grid(row=3,column=0)
button2 = tk.Button(app, text="Bye :-(").grid(row=3,column=1)

lb1=tk.Label(app, text='First Name').grid(row=0)
lb2=tk.Label(app, text='Last Name').grid(row=1)

submit=tk.Button(app,text="Submit").grid(row=2, column=0)


app.mainloop()
'''


import tkinter as tk

config_items=[]
with open("/home/thrilok/Projects/environment/config_list.txt", "r") as file:
    data = file.read()
    data=data.splitlines()
    for line in data:
        config_items.append(line.split(','))
#print(config_items)




def on_button_click(event):
    text = event.widget.cget("text")

    if text == "=":
        try:
            result = eval(screen.get("1.0", tk.END))
            screen.delete("1.0", tk.END)
            screen.insert(tk.END, result)
        except Exception as e:
            screen.delete("1.0", tk.END)
            screen.insert(tk.END, "Error")

    elif text == "C":
        screen.delete("1.0", tk.END)

    else:
        screen.insert(tk.END, text)

root = tk.Tk()
root.geometry("600x720")
root.title("Calculator")

# Entry widget to display and input numbers
screen = tk.Text(root, height=2, width=16, font=("Helvetica", 12), wrap=tk.WORD)
screen.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()



buttons = [
    (".", 4, 0), ("C", 4, 1), ("+", 4, 2),("=", 4, 3)  # Removed colspan for "=" button
]
    
for (text, row, col) in (config_items + buttons):
    button = tk.Button(button_frame, text=text, font=("Helvetica", 12), height=2, width=7)
    button.grid(row=row, column=col)
    button.bind("<Button-1>", on_button_click)



root.mainloop()


