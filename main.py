from tkinter import Tk, Button, PhotoImage, Canvas, filedialog
from csv import reader, writer
from random import choice
from os import path

BACKGROUND_COLOR = "#B1DDC6"
FOLDER_DATA = "./data/"
FOLDER_IMAGES = "./images/"
PREFIX = "training_"
words = []
word_combo = []

def flip_card():
    """
    * activate buttons
    * bring front side of card to the background, so
    * backside is displayed
    * display to_language text and translated word
    """
    global word_combo

    button_ok.config(state="active")
    button_nok.config(state="active")
    canvas_card.tag_lower("fg")
    canvas_card.itemconfigure("language", text=to_language)
    canvas_card.itemconfigure("word", text=word_combo[1])


def new_word():
    """
    * randomly get a word combo
    * deactivate buttons
    * bring front side of card to foreground
    * display from_language text and new word
    * set timer to 3 seconds
    """
    global word_combo

    word_combo = choice(words)
    button_ok.config(state="disabled")
    button_nok.config(state="disabled")
    canvas_card.tag_lower("bg")
    canvas_card.itemconfigure("language", text=from_language)
    canvas_card.itemconfigure("word", text=word_combo[0])
    root.after(3000,flip_card)


def pressed_ok():
    """
    * remove the known word combo from list
    * call function new_word()
    """
    global words
    global word_combo

    words.remove(word_combo)
    new_word()


def pressed_nok():
    """
    * call function new_word()
    """
    new_word()


root = Tk()
root.config(width=900, height=613, padx=50, pady=50, bg=BACKGROUND_COLOR)
root.title("Flashy")

#* create the canvas and load the two images with tags so we can flip
#* as well with the two text lines
canvas_card = Canvas(width=800,height=526,background=BACKGROUND_COLOR, highlightthickness=0)
image_card1 = PhotoImage(file=FOLDER_IMAGES + "card_front.png")
image_card2 = PhotoImage(file=FOLDER_IMAGES + "card_back.png")
canvas_card.create_image(0, 0, image=image_card2, anchor="nw", tags="bg")
canvas_card.create_image(0, 0, image=image_card1, anchor="nw", tags="fg")
canvas_card.grid(row=1,column=1,columnspan=2)
canvas_card.create_text(400,150,font=("Arial",40,"italic"), tags="language")
canvas_card.create_text(400,263,font=("Arial",60,"bold"), tags="word")

#* create buttons
button_image_ok = PhotoImage(file=FOLDER_IMAGES + "right.png")
button_image_nok = PhotoImage(file=FOLDER_IMAGES + "wrong.png")
button_ok = Button(image=button_image_ok,  background=BACKGROUND_COLOR, highlightthickness=0,
                    command=pressed_ok)
button_nok = Button(image=button_image_nok, background=BACKGROUND_COLOR, highlightthickness=0,
                    command=pressed_nok)
button_ok.grid(row=2, column=2)
button_nok.grid(row=2, column=1)

#* show filedialog
filename = filedialog.askopenfilename(
    title="Select file",
    filetypes=[
        ("csv files", "*.csv")],
    initialdir=FOLDER_DATA
)

if filename:
    #* extract only the filename
    filename = path.basename(filename)
    #* read the csv file
    with open(file=FOLDER_DATA + filename, mode="r", encoding="utf8") as fp:
        words = list(reader(fp))
        #* get the languages from first row
        from_language = words[0][0]
        to_language = words[0][1]
        #* delete the first row = header
        words.pop(0)
    new_word()
    root.mainloop()

    #* if this is the original file add prefix "training_"
    if PREFIX not in filename:
        filename = PREFIX + filename
    #* write csv file
    with open(file=FOLDER_DATA + filename, mode="w", encoding="utf8", newline="") as fp:
        writer = writer(fp)
        #* write header
        writer.writerow([from_language,to_language])
        writer.writerows(words)





