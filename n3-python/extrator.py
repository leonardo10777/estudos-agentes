import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
client = anthropic.Anthropic()


class ResultadoCampanha(BaseModel):
    campanha: str
    canal: str = Field(description="Meta Ads, Google Ads ou TikTok Ads")
    gasto: float | None = None
    conversoes: int
    periodo: str = Field(description="período citado no texto, como escrito")
    cliques: int | None = None


texto = (
    "A Campanha de Google de P Max, ela teve somente 5 conversões e gastou "
    "R$ 1.500 na semana passada, dos dias 08 até 14 de Setembro."
)

resposta = client.messages.parse(
    model="claude-haiku-5-5",
    max_tokens=2048,
    output_config={"effort": "low"},
    messages=[{
        "role": "user",
        "content": f"Extraia os dados da campanha deste texto. Se um dado não estiver no texto, use null.\n\n{texto}",
    }],
    output_format=ResultadoCampanha,
)

print("stop_reason:", resposta.stop_reason)
dados = resposta.parsed_output
print(dados)

if dados.gasto is None:
    print("CPA indisponível: gasto não informado")
else:
    print(f"CPA calculado no Python: R$ {dados.gasto / dados.conversoes:.2f}")