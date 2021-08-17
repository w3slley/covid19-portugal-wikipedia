import pdf
import sys

#write function(s) that return information on pdf

#example for you: getting string from pdf:
filename = sys.argv[1]
txt = pdf.convert_pdf_to_txt(filename)
print(txt.splitlines())
