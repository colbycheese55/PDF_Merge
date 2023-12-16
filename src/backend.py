import PyPDF2 as pdf
import re as regex
import os
import datetime



def executeInstruction(char: str, fileMap: dict[str, pdf.PdfReader], mergePDF: pdf.PdfMerger, start=1, end=None) -> str | bool: #TODO rework error messages
    if char not in fileMap:
        return f"\"{char}\" was not assigned to a file"
    addPDF = fileMap[char]
    if end is None:
        end = len(addPDF.pages)
    if start <= 0 or end <= 0 or start > end:
        return f"Invalid page number(s)"
    if end > len(addPDF.pages):
        return f"Page {start} is out of range of the input PDF"
    mergePDF.append(addPDF, None, (start-1, end))
    return True

def saveMergedPDF(savepath: str, mergePDF: pdf.PdfMerger) -> None:
    if savepath is not None and not savepath.endswith(".pdf"):
        savepath += ".pdf"
    if savepath is None:
        desktop_path = os.path.expanduser("~") + "\\Desktop"
        timestamp = datetime.datetime.now().strftime("%S%M%H")
        savepath = f"{desktop_path}\\merged_{timestamp}.pdf"
    with open(savepath, "wb") as out:
        mergePDF.write(out)

def processInstructions(instructions: str, fileMap: dict[str, pdf.PdfReader], savepath: str) -> str:
    instructions = instructions.lower().replace(" ", "")
    instructions = instructions.split(",")
    mergePDF = pdf.PdfMerger()

    for instruction in instructions: #TODO clean
        result = False
        if instruction == "":
            continue
        if result == False:
            match = regex.match(r"^[a-z]$", instruction)
            if match is not None:
                char = match.group(0)
                result = executeInstruction(char, fileMap, mergePDF)
        if result == False:
            match = regex.match(r"^([a-z])(\d+)$", instruction)
            if match is not None:
                char = match.group(1)
                page = int(match.group(2))
                result = executeInstruction(char, fileMap, mergePDF, start=page, end=page)
        if result == False:
            match = regex.match(r"^([a-z])(\d+)-(\d+)$", instruction)
            if match is not None:
                char = match.group(1)
                start = int(match.group(2))
                end = int(match.group(3))
                result = executeInstruction(char, fileMap, mergePDF, start=start, end=end)
        if result == False:
            match = regex.match(r"^([a-z])(\d+)-$", instruction)
            if match is not None:
                char = match.group(1)
                start = int(match.group(2))
                result = executeInstruction(char, fileMap, mergePDF, start=start)
        
        if result == False:
            return f"Instruction \"{instruction}\" is an unrecognizd pattern"
        if result != True:
            return f"Instruction \"{instruction}\": {result}"
        
    saveMergedPDF(savepath, mergePDF)
    return None

def registerNewFiles(newFiles: tuple[str], fileMap: dict[str, pdf.PdfReader]) -> str:
    text = ""
    for i in range(len(newFiles)):
        char = chr(ord('a') + i)
        filename = os.path.basename(newFiles[i])
        reader = pdf.PdfReader(newFiles[i])
        fileMap[char] = reader
        text += f"{char}:     {filename}\n"
    return text


# if __name__=="__main__":
#     filemap = {'a': "testing\\1.2 Boolean Algebra.pdf", 'b': "testing\\1.3 Binary Arithmetic P1.pdf", 'c': "testing\\1.4 Binary Arithmetic P2.pdf"}
#     savepath = "testing\\merge.pdf"
#     instructions = "a20"
#     print(processInstructions(instructions, filemap, savepath))