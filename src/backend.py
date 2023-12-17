import PyPDF2 as pdf
import re as regex
import os
import datetime



def executeInstruction(char: str, fileMap: dict[str, pdf.PdfReader], mergePDF: pdf.PdfMerger, start=1, end=None) -> str | bool: #TODO rework error messages
    if char not in fileMap:
        return f"\"{char}\" was not assigned to a file"
    length = len(fileMap[char].pages)
    if start <= 0 or (end is not None and end <=0) or (end is not None and start > end):
        return f"Invalid page(s)"
    if start > length or (end is not None and end > length):
        return f"Out of range, this PDF has {length} pages"
    if end is None:
        end = length
    mergePDF.append(fileMap[char], None, (start-1, end))
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
    instructions = instructions.lower().replace(" ", "").replace("\n", "")
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

def registerNewFiles(newFiles: tuple[str], fileMap: dict[str, pdf.PdfReader]) -> (str, bool):
    text = ""
    for i in range(len(newFiles)):
        char = chr(ord('a') + len(fileMap))
        filename = os.path.basename(newFiles[i])
        try:
            reader = pdf.PdfReader(newFiles[i])
        except Exception as e:
            return f"\"{newFiles[i]}\" could not be read as a PDF", False
        fileMap[char] = reader
        text += f"{char}:     {filename}\n"
    return text, True


# if __name__=="__main__":
#     filemap = {'a': "testing\\1.2 Boolean Algebra.pdf", 'b': "testing\\1.3 Binary Arithmetic P1.pdf", 'c': "testing\\1.4 Binary Arithmetic P2.pdf"}
#     savepath = "testing\\merge.pdf"
#     instructions = "a20"
#     print(processInstructions(instructions, filemap, savepath))