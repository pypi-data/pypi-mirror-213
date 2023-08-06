This is a simple example package. You can use

from GraficaWithGamba import grafica
from tkinter import *


if __name__ == "__main__" # Aqui Se Crea La istancia y la ventana donde ve la graficadora
    root = Tk()
    root.configure(bg = "#17202A")
    root.title("Calculadora/Graficadora")
    root = grafica.App(root)
    root.mainloop()
