import json

import anthropic
import requests
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()
MODELO = "claude-haiku-5-5"


def buscar_cep(cep):
    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=10)
        resposta.raise_for_status()
    except requests.RequestException as erro:
        return {"erro": f"Falha ao consultar a API: {erro}"}
    dados = resposta.json()
    if dados.get("erro"):
        return {"erro": "CEP não encontrado"}
    return {"rua": dados["logradouro"], "bairro": dados["bairro"], "cidade": dados["localidade"]}


FERRAMENTAS = [
    {
        "name": "buscar_cep",
        "description": "Busca rua, bairro e cidade de um CEP brasileiro.",
        "input_schema": {
            "type": "object",
            "properties": {"cep": {"type": "string", "description": "8 dígitos, só números"}},
            "required": ["cep"],
        },
    }
]

mensagens = [{"role": "user", "content": "Em que bairro fica o CEP 01001-000?"}]

print("1) Enviando a pergunta e a lista de ferramentas...")
resposta = client.messages.create(
    model=MODELO, max_tokens=2048, tools=FERRAMENTAS,
    output_config={"effort": "low"}, messages=mensagens,
)
print("2) stop_reason:", resposta.stop_reason)

if resposta.stop_reason != "tool_use":
    print("O modelo respondeu sem usar ferramenta:")
    print("".join(b.text for b in resposta.content if b.type == "text"))
else:
    bloco = next(b for b in resposta.content if b.type == "tool_use")
    print(f"3) O modelo pediu: {bloco.name}({bloco.input})")

    resultado = buscar_cep(**bloco.input)
    print("4) Resultado da ferramenta:", resultado)

    mensagens.append({"role": "assistant", "content": resposta.content})
    mensagens.append({"role": "user", "content": [{
        "type": "tool_result",
        "tool_use_id": bloco.id,
        "content": json.dumps(resultado, ensure_ascii=False),
    }]})

    final = client.messages.create(
        model=MODELO, max_tokens=2048, tools=FERRAMENTAS,
        output_config={"effort": "low"}, messages=mensagens,
    )
    print("5) Resposta final:", "".join(b.text for b in final.content if b.type == "text"))