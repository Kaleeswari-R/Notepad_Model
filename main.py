from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from tkinter.colorchooser import askcolor
from tkinter.font import Font, families

from PIL import Image, ImageTk
import os
import subprocess
import sys


def open_file():
    global file
    file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt")])
    if file:
        root.title(os.path.basename(file) + " - Notepad")  
        text_area.delete(1.0, END)
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
            

def open_new_file():
    root.title("Untitled - Notepad")  
    text_area.delete(1.0, END)  
    global file
    file = None
    

def save_file():
    global file
    if file is None:
        save_as_file()
    else:
        with open(file, "w") as file_:
            file_.write(text_area.get(1.0, END))  
        root.title(os.path.basename(file) + " - Notepad")  


def save_as_file():
    global file
    file = fd.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt',
                                filetypes=[("Text File", "*.txt"), ("All Files", "*.*")])
    if file:
        with open(file, "w") as file_:
            file_.write(text_area.get(1.0, END))  
        root.title(os.path.basename(file) + " - Notepad")  

def new_window():
    if sys.platform.startswith('win'):
        subprocess.Popen([sys.executable, os.path.abspath(__file__)])
    else:
        os.system(sys.executable + " " + os.path.abspath(__file__) + " &")

def exit_application():
    root.destroy()  
def copy_text():
    text_area.clipboard_clear()
    text_area.clipboard_append(text_area.selection_get())  

def cut_text():
    copy_text()
    text_area.delete("sel.first", "sel.last")  

def paste_text():
    text_area.insert("insert", text_area.clipboard_get())  

def select_all():
    text_area.tag_add(SEL, "1.0", END)  
    text_area.mark_set(INSERT, "1.0")
    text_area.see(INSERT)

def delete_last_char():
    if text_area.get("1.0", END).strip():
        text_area.delete("end-2c", END)  

def about_notepad():
    about_text = "This Notepad application is a simple text editor written in Python using Tkinter.\n\n"\
                 "It allows you to create, open, edit, and save text files.\n"\
                 "You can also change the font and text color.\n\n"\
                 "Enjoy using this Notepad!"
    mb.showinfo("About Notepad", about_text)

def notepad_commands():
    commands_text = """
File Menu:
- 'New' clears the entire Text Area
- 'New Window' opens a new instance of Notepad
- 'Open' opens an existing text file
- 'Save' saves the current file
- 'Save As' saves the current file with a new name
- 'Close File' exits the application

Edit Menu:
- 'Copy' copies the selected text to clipboard
- 'Cut' cuts the selected text and removes it
- 'Paste' pastes the copied/cut text
- 'Select All' selects all text in the editor
- 'Delete' deletes the last character in the editor

Format Menu:
- 'Font' allows you to choose and apply a font to the text
- 'Color' allows you to choose and apply a color to the text
"""
    mb.showinfo("Notepad Commands", commands_text)

def update_counts(event=None):
    text_content = text_area.get(1.0, 'end-1c')
    char_count.set(f"{len(text_content)} characters")
    word_count.set(f"{len(text_content.split())} words")

def choose_font():
    font_window = Toplevel(root)
    font_window.title("Choose Font")

    font_name = StringVar(font_window)
    font_name.set(current_font.actual()['family'])

    font_size = StringVar(font_window)
    font_size.set(current_font.actual()['size'])

    font_label = Label(font_window, text="Font:")
    font_label.grid(row=0, column=0, padx=10, pady=10)
    
    font_dropdown = OptionMenu(font_window, font_name, *families(root))
    font_dropdown.grid(row=0, column=1, padx=10, pady=10)

    size_label = Label(font_window, text="Size:")
    size_label.grid(row=1, column=0, padx=10, pady=10)
    
    size_dropdown = Spinbox(font_window, from_=8, to=72, textvariable=font_size)
    size_dropdown.grid(row=1, column=1, padx=10, pady=10)

    def apply_font():
        new_font = Font(family=font_name.get(), size=font_size.get())
        text_area.config(font=new_font)
        font_window.destroy()

    apply_button = Button(font_window, text="Apply", command=apply_font)
    apply_button.grid(row=2, columnspan=2, pady=10)

def choose_color():
    color = askcolor()[1]
    if color:
        text_area.config(fg=color)

root = Tk()
root.title("Untitled - Notepad")
root.geometry('800x500')
root.resizable(0, 0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

icon = ImageTk.PhotoImage(Image.open('Notepad.png'))
root.tk.call('wm', 'iconphoto', root._w, icon)
file = None

current_font = Font(family="Times New Roman", size=12)

menu_bar = Menu(root)
root.config(menu=menu_bar)

text_area = Text(root, font=current_font)
text_area.grid(sticky=NSEW)
text_area.bind("<KeyRelease>", update_counts)

scroller = Scrollbar(text_area, orient=VERTICAL, command=text_area.yview)
scroller.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroller.set)

file = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
file.add_command(label="New", command=open_new_file)
file.add_command(label="New Window", command=new_window)
file.add_separator()
file.add_command(label="Open", command=open_file)
file.add_separator()
file.add_command(label="Save", command=save_file)
file.add_command(label="Save As", command=save_as_file)
file.add_separator()
file.add_command(label="Exit", command=exit_application)
menu_bar.add_cascade(label="File", menu=file)

edit = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
edit.add_command(label='Copy', command=copy_text)
edit.add_command(label='Cut', command=cut_text)
edit.add_command(label='Paste', command=paste_text)
edit.add_separator()
edit.add_command(label='Select All', command=select_all)
edit.add_command(label='Delete', command=delete_last_char)
menu_bar.add_cascade(label="Edit", menu=edit)

format = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
format.add_command(label='Font', command=choose_font)
format.add_command(label='Color', command=choose_color)
menu_bar.add_cascade(label="Format", menu=format)

help = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
help.add_command(label='About Notepad', command=about_notepad)
help.add_command(label='Notepad Commands', command=notepad_commands)
menu_bar.add_cascade(label="Help", menu=help)

root.mainloop()
