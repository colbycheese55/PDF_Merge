import tkinter as tki
import backend


root = tki.Tk()
root.geometry("1010x500")
root.title("PDF Merge")
padding = 10

#BUTTONS
addFilesBtn = tki.Button(root, text="Add PDF(s)", width=40, height=2)
addFilesBtn.grid(row=0, rowspan=1, column=1, columnspan=3, padx=padding, pady=padding)

clearBtn = tki.Button(root, text="Clear", width=40, height=2)
clearBtn.grid(row=0, rowspan=1, column=6, columnspan=3, padx=padding, pady=padding)

saveBtn = tki.Button(root, text="Save", width=20, height=2)
saveBtn.grid(row=6, rowspan=1, column=6, columnspan=1, padx=padding, pady=padding)

saveAsBtn = tki.Button(root, text="Save as", width=20, height=2)
saveAsBtn.grid(row=6, rowspan=1, column=8, columnspan=1, padx=padding, pady=padding)

#TEXT BOXES
instructionBox = tki.Text(root, wrap=tki.WORD, width=60, height=20)
instructionBox.grid(row=2, rowspan=4, column=5, columnspan=5, padx=padding, pady=padding)

fileDisplayBox = tki.Text(root, wrap=tki.WORD, width=60, height=25)
fileDisplayBox.insert(tki.END, "Text")
fileDisplayBox.config(state=tki.DISABLED)
fileDisplayBox.grid(row=2, rowspan=5, column=0, columnspan=5, padx=padding, pady=padding)



root.mainloop()