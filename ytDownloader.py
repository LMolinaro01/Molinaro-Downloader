import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import customtkinter
from pytube import YouTube, exceptions
from moviepy.editor import AudioFileClip
import os

# exibir mensagem quando "is age restricted, and can't be accessed without logging in."
# python -m auto_py_to_exe

QUALITY_OPTIONS = ['MP4', 'MP3']

def selecionar_diretorio():
    diretorio_destino = filedialog.askdirectory()
    if diretorio_destino:
        label_diretorio.configure(text=f"Diretório selecionado: {diretorio_destino}")

def realizar_download():
    try:
        link_video = entrada_link.get()
        youtube_object = YouTube(link_video, on_progress_callback=atualizar_progresso)
        
        if combobox_var.get() == 'MP4':
            video = youtube_object.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        elif combobox_var.get() == 'MP3':
            video = youtube_object.streams.filter(only_audio=True).first()
        
        if video:
            # Perguntar ao usuário onde salvar o vídeo
            diretorio_destino = filedialog.askdirectory()
            if diretorio_destino:
                # Mostrar a barra de progresso antes de iniciar o download
                barra_progresso.pack(pady=10)
                barra_progresso.set(0)
                label_porcentagem.configure(text="0%")
                label_status.configure(text="Download em Andamento", text_color="white")

                # Iniciar o download no diretório selecionado
                arquivo = video.download(output_path=diretorio_destino)

                # Se for MP3, converter para MP3
                if combobox_var.get() == 'MP3':
                    
                    # Carregar o arquivo de vídeo baixado
                    clip = AudioFileClip(arquivo)
                    
                    # Nome do arquivo de saída MP3
                    arquivo_mp3 = f"{youtube_object.title}.mp3"
                    
                    # Salvar o arquivo como MP3
                    clip.write_audiofile(os.path.join(diretorio_destino, arquivo_mp3))
                    
                    # Excluir o arquivo de vídeo original (opcional)
                    os.remove(arquivo)
                    
                # Atualizar status de download concluído
                label_status.configure(text="Download Concluído!", text_color="white")
                label_titulo.configure(text=youtube_object.title, text_color="white")

                # Mostrar a thumbnail do vídeo
                mostrar_thumbnail(youtube_object.thumbnail_url)
        else:
            label_status.configure(text="Não foi possível encontrar uma stream disponível.", text_color="red")
    except exceptions.VideoPrivate:
        label_status.configure(text="Vídeo não pode ser acessado devido a direitos autorais.", text_color="red")
    except exceptions.MembersOnly:
        label_status.configure(text="Vídeo só pode ser acessado por Membros.", text_color="red")
    except exceptions.HTMLParseError:
        label_status.configure(text="HTML não pôde ser analisado.", text_color="red")
    except exceptions.LiveStreamError:
        label_status.configure(text="Não é possivel baixar uma live stream.", text_color="red")
    except exceptions.VideoRegionBlocked:
        label_status.configure(text="Vídeo não disponível na sua região.", text_color="red")
    except exceptions.AgeRestrictedError:
        label_status.configure(text="Vídeo não pode ser baixado devido a restrições de idade.", text_color="red")
    except exceptions.VideoUnavailable:
        label_status.configure(text="Vídeo indisponível.", text_color="red")
    except Exception as e:
        label_status.configure(text="Erro ao Realizar o Download", text_color="red")
        print(e)

def atualizar_progresso(stream, chunk, bytes_restantes):
    try:
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_restantes
        percent_completion = bytes_downloaded / total_size * 100
        percent_text = f"{int(percent_completion)}%"
        
        label_porcentagem.configure(text=percent_text)
        barra_progresso.set(float(percent_completion / 100))
        
        # Forçar a atualização da interface
        label_porcentagem.update()
        barra_progresso.update()
    except Exception as e:
        print(f"Erro ao atualizar progresso: {e}")

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
combobox = customtkinter.CTkComboBox(janela, values=QUALITY_OPTIONS, variable=combobox_var, width= 250)
combobox.pack(pady=15)

botao_download = customtkinter.CTkButton(janela, text="Download", command=realizar_download, width= 250, font=("Consolas", 13))
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

janela.mainloop()
