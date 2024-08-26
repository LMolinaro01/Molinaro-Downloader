import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import customtkinter
import yt_dlp
import os

QUALITY_OPTIONS = ['MP4', 'MP3']

def selecionar_diretorio():
    return filedialog.askdirectory()

def realizar_download():
    try:
        link_video = entrada_link.get()

        # Selecionar o diretório antes de configurar as opções de download
        diretorio_destino = selecionar_diretorio()
        if not diretorio_destino:
            label_status.configure(text="Nenhum diretório selecionado.", text_color="red")
            return
        
        ydl_opts = {}
        if combobox_var.get() == 'MP4':
            ydl_opts = {
                'format': 'best[ext=mp4]',  # Seleciona o melhor vídeo em MP4 com áudio embutido
                'outtmpl': os.path.join(diretorio_destino, '%(title)s.%(ext)s'),
            }
        elif combobox_var.get() == 'MP3':
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',  # Seleciona o melhor áudio (M4A é suportado sem ffmpeg)
                'outtmpl': os.path.join(diretorio_destino, '%(title)s.%(ext)s'),
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link_video, download=False)
            video_title = info_dict.get('title', None)
            label_titulo.configure(text=video_title, text_color="white")
            
            # Mostrar a barra de progresso antes de iniciar o download
            barra_progresso.pack(pady=10)
            barra_progresso.set(0)
            label_porcentagem.configure(text="0%")
            label_status.configure(text="Download em Andamento", text_color="white")
            
            # Iniciar o download
            ydl.download([link_video])
            
            label_status.configure(text="Download Concluído!", text_color="white")

            # Mostrar a thumbnail do vídeo
            thumbnail_url = info_dict['thumbnail']
            mostrar_thumbnail(thumbnail_url)

    except Exception as e:
        label_status.configure(text="Erro ao Realizar o Download", text_color="red")
        print(e)

def mostrar_thumbnail(thumbnail_url):
    try:
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((320, 180), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        
        label_thumbnail.configure(image=img_tk)
        label_thumbnail.image = img_tk  # Manter uma referência da imagem para não ser coletada pelo garbage collector
    except Exception as e:
        print(f"Erro ao carregar a thumbnail: {e}")

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

combobox_var = customtkinter.StringVar(value='MP4')
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

#Arrumar a barra de progresso e adicionar tamanho estimado
janela.mainloop()
