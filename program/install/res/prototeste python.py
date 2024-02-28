# Importação de módulos necessários
import pygame
import os
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, Text, messagebox, ttk
import json
import random

# Função para reproduzir uma música
def reproduzir_musica(musica, current_song_label):
    pygame.mixer.music.load(musica)  # Carrega o arquivo de música
    pygame.mixer.music.play()  # Reproduz a música

    current_song_label.delete("1.0", "end")  # Limpa o texto atual no rótulo
    current_song_label.insert("1.0", os.path.basename(musica))  # Insere o novo nome da música no rótulo

    # Rolar para o início do texto para simular o efeito de rolagem automática
    current_song_label.see("1.0")

# Função para iniciar a rolagem automática do nome da música
def iniciar_rolagem_automatica():
    global current_song_label
    current_song_label.see("end")  # Rolagem para o final do texto
    current_song_label.xview_moveto(0)  # Rolagem para a esquerda
    current_song_label.after(2000, iniciar_rolagem_automatica)  # Chama esta função novamente após 2 segundos  

# Função para pausar a reprodução da música
def parar_reproducao():
    pygame.mixer.music.pause()

# Função para continuar a reprodução da música
def continuar_reproducao():
    pygame.mixer.music.unpause()

# Função para alternar entre pausar e retomar a reprodução da música
def alternar_reproducao():
    if pygame.mixer.music.get_busy():
        parar_reproducao()
        button_pause_play.config(text="Continuar", image=continue_icon)
    else:
        continuar_reproducao()
        button_pause_play.config(text="Pausar", image=pause_icon)

# Função para reproduzir a música selecionada a partir da lista
def play_selected(resultados, current_song_label):
    global listbox, musica_atual
    selected_index = listbox.curselection()  # Obtém o índice da música selecionada na lista
    if selected_index:
        musica_atual = selected_index[0]  # Atualiza a variável de controle da música atual
        selecionado = resultados[musica_atual]  # Obtém o caminho da música selecionada
        reproduzir_musica(selecionado, current_song_label)  # Chama a função para reproduzir a música

# Função de wrapper para reproduzir a música selecionada
def play_selected_wrapper(current_song_label):
    global resultados
    play_selected(resultados, current_song_label)

# Função para reproduzir a música anterior na lista
def play_previous(current_song_label):
    global musica_atual, resultados
    parar_reproducao()  # Pausa a reprodução atual
    if musica_atual > 0:
        musica_atual -= 1  # Volta para a música anterior
    else:
        messagebox.showinfo("Início da Lista", "Você está no início da lista de reprodução.")  # Exibe uma mensagem de aviso
        return
    reproduzir_musica(resultados[musica_atual], current_song_label)  # Reproduz a música anterior

# Função para reproduzir a próxima música na lista
def play_next(current_song_label):
    global musica_atual, resultados
    parar_reproducao()  # Pausa a reprodução atual
    if musica_atual < len(resultados) - 1:
        musica_atual += 1  # Avança para a próxima música
    else:
        messagebox.showinfo("Fim da Lista", "Você chegou ao final da lista de reprodução.")  # Exibe uma mensagem de aviso
        return
    reproduzir_musica(resultados[musica_atual], current_song_label)  # Reproduz a próxima música

# Função para listar todas as músicas em uma determinada pasta
def listar_musicas(caminho):
    return [os.path.join(caminho, arquivo) for arquivo in os.listdir(caminho) if arquivo.endswith(('.mp3'))]

# Função para selecionar uma pasta contendo músicas
def selecionar_musica(listbox):
    global resultados
    pasta_musica = filedialog.askdirectory()  # Abre uma janela para selecionar a pasta de músicas

    if pasta_musica:
        salvar_configuracao(pasta_musica)  # Salva a pasta selecionada como configuração
        resultados = listar_musicas(pasta_musica)  # Lista todas as músicas na pasta selecionada
        listbox.delete(0, tk.END)  # Limpa a lista atual de músicas
        for musica in resultados:
            listbox.insert(tk.END, os.path.basename(musica))  # Adiciona as músicas à lista

# Função para carregar a última pasta de música selecionada
def carregar_configuracao():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)  # Carregar o arquivo JSON
            return config["last_folder"]  # Retornar a última pasta selecionada
    except FileNotFoundError:
        return ""  # Se o arquivo não existir, retornar uma string vazia

# Função para salvar a última pasta de música selecionada
def salvar_configuracao(pasta_musica):
    config = {"last_folder": pasta_musica}  # Criar um dicionário com a pasta selecionada
    with open("config.json", "w") as f:
        json.dump(config, f)  # Salvar o dicionário como um arquivo JSON

# Função para reproduzir a música atual repetidamente
def repetir_musica():
    pygame.mixer.music.play(-1)  # Reproduz a música atual repetidamente

# Função para reproduzir todas as músicas da lista repetidamente
def repetir_todas():
    global resultados
    musica_aleatoria = random.choice(resultados)  # Escolhe uma música aleatória da lista
    reproduzir_musica(musica_aleatoria, current_song_label)  # Reproduz a música aleatória
    pygame.mixer.music.queue(resultados)  # Adiciona todas as músicas na fila de reprodução
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Define um evento de fim de música
    pygame.mixer.music.play()  # Reproduz a lista de músicas

# Função para reproduzir aleatoriamente uma música da lista
def reproducao_aleatoria():
    global resultados
    musica_aleatoria = random.choice(resultados)  # Escolhe uma música aleatória da lista
    reproduzir_musica(musica_aleatoria, current_song_label)  # Reproduz a música aleatória

# Função principal
def main():
    global current_song_label  # Definindo current_song_label como global
    global play_icon, pause_icon, button_pause_play, continue_icon, stop_icon  # Variáveis globais para os ícones de play, pause e stop, e os botões correspondentes

    pygame.mixer.init()  # Inicializa o mixer do pygame para reprodução de áudio

    root = tk.Tk()  # Cria uma instância de Tk para a interface gráfica
    root.title("Music Player - MK II")  # Define o título da janela
    root.geometry("210x355")  # Define as dimensões da janela

    # Cria um rótulo para exibir a música atual
    current_song_label = Text(root, height=1, width=20, bg="#b2dafb", fg="#000000", wrap="none")
    current_song_label.grid(row=0, column=0, columnspan=5)  # Define a posição do rótulo na interface
    
    iniciar_rolagem_automatica()  # Inicia a rolagem automática do nome da música

    # Carregar configuração e inicializar variáveis globais
    pasta_musica = carregar_configuracao()
    global musica_atual
    musica_atual = 0

    global resultados
    resultados = []  # Inicializar resultados como uma lista vazia

    global listbox
    listbox = tk.Listbox(root)  # Cria uma lista para exibir as músicas disponíveis
    listbox.grid(row=1, column=0, columnspan=4, rowspan=5, padx=5, pady=5, sticky='ns')  # Define a posição da lista na interface

    # Se houver uma pasta de música selecionada anteriormente, lista as músicas
    if pasta_musica:
        resultados = listar_musicas(pasta_musica)
        for musica in resultados:
            listbox.insert(tk.END, os.path.basename(musica))

    # Carregar ícones
    folder_icon = ImageTk.PhotoImage(Image.open("folder.png"))
    play_icon = ImageTk.PhotoImage(Image.open("play.png"))
    pause_icon = ImageTk.PhotoImage(Image.open("pause.png"))
    continue_icon = ImageTk.PhotoImage(Image.open("continue.png"))
    previous_icon = ImageTk.PhotoImage(Image.open("previous.png"))
    next_icon = ImageTk.PhotoImage(Image.open("next.png"))
    volume_icon = ImageTk.PhotoImage(Image.open("volume.png"))
    stop_icon = ImageTk.PhotoImage(Image.open("stop.png"))
    repeat_icon = ImageTk.PhotoImage(Image.open("repeat.png"))
    random_icon = ImageTk.PhotoImage(Image.open("shuffle.png"))
    repeat_all_icon = ImageTk.PhotoImage(Image.open("repeat_all.png"))

    # Criar botões para interagir com as músicas
    button_folder = tk.Button(root, image=folder_icon, command=lambda: selecionar_musica(listbox), bg="#b2dafb", fg="#000000")
    button_play = tk.Button(root, image=play_icon, command=lambda: play_selected_wrapper(current_song_label), bg="#b2dafb", fg="#000000")
    button_pause_play = tk.Button(root, text="Pausar", image=pause_icon, command=alternar_reproducao, bg="#b2dafb", fg="#000000")
    button_stop = tk.Button(root, image=stop_icon, command=parar_reproducao, bg="#b2dafb", fg="#000000")
    button_previous = tk.Button(root, image=previous_icon, command=lambda: play_previous(current_song_label), bg="#b2dafb", fg="#000000")
    button_next = tk.Button(root, image=next_icon, command=lambda: play_next(current_song_label), bg="#b2dafb", fg="#000000")
    button_repeat = tk.Button(root, image=repeat_icon, command=repetir_musica, bg="#b2dafb", fg="#000000")
    button_repeat_all = tk.Button(root, image=repeat_all_icon, command=repetir_todas, bg="#b2dafb", fg="#000000")
    button_random = tk.Button(root, image=random_icon, command=reproducao_aleatoria, bg="#b2dafb", fg="#000000")

    # Slider para ajustar o volume
    volume_slider = ttk.Scale(root, from_=0, to=100, orient="vertical", command=lambda volume: pygame.mixer.music.set_volume(1 - float(volume) / 100))
    volume_slider.set(50)  # Define o valor inicial do volume

    # Posicionar os botões na interface
    button_folder.grid(row=9, column=1)  # Botão para selecionar a pasta de músicas
    button_pause_play.grid(row=8, column=2)  # Botão para pausar ou retomar a reprodução da música atual
    button_previous.grid(row=8, column=1)  # Botão para reproduzir a música anterior na lista
    button_play.grid(row=7, column=2)  # Botão para reproduzir a música selecionada na lista
    button_next.grid(row=8, column=3)  # Botão para reproduzir a próxima música na lista
    button_folder.grid(row=9, column=2)  # Botão para selecionar a pasta de músicas
    button_repeat.grid(row=7, column=4)  # Botão para repetir a música atual
    button_repeat_all.grid(row=8, column=4)  # Botão para repetir todas as músicas
    button_random.grid(row=9, column=4)  # Botão para reprodução aleatória
    volume_slider.grid(row=1, column=4, rowspan=5, padx=5, pady=5)  # Slider para ajustar o volume

    # Criar e posicionar um rótulo de rodapé
    footer_label = tk.Label(root, text="Feito por Danilo Lopes, Aluno da UDF. \n Proof of Concept", bg="#b2dafb", fg="#000000")
    footer_label.grid(row=11, column=0, columnspan=5)

    root.mainloop()  # Iniciar o loop principal da interface gráfica

# Chamar a função principal ao executar o script
if __name__ == "__main__":
    main()



# codigo testado as 02:14 da manha