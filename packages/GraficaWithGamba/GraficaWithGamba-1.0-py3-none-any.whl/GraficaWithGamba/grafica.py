from tkinter import *
from tkinter import messagebox
from numpy import sin, cos, linspace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class App(Frame): # Clase 
  
    def __init__(self, master): # Inicializador
        Frame.__init__(self, master)
        self.master = master
        # Caja Texto
        self.e_texto = Entry(self.master, font = "Calibri 20")
        self.e_texto.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5)

        # Botonoes
        self.bot_1 = Button(self.master, text = "1", width = 8, height = 3, command = lambda:self.click(1),bg = "#566573")
        self.bot_2 = Button(self.master, text = "2", width = 8, height = 3, command = lambda:self.click(2),bg = "#566573")
        self.bot_3 = Button(self.master, text = "3", width = 8, height = 3, command = lambda:self.click(3),bg = "#566573")
        self.bot_4 = Button(self.master, text = "4", width = 8, height = 3, command = lambda:self.click(4),bg = "#566573")
        self.bot_5 = Button(self.master, text = "5", width = 8, height = 3, command = lambda:self.click(5),bg = "#566573")
        self.bot_6 = Button(self.master, text = "6", width = 8, height = 3, command = lambda:self.click(6),bg = "#566573")
        self.bot_7 = Button(self.master, text = "7", width = 8, height = 3, command = lambda:self.click(7),bg = "#566573")
        self.bot_8 = Button(self.master, text = "8", width = 8, height = 3, command = lambda:self.click(8),bg = "#566573")
        self.bot_9 = Button(self.master, text = "9", width = 8, height = 3, command = lambda:self.click(9),bg = "#566573")
        self.bot_0 = Button(self.master, text = "0", width = 19, height = 3, command = lambda:self.click(0),bg = "#566573")

        self.bot_b = Button(self.master, text = "AC", width = 8, height = 3, command = lambda:self.borrar(), bg = "#E74C3C")
        self.bot_p = Button(self.master, text = "(", width = 8, height = 3, command = lambda:self.click("("),bg = "#6C3483")
        self.bot_p1 = Button(self.master, text = ")", width = 8, height = 3, command = lambda:self.click(")"),bg = "#6C3483")
        self.bot_pp = Button(self.master, text = ".", width = 8, height = 3, command = lambda:self.click("."),bg = "#6C3483")

        self.bot_s = Button(self.master, text = "+", width = 8, height = 3, command = lambda:self.click("+"), bg = "#17A589")
        self.bot_r = Button(self.master, text = "-", width = 8, height = 3, command = lambda:self.click("-"), bg = "#17A589")
        self.bot_m = Button(self.master, text = "*", width = 8, height = 3, command = lambda:self.click("*"), bg = "#17A589")
        self.bot_d = Button(self.master, text = "/", width = 8, height = 3, command = lambda:self.click("/"), bg = "#17A589")
        self.bot_i = Button(self.master, text = "=", width = 8, height = 3, command = lambda:self.opera(),bg = "#E74C3C")

        self.bot_seno = Button(self.master, text="Sin", width = 8, height = 3,command=lambda: self.click("sin(x)"),bg = "#3498DB")
        self.bot_coseno = Button(self.master, text="Cos", width = 8, height = 3,command=lambda: self.click("cos(x)"),bg = "#3498DB")
        self.bot_x = Button(self.master, text="x", width = 8, height = 3,command=lambda: self.click("x"),bg = "#6C3483")
        self.bot_graficar = Button(self.master, text="Grafig", width = 8, height = 3,command=lambda: self.graficar_funcion(), bg = "#17A589")

        #Agregar A Pantalla

        self.bot_1.grid(row = 4, column =0, padx = 3, pady = 3)
        self.bot_2.grid(row = 4, column =1, padx = 3, pady = 3)
        self.bot_3.grid(row = 4, column =2, padx = 3, pady = 3)
        self.bot_4.grid(row = 3, column =0, padx = 3, pady = 3)
        self.bot_5.grid(row = 3, column =1, padx = 3, pady = 3)
        self.bot_6.grid(row = 3, column =2, padx = 3, pady = 3)
        self.bot_7.grid(row = 2, column =0, padx = 3, pady = 3)
        self.bot_8.grid(row = 2, column =1, padx = 3, pady = 3)
        self.bot_9.grid(row = 2, column =2, padx = 3, pady = 3)
        self.bot_0.grid(row = 5, column =0, columnspan= 2, padx = 3, pady = 3)

        self.bot_b.grid(row = 1, column =0, padx = 3, pady = 3)
        self.bot_p.grid(row = 1, column =1, padx = 3, pady = 3)
        self.bot_p1.grid(row = 1, column =2, padx = 3, pady = 3)
        self.bot_pp.grid(row = 5, column =2, padx = 3, pady = 3)

        self.bot_s.grid(row = 2, column =3, padx = 3, pady = 3)
        self.bot_r.grid(row = 3, column =3, padx = 3, pady = 3)
        self.bot_m.grid(row = 4, column =3, padx = 3, pady = 3)
        self.bot_d.grid(row = 1, column =3, padx = 3, pady = 3)
        self.bot_i.grid(row = 5, column =3, padx = 3, pady = 3)

        self.bot_x.grid(row = 6, column =0, padx = 3, pady = 3)
        self.bot_seno.grid(row = 6, column =1, padx = 3, pady = 3)
        self.bot_coseno.grid(row = 6, column =2, padx = 3, pady = 3)
        self.bot_graficar.grid(row = 6, column =3, padx = 3, pady = 3)

        self.i = 0

    def click(self,valor):
        corri = len(self.e_texto.get())
        self.e_texto.insert(corri, valor)
        self.i += 1

    def borrar(self):
        self.e_texto.delete(0,END)
        self.i = 0

    def opera(self):
        try:
            cosas = self.e_texto.get()
            resul = "{:.1f}".format(eval(cosas))
            self.e_texto.delete(0, END)
            self.e_texto.insert(0, resul)
            self.i = 0
        except:
            messagebox.showinfo("Aviso!","No se puedo operar la expresion")

    def graficar_funcion(self):
        expresion = self.e_texto.get()

        x = linspace(-20, 20, 100)

        y = self.evaluar_funcion(x, expresion)

        if y is not None:
            
            ventana_grafica = Toplevel(self.master)
            ventana_grafica.title("Gráfica de la función")

            figura = plt.figure()
            axes = figura.add_subplot(111)

            axes.plot(x, y)
            axes.set_xlabel('Eje X')
            axes.set_ylabel('Eje Y')
            axes.set_title('Gráfico de la función: ' + expresion)
            axes.grid(True)

            lienzo = FigureCanvasTkAgg(figura, master=ventana_grafica)
            lienzo.draw()
            lienzo.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

            barra_herramientas = NavigationToolbar2Tk(lienzo, ventana_grafica)
            barra_herramientas.update()
            lienzo.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        else:
            messagebox.showerror("Error", "La función ingresada es inválida.")

    def evaluar_funcion(self,x, expresion):
        try:
            return eval(expresion)
        except:
            return None


if __name__ == "__main__": # No Me Acuerdo De Donde Salio Menor No Tocar
    root = Tk()
    root.configure(bg = "#17202A")
    root.title("Calculadora/Graficadora")
    root = App(root)
    root.mainloop()