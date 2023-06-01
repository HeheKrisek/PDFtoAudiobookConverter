from tkinter import *
from tkinter import filedialog, messagebox
from pypdf import PdfReader
from gtts import gTTS
import shutil

FONT_NAME = "Courier"
COLOR_1 = "#2A2F4F"
COLOR_2 = "#917FB3"
COLOR_3 = "#E5BEEC"
COLOR_4 = "#FDE2F3"


def gettext():
    global filename_path
    global text
    reader = PdfReader(filename_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    print(text)


def getpdf():
    global filename
    global filename_path
    try:
        filename_path = filedialog.askopenfilename(initialdir="/",
                                              title="Select a PDF File",
                                              filetypes=[('pdf file', '*.pdf')])
        print(filename_path)
        filename_list = filename_path.split("/")
        filename = filename_list[-1]
        pdf_path_label.config(text=f"Selected file: {filename}")
        gettext()

    except FileNotFoundError:
        pdf_path_label.config(text=f"Selected file: none")

def convert():
    global text
    global filename
    global filename_path
    try:
        l = lng.get()
        converted = gTTS(text=text, lang=l, slow=False)
        converted.save(f"{filename.strip('.pdf')}_{l}.mp3")
        save_path = filename_path.strip(f"{filename}")
        shutil.move(f"{filename.strip('.pdf')}_{l}.mp3", save_path)
        # main_file = open(f"{filename.strip('.pdf')}.mp3", "rb").read()
        # converted_name = f"{filename.strip('.pdf')}.mp3"
        # dest_file = open(save_path+converted_name)
        # dest_file.write(main_file)
        # dest_file.close()

    except NameError:
        messagebox.showerror(title="Error!", message="You need to choose a file!")

    except shutil.Error:
        messagebox.showinfo(title="File already exists", message="You already converted this file!")


window = Tk()
window.title("PDF to audio converter")
window.minsize(500, 300)
window.maxsize(750, 300)
window.config(padx=50, pady=50, bg=COLOR_4)

title_label = Label(text="Select a PDF file", font=(FONT_NAME, 20, "bold"), bg=COLOR_4, fg=COLOR_1, pady=25)
title_label.grid(row=0, column=1)

pdf_path_label = Label(text="Selected file: none", font=(FONT_NAME, 10, "bold"), bg=COLOR_4, fg=COLOR_2)
pdf_path_label.grid(row=1, column=1)

get_pdf_button = Button(text="Choose file", highlightthickness=0, command=getpdf)
get_pdf_button.grid(row=2, column=0)

convert_button = Button(text="Convert", highlightthickness=0, command=convert)
convert_button.grid(row=2, column=2)

language_label = Label(text="Select language", font=(FONT_NAME, 10, "bold"), bg=COLOR_4, fg=COLOR_2)
language_label.grid(row=3, column=1)


lng = StringVar()
lng.set("en")
size1 = Radiobutton(window, text="English", variable=lng, value="en", bg=COLOR_4, fg=COLOR_1)
size1.grid(row=4, column=1)
size2 = Radiobutton(window, text="Polish", variable=lng, value="pl", bg=COLOR_4, fg=COLOR_1)
size2.grid(row=5, column=1)
size2 = Radiobutton(window, text="Spanish", variable=lng, value="es", bg=COLOR_4, fg=COLOR_1)
size2.grid(row=6, column=1)

window.mainloop()
