import pygame
import os
import glob
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog, Text, messagebox, ttk, Menu
import json
import random
from functools import partial

resultados = []  
resultados_originais = []  # Adicionando a lista original de resultados
resultados_filtrados = []  # Adicionando a lista filtrada de resultados

def reproduzir_musica(musica=None):
    global musica_atual, current_song_label
    if musica is not None:
        pygame.mixer.music.load(musica)
        pygame.mixer.music.play()
        current_song_label.delete("1.0", "end")
        current_song_label.insert("1.0", os.path.basename(musica))
        current_song_label.see("1.0")

def iniciar_rolagem_automatica():
    global current_song_label
    current_song_label.see("end")
    current_song_label.xview_moveto(0)
    current_song_label.after(2000, iniciar_rolagem_automatica)

def parar_reproducao():
    pygame.mixer.music.pause()

def continuar_reproducao():
    pygame.mixer.music.unpause()

def alternar_reproducao():
    if pygame.mixer.music.get_busy():
        parar_reproducao()
        button_pause_play.config(text="Continuar", image=continue_icon)
    else:
        continuar_reproducao()
        button_pause_play.config(text="Pausar", image=pause_icon)

def buscar_musicas(event=None):
    termo_busca = search_var.get().lower() if event else ""
    global resultados, resultados_originais, resultados_filtrados

    resultados_filtrados = [musica for musica in resultados_originais if termo_busca in os.path.basename(musica).lower()]

    if resultados_filtrados != listbox.get(0, tk.END):
        listbox.delete(0, tk.END)
        for musica in resultados_filtrados:
            listbox.insert(tk.END, os.path.basename(musica))

        selected_index = listbox.curselection()
        if not selected_index:
            reproduzir_musica()
    else:
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(musica_atual)

def play_selected(event=None):
    global resultados, resultados_originais, musica_atual, current_song_label

    selected_index = listbox.curselection()

    if resultados_filtrados:  
        if selected_index:
            selecionado = resultados_filtrados[selected_index[0]]
            musica_atual = resultados_originais.index(selecionado)
            reproduzir_musica(selecionado)
        else:
            messagebox.showinfo("Nenhuma música selecionada", "Por favor, selecione uma música para reproduzir.")
    else:  
        if selected_index:
            selecionado = resultados[selected_index[0]]
            musica_atual = resultados.index(selecionado)
            reproduzir_musica(selecionado)
        else:
            messagebox.showinfo("Nenhuma música selecionada", "Por favor, selecione uma música para reproduzir.")

def play_previous(event=None):
    global musica_atual
    parar_reproducao()
    if musica_atual > 0:
        musica_atual -= 1
    else:
        messagebox.showinfo("Início da Lista", "Você está no início da lista de reprodução.")
        return
    reproduzir_musica()

def play_next(event=None):
    global musica_atual
    parar_reproducao()
    if musica_atual < len(resultados) - 1:
        musica_atual += 1
    else:
        messagebox.showinfo("Fim da Lista", "Você chegou ao final da lista de reprodução.")
        return
    reproduzir_musica()

def listar_musicas(caminho):
    return [
        os.path.join(caminho, arquivo)
        for caminho, _, arquivos in os.walk(caminho)
        for arquivo in arquivos
        if arquivo.endswith(('.mp3'))
    ]

def selecionar_musica(listbox):
    global resultados, resultados_originais
    pasta_musica = filedialog.askdirectory()
    if pasta_musica:
        salvar_configuracao(pasta_musica)
        resultados = listar_musicas(os.path.expanduser(glob.escape(pasta_musica)))
        resultados_originais = resultados.copy()
        listbox.delete(0, tk.END)
        for musica in resultados:
            listbox.insert(tk.END, os.path.basename(musica))

def carregar_configuracao():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config["last_folder"]
    except FileNotFoundError:
        return ""

def salvar_configuracao(pasta_musica):
    config = {"last_folder": pasta_musica}
    with open("config.json", "w") as f:
        json.dump(config, f)

def repetir_musica():
    global musica_atual
    pygame.mixer.music.play(-1, start=pygame.mixer.music.get_pos() / 1000)
    musica_atual = resultados.index(resultados[musica_atual])

def repetir_todas(root):
    global musica_atual, resultados
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play()
    root.after(100, lambda: check_music_status(root))
    pygame.mixer.music.queue(resultados[(musica_atual + 1) % len(resultados)])

def check_music_status(root):
    global musica_atual, resultados
    if pygame.mixer.music.get_busy():
        root.after(100, lambda: check_music_status(root))
    else:
        musica_atual = (musica_atual + 1) % len(resultados)
        reproduzir_musica()
        current_song_label.delete("1.0", "end")
        current_song_label.insert("1.0", os.path.basename(resultados[musica_atual]))
        pygame.mixer.music.play()

def on_music_end():
    global musica_atual, resultados
    musica_atual = (musica_atual + 1) % len(resultados)
    reproduzir_musica()

def reproducao_aleatoria():
    global musica_atual
    musica_aleatoria = random.choice(resultados)
    musica_atual = resultados.index(musica_aleatoria)
    reproduzir_musica(musica_aleatoria)

def main():
    global current_song_label
    global play_icon, pause_icon, button_pause_play, continue_icon, stop_icon

    pygame.mixer.init()

    root = tk.Tk()
    root.title("Music Player - MK II")
    root.geometry("320x400")

    global search_var
    search_var = tk.StringVar()
    search_entry = tk.Entry(root, textvariable=search_var)
    search_entry.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="ew")
    search_entry.bind("<Return>", buscar_musicas)

    search_button = tk.Button(root, text="Buscar", command=buscar_musicas)
    search_button.grid(row=1, column=5, padx=5, pady=5)

    current_song_label = Text(root, height=1, width=20, bg="#b2dafb", fg="#000000", wrap="none")
    current_song_label.grid(row=0, column=0, columnspan=6, sticky='ew')

    iniciar_rolagem_automatica()

    pasta_musica = carregar_configuracao()
    global musica_atual
    musica_atual = 0

    global resultados, resultados_originais
    resultados = []
    resultados_originais = []

    global listbox
    listbox = tk.Listbox(root)
    listbox.grid(row=2, column=0, columnspan=7, rowspan=6, padx=5, pady=5, sticky='ew')

    if pasta_musica:
        resultados = listar_musicas(pasta_musica)
        resultados_originais = resultados.copy()
        for musica in resultados:
            listbox.insert(tk.END, os.path.basename(musica))

    folder_icon = ImageTk.PhotoImage(Image.open("folder.png"))
    play_icon = ImageTk.PhotoImage(Image.open("play.png"))
    pause_icon = ImageTk.PhotoImage(Image.open("pause.png"))
    continue_icon = ImageTk.PhotoImage(Image.open("continue.png"))
    previous_icon = ImageTk.PhotoImage(Image.open("previous.png"))
    next_icon = ImageTk.PhotoImage(Image.open("next.png"))
    stop_icon = ImageTk.PhotoImage(Image.open("stop.png"))
    repeat_icon = ImageTk.PhotoImage(Image.open("repeat.png"))
    random_icon = ImageTk.PhotoImage(Image.open("shuffle.png"))
    repeat_all_icon = ImageTk.PhotoImage(Image.open("repeat_all.png"))

    button_folder = tk.Button(root, image=folder_icon, command=lambda: selecionar_musica(listbox), bg="#b2dafb", fg="#000000")
    button_play = tk.Button(root, image=play_icon, command=play_selected, bg="#b2dafb", fg="#000000")
    button_pause_play = tk.Button(root, text="Pausar", image=pause_icon, command=alternar_reproducao, bg="#b2dafb", fg="#000000")
    button_previous = tk.Button(root, image=previous_icon, command=play_previous, bg="#b2dafb", fg="#000000")
    button_next = tk.Button(root, image=next_icon, command=play_next, bg="#b2dafb", fg="#000000")
    button_repeat = tk.Button(root, image=repeat_icon, command=repetir_musica, bg="#b2dafb", fg="#000000")
    button_repeat_all = tk.Button(root, image=repeat_all_icon, command=lambda: repetir_todas(root), bg="#b2dafb", fg="#000000")
    button_random = tk.Button(root, image=random_icon, command=reproducao_aleatoria, bg="#b2dafb", fg="#000000")

    volume_slider = ttk.Scale(root, from_=0, to=100, orient="vertical", command=lambda volume: pygame.mixer.music.set_volume(1 - float(volume) / 100))
    volume_slider.set(50)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=listbox.yview)
    scrollbar.grid(row=2, column=6, rowspan=6, sticky='ns')
    listbox.config(yscrollcommand=scrollbar.set)

    listbox.bind("<Double-Button-1>", lambda event: play_selected())
    listbox.bind("<Return>", lambda event: play_selected())

    search_var = tk.StringVar()
    search_entry = tk.Entry(root, textvariable=search_var)
    search_entry.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

    search_entry.bind("<KeyRelease>", buscar_musicas)

    button_folder.grid(row=13, column=1)
    button_pause_play.grid(row=12, column=2)
    button_previous.grid(row=12, column=1)
    button_play.grid(row=11, column=2)
    button_next.grid(row=12, column=3)
    button_folder.grid(row=13, column=2)
    button_repeat.grid(row=11, column=4)
    button_repeat_all.grid(row=12, column=4)
    button_random.grid(row=13, column=4)
    volume_slider.grid(row=10, column=5, rowspan=5, padx=5, pady=5)

    footer_label = tk.Label(root, text="Feito por Danilo Lopes, Aluno da UDF. Proof of Concept", bg="#b2dafb", fg="#000000")
    footer_label.grid(row=14, column=0, rowspan=15, columnspan=6)

    root.mainloop()

if __name__ == "__main__":
    main()
