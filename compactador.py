import os
from tkinter import *
import customtkinter
from PIL import Image
import shutil
import pyzipper

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")

win = customtkinter.CTk()
win.geometry("330x200")
win.title('Compactador de Imagens')
win.resizable(False, False)

def botao_compactar():
   compactar(entradacaminho.get())

titulo = customtkinter.CTkLabel(win, text="Compactador de Imagens")
titulo.grid(row=0, column=0, padx=5, pady=5)

entradacaminho= customtkinter.CTkEntry(win, width= 300)
entradacaminho.focus_set()
entradacaminho.grid(row=1,column=0, padx=10, pady=15)

def selecionar_arquivo():
    filename = customtkinter.filedialog.askdirectory(
        title='Selecione uma Pasta',
        initialdir='/')
    entradacaminho.delete(0, END)
    entradacaminho.insert(0,filename +'/')

botao_pesquisar = customtkinter.CTkButton(win,text='Pesquisar Pasta...',width= 300 , command=selecionar_arquivo).grid(row=2,column=0, padx=5, pady=5)

botao_compactar = customtkinter.CTkButton(win, text= "Dezipar/Compactar Imgs/Zipar",width= 300, command= botao_compactar).grid(row=3,column=0, padx=5, pady=5)

def compactar(path):
     for p, _, files in os.walk(os.path.abspath(path)):
       for file in files:
        nomearquivo = os.path.join(p, file)
        dir = path + file[:-4]
        os.mkdir(dir)
        unzippar(nomearquivo,path,file)
        reduzir_tamanho_imagens(dir, dir, ext='.jpg')
        zippar(dir)
        excluir_arquivos(dir)

def unzippar(nomearquivo,path,file):
 senha = ''
 with pyzipper.AESZipFile(nomearquivo, 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as extracted_zip:
    extracted_zip.extractall(path + file[:-4], pwd=str.encode(senha))

 #metodo para sem encriptação
 #z = zipf.ZipFile(nomearquivo, 'r')
 #senha = ''
 #z.extractall(path + file[:-4], pwd=str.encode(senha))
 #z.close()

def eh_imagem(nome_arquivo):  
    if nome_arquivo.endswith('png') or nome_arquivo.endswith('jpg'):
        return True
    return False

def reduzir_tamanho_imagens(dir, output_dir, ext='.jpg'):
    lista_de_arquivos = [nome for nome in os.listdir(dir) if eh_imagem(nome)]
    for nome in lista_de_arquivos:
        imagem = Image.open(os.path.join(dir, nome)).convert('RGB')
        redimensionada = imagem.resize((1280, 720))
        nome_sem_ext = os.path.splitext(nome)[0]
        redimensionada.save(os.path.join(output_dir, nome_sem_ext + ext))       
        
def zippar(dir):
 z = pyzipper.AESZipFile(dir + '_new.zip','w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES)
 senha = b''
 z.setpassword(senha)
 for folder, subfolders, files in os.walk(dir):
    for file in files:
     z.write(os.path.join(folder,file), os.path.relpath(os.path.join(folder,file), dir))
 z.close()     

def excluir_arquivos(dir):
 try:
    shutil.rmtree(dir)
 except OSError as e:
    print(f"Error:{ e.strerror}")

win.mainloop()