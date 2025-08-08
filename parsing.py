import PyPDF2

def extract_text(file):
    
    text = ""
    with open(file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# if __name__ == "__main__":
#     path = r''
#     input_pdf_path = input(f"Enter PDF path (default: {path}): ") or path
#     text = extract_text(input_pdf_path)
#     print(text)