import anthropic
from dotenv import load_dotenv

from ferramentas import FERRAMENTAS, executar_ferramenta

load_dotenv()
client = anthropic.Anthropic()
MODELO = "claude-haiku-5-5"
SISTEMA = "Você é um analista de mídia paga. Os dados vão de 2026-07-28 a 2026-10-25. Nunca invente números."

pergunta = "Qual canal teve o maior CPA de 01/10 a 25/10?"
mensagens = [{"role": "user", "content": pergunta}]

resposta = client.messages.create(
    model=MODELO, max_tokens=2048, system=SISTEMA, tools=FERRAMENTAS,
    output_config={"effort": "low"}, messages=mensagens,
)
print("stop_reason:", resposta.stop_reason)

if resposta.stop_reason == "tool_use":
    mensagens.append({"role": "assistant", "content": resposta.content})
    resultados = []
    for bloco in resposta.content:
        if bloco.type == "tool_use":
            print(f"Ferramenta pedida: {bloco.name}({bloco.input})")
            saida = executar_ferramenta(bloco.name, bloco.input)
            print("Resultado:", saida)
            resultados.append({"type": "tool_result", "tool_use_id": bloco.id, "content": saida})
    mensagens.append({"role": "user", "content": resultados})

    resposta = client.messages.create(
        model=MODELO, max_tokens=2048, system=SISTEMA, tools=FERRAMENTAS,
        output_config={"effort": "low"}, messages=mensagens,
    )

print("\nResposta:", "".join(b.text for b in resposta.content if b.type == "text"))