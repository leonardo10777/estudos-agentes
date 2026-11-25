"""Funções de apoio dos grafos: texto da resposta e custo."""
from config import PRECO_ENTRADA, PRECO_SAIDA


def texto_da(mensagem):
    """A resposta pode vir em blocos (thinking, text). Junta só os blocos de texto."""
    if isinstance(mensagem.content, str):
        return mensagem.content
    return "".join(b.get("text", "") for b in mensagem.content
                   if isinstance(b, dict) and b.get("type") == "text")


def custo_usd(mensagens):
    total = 0.0
    for m in mensagens:
        uso = getattr(m, "usage_metadata", None)
        if uso:
            total += uso["input_tokens"] * PRECO_ENTRADA + uso["output_tokens"] * PRECO_SAIDA
    return total