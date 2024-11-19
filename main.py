import re
from src.keyword_classifiers import *
from src.lexical_analyzer import *
from src.syntax_analyzer import *
import tkinter as tk 
from tkinter import filedialog,ttk

# need catch deci

root = tk.Tk()
root.configure(bg="pink")
root.resizable(0,0)

root.title('GROUP 5 | LOLCODE INTERPRETER')


def get_file(file_label, text_editor):

    filename = ''

    filename = filedialog.askopenfilename( initialdir="/project-testcases", title= "Select File", filetypes=( ("LOL files", "*.lol"), ("all files", "*.*") ))

    if filename:
        file_label.config(text="File opened: " + filename)
        with open(filename, "r") as file:
            file_text = file.read()
            text_editor.delete(1.0, tk.END)  
            text_editor.insert(tk.END, file_text)  

def execute_btn(text_editor, disp_lexemes):
        # Clear previous lexeme entries
    for item in disp_lexemes.get_children():
        disp_lexemes.delete(item)

    # Initialize lexemes from the current file content
    lexemes = lexemes_init(text_editor.get("1.0", tk.END).splitlines(), disp_lexemes)
    syntax_analyzer(lexemes)

file_label = tk.Label(root, text="No file selected")
file_label.pack()

content_frame = tk.Frame(root)
content_frame.pack(side="top", fill="both", expand=True)

text_editor = tk.Text(content_frame, wrap='word', height=20, width=40)
text_editor.pack(side="left", fill="both", expand=True)

disp_lexemes = ttk.Treeview(content_frame, columns=("Lexeme", "Classification"), show="headings", height=20)
disp_lexemes.heading("Lexeme", text="Lexeme")
disp_lexemes.heading("Classification", text="Classification")
disp_lexemes.pack(side="left", fill="both", expand=True)


button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=5)
button_frame.configure(bg = "pink")

open_button = tk.Button(button_frame, text="Open File", command=lambda: get_file(file_label, text_editor))
open_button.pack(side="left", padx=5)

execute_button = tk.Button(button_frame, text="Execute", command=lambda: execute_btn(text_editor, disp_lexemes))
execute_button.pack(side="left", padx=5)

root.mainloop()