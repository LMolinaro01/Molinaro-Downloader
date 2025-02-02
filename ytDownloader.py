import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import customtkinter
import yt_dlp
import os
from time import strftime
import fpdf  # Biblioteca para gerar PDF
import re  # Biblioteca para sanitizar nomes de arquivos

# Cole sua chave de API do DeepSeek aqui
DEEPSEEK_API_KEY = "suachaveapi"

QUALITY_OPTIONS = ['Video', 'Audio', 'PDF']

def selecionar_diretorio():
    try:
        diretorio_destino = filedialog.askdirectory()
        if not diretorio_destino:
            raise Exception("Nenhum diretório selecionado.")
        label_diretorio.configure(text=f"Diretório selecionado: {diretorio_destino}", text_color="white")
        return diretorio_destino
    except Exception as e:
        label_diretorio.configure(text=str(e), text_color="red")
        raise  # Lança a exceção para ser tratada no download

def transcrever_video(video_title, video_description):
    try:
        # Configuração da chamada para a API do DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": f"Título: {video_title}\nDescrição: {video_description}\nGere um resumo e uma transcrição organizada.",
            "max_tokens": 1500,
            "temperature": 0.7,
        }
        response = requests.post(
            "https://api.deepseek.com/v1/completions",  # URL da API do DeepSeek
            headers=headers,
            json=data
        )
        response.raise_for_status()
        transcricao = response.json()['choices'][0]['text'].strip()
        return transcricao
    except requests.exceptions.RequestException as e:
        return f"Erro ao transcrever o vídeo: {e}"

def sanitize_filename(filename):
    # Remove ou substitui caracteres inválidos para nomes de arquivos no Windows
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def gerar_pdf(diretorio_destino, video_title, thumbnail_path, transcricao):
    try:
        pdf = fpdf.FPDF()
        pdf.add_page()

        # Adicionar título
        pdf.set_font("Arial", size=24, style="B")
        pdf.cell(200, 10, txt=video_title, ln=True, align='C')

        # Adicionar a transcrição
        pdf.set_font("Arial", size=12)
        pdf.ln(85)  # Pula linhas para não sobrepor a imagem
        pdf.multi_cell(0, 10, transcricao)

        # Sanitizar o título do vídeo para usá-lo como nome do arquivo
        video_title_sanitized = sanitize_filename(video_title)

        # Salvar o PDF com o nome sanitizado
        pdf_output_path = os.path.join(diretorio_destino, f"{video_title_sanitized}.pdf")
        pdf.output(pdf_output_path)
        label_status.configure(text=f"PDF criado: {pdf_output_path}", text_color="green")

    except Exception as e:
        label_status.configure(text=f"Erro ao criar PDF: {str(e)}", text_color="red")

def realizar_download():
    try:
        link_video = entrada_link.get()

        if not link_video.strip():
            raise ValueError("O link do vídeo está vazio.")

        diretorio_destino = selecionar_diretorio()

        ydl_opts = {}
        if combobox_var.get() == 'Video':
            ydl_opts = {
                'format': 'best[ext=mp4]',  # Melhor vídeo em MP4
                'outtmpl': os.path.join(diretorio_destino, '%(title)s.%(ext)s'),
                'progress_hooks': [hook_progresso],
                'nocolor': True,
            }
        elif combobox_var.get() == 'Audio':
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',  # Melhor áudio em M4A
                'outtmpl': os.path.join(diretorio_destino, '%(title)s.%(ext)s'),
                'progress_hooks': [hook_progresso],
                'nocolor': True,
            }
        elif combobox_var.get() == 'PDF':
            ydl_opts = {
                'format': 'best[ext=mp4]',  # Melhor vídeo para transcrição
                'outtmpl': os.path.join(diretorio_destino, '%(title)s.%(ext)s'),
                'progress_hooks': [hook_progresso],
                'nocolor': True,
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link_video, download=False)
            video_title = info_dict.get('title', None)
            video_description = info_dict.get('description', 'Descrição indisponível')
            thumbnail_url = info_dict.get('thumbnail', None)

            label_titulo.configure(text=video_title, text_color="white")

            # Se for a opção PDF, fazer a transcrição e gerar o PDF
            if combobox_var.get() == 'PDF':
                # Baixar o vídeo primeiro
                ydl.download([link_video])

                # Baixar a thumbnail
                thumbnail_path = None
                if thumbnail_url:
                    thumbnail_path = baixar_thumbnail(thumbnail_url, diretorio_destino)

                # Gerar a transcrição
                transcricao = transcrever_video(video_title, video_description)

                # Gerar o PDF
                gerar_pdf(diretorio_destino, video_title, thumbnail_path, transcricao)

            else:
                # Download de vídeo ou áudio
                ydl.download([link_video])

    except Exception as e:
        label_status.configure(text=f"Erro: {str(e)}", text_color="red")
        print(e)

def hook_progresso(d):
    if d['status'] == 'downloading':
        if d.get('total_bytes') and d.get('downloaded_bytes'):
            porcentagem = d['downloaded_bytes'] / d['total_bytes'] * 100
            barra_progresso.set(porcentagem / 100)
            label_porcentagem.configure(text=f"{porcentagem:.2f}%")
        else:
            label_porcentagem.configure(text="Progresso não disponível")

    if d['status'] == 'finished':
        barra_progresso.set(1)
        label_porcentagem.configure(text="100%")
        label_status.configure(text="Download Concluído!", text_color="white")

def mostrar_thumbnail(thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((320, 180), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        
        label_thumbnail.configure(image=img_tk)
        label_thumbnail.image = img_tk
    except Exception as e:
        label_status.configure(text="Erro ao carregar thumbnail", text_color="red")
        print(f"Erro ao carregar a thumbnail: {e}")

def baixar_thumbnail(thumbnail_url, diretorio_destino):
    try:
        response = requests.get(thumbnail_url)
        thumbnail_path = os.path.join(diretorio_destino, 'thumbnail.jpg')
        with open(thumbnail_path, 'wb') as f:
            f.write(response.content)
        return thumbnail_path
    except Exception as e:
        label_status.configure(text=f"Erro ao baixar a thumbnail: {str(e)}", text_color="red")
        return None

# Inicialização da interface
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

janela = customtkinter.CTk()
janela.geometry("720x650")
janela.title("Molinaro's Downloader")

label_titulo = customtkinter.CTkLabel(janela, text="Video Link", font=("Consolas bold", 17))
label_titulo.pack(padx=10, pady=10)

label_thumbnail = customtkinter.CTkLabel(janela, text="")
label_thumbnail.pack(pady=10)

url = tk.StringVar()
entrada_link = customtkinter.CTkEntry(janela, width=550, height=40, textvariable=url)
entrada_link.pack(pady=10)

combobox_var = customtkinter.StringVar(value='Video')
combobox = customtkinter.CTkComboBox(janela, values=QUALITY_OPTIONS, variable=combobox_var, width=250)
combobox.pack(pady=15)

botao_download = customtkinter.CTkButton(janela, text="Download", command=realizar_download, width=250, font=("Consolas", 13))
botao_download.pack(pady=10)

label_diretorio = customtkinter.CTkLabel(janela, text="")
label_diretorio.pack(pady=10)

label_status = customtkinter.CTkLabel(janela, text="")
label_status.pack(pady=10)

label_porcentagem = customtkinter.CTkLabel(janela, text="")
label_porcentagem.pack(pady=10)

barra_progresso = customtkinter.CTkProgressBar(janela, width=400)
barra_progresso.set(0)
barra_progresso.pack_forget()

# Relógio no canto inferior direito
def mostrar_relogio():
    horario_atual = strftime('%H:%M:%S')
    label_relogio.configure(text=horario_atual)
    label_relogio.after(1000, mostrar_relogio)

label_relogio = customtkinter.CTkLabel(janela, text="")
label_relogio.place(relx=1.0, rely=1.0, anchor="se")
mostrar_relogio()

janela.mainloop()
