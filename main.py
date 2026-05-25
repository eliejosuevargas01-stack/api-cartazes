import requests
from fastapi import FastAPI, Body
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from pydantic import BaseModel
from typing import List, Union
import base64
import os

class Produto(BaseModel):
    produto: str
    validade: str
    quantidade: Union[int, str]
    
    def __init__(self, **data):
        super().__init__(**data)
        # Converte quantidade para int se for string
        if isinstance(self.quantidade, str):
            self.quantidade = int(self.quantidade)

app = FastAPI()

WEBHOOK_URL = os.getenv(
    "N8N_WEBHOOK_URL",
    "https://myn8n.seommerce.shop/webhook/receber-pdf-pronto",
)

@app.get("/")
def health_check():
    """Endpoint de health check para o Coolify"""
    return {"status": "ok", "message": "API de cartazes funcionando"}

@app.get("/health_check")
def health_check_alternate():
    """Endpoint de health check alternativo"""
    return {"status": "ok"}


def _ajustar_fonte_produto(texto: str, largura_maxima: float) -> int:
    fonte = "Helvetica-Bold"
    tamanho_maximo = 100
    tamanho_minimo = 28

    for tamanho in range(tamanho_maximo, tamanho_minimo - 1, -2):
        largura_texto = stringWidth(texto, fonte, tamanho)
        if largura_texto <= largura_maxima:
            return tamanho

    return tamanho_minimo


@app.post("/gerar-pdf")
def processar_lista(body: Union[List[Produto], dict] = Body(...)):
    try:
        print("Iniciando processamento...")
        
        # Se for dict com 'produtos', pega o array
        if isinstance(body, dict):
            produtos_list = body.get('produtos', [])
            produtos = [Produto(**p) if isinstance(p, dict) else p for p in produtos_list]
        else:
            # Se for array direto
            produtos = body
        
        nome_arquivo = "cartazes.pdf"
        folha_paisagem = landscape(A4)
        c = canvas.Canvas(nome_arquivo, pagesize=folha_paisagem)

        largura, altura = folha_paisagem
        centro = largura / 2

        for item in produtos:
            print(f"Processando produto: {item.produto}")
            for _ in range(item.quantidade):
                nome_produto = item.produto.upper()
                largura_util = largura - 120
                tamanho_fonte = _ajustar_fonte_produto(nome_produto, largura_util)

                c.setFont("Helvetica-Bold", tamanho_fonte)
                c.drawCentredString(centro, 400, nome_produto)

                c.setFont("Helvetica-Bold", 120)
                c.drawCentredString(centro, 250, item.validade)
                c.showPage()
        
        print("Salvando arquivo...")
        c.save()
        print("Arquivo salvo com sucesso!")
        
        with open(nome_arquivo,'rb') as f:
            files = {'file': (nome_arquivo, f, 'application/pdf')}
            response = requests.post(WEBHOOK_URL, files=files, timeout=30)
            response.raise_for_status()
            print(f"Webhook enviado com sucesso: {response.status_code}")
        
        return {"message": "PDF pronto para impressão!"}
    
    except Exception as e:
        print(f"Erro ao processar PDF: {str(e)}")
        return {"error": str(e)}
