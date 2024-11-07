import tkinter as tk

class PrintWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Print Output")

        self.text_area = tk.Text(self.window)
        self.text_area.pack(expand=True, fill="both")

    def print(self, *args):
        text = " ".join(map(str, args))
        self.text_area.insert(tk.END, text + "\n")
