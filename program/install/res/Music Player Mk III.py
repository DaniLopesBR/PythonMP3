import pygame
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from random import randint
import json

def reproduce_music(selected):
    global current_song, song_list
    stop_reproduction()
    current_song = (current_song + 1) % len(song_list)
    play_music(song_list[current_song])

def play_next():
    global current_song, song_list
    stop_reproduction()
    current_song = (current_song + 1) % len(song_list)
    play_music(song_list[current_song])

def play_previous():
    global current_song, song_list
    stop_reproduction()
    current_song = (current_song - 1) % len(song_list)
    play_music(song_list[current_song])

def select_music():
    global song_list, song_listbox
    music_folder = filedialog.askdirectory()

    if music_folder:
        # Save the selected folder to the configuration file
        save_config(music_folder)

        song_list = list_music(music_folder)
        song_listbox.delete(0, tk.END)
        for song in song_list:
            song_listbox.insert(tk.END, os.path.basename(song))

def list_music(music_folder):
    return [os.path.join(music_folder, song) for song in os.listdir(music_folder) if song.endswith('.mp3')]

def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

def stop_reproduction():
    pygame.mixer.music.pause()

def save_config(music_folder):
    config = {"last_folder": music_folder}
    with open("config.json", "w") as f:
        json.dump(config, f)

def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config.get("last_folder", "")
    return ""

if __name__ == "__main__":
    # Initialize the mixer
    pygame.mixer.init()

    # Create the main window
    root = tk.Tk()
    root.title("Music Player - MK II")
    root.geometry("231x498")

    # Load the last selected folder
    music_folder = load_config()

    # Initialize the global variables
    current_song = 0
    song_list = []
    song_listbox = tk.Listbox(root)
    song_listbox.pack()

    # Load the songs from the last selected folder
    if music_folder:
        select_music()

    # Create the buttons
    play_button = tk.Button(root, text="Play", command=lambda: reproduce_music(current_song))
    play_button.pack()

    next_button = tk.Button(root, text="Next", command=play_next)
    next_button.pack()

    previous_button = tk.Button(root, text="Previous", command=play_previous)
    previous_button.pack()

    # Create the checkbuttons
    repeat_music_var = tk.BooleanVar()
    repeat_music_checkbox = tk.Checkbutton(root, text="Repeat Music", variable=repeat_music_var)
    repeat_music_checkbox.pack()

    repeat_all_var = tk.BooleanVar()
    repeat_all_checkbox = tk.Checkbutton(root, text="Repeat All", variable=repeat_all_var)
    repeat_all_checkbox.pack()

    shuffle_var = tk.BooleanVar()
    shuffle_checkbox = tk.Checkbutton(root, text="Shuffle", variable=shuffle_var)
    shuffle_checkbox.pack()

    # Create the footer label
    footer_label = tk.Label(root, text="Made by Danilo Lopes, UDF Student. \n Proof of Concept")
    footer_label.pack(side=tk.BOTTOM)

    # Start the main loop
    root.mainloop()
