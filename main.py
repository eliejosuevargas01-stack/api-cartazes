import requests
from fastapi import FastAPI
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from pydantic import BaseModel
from typing import List

class Produto(BaseModel):
    produto: str
    validade: str
    quantidade: int

app = FastAPI()

@app.post("/gerar-pdf")
def processar_lista(produtos:List[Produto], webhook_url: str = "https://myn8n.seommerce.shop/webhook/receber-pdf-pronto"):
    print("Iniciando processamento...") # <--- Verifique se isso aparece no terminal do uvicorn
    
    nome_arquivo = "cartazes.pdf"
    folha_paisagem = landscape(A4)
    c = canvas.Canvas(nome_arquivo, pagesize=folha_paisagem)
    
    largura, altura = folha_paisagem
    centro = largura / 2

    for item in produtos:
        print(f"Processando produto: {item.produto}") # <--- Verifique se isso aparece
        for _ in range(item.quantidade):
            c.setFont("Helvetica-Bold", 100)
            c.drawCentredString(centro, 400, item.produto.upper())
            c.setFont("Helvetica-Bold", 120)
            c.drawCentredString(centro, 250, item.validade)
            c.showPage()
    
    print("Salvando arquivo...") # <--- Verifique se isso aparece
    c.save()
    print("Arquivo salvo com sucesso!") # <--- Verifique se isso aparece
    
whith open(nome_arquivo,'rb') as f:
    files = {'file': (nome_arquivo, f, 'application/pdf')}
    requests.post(webhook_url, file=files)

    return {"message": "PDF pronto para impressão!"}