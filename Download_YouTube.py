import tkinter as tk
from tkinter import *

from tkinter import ttk

import datetime


from PIL import ImageTk, Image

import requests

from pytube import YouTube
import pytube as yt
from tkinter.ttk import Progressbar


import tkinter.messagebox as messagebox



def download_youtube():
    ################# cores ###############
    co0 = "#444466"  # Preta
    co1 = "#feffff"  # branca
    co2 = "#6f9fbd"  # azul
    co3 = "#38576b"  # valor
    co4 = "#403d3d"   # letra

    fundo = "#3b3b3b"


    janela = tk.Toplevel()
    janela.title('PyDownloadYT')
    janela.geometry('500x300')
    janela.configure(bg=fundo)
    icone = tk.PhotoImage(file='youtube (ico).png')  # Substitua pelo caminho do seu ícone
    janela.iconphoto(False, icone)
    janela.resizable(width=False, height=False)
    ################# Frames ####################

    ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=250)

    frame_principal = Frame(janela, width=500, height=110,bg=fundo, pady=5, padx=0, relief="flat",)
    frame_principal.grid(row=1, column=0)

    frame_quadros = Frame(janela, width=500, height=300,bg=fundo, pady=12, padx=0, relief="flat",)
    frame_quadros.grid(row=2, column=0, sticky=NW)

    logo = Image.open('youtube.png')
    logo = logo.resize((50, 50))
    logo = ImageTk.PhotoImage(logo)
    l_logo = Label(frame_principal,image=logo, compound=LEFT,  bg=fundo, fg="white",font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
    l_logo.place(x=5, y=10)

    app_nome = Label(frame_principal, text="YouTube Downloader app", width=32, height=1, padx=0, relief="flat", anchor="nw", font=('Ivy 15 bold'), bg=fundo, fg=co1)
    app_nome.place(x=65, y=15)

    #style = ttk.Style(frame_principal)
    #style.theme_use("clam")


    def search():
        global img, available_streams, Description, selected_resolution, resolution
        url = e_url.get()
        yt = YouTube(url)
        
        #Title of video
        title=yt.title
        #Number of views of video
        view= yt.views

        #Length of the video
        duration= str(datetime.timedelta(seconds=yt.length)) 

        #Description of video
        Description=yt.description

        #cover of the video
        cover=yt.thumbnail_url

        
        
        
        available_streams = yt.streams.filter(only_audio=False).order_by('resolution').desc().all()

        resolutions = [stream.resolution for stream in available_streams if 'video' in str(stream) and 'mp4' in str(stream)]

        # Criar um menu suspenso com as resoluções das streams
        selected_resolution = tk.StringVar()
        selected_resolution.set(resolutions[0])

        resolution_menu = ttk.Combobox(frame_quadros, textvariable=selected_resolution, values=resolutions, state='readonly', width=15)
        resolution_menu.place(x=250, y=110)
        print(cover)
        resolution = selected_resolution.get()

        img_ = Image.open(requests.get(cover, stream=True).raw)
        img_ = img_.resize((230, 150))
        img_ = ImageTk.PhotoImage(img_)

        img=img_
        l_image['image']=img

        l_title['text'] = f"Título: {title} (Resolução: {resolution})"
        l_view['text']="Views : " + str('{:,}'.format(view))
        l_time['text']="Duracao : " + str(duration)



    #previousprogress = 0


    def download():
        global bar
        quality = selected_resolution.get()  # Qualidade desejada (pode ser ajustada)
        
        if not available_streams:
            print("Nenhuma stream disponível.")
            return
        
        chosen_stream = None
        for stream in available_streams:
            if 'video' in str(stream) and quality in str(stream) and 'mp4' in str(stream):
                chosen_stream = stream
                break
        
        if chosen_stream is None:
            messagebox.showerror("Erro", f"Nenhuma stream de {quality} disponível.")
            return
        
        

        messagebox.showinfo("Iniciando Download", "O download está sendo iniciado...")
        chosen_stream.download()
        messagebox.showinfo("Download Concluído", "O download foi concluído com sucesso!")
        
        print("Download concluído.")
            

    l_url = Label(frame_principal, text="Enter URL", height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 10 bold'), bg=fundo, fg=co1)
    l_url.place(x=10, y=80)

    e_url = Entry(frame_principal, width=50, justify='left',relief=SOLID)
    e_url.place(x=100, y=80)

    b_search = Button(frame_principal, text="Search", width=10, height=1, bg=co2, fg=co1,font=('Ivy 7 bold'), relief=RAISED, overrelief=RIDGE,command = lambda:search())
    b_search.place(x=404, y=80)




    l_image = Label(frame_quadros, compound=LEFT,  bg=fundo, fg="white",font=('Ivy 10 bold'), anchor="nw", relief=FLAT)
    l_image.place(x=10, y=10)

    l_title = Label(frame_quadros, height=2, pady=0, padx=0, relief="flat", wraplength=225, compound=LEFT, justify='left', anchor=NW, font=('Ivy 10 bold'), bg=fundo, fg=co1)
    l_title.place(x=250, y=15)

    l_view = Label(frame_quadros, height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=fundo, fg=co1)
    l_view.place(x=250, y=60)

    l_time = Label(frame_quadros, height=1,pady=0, padx=0, relief="flat", anchor=NW, font=('Ivy 8 bold'), bg=fundo, fg=co1)
    l_time.place(x=250, y=85)



    down = Image.open('download.png')
    down = down.resize((40, 40))
    down = ImageTk.PhotoImage(down)
    b_download = Button(frame_quadros, image=down, bg=fundo, fg=co1,font=('Ivy 10 bold'), relief=FLAT, overrelief=RIDGE, command=download)
    b_download.place(x=444, y=85)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#00E676')
    style.configure("TProgressbar", thickness=6)

    bar = Progressbar(frame_quadros, length=190, style='black.Horizontal.TProgressbar', mode='determinate')
    bar.place(x=250, y=135)

        


    janela.mainloop()

root = tk.Tk()
root.title("Torquato Tech")

icone1 = tk.PhotoImage(file='MateusTor.png')
root.iconphoto(False, icone1)
root.resizable(width=False, height=False)
# Carregar a imagem da sua logo
image = tk.PhotoImage(file="TorquatoTech.png")  # Substitua pelo caminho correto da sua logo
# Redimensionar a imagem para 318x318
image = image.subsample(int(image.width() / 318))

# Criar um rótulo para exibir a imagem da logo
label = tk.Label(root, image=image)
label.pack()


# Criar um botão sobre a imagem
#button = tk.Button(root, text="Calculadora", command=Calculadora_Model)
#button.place(relx=0.95, rely=0.5, anchor=tk.E)
root.after(10000, download_youtube)
root.mainloop()