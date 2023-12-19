# PDF Merger

## Description
This program allows numerous PDFs to be merged and rearranged in a very customizable manner.

## Installation

Option 1: Install the `.exe` file
Option 2: Clone this repo, create a python virtual environment, install `requirements.txt`, run `frontend.py`

## How to use
After running the program, use the `Add PDF(s)` button to select PDF(s) to be loaded. Each PDF loaded will be assigned a letter. Using the _instruction formats_ below, write instructions in the instruction box; these instructions determine which pages from each document will be placed in what order. Then, save the merged file using `Save` or `Save as`. Any errors will be shown in a pop-up window.

**Instruction Formats:** each instruction must be separated by a comma
- Entire Document `[doc letter]` (ex. `a`)
- Specific Page `[doc letter][page number]` (ex. `a2`)
- Page Range `[doc letter][first page]-[last page]` (ex. `a4-8`)
- All pages thereafter `[doc letter][first page]-` (ex. `a5-`)

**Other Notes:**
- `Save` will save the merged PDF to the user desktop with the name `merged_[timestamp].pdf`
- Up to 26 PDFs can be loaded at once
- PDFs with annotations can cause errors
- Control-W will close the program