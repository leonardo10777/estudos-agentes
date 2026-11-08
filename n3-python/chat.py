import anthropic
from dotenv import load_dotenv      

load_dotenv()
client = anthropic.Anthropic()

MODELO = "claude-haiku-5-5"
PRECO_ENTRADA = 0.10 / 1_000_000
PRECO_SAIDA = 0.50 / 1_000_000
DOLAR = 5.50

historico = []
custo_total = 0.0

while True:
    pergunta = input("\nVocê (ou 'sair'): ")
    if pergunta.lower() == "sair":
        break
    historico.append({"role": "user", "content" : pergunta})
    
    resposta = client.messages.create(
        model=MODELO,
        max_tokens=2048,
        system="Você é um assistente de mídia paga. Responda em português, sempre em tópicos curtos.",
        output_config={"effort": "low"},
        messages=historico,
    )
    texto = "".join(b.text for b in resposta.content if b.type == "text")
    historico.append({"role": "assistant", "content" : resposta.content})
    
    entrada = resposta.usage.input_tokens
    saida = resposta.usage.output_tokens
    custo = (entrada * PRECO_ENTRADA + saida * PRECO_SAIDA) * DOLAR
    custo_total += custo
    
    print(f"\nClaude: {texto}")
    print(f"[tokens: {entrada} de entrada, {saida} de saída | R$ {custo:.5f} | total R$ {custo_total:.5f}]")