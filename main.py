from tkinter import *
from tkinter.tix import COLUMN
from tkinter import messagebox
import random
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
  letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

  nr_letters = random.randint(8, 10)
  nr_symbols = random.randint(2, 4)
  nr_numbers = random.randint(2, 4)

  password_letters = [random.choice(letters) for char in range(nr_letters)]
  password_numbers = [random.choice(numbers) for char in range(nr_numbers)]
  password_symbols = [random.choice(symbols ) for char in range(nr_symbols )]

  password_list = password_letters + password_numbers + password_symbols
  random.shuffle(password_list)

  password = "".join(password_list)
 
  password_entry.insert(0, password)
  

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {website: {"email": email, "password": password}} # new_data = {key = website : value = email,password}

    if len(website)==0 or len(password)==0: #if string of the website is equal to 0.
      messagebox.showwarning(title="Not enough", message="Make sure you fill in everything! ")
    
    else:
      is_ok = messagebox.askokcancel(title="Confirm", message= f"You entered: \n Website: {website} \n Email: {email} \n Password: {password} \n Is that all correct?") #type boolean
      if is_ok: #Check errors
        try:
            with open("data.json","r") as data_file:  #r = reads file only
              data = json.load(data_file)

        except FileNotFoundError: #there is an exception - do this instead  
            with open("data.json","w") as data_file:
              json.dump(new_data, data_file, indent=4)

        else:                     #no exception
            data.update(new_data) 

            with open("data.json","w") as data_file:   #w = open/create a file
              json.dump(data, data_file, indent=4) #dump the read data into the file.
        finally:
            website_entry.delete(0, END)    #deletes the entry box string's appearance 
            password_entry.delete(0, END) 

#----------------------FIND EMAIL AND PASSWORD-----------------------#
def find_password():
  website = website_entry.get()
  try:
      with open ("data.json", "r") as data_file:
        data = json.load(data_file)
  except FileNotFoundError:
        messagebox.showerror(message="No data file found")
  else: 
    if website in data:
      email = data[website]["email"]
      password = data[website]["password"]
      messagebox.showinfo(message = f"Your email: {email}\n Your password: {password}")
    else:
      messagebox.showerror(message=f'No details for the website "{website}" exist')
        
    
# ---------------------------- UI SETUP ------------------------------- #
windows = Tk()
windows.title(string= "Password Manager")
windows.config(padx = 40, pady=40)

#canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image = logo_img)
canvas.grid(column=1, row=0)

#website -label - box -
website = Label(text="Website: ")
website.grid(column=0, row=1)

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=2) 
website_entry.focus()                             #cursor focus on this entry box when program starts

#email
email = Label(text="Email: ")
email.grid(column=0, row=2)

email_entry= Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)

#password
password= Label(text="Password: ")
password.grid(column=0, row=3)

password_entry= Entry(width=21)
password_entry.grid(column=1, row=3,columnspan=1)

#password button
password_button = Button(text="Generate Password", command = password_gen)
password_button.grid(column=2, row=3, columnspan=2)

#add button
add=Button(text="Add", width=36, command=save)
add.grid(column=1, row=4, columnspan=2 )

#search button
search = Button(text="Search", command = find_password)
search.grid(column=3, row=1)

windows.mainloop()