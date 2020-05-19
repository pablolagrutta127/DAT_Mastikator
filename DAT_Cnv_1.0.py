# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:50:54 2019
@author:Pablo La Grutta
pablo.lg@hotmail.com.ar

"""

import tkinter as tk
from tkinter import ttk, StringVar,scrolledtext as st
from tkinter.ttk import Style
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo
import datetime
import pandas as pd
import os



import sys
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
    print('application_path de Py', application_path)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    
class GUI(tk.Tk):
    def __init__(self, window): 
        a = "soy un cambio"
        b = "soy un branch"
        self.path_resultados = ''
        self.input_text_resultados= ''
        etiq_bt1 = "Archivo BD"
        etiq_bt2 = "Resultados"
        etiq_bt3 = "Descargar en..."
        window.title("DAT Mastikator 1.0")
        window.config(bg='#321899')
        window.resizable(0, 0) 
        window.geometry("800x300")  #ancho largo

        style = Style() 
        style.configure('W.TButton', font =('calibri', 10, 'bold', 'underline'), background = "orange", foreground = 'blue') 

        ttk.Button(window, text = etiq_bt1,style = 'W.TButton', command = lambda: self.set_path_entrada()).grid(row = 0) 
        self.scrolledtext0=st.ScrolledText(window, width=80, height=2)
        self.scrolledtext0.grid(column=1,row=0, padx=0, pady=10)
        
        ttk.Label(text="Numero de líneas a separar",foreground="red").grid(row=1,column=0, ipadx=20, ipady=10)
        self.combo = ttk.Combobox(window)
        self.combo.grid(row=1,column=1, ipadx=20, ipady=10)

        self.combo["values"] = [100000,200000, 300000,400000, 500000]
        self.num_lineas = self.combo.bind("<<ComboboxSelected>>", self.selection_changed)

        ttk.Button(window, text = etiq_bt3,style = 'W.TButton', command = lambda: self.set_path_resultados()).grid(row = 2) 
        self.scrolledtext1=st.ScrolledText(window, width=80, height=2)
        self.scrolledtext1.grid(column=1,row=2, padx=0, pady=10)
        ttk.Button(window, text = etiq_bt2, style = 'W.TButton',command = lambda: self.Proceso1()).grid(row = 3) 

    def selection_changed(self, event):
        num_lineas = self.combo.get()
        self.num_lineas = int(num_lineas)
        return self.num_lineas  

    def Proceso1(self):  
        data = pd.read_csv(self.path_entrada, names=['MRBTS','RSRP','LAT','LONG','LNCEL'])
        data['RSRP'] = data['RSRP'].apply(lambda x: x - 65536)
        data[['LAT','LONG']].replace('.',',',inplace=True)
        ct = str(datetime.datetime.now() ).replace(' ','_').replace(':','').replace('.','')[0:17]

        path_origen = str(self.path_entrada).split('/')
        with pd.ExcelWriter(self.path_res + '/Resultados_'+ path_origen[-1][:-4] +'_' + ct  + '.xlsx') as writer:  # el argumento de ExcelWriter es el path al archivo, ahi tengo que cargar el path deseado

            for key, grp in data.groupby(data.index // int(self.num_lineas)):
                grp.to_excel(writer, f'sheet_{key}', header=True)
            writer.save()

        print(showinfo("Resultados", "Resultados listos!\nCargue nuevos CSV o cierre el programa."))

        gui.__init__(window)

    def set_path_entrada(self):
        self.path_entrada = askopenfilename( filetypes = [("Archivo DAT","*.dat"),("Todos los archivos","*.*")], title = "Seleccionar archivo DAT o TXT")
        self.scrolledtext0.insert("1.0", self.path_entrada)

        
    def set_path_resultados(self):
        self.path_res = askdirectory( )

        self.scrolledtext1.insert("1.0",self.path_res)


if __name__ == '__main__':
    window = tk.Tk()
    gui = GUI(window)

    window.mainloop()
