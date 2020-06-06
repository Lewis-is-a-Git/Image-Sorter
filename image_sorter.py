import os as os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil

# TODO: Show preview of next image
# TODO: go back to last image
# TODO: Show progress in folder
# TODO: Show rate of sorting
# TODO: make a scoring system with combos and streaks

# global variables
folderName = ""  # directory to folder
listing = [""]  # list of all images in selected folder
photo = ""  # deny garbage collector


# Function for opening the file explorer
def open_folder():
    global folderName
    global listing
    folderName = filedialog.askdirectory()  # choose directory
    # Change label contents
    label_file_explorer.configure(text="Folder Opened: " + folderName)
    # create list of items in directory
    listing = os.listdir(folderName)
    listing = [f for f in listing if f.__contains__('.')]  # filter list to remove folders
    get_image()


# Show image from list in canvas
def get_image():
    global folderName
    global listing
    global photo
    base_width = 800  # width of image canvas
    try:
        filename = listing[0]  # collect name of first image in list
        img = Image.open(folderName + '/' + filename)  # open image
        # resize image to fit canvas
        w, h = img.size
        w_percent = base_width / float(w)
        h_size = int((float(h) * float(w_percent)))  # assumed all images have the same aspect ratio
        img = img.resize((base_width, h_size), Image.ANTIALIAS)
        # load image to canvas
        photo = ImageTk.PhotoImage(img)
        canv.create_image((base_width / 2, h_size / 2), image=photo)
    except IndexError:
        label_file_explorer.configure(text="Folder Empty: " + folderName, fg="red")
        canv.create_text(base_width / 2, 600 / 2, fill="black", font="Times 20 italic bold",
                         text="Well Done Nerd!")
        photo.__del__()


# move to next image in list
def next_image():
    listing.pop(0)
    get_image()

# TODO: Check if arguments can be passed by button commands


def good_image():
    category = "/good"  # preferably pass arguments in button commands
    if not os.path.exists(folderName + category):
        os.makedirs(folderName + category)
    if variable.get() == "copy":
        shutil.copy(folderName + '/' + listing[0], folderName + category + '/' + listing[0])
    else:
        shutil.move(folderName + '/' + listing[0], folderName + category + '/' + listing[0])
    next_image()


def bad_image():
    category = "/bad"
    if not os.path.exists(folderName + category):
        os.makedirs(folderName + category)
    if variable.get() == "copy":
        shutil.copy(folderName + '/' + listing[0], folderName + category + '/' + listing[0])
    else:
        shutil.move(folderName + '/' + listing[0], folderName + category + '/' + listing[0])
    next_image()


def left_key(event):
    bad_image()


def right_key(event):
    good_image()


# Create the root window
window = tk.Tk()
# Set window title
window.title('Image Sorter')
# Set window size
window.geometry("800x800")
window.minsize(width=800, height=800)
# set up gui
frm_options = tk.Frame(master=window)
frm_image = tk.Frame(master=window)
frm_buttons = tk.Frame(master=window)

# Create a File Explorer label
label_file_explorer = tk.Label(frm_options,
                               text="Start by opening a folder...",
                               width=100, height=4,
                               fg="blue")
label_file_explorer.pack()

button_explore = tk.Button(frm_options,
                           text="Open Folder",
                           command=open_folder).pack()

# Drop down list copy/move
variable = tk.StringVar(window)
variable.set("copy")  # default value
operation = tk.OptionMenu(frm_options, variable, "copy", "move")
operation.pack()

# TODO: add advanced checkbox to add extra categories
"""
advanced = tk.IntVar()
tk.Checkbutton(frm_options, text="Advanced", variable=advanced, command=updateUI).pack()
"""
# TODO: update buttons based on checkbox


# show image
canv = tk.Canvas(frm_image, width=800, height=600, bg='white')
canv.pack()

# Buttons
btn_bad = tk.Button(
    frm_buttons,
    text="Bad",
    width=25,
    height=5,
    bg="red",
    font=("Courier", 14, 'bold'),
    fg="white",
    command=bad_image
)
btn_bad.pack(padx=50, pady=10, side=tk.LEFT)
btn_good = tk.Button(
    frm_buttons,
    text="Good",
    width=25,
    height=5,
    bg="green",
    font=("Courier", 14, 'bold'),
    fg="white",
    command=good_image
)
btn_good.pack(padx=50, pady=10, side=tk.RIGHT)

# Key binds
window.bind('<Left>', left_key)
window.bind('<Right>', right_key)

# pack frames
frm_options.pack(fill=tk.X, expand=True)
frm_image.pack(fill=tk.X, expand=True)
frm_buttons.pack(fill=tk.X, expand=True, side=tk.TOP)

window.mainloop()
