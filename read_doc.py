import sys
import os

filepath = r"C:\Users\dwmom\Downloads\DECLARAÇÃO DE DISPONIBILIDADE PARA CONTRA-TAÇÃO FUTURA.doc"

try:
    import win32com.client
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(filepath)
    text = doc.Content.Text
    doc.Close()
    word.Quit()
    with open("doc_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
except Exception as e:
    print(f"Failed with Word. Trying string extraction: {e}")
    with open(filepath, "rb") as f:
        data = f.read()
    strings = []
    for line in data.split(b"\n"):
        cleaned = bytes([b for b in line if 32 <= b <= 126 or b > 127])
        if cleaned:
            strings.append(cleaned.decode("latin-1", errors="ignore"))
    with open("doc_text.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(strings))
