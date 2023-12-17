import tkinter as tki
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import backend


root = tki.Tk()
root.geometry("1010x500")
root.title("PDF Merge")
root.bind("<Control-w>", lambda _: root.destroy())
padding = 10
fileMap = dict()

#FUNCTIONS
def addNewFiles() -> None:
    paths = fd.askopenfilenames(title="Select File(s)", 
                                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")], 
                                initialdir="~")
    text, success = backend.registerNewFiles(paths, fileMap)
    if success == False:
        errorPopup(text)
        return
    fileDisplayBox.config(state=tki.NORMAL)
    fileDisplayBox.insert(tki.END, text)
    fileDisplayBox.config(state=tki.DISABLED)

def clear() -> None:
    instructionBox.delete("1.0", tki.END)
    fileDisplayBox.config(state=tki.NORMAL)
    fileDisplayBox.delete("1.0", tki.END)
    fileDisplayBox.config(state=tki.DISABLED)
    fileMap.clear()

def save(getPath: bool) -> None:
    path = None
    if getPath:
        path = fd.asksaveasfilename(title="Select File(s)", 
                                    filetypes=[("PDF Files", "*.pdf")], 
                                    initialdir="~",
                                    confirmoverwrite=True)
    instructions = instructionBox.get("1.0", tki.END)
    result = backend.processInstructions(instructions, fileMap, path)
    if result is not None:
        errorPopup(result)

def errorPopup(message: str) -> None:
    mb.showerror("PDF Merge Error", message)

#BUTTONS
addFilesBtn = tki.Button(root, text="Add PDF(s)", width=40, height=2, command=addNewFiles)
addFilesBtn.grid(row=0, rowspan=1, column=1, columnspan=3, padx=padding, pady=padding)

clearBtn = tki.Button(root, text="Clear", width=40, height=2, command=clear)
clearBtn.grid(row=0, rowspan=1, column=6, columnspan=3, padx=padding, pady=padding)

saveBtn = tki.Button(root, text="Save", width=20, height=2, command=lambda: save(False))
saveBtn.grid(row=6, rowspan=1, column=6, columnspan=1, padx=padding, pady=padding)

saveAsBtn = tki.Button(root, text="Save as", width=20, height=2, command=lambda: save(True))
saveAsBtn.grid(row=6, rowspan=1, column=8, columnspan=1, padx=padding, pady=padding)

#TEXT BOXES
instructionBox = tki.Text(root, wrap=tki.WORD, width=60, height=20)
instructionBox.grid(row=2, rowspan=4, column=5, columnspan=5, padx=padding, pady=padding)

fileDisplayBox = tki.Text(root, wrap=tki.WORD, width=60, height=25)
fileDisplayBox.config(state=tki.DISABLED)
fileDisplayBox.grid(row=2, rowspan=5, column=0, columnspan=5, padx=padding, pady=padding)



root.mainloop()