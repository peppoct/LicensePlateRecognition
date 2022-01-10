# import modules
import os
from GUI import set_unregistred_user, content

from tkinter import *
from tkinter import messagebox


# Designing window for registration
global return_value

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.configure(bg='#FFe9FF')
    register_screen.title("Register")
    register_screen.geometry("400x350")

    global username
    global name
    global surname
    global city
    global password
    global username_entry
    global password_entry
    global name_entry
    global surname_entry
    global city_entry

    username = StringVar()
    password = StringVar()
    name = StringVar()
    surname = StringVar()
    city = StringVar()


    Label(register_screen, text="Please enter details below",font=("Arial", 20), bg='#6200EE',fg='#FFFFFF', width="300", height="1").pack()
    Label(register_screen, text="").pack()
    name_lable = Label(register_screen, text="Name * ")
    name_lable.pack()
    name_entry = Entry(register_screen, textvariable=name)
    name_entry.pack()
    surname_lable = Label(register_screen, text="Surname * ")
    surname_lable.pack()
    surname_entry = Entry(register_screen, textvariable=surname)
    surname_entry.pack()
    city_lable = Label(register_screen, text="City * ")
    city_lable.pack()
    city_entry = Entry(register_screen, textvariable=city)
    city_entry.pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen,
           text="Register",
           height=1,fg='#FFFFFF',
           bg='#6200EE',
           activebackground='#3700B3',
           activeforeground='#FFFFFF',
           font=("Comic sans", 12),
           width="15",
           command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.configure(bg='#FFe9FF')
    login_screen.title("Login")
    login_screen.geometry("500x250")
    Label(login_screen, text="Please enter details below to login",font=("Arial", 20), bg='#6200EE',fg='#FFFFFF', width="300", height="1").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen,
           text="Login",
           fg='#FFFFFF',
           bg='#6200EE',
           activebackground='#3700B3',
           activeforeground='#FFFFFF',
           font=("Comic sans", 12),
           width="15",
           height=1,
           command=login_verify).pack()


# Implementing event on register button

def get_users_info(username_info):
    #FILE MUST NOT BE EMPTY
    with open("users", "r") as fp:
        for line in fp.readlines():
            if (line == ""):
                return "", "", "", "", ""
            # This expects each line of a file to be (name, pass) seperated by whitespace
            username, password, name, surname, city= line.split()
            if(username == username_info):
                return username, password, name, surname, city

    return "", "", "", "", ""

def register_user():
    username_info = "".join([c for c in username.get() if (c.isalpha() or c.isnumeric())])
    username_, password_, name_, surname_, city_ = get_users_info(username_info)
    if(username_ == username_info):
        messagebox.showerror( title="Error", message="Username already used")
        return

    password_info = "".join([c for c in password.get() if (c.isalpha() or c.isnumeric())])
    city_info = "".join([c for c in city.get() if (c.isalpha())])
    name_info = "".join([c for c in name.get() if (c.isalpha())])
    surname_info = "".join([c for c in surname.get() if (c.isalpha())])
    if(password_info == "" or city_info == "" or name_info == "" or city_info == ""):
        messagebox.showwarning(title="Error", message="You must fill all the fields")
        return
    file = open("users", "a")
    file.write(username_info +" "+ password_info +" "+ name_info +" "+surname_info+" "+city_info+"\n")
    file.close()

    username_entry.delete(0, END)
    name_entry.delete(0, END)
    password_entry.delete(0, END)
    city_entry.delete(0, END)
    surname_entry.delete(0, END)

    messagebox.showinfo(title = "Registration complited", message ="Registration has been complited")
    global register_screen
    register_screen.destroy()
# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    username_, password_, name_, surname_, city_ = get_users_info(username1)
    if(username_ in ""):
        user_not_found()
        return

    if password_ == password1:
        login_sucess()
        login_screen.destroy()
        main_screen.destroy()
        set_unregistred_user(username_)
        content()
        #os.system('python GUI.py')
    else:
        password_not_recognised()


# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()


# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups
def login_user():
    return_value = ""
    main_account_screen()
    return return_value
def delete_login_success():
    login_success_screen.destroy()


def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.configure(bg='#FFe9FF')
    main_screen.title("Account Login")

    Label(text="Select Your Choice",font=("Arial", 20), bg='#6200EE',fg='#FFFFFF', width="300", height="1").pack()
    Label(text="").pack()
    Button(text="Login",
           height="2",
           fg='#FFFFFF',
           bg='#6200EE',
           activebackground='#3700B3',
           activeforeground='#FFFFFF',
           font=("Comic sans", 12),
           width="15", command=login).pack()
    Label(text="").pack()
    Button(text="Register",
           height="2",
           fg='#FFFFFF',
           bg='#6200EE',
           activebackground='#3700B3',
           activeforeground='#FFFFFF',
           font=("Comic sans", 12),
           width="15", command=register).pack()

    main_screen.mainloop()