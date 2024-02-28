import pygame
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog

def reproduzir_musica(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play()

def parar_reproducao():
    pygame.mixer.music.stop()

def listar_musicas(caminho):
    return [os.path.join(caminho, arquivo) for arquivo in os.listdir(caminho) if arquivo.endswith('.mp3')]

def selecionar_musica():
    global resultados, listbox
    pasta_musica = filedialog.askdirectory()
    resultados = listar_musicas(pasta_musica)
    listbox.delete(0, tk.END)
    for musica in resultados:
        listbox.insert(tk.END, os.path.basename(musica))

def play_selected():
    global resultados
    selected_index = listbox.curselection()
    if selected_index:
        selecionado = resultados[selected_index[0]]
        reproduzir_musica(selecionado)

def main():
    # Inicializar o mixer do pygame
    pygame.mixer.init()

    # Criar a interface gráfica
    root = tk.Tk()
    root.title("Reprodutor de Música")

    # Botões
    button_select = tk.Button(root, text="Selecionar Pasta", command=selecionar_musica)
    button_select.pack()

    # Lista de músicas
    global listbox
    listbox = tk.Listbox(root)
    listbox.pack()

    # Botão de reprodução
    button_play = tk.Button(root, text="Reproduzir Selecionada", command=play_selected)
    button_play.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
