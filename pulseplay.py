import re
import textwrap
from enum import Enum

from IPython.display import display, Markdown
from PIL import Image

import google.generativeai as genai

"""
Este script utiliza o Google Gemini para realizar tarefas relacionadas à música.
"""

# Carregue a chave da API Gemini de um arquivo ou variável de ambiente.
API_KEY_GEMINI = "AIzaSyAyiTQyntFnAU7vNSHKN4Uph9_3uineOnE"

genai.configure(api_key=API_KEY_GEMINI)

GENERATION_CONFIG = {
    "candidate_count": 1,
    "temperature": 0
}

SAFETY_SETTINGS = {
    'HATE': 'BLOCK_SOME',
    'HARASSMENT': 'BLOCK_SOME',
    'SEXUAL': 'BLOCK_SOME',
    'DANGEROUS': 'BLOCK_SOME'
}

model_img = genai.GenerativeModel(
    model_name="gemini-pro-vision",
    generation_config=GENERATION_CONFIG
)

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=GENERATION_CONFIG
)

# Converte um texto para o formato Markdown
def to_markdown(text: str) -> str:
    
    text = text.replace('•', ' *')
    text_lines = text.split('\n')
    markdown_text = '\n'.join(f"# {line}" for line in text_lines)
    return markdown_text

# Abre a imagem da partitura a partir do nome do arquivo
def abrir_imagem_partitura(nome_arquivo: str) -> Image:
    
    try:
        return Image.open(nome_arquivo)
    except FileNotFoundError:
        print(f"\033[1;31mArquivo '{nome_arquivo}' não encontrado!\033[m")
        return None
    except Exception as e:
        print(f"\033[1;31mErro ao abrir a imagem: {e}\033[m")
        return None

# Gera um guia de estudos de teoria musical com o Google Gemini
def gerar_guia_de_estudos():
    
    print("Você qual tipo de guia de estudos você quer?")
    print('''
          1 - Teoria Musical
          
          Mais opções em breve...
          ''')
    
    try:
        escolha = int(input("Digite uma opção: "))
        
        while escolha != 1:
            print("\033[1;31mDigite um opção válida\033[m")
            escolha = int(input("Digite uma opção: "))
            
        if escolha == 1:
            
            quantiade_de_dias = input("Você quer um guia de estudos para quantos dias? ")
            quantiade_de_vezes_na_semana = input("Quantas vezes na semana você quer estudar? ")
            horas_por_dia = input("Quantas horas por dia? ")
            
            response = model.generate_content(f'''Agora você é um maestro formado em havard, expert em teoria musical. Crie um guia de estudos para {quantiade_de_dias} dias, estudando {quantiade_de_vezes_na_semana} vezes na semana e {horas_por_dia} por dia, para que eu possa 
                                para aprender pelo menos o minímo de teoria musical nesse espaço tempo, não me sobrecarregando com muitos conteúdos para aprender, caso haja um curto espaço de tempo. 
                                Os conteúdos aumentaram os níveis de dificuldade gradativamente, a cada dia.''')
            
            markdown = to_markdown(response.text)
            print(markdown)
            display(markdown)
            
    except ValueError:
        print("\033[1;31mDigite uma opção válida!\033[m")
    
    except Exception: 
        print("\033[1;31mOcorreu um erro na aplicação!\033[m")

# Lê e interpreta uma partitura com o Google Gemini
def ler_partitura():
    
    arquivo = input("Digite o nome do arquivo da partitura (O arquivo precisa estar no diretório raiz): ")
    imagem = abrir_imagem_partitura(arquivo)
    
    print(100 * '-')

    try:
       response = model_img.generate_content(["Agora você um mestre em música, que é expert em partituras. Leia essa partitura",imagem , "e me faça um resumo separados por tópicos, me explicando tudo de forma detalhada e completa, porém com uma linguaguem simples, de fácil compreensão "], stream=True)
       response.resolve()
       markdown = to_markdown(response.text)
       print(markdown)
       display(markdown)

    except Exception:
        print("\033[1;31mUm erro ocorreu ao tentar processar a imagem. Tente novamente!\033[m")

# Converte uma partitura em cifra com o Google Gemini
def converter_partitura():
    
    arquivo = input("Digite o nome do arquivo da partitura (O arquivo precisa estar no diretório raiz):  ")
    imagem = abrir_imagem_partitura(arquivo)
    print(100 * '-')

    try:
       response = model_img.generate_content(["Converta essa partitura",imagem , "para cifra. Não coloque a letra da música, apenas a cifra. De um resumo geral no final sobre a partitura. "], stream=True)
       response.resolve()
       markdown = to_markdown(response.text)
       print(markdown)
       display(markdown)

    except Exception:
        print("\033[1;31mUm erro ocorreu ao tentar processar a imagem. Tente novamente!\033[m")
    


def interagir_com_lumi():
    chat = model.start_chat(history=[])
    prompt = '''A Partir de agora você é uma Inteligência artifical chamada "Lumi", uma IA especifica para música. 
    Você tem grande conhecimento sobre música e alta capacidade de compor e melhorar letras de músicas. 
    Tudo que perguntarem para você que não esteja relacionado a música você responderá: "Desculpe, não posso responder questões que não estão relacionadas a música". 
    Após o final desse comando, retorne para mim o texto: "Olá, sou a Lumi, uma inteligência artifcial treinada e com alta capacidade para compor e melhorar músicas! Como posso ajudar?'''
    response = chat.send_message(prompt)
    print("Resposta: ", response.text, "\n")
    prompt = input("Esperando prompt: ")

    while prompt != "fim":
        response = chat.send_message(prompt)
        print("Resposta: ", response.text, "\n")
        prompt = input("Esperando prompt: ")
        


class Opcoes(Enum):
    GUIA_DE_ESTUDOS = "GUIA DE ESTUDOS ( Irá montar um cronograma para o seu estudo de música )"
    LER_PARTITURA = "LER PARTITURA ( Irá ler uma partitura importada pelo usuário )"
    CONVERTER_PARTITURA = "CONVERTER PARTITURA ( Irá converter uma partitura importada pelo usuário para uma cifra )"
    LUMI = "LUMI(IA) (LUMI é uma Inteligência artificial que lhe ajudará a melhorar e compor suas músicas)"

# Define a função principal do código
def main():
    
    print(f'''Escolha uma opção:\n1 - {Opcoes.GUIA_DE_ESTUDOS.value}\n2 - {Opcoes.LER_PARTITURA.value}\n3 - {Opcoes.CONVERTER_PARTITURA.value}\n4 - {Opcoes.LUMI.value}\n''')
    try:
        
        escolha = int(input("Sua escolha: "))
        
        while escolha not in [1, 2, 3, 4]:
            print("\033[1;31mDigite uma opção válida!\033[m")
            escolha = int(input("Sua escolha: "))

        if escolha == 1:
            gerar_guia_de_estudos()
        elif escolha == 2:
            ler_partitura()
        elif escolha == 3:
            converter_partitura()
        elif escolha == 4:
            interagir_com_lumi()

    except ValueError:
        print("\033[1;31mDigite um número válido!\033[m")
    except Exception as e:
        print(f"\033[1;31mOcorreu um erro na aplicação: {e}\033[m")

if __name__ == "__main__":
    main()
    