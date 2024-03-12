import vlad_reaction_analyzer
import tkinter as tk
from tkinter import filedialog
import os
from vlad_reaction_analyzer import VladReactionAnalyzer

# 定义全局变量以存储文件路径
selected_file_path = None

def open_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

def process_file():
    global selected_file_path
    if selected_file_path:
        VladReactionAnalyzer.save_plate_layout_to_desktop(selected_file_path)
    else:
        print("No file selected.")





root = tk.Tk()
root.title("File Analyzer")

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)

open_button = tk.Button(frame, text="Load txt File", command=open_file)
open_button.pack(padx=10, pady=10)

# 添加 Process 按钮
process_button = tk.Button(frame, text="Run", command=process_file)
process_button.pack(padx=10, pady=10)

root.mainloop()