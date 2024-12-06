from tkinter import *

main_window = Tk()
img = PhotoImage(file="ICON.PNG")

main_window.title("Image Restoration AND Histogram equalization")
main_window.iconphoto(TRUE , img)
main_window.geometry("450x450+400+140")


main_window.mainloop()