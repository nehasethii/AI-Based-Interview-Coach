import zipfile
import re
import os

def extract_text_from_docx(doc_path):
    try:
        with zipfile.ZipFile(doc_path) as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            # Extract text
            text = re.sub('<w:p[^>]*>', '\n', xml_content)
            text = re.sub('<[^>]+>', '', text)
            print("Extracted Length:", len(text))
            print("--- START ---")
            print(text[:3000])
            print("--- END ---")
    except Exception as e:
        print('Error:', e)

extract_text_from_docx(r'C:\Users\Dell\Downloads\Synopsis AI-Interview-Coach.docx')
