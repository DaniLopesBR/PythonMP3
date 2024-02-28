import pygame
import os
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from pydub import AudioSegment
from pydub.playback import play
from tkinter import messagebox
from random import randint
import json

def reproduzir_musica(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play()

def parar_reproducao():
    pygame.mixer.music.pause()

def continuar_reproducao():
    pygame.mixer.music.unpause()

def play_selected(resultados):
    global listbox
    selected_index = listbox.curselection()
    if selected_index:
        selecionado = resultados[selected_index[0]]
        reproduzir_musica(selecionado)

def play_selected_wrapper():
    play_selected(resultados)

def play_next():
    global musica_atual, resultados, repetir_musica_var, repetir_todas_var, reproducao_aleatoria_var
    parar_reproducao()
    if repetir_todas_var.get() or (repetir_musica_var.get() and musica_atual == len(resultados) - 1):
        musica_atual = (musica_atual + 1) % len(resultados)
    elif reproducao_aleatoria_var.get():
        musica_atual = randint(0, len(resultados) - 1)
    elif musica_atual < len(resultados) - 1:
        musica_atual += 1
    else:
        messagebox.showinfo("Fim da Lista", "Você chegou ao final da lista de reprodução.")
        return
    reproduzir_musica(resultados[musica_atual])

def play_previous():
    global musica_atual, resultados, repetir_musica_var, repetir_todas_var, reproducao_aleatoria_var
    parar_reproducao()
    if repetir_todas_var.get() or (repetir_musica_var.get() and musica_atual == 0):
        musica_atual = (musica_atual - 1) % len(resultados)
    elif reproducao_aleatoria_var.get():
        musica_atual = randint(0, len(resultados) - 1)
    elif musica_atual > 0:
        musica_atual -= 1
    else:
        messagebox.showinfo("Início da Lista", "Você está no início da lista de reprodução.")
        return
    reproduzir_musica(resultados[musica_atual])

def selecionar_musica():
    global resultados, listbox
    pasta_musica = filedialog.askdirectory()

    if pasta_musica:
        salvar_configuracao(pasta_musica)
        resultados = listar_musicas(pasta_musica)
        listbox.delete(0, tk.END)
        for musica in resultados:
            listbox.insert(tk.END, os.path.basename(musica))

def listar_musicas(caminho):
        return [os.path.join(caminho, arquivo) for arquivo in os.listdir(caminho) if arquivo.endswith(('.mp3', '.m4a'))]

def main():
    pygame.mixer.init()

    root = tk.Tk()
    root.title("Music Player - MK II")
    root.geometry("211x416")

    # Carregar configuração e inicializar variáveis globais
    pasta_musica = carregar_configuracao()
    global musica_atual
    musica_atual = 0

    global resultados
    resultados = []  # Inicializar resultados como uma lista vazia

    global listbox
    listbox = tk.Listbox(root)
    listbox.grid(row=0, column=0, columnspan=4)

    if pasta_musica:
        resultados = listar_musicas(pasta_musica)
        for musica in resultados:
            listbox.insert(tk.END, os.path.basename(musica))

    # Defina o caminho para os ícones
    icon_folder = ""

    # Carregue os ícones
    folder_icon = ImageTk.PhotoImage(Image.open("folder.png"))
    play_icon = ImageTk.PhotoImage(Image.open("play.png"))
    stop_icon = ImageTk.PhotoImage(Image.open("stop.png"))
    continue_icon = ImageTk.PhotoImage(Image.open("continue.png"))
    previous_icon = ImageTk.PhotoImage(Image.open("previous.png"))
    next_icon = ImageTk.PhotoImage(Image.open("next.png"))


    button_folder = tk.Button(root, image=folder_icon, command=selecionar_musica, bg="#b2dafb", fg="#000000")
    button_play = tk.Button(root, image=play_icon, command=play_selected_wrapper, bg="#b2dafb", fg="#000000")
    button_stop = tk.Button(root, image=stop_icon, command=parar_reproducao, bg="#b2dafb", fg="#000000")
    button_continue = tk.Button(root, image=continue_icon, command=continuar_reproducao, bg="#b2dafb", fg="#000000")
    button_previous = tk.Button(root, image=previous_icon, command=play_previous, bg="#b2dafb", fg="#000000")
    button_next = tk.Button(root, image=next_icon, command=play_next, bg="#b2dafb", fg="#000000")

    # Posicionar os botões
    button_folder.grid(row=1, column=0)
    button_previous.grid(row=2, column=0)
    button_play.grid(row=2, column=1)
    button_next.grid(row=2, column=2)
    button_stop.grid(row=3, column=1)
    button_continue.grid(row=1, column=1)

    global repetir_musica_var, repetir_todas_var, reproducao_aleatoria_var
    repetir_musica_var = tk.IntVar()
    repetir_todas_var = tk.IntVar()
    reproducao_aleatoria_var = tk.IntVar()

    checkbox_repetir_musica = tk.Checkbutton(root, text="Repeat", variable=repetir_musica_var)
    checkbox_repetir_musica.grid(row=4, column=0)

    checkbox_repetir_todas = tk.Checkbutton(root, text="Repeat All", variable=repetir_todas_var)
    checkbox_repetir_todas.grid(row=4, column=2)

    checkbox_reproducao_aleatoria = tk.Checkbutton(root, text="Shuffle", variable=reproducao_aleatoria_var)
    checkbox_reproducao_aleatoria.grid(row=5, column=1)

    footer_label = tk.Label(root, text="Feito por Danilo Lopes, Aluno da UDF. \n Proof of Concept", bg="#b2dafb", fg="#000000")
    footer_label.grid(row=6, column=0, columnspan=4)

    root.mainloop()  # Iniciar o loop principal da interface gráfica

# Função para salvar a última pasta de música selecionada
def salvar_configuracao(pasta_musica):
    config = {"last_folder": pasta_musica}  # Criar um dicionário com a pasta selecionada
    with open("config.json", "w") as f:
        json.dump(config, f)  # Salvar o dicionário como um arquivo JSON

# Função para carregar a última pasta de música selecionada
def carregar_configuracao():
    pasta_musica = ""  # Inicializar a variável
    if os.path.exists("config.json"):  # Verificar se o arquivo de configuração existe
        with open("config.json", "r") as f:
            config = json.load(f)  # Carregar o arquivo JSON
            pasta_musica = config.get("last_folder", "")  # Obter a última pasta selecionada, se existir
    return pasta_musica  # Retornar a última pasta selecionada

if __name__ == "__main__":
    main()  # Chamar a função principal quando o script for executado diretamente
