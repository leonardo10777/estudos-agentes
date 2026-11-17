"""Agente de campanhas v2: erros, retries, logs, custo e tempo."""
import json
from datetime import datetime
from time import perf_counter

import anthropic
from dotenv import load_dotenv

from ferramentas import FERRAMENTAS, executar_ferramenta

load_dotenv()
client = anthropic.Anthropic(max_retries=4, timeout=60)

MODELO = "claude-haiku-5-5"
MAX_VOLTAS = 8
PRECO_ENTRADA = 0.10 / 1_000_000
PRECO_SAIDA = 0.50 / 1_000_000
SISTEMA = (
    "Você é um analista de mídia paga. Responda perguntas sobre as campanhas "
    "usando só os dados das ferramentas. Os dados vão de 2026-07-28 a 2026-10-25. "
    "Use sempre as ferramentas para buscar os números antes de responder. "
    "Nunca invente números. "
    "Se faltar dado (outro canal, outro período), diga claramente que a informação não está disponível. "
    "Quando a pergunta pedir um total, some os valores devolvidos pelas ferramentas. "
    "Responda em português, em até 4 frases, com os números que sustentam a resposta."
)


def registrar(evento):
    evento["hora"] = datetime.now().isoformat(timespec="seconds")
    with open("log_agente.jsonl", "a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(evento, ensure_ascii=False) + "\n")


def perguntar(pergunta):
    mensagens = [{"role": "user", "content": pergunta}]
    custo_usd = 0.0

    for volta in range(1, MAX_VOLTAS + 1):
        try:
            inicio = perf_counter()
            resposta = client.messages.create(
                model=MODELO,
                max_tokens=4096,
                system=SISTEMA,
                tools=FERRAMENTAS,
                output_config={"effort": "low"},
                messages=mensagens,
            )
            duracao = perf_counter() - inicio
        except anthropic.APIConnectionError:
            registrar({"pergunta": pergunta, "volta": volta, "erro": "sem conexão"})
            return "Erro: sem conexão com a API (tentei de novo e não deu)."
        except anthropic.APIStatusError as erro:
            registrar({
                "pergunta": pergunta,
                "volta": volta,
                "erro": f"HTTP {erro.status_code}",
            })
            return f"Erro da API: HTTP {erro.status_code}."

        uso = resposta.usage
        custo_usd += (
            uso.input_tokens * PRECO_ENTRADA
            + uso.output_tokens * PRECO_SAIDA
        )
        mensagens.append({"role": "assistant", "content": resposta.content})

        chamadas = [b for b in resposta.content if b.type == "tool_use"]
        registrar({
            "pergunta": pergunta,
            "volta": volta,
            "stop_reason": resposta.stop_reason,
            "tokens_entrada": uso.input_tokens,
            "tokens_saida": uso.output_tokens,
            "tempo_segundos": round(duracao, 3),
            "ferramentas": [
                {"nome": b.name, "entrada": b.input}
                for b in chamadas
            ],
        })

        if resposta.stop_reason != "tool_use":
            texto = "".join(
                b.text for b in resposta.content if b.type == "text"
            )
            print(f"  [{volta} volta(s) | custo US$ {custo_usd:.5f}]")
            return texto

        resultados = []
        for bloco in chamadas:
            try:
                saida = executar_ferramenta(bloco.name, bloco.input)
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": bloco.id,
                    "content": saida,
                })
            except Exception as erro:
                registrar({
                    "pergunta": pergunta,
                    "volta": volta,
                    "erro_ferramenta": str(erro),
                })
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": bloco.id,
                    "content": f"Erro: {erro}",
                    "is_error": True,
                })

        mensagens.append({"role": "user", "content": resultados})

    return "Parei: limite de voltas atingido sem resposta final."


if __name__ == "__main__":
    print(perguntar(input("Pergunta: ")))