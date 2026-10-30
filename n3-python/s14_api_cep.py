import requests

def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        return {"erro": f"Falha ao consultar a API: {erro}"}
    
    dados = resposta.json()
    if dados.get("erro"):
        return {"erro": "CEP não encontrado."}
    return {"rua": dados["logradouro"], "bairro": dados["bairro"], "cidade": dados["localidade"], "unidade federativa": dados["uf"]}



print(buscar_cep("01001000"))
print(buscar_cep("99999999"))
print(buscar_cep("123"))
