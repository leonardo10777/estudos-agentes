import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("Python:", sys.version.split()[0])
print("Chave carregada?", "sim" if os.getenv("ANTHROPIC_API_KEY") else "não")