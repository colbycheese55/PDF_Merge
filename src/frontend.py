import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import backend


root = ctk.CTk()
root.geometry("840x350")
root.resizable(width=False, height=False)
root.title("PDF Merge")
padding = 10
fileMap = dict()

#FUNCTIONS
def addNewFiles() -> None:
    paths = fd.askopenfilenames(title="Select File(s)", 
                                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")], 
                                initialdir="~")
    text, error = backend.registerNewFiles(paths, fileMap)
    if error != False:
        errorPopup(error)
    fileDisplayBox.configure(state=ctk.NORMAL)
    fileDisplayBox.insert(ctk.END, text)
    fileDisplayBox.configure(state=ctk.DISABLED)

def clear() -> None:
    instructionBox.delete("1.0", ctk.END)
    fileDisplayBox.configure(state=ctk.NORMAL)
    fileDisplayBox.delete("1.0", ctk.END)
    fileDisplayBox.configure(state=ctk.DISABLED)
    fileMap.clear()

def save(getPath: bool) -> None:
    path = None
    instructions = instructionBox.get("1.0", ctk.END)
    openAfter = openAfterBtn.get() == 1
    if getPath:
        path = fd.asksaveasfilename(title="Select File(s)", 
                                    filetypes=[("PDF Files", "*.pdf")], 
                                    initialdir="~",
                                    confirmoverwrite=True)
    if path == "":
        return
    try:
        result = backend.processInstructions(instructions, fileMap, path, openAfter)
        if result is not None:
            errorPopup(result)
    except Exception as e:
        errorPopup("An unknown error has occured")

def errorPopup(message: str) -> None:
    mb.showerror("PDF Merge Error", message)

#BUTTONS
btnParams = {"width": 150, "height": 4, "font": ("Franklin Gothic Heavy", 20)}

addFilesBtn = ctk.CTkButton(root, text="Add PDF(s)", **btnParams, command=addNewFiles)
addFilesBtn.grid(row=0, rowspan=1, column=1, columnspan=3, padx=padding, pady=padding)

clearBtn = ctk.CTkButton(root, text="Clear", **btnParams, command=clear)
clearBtn.grid(row=0, rowspan=1, column=6, columnspan=3, padx=padding, pady=padding)

saveBtn = ctk.CTkButton(root, text="Save", **btnParams, command=lambda: save(False))
saveBtn.grid(row=7, rowspan=1, column=6, columnspan=1, padx=padding, pady=padding)

saveAsBtn = ctk.CTkButton(root, text="Save as", **btnParams, command=lambda: save(True))
saveAsBtn.grid(row=7, rowspan=1, column=8, columnspan=1, padx=padding, pady=padding)

openAfterBtn = ctk.CTkCheckBox(root, text="Open After Save", **btnParams)
openAfterBtn.grid(row=6, rowspan=1, column=6, columnspan=3, padx=padding, pady=padding)
openAfterBtn.select()

#TEXT BOXES
textFont = ("Calibri", 15)

instructionBox = ctk.CTkTextbox(root, wrap=ctk.WORD, width=400, height=170, font=textFont)
instructionBox.grid(row=3, rowspan=3, column=5, columnspan=5, padx=padding, pady=0)

fileDisplayBox = ctk.CTkTextbox(root, wrap=ctk.WORD, width=400, height=250, font=textFont)
fileDisplayBox.configure(state=ctk.DISABLED)
fileDisplayBox.grid(row=3, rowspan=5, column=0, columnspan=5, padx=padding, pady=0)

#Labels
labelFont = ("Calibri", 20)

fileDisplayLabel = ctk.CTkLabel(root, text="Loaded PDF(s)", font=labelFont)
fileDisplayLabel.grid(row=2, rowspan=1, column=0, columnspan=5)

instructionsLabel = ctk.CTkLabel(root, text="Instructions", font=labelFont)
instructionsLabel.grid(row=2, rowspan=1, column=5, columnspan=5)

#KEYBINDS
root.bind("<Control-w>", lambda _: root.destroy())
root.bind("<Control-o>", lambda _: openAfterBtn.toggle())
root.bind("<Control-Return>", lambda _: save(True))
root.bind("<Control-Shift-Return>", lambda _: save(False))


root.mainloop()