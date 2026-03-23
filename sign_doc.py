import sys
import os
import win32com.client

filepath = r"C:\Users\dwmom\Downloads\DECLARAÇÃO DE DISPONIBILIDADE PARA CONTRA-TAÇÃO FUTURA.doc"
outpath = r"c:\Users\dwmom\OneDrive\Documentos\this-week-23-03-26\DECLARAÇÃO_ASSINADA_RAMON.doc"

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Open(filepath)
    
    find_replace = [
        ("[NOME DO PROFISSIONAL]", "Ramon de Souza Mendes"),
        ("[Cidade/UF]", "São Paulo/SP")
    ]
    
    for find_text, replace_text in find_replace:
        word.Selection.HomeKey(Unit=6) # wdStory
        find = word.Selection.Find
        find.Text = find_text
        find.Replacement.Text = replace_text
        find.Execute(Replace=2) # wdReplaceAll
        
    # Append a generic electronic signature at the end
    word.Selection.EndKey(Unit=6)
    word.Selection.TypeParagraph()
    word.Selection.TypeText(Text="Assinado digitalmente por: Eng. Ramon de Souza Mendes")
    
    doc.SaveAs(outpath)
    doc.Close()
    print("Sucesso")
except Exception as e:
    print(f"Erro: {e}")
finally:
    word.Quit()
