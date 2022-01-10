from tkinter import *
from tkinter import messagebox
from string import ascii_uppercase
import random

global lblWord
global imgLabel
global photos
global the_word_withSpaces
global word_list


def newGame():
    global the_word_withSpaces
    global numberOfGuesses
    global lblWord
    global imgLabel
    global word_list
    global plate_letters

    numberOfGuesses = 0

    #We choose randomly a word from the set of words
    the_word = (random.choice(word_list))
    the_new_word = ""
    city_to_guess = ""

    #Here we inizialize the word to guess
    for word in the_word:
        if(word == " " or word == "'"):
            the_new_word = the_new_word + word
            city_to_guess = city_to_guess + word
        elif word in plate_letters:
            the_new_word = the_new_word + word
            city_to_guess = city_to_guess + word
        else:
            the_new_word = the_new_word + word
            city_to_guess = city_to_guess +"_"
    the_word_withSpaces = " ".join(the_new_word)
    city_to_guess = " ".join(city_to_guess)
    lblWord.set(city_to_guess)

def guess(letter):
    from GUI import compute_score
    global lblWord
    global imgLabel
    global numberOfGuesses
    global photos
    global the_word_withSpaces
    global window2
    global plate_letters


    if numberOfGuesses < 11:
        txt = list(the_word_withSpaces)
        guessed = list(lblWord.get())
        #Check if the selected word is present or not
        if the_word_withSpaces.count(letter) > 0:
            for c in range(len(txt)):
                if txt[c] == letter:
                    guessed[c] = letter
                lblWord.set("".join(guessed))
                if lblWord.get() == the_word_withSpaces:
                    messagebox.showinfo("Hangman", "You guessed it!")
                    window2.destroy()
                    compute_score("".join([c for c in the_word_withSpaces if (c.isalpha())]), plate_letters)
                    return
        else:
            numberOfGuesses += 1
            imgLabel.config(image=photos[numberOfGuesses])
            if numberOfGuesses == 11:
                messagebox.showwarning("Hangman", "Game Over, the word was: " + the_word_withSpaces)
                window2.destroy()
                compute_score("", plate_letters)
                return


def start_hangman_game(window, cities, letters):
    #We create the window where we will play the game
    global window2
    window2= Toplevel(window)
    window2.title('Hangman-GUESS CITIES NAME')

    global photos
    global lblWord
    global imgLabel
    global word_list
    global plate_letters
    plate_letters = letters
    word_list = cities

    #We get all the images of the various phases of the hangman
    photos = [PhotoImage(file="images/hang0.png"), PhotoImage(file="images/hang1.png"),
			  PhotoImage(file="images/hang2.png"),
			  PhotoImage(file="images/hang3.png"), PhotoImage(file="images/hang4.png"),
			  PhotoImage(file="images/hang5.png"),
			  PhotoImage(file="images/hang6.png"), PhotoImage(file="images/hang7.png"),
			  PhotoImage(file="images/hang8.png"),
			  PhotoImage(file="images/hang9.png"), PhotoImage(file="images/hang10.png"),
			  PhotoImage(file="images/hang11.png")]

    #The label will show the state of the hangman
    imgLabel = Label(window2)
    imgLabel.grid(row=0, column=0, columnspan=3, padx=10, pady=40)

    #This label will show the word to guess
    lblWord = StringVar()
    Label(window2, textvariable=lblWord, font=('consolas 24 bold')).grid(row=0, column=3, columnspan=6, padx=10)

    #We will create all button for the letters to select
    n = 0
    for c in ascii_uppercase:
        Button(window2, text=c, command=lambda c=c: guess(c), font=('Helvetica 18'), width=10).grid(row=1 + n // 9,
																								  column=n % 9)
        n += 1

    #We give the possibility to the user to play a new game
    Button(window2, text="New\nGame", command=lambda: newGame(), font=("Helvetica 10 bold")).grid(row=3, column=8)
    #THE LETTERS MUST ALL BE UPPER LETTERS
    newGame()
    window2.mainloop()

