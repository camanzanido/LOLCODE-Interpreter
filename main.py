import re
from symtable import SymbolTable
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

    filename = filedialog.askopenfilename( initialdir="/project-cases", title= "Select File", filetypes=( ("LOL files", "*.lol"), ("all files", "*.*") ))

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
    for item in disp_symbolTable.get_children():
        disp_symbolTable.delete(item)
    console_box.delete(1.0, tk.END)

    # Initialize lexemes from the current file content
    lexemes = lexemes_init(text_editor.get("1.0", tk.END).splitlines(), disp_lexemes)
    symbol_table= syntax_analyzer(lexemes)

    for identifier, value in symbol_table:
        disp_symbolTable.insert("", tk.END, values=(identifier, value))
   
   
    # for _, value in symbol_table:
    #     console_box.insert(tk.END, f"{value}\n")

file_label = tk.Label(root, text="No file selected", bg="pink", fg= "black",font=("Arial", 15))
file_label.pack(pady=10)  

content_frame = tk.Frame(root, bg="pink") 
content_frame.pack(side="top", fill="both", expand=True, pady=10)  

text_editor_frame = tk.Frame(content_frame)  
text_editor_frame.pack(side="left", fill="both", expand=True, padx=10)

text_editor_title = tk.Label(text_editor_frame, text="Source Code", font=("Arial", 12, "bold"))
text_editor_title.pack(side="top", pady=5)  

text_editor = tk.Text(text_editor_frame, wrap='word', height=20, width=40) 
text_editor.pack(side="top", fill="both", expand=True)


lexeme_frame = tk.Frame(content_frame)  
lexeme_frame.pack(side="left", fill="both", expand=True, padx=10)

disp_lexemes_title = tk.Label(lexeme_frame, text="Lexemes", font=("Arial", 12, "bold"))
disp_lexemes_title.pack(side="top", pady=5)  

disp_lexemes = ttk.Treeview(lexeme_frame, columns=("Lexeme", "Classification"), show="headings", height=20)
disp_lexemes.heading("Lexeme", text="Lexeme")
disp_lexemes.heading("Classification", text="Classification")
disp_lexemes.pack(side="top", fill="both", expand=True)

symbol_table_frame = tk.Frame(content_frame) 
symbol_table_frame.pack(side="left", fill="both", expand=True, padx=10)

disp_symbolTable_title = tk.Label(symbol_table_frame, text="Symbol Table", font=("Arial", 12, "bold"))
disp_symbolTable_title.pack(side="top", pady=5)  

disp_symbolTable = ttk.Treeview(symbol_table_frame, columns=("Identifier", "Value"), show="headings", height=20)
disp_symbolTable.heading("Identifier", text="Identifier")
disp_symbolTable.heading("Value", text="Value")
disp_symbolTable.pack(side="top", fill="both", expand=True)


button_frame = tk.Frame(root, bg="pink")  
button_frame.pack(side="bottom", pady=10)  

open_button = tk.Button(button_frame, text="Open File", command=lambda: get_file(file_label, text_editor), bg="#FFD9EC", relief="ridge")
open_button.pack(side="left", padx=5)

execute_button = tk.Button(button_frame, text="Execute", command=lambda: execute_btn(text_editor, disp_lexemes), bg="#FFD9EC", relief="ridge")
execute_button.pack(side="left", padx=5)

console_frame = tk.Frame(root, bg="pink")
console_frame.pack(side="bottom", fill="x", pady=10)


console_box = tk.Text(console_frame, height=10, width=80)
console_box.pack(side="top", fill="both", padx=10)

root.mainloop()
