

# -*- coding: utf-8 -*-
"""

Created by Pablo La Grutta
pablo.lg@hotmail.com.ar


"""
import tkinter as tk

from tkinter import ttk, StringVar,scrolledtext as st
from tkinter.ttk import Style
from tkinter.filedialog import askopenfilename, askdirectory

from tkinter.messagebox import showinfo
from os import listdir
from os.path import isfile, join

import datetime
import pandas as pd
import numpy as np

import os
import glob
import sys

from geopy.distance import great_circle
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint


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
                # parameters that you want to send through the Frame class. 
        ##-- ttk.Frame.__init__(self, window)   

        ##--tk.Tk.__init__(self)
        self.path_resultados = ''
        self.input_text_resultados= ''
        self.var3100 = tk.StringVar()
        self.var3150 = tk.StringVar()
        self.var2225 = tk.StringVar()
        self.var950 = tk.StringVar()
        self.var975 = tk.StringVar()
        self.var9360 = tk.StringVar()
        etiq_bt1 = "Archivo BD"
        etiq_bt2 = "Procesar archivos"
        etiq_bt3 = "Descargar en..."
        etiq_bt4 = "Archivo LNCEL"
        etiq_bt5= "Concatenar archivos"

        window.title("DAT Mastikator 1.2")
        window.config(bg='#108ceb')
        window.resizable(0, 0) 
        window.geometry("800x400")  #ancho largo
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)
 
        style = Style() 

        style.configure('W.TButton', font =('calibri', 10, 'bold', 'underline'), background = "orange", foreground = 'blue') 
   
        style.configure('FrameRB.TFrame', background = "orange") 
        FrameRB = ttk.Frame(window,style='FrameRB.TFrame')
        FrameRB.grid(row=2,column=1,padx=10,pady=10,sticky="ns")
            
        ttk.Button(window, text = etiq_bt1,style = 'W.TButton', command = lambda: self.set_path_dat()).grid(row = 0) 
        self.scrolledtext0=st.ScrolledText(window, width=80, height=1)

        self.scrolledtext0.grid(column=1,row=0, padx=0, pady=10)
        ttk.Button(window, text = etiq_bt5,style = 'W.TButton', command = lambda: self.set_path_ws()).grid(row = 5,column=2,padx=100) 



        ttk.Button(window, text = etiq_bt4,style = 'W.TButton', command = lambda: self.set_path_lncel()).grid(row = 1) 
        self.scrolledtext1=st.ScrolledText(window, width=80, height=1)
        self.scrolledtext1.grid(column=1,row=1, padx=0, pady=10)


        ttk.Label(text="Filtro de banda",foreground="red").grid(row=2,column=0, ipadx=10, ipady=8)

        self.cb3100 = tk.Checkbutton(FrameRB, text = "2600: 3100", variable = self.var3100, 
                 onvalue = 3100, offvalue = 0, bg ='#10ebe4').grid(row=2,column=1,padx=150,pady=5)
        self.cb3150 = tk.Checkbutton(FrameRB, text = "2600: 3150", variable = self.var3150, 
                 onvalue = 3150, offvalue = 0,bg ='#10ebe4').grid(row=2,column=2,padx=50,pady=5)
        self.cb2225 = tk.Checkbutton(FrameRB, text = "2100: 2225", variable = self.var2225, 
                 onvalue = 2225, offvalue = 0,bg ='#10ebe4').grid(row=3,column=1,padx=150,pady=5)

        self.cb950 = tk.Checkbutton(FrameRB, text = "1900: 950", variable = self.var950, 
                 onvalue = 950, offvalue = 0,bg ='#10ebe4').grid(row=3,column=2,padx=50,pady=5)
        self.cb975 =  tk.Checkbutton(FrameRB, text = "1900: 975", variable = self.var975, 
                 onvalue = 975, offvalue = 0,bg ='#10ebe4').grid(row=4,column=1,padx=150,pady=5)
        self.cb9360 = tk.Checkbutton(FrameRB, text = "700: 9360", variable = self.var9360, 
                 onvalue = 9360, offvalue = 0,bg ='#10ebe4').grid(row=4,column=2,padx=50,pady=5)

        
        ttk.Label(text="Filas por hoja",foreground="red").grid(row=3,column=0, ipadx=20, ipady=5)
        self.combo1 = ttk.Combobox(window)
        self.combo1.grid(row=3,column=1, ipadx=20, ipady=5)


        self.combo1["values"] = [10000,20000,30000,40000,50000,100000,200000, 300000,400000, 500000]
        self.num_lineas = self.combo1.bind("<<ComboboxSelected>>", self.sel_combo1)
        ttk.Label(text="Binning en Mts",foreground="red").grid(row=4,column=0, ipadx=20, ipady=5)
        self.combo2 = ttk.Combobox(window)
        self.combo2.grid(row=4,column=1, ipadx=20, ipady=5)


        self.combo2["values"] = [1,2,5,10,20,50]
        self.distBinning = self.combo2.bind("<<ComboboxSelected>>", self.sel_combo2)

        ttk.Button(window, text = etiq_bt3,style = 'W.TButton', command = lambda: self.set_path_resultados()).grid(row = 5) 
        self.scrolledtext2=st.ScrolledText(window, width=80, height=2)
        self.scrolledtext2.grid(column=1,row=5, padx=0, pady=5)
        
        ttk.Button(window, text = etiq_bt2, style = 'W.TButton',command = lambda: self.Proceso1()).grid(row = 6,column=1,padx=50) 

        

    def sel_combo1(self, event):
        num_lineas = self.combo1.get()

        self.num_lineas = int(num_lineas)
        return self.num_lineas  
    def sel_combo2(self, event):
        distB = self.combo2.get()

        self.distB = int(distB)
        return self.distB

    def Proceso1(self):   

        listaRB = [self.var3100.get(),self.var3150.get(),self.var2225.get(),self.var950.get(),self.var975.get(),self.var9360.get()]

        listaRB = [int(a) for a in listaRB if a!='']
        data = self.data
        dfLncel = self.dfLncel
        data = pd.merge(data,dfLncel,how='inner',on=['MRBTS','LCRID']) 
        data['RSRP'] = data['RSRP'].apply(lambda x: x - 65536)

        dictRSRQ = {0:-20,1:-19.5,2:-19,3:-18.5,4:-18,5:-17.5,6:-17,7:-16.5,8:-16,9:-15.5,10:-15,
                    11:-14.5,12:-14,13:-13.5,14:-13,15:-12.5,16:-12,17:-11.5,18:-11,19:-10.5,20:-10,
                    21:-9.5,22:-9,23:-8.5,24:-8,25:-7.5,26:-7,27:-6.5,28:-6,29:-5.5,
                    30:-5,31:-4.5,32:-4,33:-3.5,34: -3.0}
                    
                    
        data['RSRQ'] = data['RSRQ'].map(dictRSRQ)
        data = data.loc[data['EARFCN'].isin(listaRB)] ##--Filtro el DF por las bandas seleccionadas enRadioButton
        coords_sk = data[['LAT', 'LONG']].values
        kms_per_radian = 6371.0088
        epsilon = (self.distB/1000) / kms_per_radian
        db = (eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords_sk))
        cluster_labels = db.labels_
        num_clusters = len(set(cluster_labels))
        clusters = pd.Series([coords_sk[cluster_labels == n] for n in range(num_clusters)])
        data['Cluster_ID'] = pd.Series(cluster_labels, index=data.index)
        data['Avg_RSRP'] = data.groupby(['Cluster_ID'], as_index=False)['RSRP'].transform('mean')
        def get_centermost_point(cluster):
            centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
            centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
            return tuple(centermost_point)
        centermost_points = clusters.map(get_centermost_point)
        lats, lons = zip(*centermost_points)

        rep_points = pd.DataFrame({'LONG':lons, 'LAT':lats})

        data_rs = rep_points.apply(lambda row: data[(data['LAT']==row['LAT']) & (data['LONG']==row['LONG'])].iloc[0], axis=1)

        data_rs[['LAT','LONG']].replace('.',',',inplace=True)

        names = data_rs['NAME'].unique().tolist()
        ct = str(datetime.datetime.now() ).replace(' ','_').replace(':','').replace('.','')[0:17]
        path_origen = str(self.path_dat).split('/')
        with pd.ExcelWriter(self.path_res + '/Resultados_'+ path_origen[-1][:-4] +'_' + ct  + '.xlsx') as writer:  # el argumento de ExcelWriter es el path al archivo, ahi tengo que cargar el path deseado
            for myname in names:
                mydf = data_rs.loc[data_rs.NAME==myname]
                #mydf.to_excel(writer, sheet_name=myname)
                for key, grp in mydf.groupby(mydf.index // int(self.num_lineas)): 

                    grp.to_excel(writer, f'sheet_{myname}_{key}', header=True)
    
            writer.save()       

        print(showinfo("Results", "Results are ready!\n Upload new files or close the app."))


        gui.__init__(window)

    def set_path_lncel(self):

        self.path_lncel = askopenfilename( filetypes = [("Archivo LNCEL","*.xlsx"),("Todos los archivos","*.*")], title = "Seleccionar archivo LNCEL")
        self.scrolledtext1.insert("1.0", self.path_lncel)

        self.dfLncel = pd.read_excel(self.path_lncel)#,sheet_nameA_LTE_MRBTS_LNBTS_LNCEL')
        self.dfLncel = self.dfLncel[['mrbtsId','lnCelId','name']]
        self.dfLncel.rename(columns={'mrbtsId':'MRBTS','lnCelId':'LCRID','name':'NAME'},inplace=True)
        
    def set_path_dat(self):     
        self.path_dat = askopenfilename( filetypes = [("Archivo DAT","*.dat"),("Todos los archivos","*.*")], title = "Seleccionar archivo DAT o TXT")
        self.scrolledtext0.insert("1.0", self.path_dat)
        self.data = pd.read_csv(self.path_dat, names=['MRBTS','RSRP','RSRQ','LAT','LONG','LCRID','EARFCN'])

        
    def set_path_ws(self):
        self.path_ws = askdirectory()
        files_ws= [f for f in listdir(self.path_ws) if isfile(join(self.path_ws, f))]
        str(files_ws).split(', \n')
        self.scrolledtext3.insert("1.0", files_ws)
        os.chdir(self.path_ws)
        extension = 'dat'
        all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
        #combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        #export to csv
        combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

    def set_path_resultados(self):
        self.path_res = askdirectory( )
        print('path_res',self.path_res)
        self.scrolledtext2.insert("1.0",self.path_res)


if __name__ == '__main__':
    window = tk.Tk()
    gui = GUI(window)
    window.mainloop()

