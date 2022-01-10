from tkinter import messagebox

from main import detect_plate_video
from main import detect_plate
from main import get_picture_from_camera
from tkinter import filedialog
from tkinter import *
from hangman import start_hangman_game

import tkinter as tk
import csv
global platecharacter_label
global registred_user
global game2

def set_unregistred_user(value):
    global registred_user
    registred_user = value

def get_registred_user_value():
    global registred_user
    return registred_user

def clear_all():
    text_label.place_forget()
    platecharacter_label.place_forget()
    score_window.destroy()

def add_score(score):
    new_classification = ""
    classification_changed = False
    with open("classification", "r") as fp:
        for line in fp.readlines():
            if(line == ""):
                break
            username, score_old = line.split()
            if(get_registred_user_value() == username):
                classification_changed = True
                new_classification = new_classification + username + " "+ str(score+ int(score_old)) + "\n"
            else :
                new_classification = new_classification + username+" "+score_old+ "\n"
    if(classification_changed):
        file = open("classification", "w")
        file.write(new_classification)
        file.close()
    else:
        file = open("classification", "a")
        file.write(get_registred_user_value() + " " +str(score) +"\n")
        file.close()


def show_table():
    classification = []
    count = 0
    with open("classification", "r") as fp:
        for line in fp.readlines():
            if line != "":
                username, score = line.split()
                value = { 'username':username, 'score':int(score)}
                classification.insert(count, value)
                count =count + 1
    print(classification)
    classification.sort(key=lambda x: x.get('score'), reverse=True)
    print(classification)
    output =""
    count = 0
    for values in classification:
        count =count +1
        output = output + str(count) + ") " + str(values.get('username')) + " with score: " + str(values.get('score')) + "\n"

    global table_window
    global score_window
    table_window = Toplevel(window)
    table_window.title("Score Result")
    table_window.configure(bg='#FFe9FF')
    table_window.geometry("300x300")

    Label(table_window, text="TOP 5", font=("Arial", 13), bg='#6200EE',fg='#FFFFFF', width="300", height="2").pack()
    Label(table_window, text=output, font=("Arial", 13), bg='#6200EE',fg='#FFFFFF', width="300", height="10").pack()
    clear_all()

def compute_score(city, platecharacter):
   score = 0
   if(len(city) > 0):
       for char in platecharacter:
           score = score + city.count(char)

   add_score(score)

   global score_window
   score_window = Toplevel(window)
   score_window.title("Score Result")
   score_window.configure(bg='#FFe9FF')
   score_window.geometry("300x300")

   Label(score_window, text="Your score is: "+str(score) +"\nDo you want to check the classification?" ,
         font=("Arial", 13), bg='#6200EE',fg='#FFFFFF', width="300", height="2").pack()
   Label(score_window, text="").pack()
   Label(score_window, text="").pack()
   Button(score_window, text="Yes",
          height="1",
          fg='#FFFFFF',
          bg='#6200EE',
          activebackground='#3700B3',
          activeforeground='#FFFFFF',
          font=("Comic sans", 15),
          width="6", command=show_table).place(relx=0.27, rely=0.5)
   Button(score_window,text="No",
          height="1",
          fg='#FFFFFF',
          bg='#6200EE',
          activebackground='#3700B3',
          activeforeground='#FFFFFF',
          font=("Comic sans", 15),
          width="6", command=clear_all).place(relx=0.55, rely=0.5)

   global game2
   game2.destroy()


def game(text):
   if text == '':
       tk.messagebox.showerror(title="Error",  message="Plate not found")
       return

   platecharacter=''.join([c for c in text if (c.isalpha())])

   text_label.config(text="The following plate has been detected:\n" + text )
   text_label.place(relx=0.5, rely=0.60, anchor="center")
   platecharacter_label.config(text= platecharacter,
                               font=('Helvetica20 italic',18),
                               bg='#FFe9FF',
                               fg='#018786')
   platecharacter_label.place_forget()
   Button(text="Hangman",
          height="2",
          fg='#FFFFFF',
          bg='#6200EE',
          activebackground='#3700B3',
          activeforeground='#FFFFFF',
          font=("Comic sans", 15),
          width="12", command=hangman_game).place(relx= 0.27, rely=0.7)
   Button(text="Game 2",
          height="2",
          fg='#FFFFFF',
          bg='#6200EE',
          activebackground='#3700B3',
          activeforeground='#FFFFFF',
          font=("Comic sans", 15),
          width="12", command=game2).place(relx= 0.55, rely=0.7)
   #

def game2():
    global game2
    game2 = Toplevel(window)
    game2.title("GAME 2")
    game2.geometry("300x300")

    platecharacter = platecharacter_label.cget("text")
    Label(game2, text="Please insert an Italian city that contains\nmost of the following letters: \n", font=("Arial", 13), bg='#6200EE',fg='#FFFFFF', width="300", height="3").pack()
    Label(game2, text=platecharacter, font=("Arial", 15), bg='#6200EE',fg='red', width="300", height="1").place(relx=0.5, rely=0.20,anchor="center")
    global input_label
    input_label = Entry(game2)
    input_label.place(relx=0.5, rely=0.35, anchor="center")
    Button(game2, text="Check",
           height="1",
           fg='#FFFFFF',
           bg='#6200EE',
           activebackground='#3700B3',
           activeforeground='#FFFFFF',
           font=("Comic sans", 15),
           width="10", command=check_win).place(relx=0.5, rely=0.5, anchor="center")


def camera_picture():
    get_picture_from_camera()
    decision = tk.messagebox.askquestion(title="Acquisition done", message="Acquisition done correctly \nDo you want to start the game?")
    if decision == 'yes':
        text, conf = detect_plate('capture/frame.jpg',1)
        game(text)
    return
   
   
def check_win():
    city = str(input_label.get()).upper()
    print(city)
    with open('cities.csv', 'r') as file:
        reader= csv.reader(file, delimiter=',')
        for row in reader:
            if row[0].upper()==city:
                platecharacter=platecharacter_label.cget("text")
                compute_score(city, platecharacter)
                return
            
    print("City not found")
    compute_score("", 0)

def hangman_game():
    letters = []
    count = 0
    platecharacter = platecharacter_label.cget("text")
    for character in platecharacter:
        letters.insert(count, character)
        count =count +1
    cities = []
    print(letters)
    count = 0
    with open('cities.csv', 'r') as file:
        reader= csv.reader(file, delimiter=',')
        for row in reader:
            for character in letters:
                if character in row[0].upper():
                    cities.insert(count, row[0].upper())
                    count = count +1
                    break
            if( count >= 50):
                break

    if(count > 0):
        start_hangman_game(window, cities, letters)
    else :
        print("CITY WITH THOSE CHARACTER NOT FOUND")
    return

def open_file():
    file = tk.Tk()
    file.withdraw()
    file_path = filedialog.askopenfilename()
    text = ""
    if file_path.endswith(image_file_extensions):
        text, conf = detect_plate(file_path,1)
    elif file_path.endswith(video_file_extensions):
        text, conf = detect_plate_video(file_path, 5)
    if(len(text) == 0 ):
        return
    print(text, conf)
    game(text)

def content():
    global window
    window = tk.Tk()
    window.geometry('700x700')
    window.title('Car plate recognition')
    window.configure(bg='#FFe9FF')
    global video_file_extensions
    video_file_extensions  = ('.wmv', '.mp4', '.MOV', 'avi')
    global image_file_extensions
    image_file_extensions = ('.jpg', '.PNG', 'bmp')

    global title
    title = tk.Label(window,
                     text="Welcome in Car Plate Recognition!",
                     font=("Arial",25),
                     bg='#6200EE',
                     fg='#FFFFFF')
    title.config(width=600)
    title.pack(ipady=10, side="top")

    global folder_icon
    folder_icon = PhotoImage(file = r"GUI_files/folder.png")
    folder_icon = folder_icon.subsample(6,6)
    global button
    button = tk.Button(window,
                       text = 'Press here to select \n a file',
                       fg = '#FFFFFF',
                       bg = '#6200EE',
                       activebackground = '#3700B3',
                       activeforeground = '#FFFFFF',
                       font = ("Comic sans", 15),
                       image = folder_icon,
                       compound=LEFT,
                       command = open_file)
    button.pack(side="bottom")
    button.config(width=270)
    button.place(relx=0.5, rely=0.25, anchor="center")

    global camera_icon
    camera_icon = PhotoImage(file = r"GUI_files/camera.png")
    camera_icon = camera_icon.subsample(10,10)
    global button2
    button2= tk.Button(text = 'Get a picture from \ncamera',
                        fg = '#FFFFFF',
                        bg = '#6200EE',
                        activebackground = '#3700B3',
                        activeforeground = '#FFFFFF',
                        font = ("Calibri", 15),
                        image = camera_icon,
                        compound=LEFT,
                        command = camera_picture)
    button2.pack(side="bottom")
    button2.config(width=270)
    button2.place(relx=0.5, rely=0.45, anchor="center")

    global text_label
    text_label = tk.Label(window,
                       text="",
                       font=("Arial",16),
                       bg='#FFe9FF')
    text_label.place(relx=0.5, rely=0.55, anchor="center")
    text_label.place_forget()

    global platecharacter_label
    platecharacter_label = tk.Label(window, text="", font=("Arial",10))
    platecharacter_label.place_forget()


    global button4
    button4 = tk.Button(text='Logout',
                        command=logout,
                        fg='#FFFFFF',
                        bg='#6200EE',
                        activebackground='#3700B3',
                        font=("Calibri", 15),
                        activeforeground='#FFFFFF')
    button4.pack(side="bottom")
    button4.place(relx=0.5, rely=0.95, anchor="center")
    window.mainloop()
    print(get_registred_user_value())

def logout():
    from login import login_user
    set_unregistred_user("")
    window.destroy()
    login_user()

def start():
    from login import login_user
    set_unregistred_user("")
    login_user()

if __name__=='__main__':
    start()