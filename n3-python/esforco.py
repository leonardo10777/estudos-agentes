import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODELO = "claude-haiku-5-5"
PERGUNTA = (
    "A campanha A gastou R$ 1.260 e teve 35 conversões. "
    "A campanha B gastou R$ 630 e teve 13 conversões. "
    "Qual tem o menor CPA e quantos por cento o outro é mais caro? Mostre a conta."
)

for esforco in ["low", "medium"]:
    resposta = client.messages.create(
        model=MODELO,
        max_tokens=4096,
        output_config={"effort": esforco},
        messages=[{"role": "user", "content": PERGUNTA}],
    )
    texto = "".join(b.text for b in resposta.content if b.type == "text")
    print(f"\n=== esforço: {esforco} ===")
    print(texto)
    print(f"[tokens: {resposta.usage.input_tokens} de entrada, {resposta.usage.output_tokens} de saída]")