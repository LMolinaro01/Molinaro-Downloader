# Molinaro's Downloader - Versão 3.0

**Molinaro's Downloader** é uma aplicação Python desenvolvida com Tkinter e CustomTkinter, projetada para facilitar o download de vídeos e áudios do YouTube. A versão 3.0 traz melhorias significativas, incluindo a capacidade de gerar PDFs com transcrições detalhadas usando a API GPT-3 da OpenAI.

![Interface Principal](https://github.com/LMolinaro01/YouTube-Downloader/assets/126402616/b309ec19-c7a9-4849-b8ae-d023219f6150)

## Novidades na Versão 3.0 (Em Fase de Testes)

- **Integração com a API OpenAI**: Utiliza a GPT-3 para criar resumos e transcrições organizadas dos vídeos. A API da OpenAI é essencial para transformar as descrições dos vídeos em transcrições detalhadas.
- **Geração de PDF**: Converte vídeos em PDFs com transcrições, proporcionando uma maneira prática de armazenar e compartilhar o conteúdo dos vídeos.
- **Interface Melhorada**: Atualizações na interface gráfica para proporcionar uma experiência de usuário mais intuitiva e eficiente.

![Exemplo de PDF](https://github.com/user-attachments/assets/60ee3c6c-9c90-4062-b9be-da63e20f875b)

## Funcionalidades

- **Seleção do Diretório de Destino**: O usuário pode selecionar onde deseja salvar os arquivos baixados e os PDFs gerados.
- **Download em MP4 e M4A**: Permite baixar vídeos em formato MP4 ou áudio em formato M4A.
- **Geração de PDF**: Para vídeos selecionados, o aplicativo pode gerar um PDF com a transcrição do conteúdo do vídeo.
- **Exibição de Thumbnail**: Mostra a miniatura do vídeo diretamente na interface.
- **Barra de Progresso**: Mostra o andamento do download em tempo real.
- **Tratamento de Exceções**: A aplicação lida com erros comuns e mostra mensagens de status apropriadas.

## Funcionamento

![Interface do Aplicativo](https://github.com/LMolinaro01/YouTube-Downloader/assets/126402616/b4ca285d-cc43-43de-a06b-b9984d55688e)

1. **Execute o Script Python**.
2. **Insira o link do vídeo do YouTube** que deseja baixar.
3. **Escolha o formato desejado** (Vídeo, Áudio ou PDF) usando a combobox.
4. **Clique no botão "Download"**.
5. **Selecione o diretório onde deseja salvar o arquivo baixado ou o PDF**.
6. **Acompanhe a barra de progresso e as mensagens de status** para verificar o andamento do download e a criação do PDF.


## Configuração

1. **Chave de API da OpenAI**: Substitua `"chaveapi"` no código pela sua chave de API da OpenAI. A API GPT-3 é utilizada para criar resumos e transcrições detalhadas dos vídeos.

   ```python
   openai.api_key = "chaveapi"
   ```

2. **Inicialização do Aplicativo**: O código cria uma interface gráfica com as opções de download e geração de PDF.


## **Contato**

Se você tiver dúvidas ou precisar de mais informações, sinta-se a vontade para entrar em [Contato](https://linktr.ee/leomolinarodev01)!

