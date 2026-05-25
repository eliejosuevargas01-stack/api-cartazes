# 1. // IMPORTAÇÃO DAS BIBLIOTECAS
# // Aqui você chama as ferramentas que o Python vai usar.
# from fastapi import FastAPI, Request
# import uvicorn # Usado para ligar o servidor
# from reportlab.pdfgen import canvas # Biblioteca para desenhar o PDF
from fastapi import FastAPI, Request
import uvicorn
from reportlab.pdfgen import canvas
# 2. // INICIALIZAÇÃO DO SERVIDOR
# // Cria a instância da sua API.
# app = FastAPI()
app = FastAPI()
# 3. // LISTA DE ARMAZENAMENTO (MEMÓRIA TEMPORÁRIA)
# // Como você vai enviar um por um, crie uma lista vazia fora das rotas, no escopo global.
# lista_de_produtos = []
lista_de_produtos = []
# 4. // ROTA PARA RECEBER PRODUTOS (MÉTODO POST)
# // O n8n vai enviar os dados aqui. 
# // Use a função @app.post("/adicionar")
# // Dentro da função, você deve receber os dados do JSON (Request).
# // Pegue os dados (nome, validade, quantidade) e use o método .append() na lista.
# // Exemplo: lista_de_produtos.append(novo_item)
@app.post("/adicionar")
async def adicionar_produto(request: Request):
    dados = await request.json()
    lista_de_produtos.append(dados)
    return {"status": "Produto adicionado"}

# 5. // ROTA PARA GERAR O PDF E LIMPAR
# // Use @app.post("/finalizar")
# // O que fazer aqui:
# // a) Use o 'for' para percorrer a sua lista_de_produtos.
# // b) Para cada item, use a biblioteca reportlab (canvas) para criar o PDF.
# // c) O 'x' na sua mensagem vira o multiplicador: use um 'for' aninhado (um 'for' dentro de outro)
# //    para repetir a criação da página/cartaz a quantidade de vezes que o multiplicador pede.
# // d) Depois que o PDF for salvo, limpe a lista usando lista_de_produtos.clear()
# //    para que a próxima rodada comece vazia.

# 6. // EXECUÇÃO DO SERVIDOR
# // No final do arquivo, coloque a condição para rodar o servidor:
# // if __name__ == "__main__":
# //    uvicorn.run(app, host="0.0.0.0", port=8000)

# DICA DE FUNÇÕES ADICIONAIS:
# Você pediu outras funções além de if/else/for.
# 1. Definição de função: Use 'def nome_da_funcao(argumentos):'.
#    Isso ajuda a organizar o código. Ex: def criar_cartaz(nome, validade):
# 2. Manipulação de lista: Use '.append()' para adicionar e '.clear()' para esvaziar.
# 3. Manipulação de String: Use '.split()' para separar os campos que o n8n enviar.