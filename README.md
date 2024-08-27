<h1 align = "center"> Molinaro's Downloader V2.0 </h1>


Molinaro's Downloader é uma aplicação de desktop desenvolvida em Python que permite aos usuários baixar vídeos do YouTube em formatos MP4 ou M4A. A aplicação utiliza as bibliotecas `Tkinter` e `Custom Tkinter` para a interface gráfica, e `yt-dlp` para realizar os downloads de vídeos do YouTube de forma eficiente e precisa.

![image](https://github.com/LMolinaro01/YouTube-Downloader/assets/126402616/b309ec19-c7a9-4849-b8ae-d023219f6150)

## Novidades na Versão 2.0

- **Integração com `yt-dlp`:** Agora a aplicação utiliza `yt-dlp` para downloads, permitindo maior compatibilidade com diferentes formatos de vídeo e áudio.
<!-- - **Estimativa de Tamanho do Arquivo:** A aplicação agora exibe uma estimativa do tamanho do arquivo antes de solicitar ao usuário o diretório de salvamento. -->
- **Barra de Progresso Aprimorada:** A barra de progresso foi melhorada para refletir o status do download em tempo real, oferecendo feedback visual mais preciso.

![image](https://github.com/user-attachments/assets/60ee3c6c-9c90-4062-b9be-da63e20f875b)

## Funcionalidades

- **Seleção do Diretório de Destino:** O usuário pode selecionar onde deseja salvar os arquivos baixados.
- **Download em MP4 e M4A:** Permite baixar vídeos em formato MP4 ou áudio em formato M4A com conversão automática.
- **Barra de Progresso:** Mostra o andamento do download em tempo real.
  <!-- - **Estimativa do Tamanho do Arquivo:** Mostra uma estimativa do tamanho do arquivo antes do download começar. -->
- **Exibição de Thumbnail:** Exibe a miniatura do vídeo após o início do download.
- **Tratamento de Exceções:** A aplicação lida com erros comuns, garantindo que o usuário seja informado caso algo dê errado.

## Funcionamento

![image](https://github.com/LMolinaro01/YouTube-Downloader/assets/126402616/b4ca285d-cc43-43de-a06b-b9984d55688e)

1. Execute o script Python.
2. Na janela da aplicação, insira o link do vídeo do YouTube que deseja baixar.
3. Selecione o formato desejado (MP4 ou M4A) usando a combobox.
4. Clique no botão "Download".
5. Selecione o diretório onde deseja salvar o arquivo baixado.
6. Acompanhe a barra de progresso e as mensagens de status para verificar o andamento do download.
