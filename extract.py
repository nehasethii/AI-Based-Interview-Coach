import zipfile
import re
def extract_text(doc_path):
    with zipfile.ZipFile(doc_path) as docx:
        text = re.sub('<w:p[^>]*>', '\n', docx.read('word/document.xml').decode('utf-8'))
        text = re.sub('<[^>]+>', '', text)
        with open('prd.txt', 'w', encoding='utf-8') as f:
            f.write(text)
extract_text(r'C:\Users\Dell\Downloads\Synopsis AI-Interview-Coach.docx')
