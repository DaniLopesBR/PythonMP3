import subprocess
import ctypes

def run_program():
    # Executa o programa
    subprocess.Popen(["python", "Music Player Mk II.py"])

    # Minimiza a janela do terminal
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

if __name__ == "__main__":
    run_program()