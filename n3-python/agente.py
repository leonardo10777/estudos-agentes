"""Agente de campanhas: loop com ferramentas e limite de voltas."""
import anthropic
from dotenv import load_dotenv

from ferramentas import FERRAMENTAS, executar_ferramenta

load_dotenv()
client = anthropic.Anthropic()

MODELO = "claude-haiku-5-5"
MAX_VOLTAS = 8
SISTEMA = (
    "Você é um analista de mídia paga. Responda perguntas sobre as campanhas "
    "usando só os dados das ferramentas. Os dados vão de 2026-07-28 a 2026-10-25. "
    "Nunca invente números. Se não der para responder com as ferramentas, diga isso. "
    "Responda em português, em até 4 frases, com os números que sustentam a resposta."
)


def perguntar(pergunta):
    mensagens = [{"role": "user", "content": pergunta}]

    for volta in range(1, MAX_VOLTAS + 1):
        resposta = client.messages.create(
            model=MODELO,
            max_tokens=4096,
            system=SISTEMA,
            tools=FERRAMENTAS,
            output_config={"effort": "low"},
            messages=mensagens,
        )
        print(f"[volta {volta}] stop_reason: {resposta.stop_reason}")
        mensagens.append({"role": "assistant", "content": resposta.content})

        if resposta.stop_reason != "tool_use":
            return "".join(b.text for b in resposta.content if b.type == "text")

        resultados = []
        for bloco in resposta.content:
            if bloco.type != "tool_use":
                continue
            print(f"  [volta {volta}] {bloco.name}({bloco.input})")
            try:
                saida = executar_ferramenta(bloco.name, bloco.input)
                resultados.append({"type": "tool_result", "tool_use_id": bloco.id, "content": saida})
            except Exception as erro:
                resultados.append({"type": "tool_result", "tool_use_id": bloco.id,
                                   "content": f"Erro: {erro}", "is_error": True})
        mensagens.append({"role": "user", "content": resultados})

    return "Parei: limite de voltas atingido sem resposta final."


if __name__ == "__main__":
    pergunta = input("Pergunta: ")
    print(perguntar(pergunta))