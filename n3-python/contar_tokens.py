import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODELO = "claude-haiku-5-5"
PERGUNTAS = {
    "português": "Qual canal teve o maior CPA na semana passada?",
    "inglês": "Which channel had the highest CPA last week?",
}

for idioma, pergunta in PERGUNTAS.items():
    contagem = client.messages.count_tokens(
        model=MODELO,
        messages=[{"role": "user", "content": pergunta}],
    )
    print(f"{idioma}: {contagem.input_tokens} tokens")