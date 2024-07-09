# script.py

import os
import time
from instagrapi import Client
from datetime import datetime
import pytz

# Carregar credenciais do arquivo de configuração
from config import USERNAME, PASSWORD

# Função para agendar a postagem
def schedule_post(image_path, caption, post_time):
    current_time = datetime.now()
    time_difference = (post_time - current_time).total_seconds()

    if time_difference > 0:
        print(f"Aguardando {time_difference} segundos para postar...")
        time.sleep(time_difference)

    post_to_instagram(image_path, caption)

# Função para postar no Instagram
def post_to_instagram(image_path, caption):
    cl = Client()
    
    # Função de login com suporte para 2FA
    def login_with_2fa(username, password):
        try:
            cl.login(username, password)
        except Exception as e:
            if 'challenge_required' in str(e):
                print("Autenticação de dois fatores necessária.")
                cl.challenge_resolve_login(username, password)
            else:
                raise e

    login_with_2fa(USERNAME, PASSWORD)
    
    # Poste a imagem
    cl.photo_upload(image_path, caption)
    print("Postagem realizada com sucesso!")

# Função para ler o caption de um arquivo
def read_caption(caption_path):
    with open(caption_path, 'r', encoding='utf-8') as file:
        caption = file.read()
    return caption

# Obter a data atual no formato 'DD-MM-YY'
current_date = datetime.now().strftime('%d-%m-%y')

# Construir o caminho da pasta da data atual
current_directory = os.getcwd()
post_directory = os.path.join(current_directory, 'posts', current_date)

# Caminhos dos arquivos de imagem e caption
image_path = os.path.join(post_directory, 'post.png')
caption_path = os.path.join(post_directory, 'caption.txt')

# Ler o caption do arquivo
caption = read_caption(caption_path)

# Data e hora da postagem (hoje às 12:00)
post_time = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

# Agendar a postagem
schedule_post(image_path, caption, post_time)
