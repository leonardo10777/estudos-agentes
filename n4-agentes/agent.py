"""Agente do zero: a classe Agent separa estado, ferramentas e loop."""
import anthropic
from dotenv import load_dotenv

from config import MAX_VOLTAS, MODELO, PRECO_ENTRADA, PRECO_SAIDA, SISTEMA
from ferramentas import FERRAMENTAS, executar_ferramenta

load_dotenv()


class Agent:
    def __init__(self, sistema, ferramentas, executar, max_voltas=MAX_VOLTAS):
        self.client = anthropic.Anthropic(max_retries=4, timeout=60)
        self.sistema = sistema            # instruções
        self.ferramentas = ferramentas    # o que o modelo enxerga (descrições)
        self.executar = executar          # o que o código realmente roda
        self.max_voltas = max_voltas      # freio
        self.mensagens = []               # estado: o bloco de notas
        self.custo_usd = 0.0

    def _chamar_modelo(self):
        resposta = self.client.messages.create(
            model=MODELO,
            max_tokens=4096,
            system=self.sistema,
            tools=self.ferramentas,
            output_config={"effort": "low"},
            messages=self.mensagens,
        )
        self.custo_usd += (resposta.usage.input_tokens * PRECO_ENTRADA
                           + resposta.usage.output_tokens * PRECO_SAIDA)
        return resposta

    def _usar_ferramentas(self, resposta, volta):
        resultados = []
        for bloco in resposta.content:
            if bloco.type != "tool_use":
                continue
            print(f"  [volta {volta}] {bloco.name}({bloco.input})")
            try:
                saida = self.executar(bloco.name, bloco.input)
                resultados.append({"type": "tool_result", "tool_use_id": bloco.id, "content": saida})
            except Exception as erro:
                resultados.append({"type": "tool_result", "tool_use_id": bloco.id,
                                   "content": f"Erro: {erro}", "is_error": True})
        return resultados

    def rodar(self, pergunta):
        self.mensagens.append({"role": "user", "content": pergunta})

        for volta in range(1, self.max_voltas + 1):
            resposta = self._chamar_modelo()
            self.mensagens.append({"role": "assistant", "content": resposta.content})

            if resposta.stop_reason != "tool_use":
                print(f"O agente usou {volta} volta(s).")
                return "".join(b.text for b in resposta.content if b.type == "text")

            self.mensagens.append({"role": "user", "content": self._usar_ferramentas(resposta, volta)})

        print(f"O agente usou {self.max_voltas} volta(s).")
        return "Parei: limite de voltas atingido sem resposta final."


if __name__ == "__main__":
    agente = Agent(SISTEMA, FERRAMENTAS, executar_ferramenta)
    for pergunta in [
        "Qual canal teve o maior CPA de 01/10 a 25/10?",
        "E qual teve o menor?",
    ]:
        print(agente.rodar(pergunta))
        print(f"mensagens: {len(agente.mensagens)} | custo acumulado: US$ {agente.custo_usd:.5f}")