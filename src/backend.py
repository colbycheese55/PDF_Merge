import fitz
import re as regex
import os
import datetime
import subprocess


def executeInstruction(char: str, fileMap: dict[str, "PDF"], mergePDF: "PDF", start=1, end=None) -> str | bool:
    if char not in fileMap:
        return f"\"{char}\" was not assigned to a file"
    length = len(fileMap[char])
    if start <= 0 or (end is not None and end <=0) or (end is not None and start > end):
        return f"Invalid page(s)"
    if start > length or (end is not None and end > length):
        return f"Out of range, this PDF has {length} pages"
    if end is None:
        end = length
    mergePDF.appendPages(fileMap[char], start, end)
    return True

def saveMergedPDF(savepath: str, mergePDF: "PDF", openAfter: bool) -> None:
    if savepath is not None and not savepath.endswith(".pdf"):
        savepath += ".pdf"
    if savepath is None:
        desktop_path = os.path.expanduser("~") + "\\Desktop"
        timestamp = datetime.datetime.now().strftime("%S%M%H")
        savepath = f"{desktop_path}\\merged_{timestamp}.pdf"
    mergePDF.writeFile(savepath)
    if openAfter:
        subprocess.Popen(["cmd", "/c", "start", "", savepath], shell=True)

def processInstructions(instructions: str, fileMap: dict[str, "PDF"], savepath: str, openAfter: bool) -> str:
    instructions = instructions.lower().replace(" ", "").replace("\n", "")
    instructions = instructions.split(",")
    mergePDF = PDF()

    validFormats = dict()
    commonArgs = (fileMap, mergePDF)
    validFormats[r"^[a-z]$"] = lambda match, args: executeInstruction(match.group(0), *args) #[file]
    validFormats[r"^([a-z])(\d+)$"] = lambda match, args: executeInstruction(match.group(1), *args, start=int(match.group(2)), end=int(match.group(2))) #[file][page]
    validFormats[r"^([a-z])(\d+)-(\d+)$"] = lambda match, args: executeInstruction(match.group(1), *args, start=int(match.group(2)), end=int(match.group(3))) #[file][start]-[end]
    validFormats[r"^([a-z])(\d+)-$"] = lambda match, args: executeInstruction(match.group(1), *args, start=int(match.group(2))) #[file][start]-

    for instruction in instructions:
        result = False
        if instruction == "":
            continue
        for format, func in validFormats.items():
            match = regex.match(format, instruction)
            if match is not None:
                result = func(match, commonArgs)
                break
        if result == False:
            return f"Instruction \"{instruction}\" is an unrecognizd pattern"
        if result != True:
            return f"Instruction \"{instruction}\": {result}"

    if len(mergePDF) == 0:
        return "No instructions given; PDF would have been empty"    
    saveMergedPDF(savepath, mergePDF, openAfter)
    return None

def registerNewFiles(newFiles: tuple[str], fileMap: dict[str, "PDF"]) -> (str, bool | str):
    text = ""
    for i in range(len(newFiles)):
        if len(fileMap) == 26:
            return text, "Only 26 PDFs can be loaded at once"
        char = chr(ord('a') + len(fileMap))
        filename = os.path.basename(newFiles[i])
        try:
            reader = PDF(newFiles[i])
        except Exception as e:
            return text, f"\"{newFiles[i]}\" could not be read as a PDF"
        fileMap[char] = reader
        text += f"{char}:\t{filename}\n"
    return text, False


class PDF:
    def __init__(this, path=None) -> None:
        this.obj = fitz.open(path)

    def __len__(this) -> int:
        return this.obj.page_count

    def appendPages(this, source: "PDF", start: int, end: int) -> None:
        this.obj.insert_pdf(source.obj, from_page=start-1, to_page=end-1)

    def writeFile(this, path: str) -> None:
        this.obj.save(path)