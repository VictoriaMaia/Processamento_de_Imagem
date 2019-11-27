from tkinter import Tk, BOTH, Frame, Menu, Button, filedialog, Label, messagebox, colorchooser, Toplevel, Radiobutton
from tkinter import Checkbutton, IntVar
from tkinter import LEFT, TOP, X, FLAT, RAISED, W
import tkinter

# from tkinter.ttk import Frame
from PIL import Image, ImageTk
import cv2
import pyscreenshot as ImageGrab 
import time
import os
import math
import numpy as np
from PIL import ImagePalette
from PIL import Image

class Example(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.master.title(";D")
        self.pack(fill=BOTH, expand=1)
        self.width = 800
        self.height = 540
        self.tamIcon = 30
        self.str_tamanho_janela = str(self.width)+ 'x' + str(self.height)
        #  geometry(width x height)
        self.master.geometry(self.str_tamanho_janela+'+300+100')
        
        # auxiliares
        self.filepath = ""
        self.Im_height = 0
        self.Im_width = 0
        self.canais = 0
        self.rgb = 1
        self.desenhar = 0
        self.desenho = 0
        self.desenhoLinha = 0
        self.trace = 0
        self.listObj = []
        self.ObjCorte = []
        self.objectId = 0
        self.fillCor = ""
        self.outline = "black"
        self.tamLinha = 1
        self.R = IntVar()
        self.G = IntVar()
        self.B = IntVar()
        self.H = IntVar()
        self.S = IntVar()
        self.V = IntVar()
        self.mostrarUmavez = 0
        self.VarFiltroMedia = IntVar()
        self.cortar = 0
        self.TemFFT = 0
        self.ListaAlteracoesFeitas = []
        # self.ListaAlteracoesDesfeitas = []
                    
        self.initMenu()      

        self.canvas = tkinter.Canvas(self.master, width = self.width, height = self.height)
        self.canvas.pack()

        self.canvas.bind('<ButtonPress-1>', self.onStart)
        self.canvas.bind('<B1-Motion>',     self.onGrow) 
        self.canvas.bind('<ButtonPress-3>', self.onDelete)
        self.canvas.bind('<ButtonRelease-1>', self.onSabeIdObj)
        
        self.pack()


    def initMenu(self):
        self.menubar = Menu(self.master)

        # Criar menus
        self.fileMenu = Menu(self.master, tearoff=0)
        self.visualizarMenu = Menu(self.master, tearoff=0)
        self.ferramentaMenu = Menu(self.master, tearoff=0)   
        self.corMenu = Menu(self.master, tearoff=0)
        self.linhaMenu = Menu(self.master, tearoff=0)
        self.segmentacaoMenu = Menu(self.master, tearoff=0)
        self.selecaoAreasMenu = Menu(self.master, tearoff=0)
        self.correcaoDeCoresMenu = Menu(self.master, tearoff=0)
        self.filtrosMenu = Menu(self.master, tearoff=0)
        self.desfazerMenu = Menu(self.master, tearoff=0)
         

        # Adicionar comando
        self.fileMenu.add_command(label="Abrir Imagem", command=self.onOpen)
        self.fileMenu.add_command(label="Salvar Imagem", command=self.onSave)
        self.fileMenu.add_command(label="Informações", command=self.onInfo)
        self.fileMenu.add_command(label="Sair", command=self.onExit)
        
        self.visualizarMenu.add_command(label="RGB", command=self.onRGB)
        self.visualizarMenu.add_command(label="HSV", command=self.onHSV)

        self.ferramentaMenu.add_command(label="Desenhar", command=self.onDesenhar)
        
        self.corMenu.add_command(label="Contorno", command=self.onEscolherCor_Contorno)
        self.corMenu.add_command(label="Preenchimento", command=self.onEscolherCor_Preencher)
        self.corMenu.add_command(label="Contorno e Preenchimento", command=self.onPreen_Contor)
        self.corMenu.add_command(label="Default", command=self.onDefault)

        self.linhaMenu.add_command(label="Espessura", command=self.new_winEspessura)
        self.linhaMenu.add_command(label="Default", command=self.onDefaultLinha)

        self.segmentacaoMenu.add_command(label="Threshold", command=self.onbarThre)
        # self.segmentacaoMenu.add_command(label="Default", command=self.onDefaultRGBHSV)
        # self.segmentacaoMenu.add_command(label="Watershed", command=self.onWatershed)

        self.selecaoAreasMenu.add_command(label="Retângulo", command=self.onSelectRetangulo)
        self.selecaoAreasMenu.add_command(label="Cortar área", command=self.onCortarArea)
        

        self.correcaoDeCoresMenu.add_command(label="Historgrama", command=self.onHistogramaEq)
        self.correcaoDeCoresMenu.add_command(label="Quantização", command=self.onQuantizar)
        self.correcaoDeCoresMenu.add_command(label="Saturação", command=self.onSaturacao)
        self.correcaoDeCoresMenu.add_command(label="Colorizar por indice", command=self.onColorizar)
        self.correcaoDeCoresMenu.add_command(label="Balanço de branco", command=self.white_balance)
        

        self.filtrosMenu.add_command(label="FFT", command=self.onFFT)
        self.filtrosMenu.add_command(label="IFFT", command=self.onIFFT)
        self.filtrosMenu.add_command(label="Realcar com Media", command=self.filterRealceMedia)
        self.filtrosMenu.add_command(label="Aplicar Gaussiana", command=self.filterGauss)
        
        self.desfazerMenu.add_command(label="Desfazer ação", command=self.onDesfazer)

        # Mostrar os menus
        self.menubar.add_cascade(label= "Arquivo", menu=self.fileMenu)
        self.menubar.add_cascade(label= "Visualizar", menu=self.visualizarMenu)
        self.menubar.add_cascade(label= "Ferramentas", menu = self.ferramentaMenu)
        self.menubar.add_cascade(label= "Segmentação", menu = self.segmentacaoMenu)
        self.menubar.add_cascade(label= "Seleção Áreas", menu = self.selecaoAreasMenu)
        self.menubar.add_cascade(label= "Correção Cor", menu = self.correcaoDeCoresMenu)
        self.menubar.add_cascade(label= "Filtros", menu = self.filtrosMenu)
        self.menubar.add_cascade(label= "Desfazer", menu = self.desfazerMenu)

        self.ferramentaMenu.add_cascade(label= "Cor", menu = self.corMenu)
        self.ferramentaMenu.add_cascade(label= "Linha", menu = self.linhaMenu)

        

        self.master.config(menu=self.menubar)

# FUNÇÕES DE BACKUP

    def onSalvarAlterações(self):
        if len(self.filepath) != 0:
            self.ListaAlteracoesFeitas.append(self.cv_img.copy())

    def onDesfazer(self):
        if len(self.filepath) != 0:
            if len(self.ListaAlteracoesFeitas) > 1:
                self.ListaAlteracoesFeitas.pop()
                self.cv_img = self.ListaAlteracoesFeitas[-1]
                try:
                    self.Im_height, self.Im_width, self.canais = self.cv_img.shape
                except:
                    self.Im_height, self.Im_width = self.cv_img.shape
                self.canvas.config(width = self.Im_width, height = self.Im_height)
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            elif len(self.ListaAlteracoesFeitas) == 1:
                self.cv_img = self.ListaAlteracoesFeitas[0]
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


# FUNÇÕES INICIAIS
 
    def onExit(self): self.quit()

    def onOpen(self):
        self.filepath = filedialog.askopenfilename(filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("bmp files", "*.bmp")))

        if len(self.filepath) != 0: 
            self.ListaAlteracoesFeitas = []
            self.cv_img = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_BGR2RGB)
            self.ListaAlteracoesFeitas.append(self.cv_img.copy())
            self.Im_height, self.Im_width, self.canais = self.cv_img.shape
            self.master.geometry(str(self.Im_width)+'x'+str(self.Im_height)+'+300+100')
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.config(width = self.Im_width, height = self.Im_height)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)            

    def onSave(self):
        if len(self.filepath) != 0 or len(self.ListaAlteracoesFeitas) != 0:
            filepathSave = filedialog.asksaveasfilename(initialdir = self.filepath, filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("bmp files", "*.bmp")))
            if len(filepathSave) != 0:
                time.sleep(.5)            
                box = (self.canvas.winfo_rootx(),self.canvas.winfo_rooty(),self.canvas.winfo_rootx()+self.Im_width, self.canvas.winfo_rooty()+self.Im_height)
                grab = ImageGrab.grab(bbox = box)
                grab.save(filepathSave)
        else:
            print("salvando ", len(self.ListaAlteracoesFeitas))
            print(len(self.ListaAlteracoesFeitas) == 0)
            print(len(self.filepath) != 0)
            messagebox.showerror("Erro", "Não tem imagem para ser salva.")

    def onInfo(self):
        if(len(self.filepath) == 0):
            messagebox.showerror("Erro", "Não tem imagem a ser informada.")
        else:
            strFormato = "Formato : " + self.filepath[-4: ] + "\n"
            for i in range(len(self.filepath)-1, -1, -1):
                    if(self.filepath[i] == '/'):
                        break        
            strNome = "Nome : " + self.filepath[i+1 : ] + "\n"
            strDimensao = "Dimensões : ( " + str(self.Im_height) + " , " + str(self.Im_width) + " )\n"
            strCanais = "Canais : " + str(self.canais) + "\n"
            messagebox.showinfo("Informações", strNome+strFormato+strDimensao+strCanais)
            # escrever na imagem
            # self.canvas.create_text(20, 30, anchor=W, font="Purisa", text=strNome+strFormato)

    def atualizarImg(self):
        box = (self.canvas.winfo_rootx(),self.canvas.winfo_rooty(),self.canvas.winfo_rootx()+self.Im_width, self.canvas.winfo_rooty()+self.Im_height)
        grab = ImageGrab.grab(bbox = box)
        grab.save("new_img.png")
        self.cv_img = cv2.cvtColor(cv2.imread("new_img.png"), cv2.COLOR_BGR2RGB)    
        self.onSalvarAlterações()
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        os.remove("new_img.png")


# FUNÇÕES DE VISUALIZAR RGB

    def salvarRGB(self):
        self.cv_img = self.imgCopy.copy()
        self.onSalvarAlterações()

    def oncanaisRGB(self):
        if len(self.filepath) != 0:
            self.imgCopy = self.ListaAlteracoesFeitas[-1].copy()

            if (self.R.get() and self.G.get() == 0 and self.B.get() == 0): #apenas canal vermelho
                self.imgCopy[:,:,1] = 0
                self.imgCopy[:,:,2] = 0                

            elif (self.G.get() and self.R.get() == 0 and self.B.get() == 0): #apenas canal verde
                self.imgCopy[:,:,0] = 0
                self.imgCopy[:,:,2] = 0  

            elif (self.B.get() and self.R.get() == 0 and self.G.get() == 0): #apenas canal azul
                self.imgCopy[:,:,0] = 0
                self.imgCopy[:,:,1] = 0  
            
            elif (self.B.get() and self. R.get() and self.G.get() == 0): #apenas canal azul e vermelho
                self.imgCopy[:,:,1] = 0 
            
            elif (self.B.get() and self.G.get() and self.R.get() == 0): #apenas canal azul e verde
                self.imgCopy[:,:,0] = 0 
            
            elif (self.R.get() and self.G.get() and self.B.get() == 0): #apenas canal vermelho e verde
                self.imgCopy[:,:,2] = 0 
                        
            elif (self.R.get() == 0 and self.G.get() == 0 and self.B.get() == 0): #apagou geral
                self.imgCopy[:,:,0] = 0
                self.imgCopy[:,:,1] = 0  
                self.imgCopy[:,:,2] = 0  
            
            elif (self.R.get() and self.G.get() and self.B.get()): #Tudo
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.imgCopy))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)    
                return
                
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.imgCopy))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
                    
    def onFecharNewWindowRGB(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinRGB.destroy()

    def onRGB(self):
        try:
            a,b,c = self.ListaAlteracoesFeitas[-1].shape
            self.newwinRGB = Toplevel(self.master)
            self.newwinRGB.geometry('200x100')
            cR = Checkbutton(self.newwinRGB, text="Canal R", variable=self.R, command=self.oncanaisRGB)
            cG = Checkbutton(self.newwinRGB, text="Canal G", variable=self.G, command=self.oncanaisRGB)
            cB = Checkbutton(self.newwinRGB, text="Canal B", variable=self.B, command=self.oncanaisRGB)
            salvar = Button(self.newwinRGB, text="Salvar alterações", command=self.salvarRGB)
            fechar = Button(self.newwinRGB, text="Fechar", command=self.onFecharNewWindowRGB)

            cR.pack()
            cG.pack()
            cB.pack()
            salvar.pack()
            fechar.pack()
        except:
            messagebox.showerror("Error", "Imagem não tem 3 canais")
    

# FUNÇÕES DE VISUALIZAR HSV 
    def onFecharNewWindowHSV(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinHSV.destroy()

    def cHsv(self):
        self.cv_img = self.img_h
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW) 

    def chSv(self):
        self.cv_img = self.img_s
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW) 

    def chsV(self):
        self.cv_img = self.img_v
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW) 

    def onHSV(self):
        try:
            a,b,c = self.ListaAlteracoesFeitas[-1].shape
            if len(self.filepath) != 0:
                imgCopy = self.ListaAlteracoesFeitas[-1].copy()
                imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_RGB2HSV)
                self.img_h, self.img_s, self.img_v = cv2.split(imgCopy)

                self.newwinHSV = Toplevel(self.master)
                self.newwinHSV.geometry('200x100')
                cH = Radiobutton(self.newwinHSV, text="Canal H", value=1, command=self.cHsv)
                cS = Radiobutton(self.newwinHSV, text="Canal S", value=2, command=self.chSv)
                cV = Radiobutton(self.newwinHSV, text="Canal V", value=3, command=self.chsV)
                salvar = Button(self.newwinHSV, text="Salvar alterações", command=self.onSalvarAlterações)
                fechar = Button(self.newwinHSV, text="Fechar", command=self.onFecharNewWindowHSV)

                cH.pack()
                cS.pack()
                cV.pack()
                salvar.pack()
                fechar.pack()
        except:
            messagebox.showerror("Error", "Imagem não tem 3 canais")


# FUNÇÕES DE DESENHO

    def onconfigDesenhos(self):
        self.desenhar = 1    
        self.cortar = 0 
            
    def salvarDesenho(self):
        self.desenhar = 0
        self.desenho = 0
        self.desenhoLinha = 0
        self.atualizarImg()
        self.newwinDesenho.destroy()

    def fecharSemSalvar(self):
        self.desenhar = 0
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinDesenho.destroy()

    def onDesenhar(self):
        if len(self.filepath) != 0:
            self.newwinDesenho = Toplevel(self.master)
            self.newwinDesenho.geometry('200x200')
            D = Button(self.newwinDesenho, text="Desenhar", command=self.onconfigDesenhos)
            circulo = Radiobutton(self.newwinDesenho, text="Circulo", value=1, command=self.onDesenharCir)
            quadrado = Radiobutton(self.newwinDesenho, text="Quadrado", value=2, command=self.onDesenharQuadrado)
            linha = Radiobutton(self.newwinDesenho, text="Linha", value=3, command=self.onDesenharLinha)
            linhaTracejada = Radiobutton(self.newwinDesenho, text="Linha Tracejada", value=4, command=self.onDesenharLinhaTrac)
            S = Button(self.newwinDesenho, text="Sair e salvar desenho", command=self.salvarDesenho)
            Sair = Button(self.newwinDesenho, text="Sair sem salvar", command=self.fecharSemSalvar)
        
            D.pack()
            circulo.pack()
            quadrado.pack()
            linha.pack()
            linhaTracejada.pack()
            S.pack()
            Sair.pack()

    def onDesenharCir(self):
        self.desenho = 1
        self.desenhoLinha = 0
        self.action = self.canvas.create_oval

    def onDesenharQuadrado(self):
        self.desenho = 1
        self.desenhoLinha = 0
        self.action = self.canvas.create_rectangle

    def onDesenharLinha(self):
        self.desenho = 1
        self.desenhoLinha = 1
    
    def onDesenharLinhaTrac(self):
        self.desenho = 1
        self.desenhoLinha = 2
    

    # PEGAR MOVIMENTOS DO MOUSE PARA DESENHO

    def onStart(self, event):
        if self.desenhar != 0: 
            self.start = event
            self.drawn = None

    def onGrow(self, event):      
        if self.desenhar != 0: 
            self.canvas = event.widget
            if self.drawn: self.canvas.delete(self.drawn)
            if(self.desenho != 0):
                if(self.desenhoLinha == 1):
                    self.objectId = self.canvas.create_line(self.start.x, self.start.y, event.x, event.y, fill=self.outline, width=self.tamLinha)
                elif(self.desenhoLinha == 2):
                    self.objectId = self.canvas.create_line(self.start.x, self.start.y, event.x, event.y, fill=self.outline, width=self.tamLinha, dash=(4, 4))
                else:                    
                    self.objectId = self.action(self.start.x, self.start.y, event.x, event.y, fill=self.fillCor, outline=self.outline, width=self.tamLinha)

            self.drawn = self.objectId

    def onSabeIdObj(self, event):
        if self.desenhar != 0:
            # print("id: ", self.objectId)
            if(self.objectId != 0):
                if self.cortar == 1:
                    self.ObjCorte.append(self.objectId)
                else:
                    self.listObj.append(self.objectId)
        
    def onDelete(self, event):
        if(len(self.listObj) != 0):
            self.canvas.delete(self.listObj[-1])
            self.listObj.pop()


    # SELEÇÃO DE COR

    def onEscolherCor_Preencher(self):
        (_, hx) = colorchooser.askcolor()
        self.fillCor = hx

    def onEscolherCor_Contorno(self):
        (_, hx) = colorchooser.askcolor()
        self.outline = hx

    def onDefault(self):
        self.fillCor = ""
        self.outline = "black"
    
    def onPreen_Contor(self):
        (_, hx) = colorchooser.askcolor()
        self.fillCor = hx
        self.outline = hx
    

    # SELEÇÃO DE ESPESSURA DE LINHA

    def new_winEspessura(self): # new window definition
        newwin = Toplevel(self.master)
        display = Label(newwin, text="Humm, see a new window !")
        self.canvasNewWind = tkinter.Canvas(newwin, width = 250, height = 70)
        self.canvasNewWind.create_line(50, 25, 200, 25)
        self.tkScale = tkinter.Scale(newwin, from_=1, to=20, orient=tkinter.HORIZONTAL, command=self.atualiza)
        self.tkScale.pack(anchor=tkinter.CENTER)
        self.canvasNewWind.pack()
        display.pack() 
            
    def atualiza(self, event):
        self.canvasNewWind.delete('all')
        self.canvasNewWind.create_line(50, 25, 200, 25, width=self.tkScale.get())
        self.tamLinha = self.tkScale.get()
    
    def onDefaultLinha(self):
        self.tamLinha = 1

# FALTA AJEITAR O WATERSHED
# FERRAMENTAS DE SEGMENTAÇÃO
    ##### THRESOLD #####
    def onFecharNewWindowThre(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinTre.destroy()


    def onthresold(self, event):
        valor = self.tkScale.get()   
        try:     
            img_gray = cv2.cvtColor(self.ListaAlteracoesFeitas[-1], cv2.COLOR_BGR2GRAY) 
        except:
            img_gray = self.ListaAlteracoesFeitas[-1]
        ret,self.cv_img = cv2.threshold(img_gray ,valor, 255, cv2.THRESH_BINARY)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onbarThre(self):
        if len(self.filepath) != 0: 
            self.newwinTre = Toplevel(self.master)
            self.newwinTre.geometry('280x120')
            display = Label(self.newwinTre, text="THRESOLD")
            self.tkScale = tkinter.Scale(self.newwinTre, from_=0, to=255, orient=tkinter.HORIZONTAL, length=200, command=self.onthresold)
            salvar = Button(self.newwinTre, text="Salvar alterações", command=self.onSalvarAlterações)
            fechar = Button(self.newwinTre, text="Fechar", command=self.onFecharNewWindowThre)
            
            display.pack() 
            self.tkScale.pack(anchor=tkinter.CENTER)            
            salvar.pack()
            fechar.pack()
            
        


    ##### WATERSHED #####
        def aplicarNot(self):
            self.im_thresh = cv2.bitwise_not(self.im_thresh)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.im_thresh))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onThresholdW(self, event):
            valor = self.tkScaleThresold.get()        
            ret, self.im_thresh = cv2.threshold(self.gray ,valor, 255, cv2.THRESH_BINARY)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.im_thresh))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onExtracaoRuido(self, event):
            valor = self.tkScaleRuido.get()
            self.opening = cv2.morphologyEx(self.im_thresh,cv2.MORPH_OPEN, self.kernel, iterations = valor)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.opening))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onDilata(self, event):
            valor = self.tkScaleDilata.get()
            self.sure_bg = cv2.dilate(self.opening, self.kernel,iterations=valor)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.sure_bg))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onErosao(self, event):
            valor = self.tkScaleErosao.get()
            dist_transform = cv2.distanceTransform(self.opening, cv2.DIST_L2, 5)
            ret, self.sure_fg = cv2.threshold(dist_transform,valor, 255, 0)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.sure_fg))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onRegioes(self):        
            self.sure_fg = np.uint8(self.sure_fg)
            unknown = cv2.subtract(self.sure_bg, self.sure_fg)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(unknown))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onAplicarFinalW(self):
            img = self.cv_img.copy()
            ret, markers = cv2.connectedComponents(self.sure_fg)
            markers = cv2.watershed(self.cv_img, markers)
            markers = markers.astype(np.uint8)
            ret, m2 = cv2.threshold(markers, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
            contours, hierarchy = cv2.findContours(m2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)    
            for c in contours:
                cv2.drawContours(img, c, -1, (255, 0, 0), 2)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        def onWatershed(self):
            # baseado em https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
            if len(self.filepath) != 0: 
                self.kernel = np.ones((3,3),np.uint8)        
                self.gray = cv2.cvtColor(self.cv_img,cv2.COLOR_BGR2GRAY)
                self.im_thresh = cv2.cvtColor(self.cv_img,cv2.COLOR_BGR2GRAY)
                self.opening = cv2.cvtColor(self.cv_img,cv2.COLOR_BGR2GRAY)

                
                newwin = Toplevel(self.master)

                # Coisas que irão ter na nova janela!
                lEtapa1 = Label(newwin, text="Etapa 1\nEscolher thresold.\nRealçando o objeto\nAviso: Se o fundo da imagem estiver branco clique em 'Aplicar NOT'")
                self.tkScaleThresold = tkinter.Scale(newwin, from_=0, to=255, orient=tkinter.HORIZONTAL, length=200, command=self.onThresholdW)
                bNOT = Checkbutton(newwin, text="Aplicar NOT", command=self.aplicarNot)
                
                lEtapa2 = Label(newwin, text="Etapa 2.\nExtrair área de interesse.") #erosao e dilatacao
                lExtRuido = Label(newwin, text="Extração de ruído.\nEscolha o número de iterações para aplicar a extração.")
                self.tkScaleRuido = tkinter.Scale(newwin, from_=0, to=200, orient=tkinter.HORIZONTAL, length=200, command=self.onExtracaoRuido)
                lDilata = Label(newwin, text="Dilatação.\nEscolha o número de iterações para aplicar a dilatação.\nEsse passo é para separar o que de certeza não é o objeto.")
                self.tkScaleDilata = tkinter.Scale(newwin, from_=0, to=200, orient=tkinter.HORIZONTAL, length=200, command=self.onDilata)

                lEtapa3 = Label(newwin, text="Etapa 3.\nEncontrar regiões e aplicar o Watershed")
                lErosao = Label(newwin, text="Erosão.\nEscolha o número de iterações para aplicar a erosão.\nEsse passo é para extrair a área do objeto.")
                self.tkScaleErosao = tkinter.Scale(newwin, from_=0, to=50, orient=tkinter.HORIZONTAL, length=200, command=self.onErosao)
                lRegioes = Label(newwin, text="Ver as regiões encontradas com as operações feitas!\nQuando não quiser mais mudar clique no botão para aplicar o Watershed.")
                bRegioes = Button(newwin, text="Regiões", command=self.onRegioes)
                bWatershed = Button(newwin, text="Aplicar Watershed", command=self.onAplicarFinalW)
                
                
                # ordem de aparição!
                lEtapa1.pack()
                self.tkScaleThresold.pack()
                bNOT.pack()

                lEtapa2.pack()
                lExtRuido.pack()
                self.tkScaleRuido.pack()
                lDilata.pack()
                self.tkScaleDilata.pack()

                lEtapa3.pack()
                lErosao.pack()
                self.tkScaleErosao.pack()
                lRegioes.pack()
                bRegioes.pack()
                bWatershed.pack()
            else:
                messagebox.showerror("Erro", "Para fazer esta ação é necessário carregar uma imagem.")

        
# FERRAMENTAS DE SELEÇÃO DE ÁREAS
    def avisoSelecao(self):
        messagebox.showinfo("Aviso", "Clique novamente no botão para parar de selecionar retângulos.")

    def onSelectRetangulo(self):
        if self.desenhar == 0:
            if self.mostrarUmavez == 0:
                self.avisoSelecao()
                self.mostrarUmavez = 1
            self.desenhar = 1
            self.desenho = 1
            self.cortar = 1
            self.action = self.canvas.create_rectangle
        else:
            self.desenhar = 0
            self.desenho = 0
            self.cortar = 0
    
    def onCortarArea(self):
        # self.canvas.itemconfig(self.listObj[-1], fill="white", outline="white")
        if len(self.filepath) != 0:         
            if len(self.ObjCorte) != 0:    
                xbegin, ybegin, xend, yend = map(int, self.canvas.coords(self.ObjCorte[-1]))
                self.canvas.delete(self.ObjCorte[-1])
                self.ObjCorte.pop()
                self.cv_img = self.cv_img[ybegin:yend, xbegin:xend]
                self.ListaAlteracoesFeitas.append(self.cv_img.copy())
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
                try:
                    self.Im_height, self.Im_width, self.canais = self.cv_img.shape
                except:
                    self.Im_height, self.Im_width = self.cv_img.shape
                self.canvas.config(width = self.Im_width, height = self.Im_height)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        else:
            messagebox.showerror("Error", "Não tem imagem a ser cortada")
    

# FERRAMENTAS DE CORREÇÃO DE CORES
    # Histograma
    def onHistogramaEq(self):
        if (len(self.filepath) != 0) and (len(self.cv_img.shape) == 3): 
            iB, iG, iR = cv2.split(self.ListaAlteracoesFeitas[-1])
            bEq = cv2.equalizeHist(iB)
            gEq = cv2.equalizeHist(iG)
            rEq = cv2.equalizeHist(iR)
            self.cv_img = cv2.merge((bEq, gEq, rEq))
            self.onSalvarAlterações()
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Saturação
    def onSaturacao(self):
        if (len(self.filepath) != 0) and (len(self.cv_img.shape) == 3): 
            img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2HSV)
            valor = 50
            # valor = 100
            for j in range(img.shape[1]):
                for k in range(img.shape[0]):
                    if img[k,j,1] + valor > 255:
                        img[k,j,1] = 255
                    else:
                        img[k,j,1] = img[k,j,1] + valor
            img[:,:,1] = cv2.equalizeHist(img[:,:,1])
            self.cv_img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
            self.onSalvarAlterações()
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # Colorização por indice de cores
    # Feito por Beatriz Precebes <be.precebes@gmail.com>
    def onFecharNewWindowColring(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinCorloring.destroy()

    def paletteInit(self):
        r1 = self.tkScaleR1.get()
        g1 = self.tkScaleG1.get()
        b1 = self.tkScaleB1.get()
        r2 = self.tkScaleR2.get()
        g2 = self.tkScaleG2.get()
        b2 = self.tkScaleB2.get()

        b = np.linspace(b1, b2, 256)
        g = np.linspace(g1, g2, 256)
        r = np.linspace(r1, r2, 256)
        
        p1 = np.tile( b.reshape(256,1), 256 )
        p2 = np.tile( g.reshape(256,1), 256 )
        p3 = np.tile( r.reshape(256,1), 256 )
        
        p1 = np.uint8(p1)
        p2 = np.uint8(p2)
        p3 = np.uint8(p3)
            
        return np.dstack( (np.dstack( (p1,p2) ), p3) )
                
    def onAplicarColoring(self):
        palette = self.paletteInit()
        out = np.zeros( (self.Im_height, self.Im_width, 3) )
        if (len(self.ListaAlteracoesFeitas[-1].shape) == 3):
                self.cv_img = cv2.cvtColor(self.ListaAlteracoesFeitas[-1], cv2.COLOR_RGB2GRAY)
                
        for i in range(self.Im_height):
            for j in range(self.Im_width):
                out[i][j] = palette [ self.cv_img[i][j] ][0]

        self.cv_img = np.uint8(out)
        
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
    
    def onColorizar(self):
        if len(self.filepath) != 0:         
                self.newwinCorloring = Toplevel(self.master)
                # self.newwinCorloring.geometry('280x120')
                instrucoes = Label(self.newwinCorloring, text="Selecione os valores iniciais e finais de RGB para gerar a paleta de cores.")
                Ri = Label(self.newwinCorloring, text="R inicial")
                Gi = Label(self.newwinCorloring, text="G inicial")
                Bi = Label(self.newwinCorloring, text="B inicial")
                Rf = Label(self.newwinCorloring, text="R final")    
                Gf = Label(self.newwinCorloring, text="G final")    
                Bf = Label(self.newwinCorloring, text="B final")    
                self.tkScaleR1 = tkinter.Scale(self.newwinCorloring, from_=0, to=255, orient=tkinter.HORIZONTAL, length=400)
                self.tkScaleG1 = tkinter.Scale(self.newwinCorloring, from_=0, to=255, orient=tkinter.HORIZONTAL, length=400)
                self.tkScaleB1 = tkinter.Scale(self.newwinCorloring, from_=0, to=255, orient=tkinter.HORIZONTAL, length=400)
                self.tkScaleR2 = tkinter.Scale(self.newwinCorloring, from_=0, to=255, orient=tkinter.HORIZONTAL, length=400)
                self.tkScaleG2 = tkinter.Scale(self.newwinCorloring, from_=0, to=255, orient=tkinter.HORIZONTAL, length=400)
                self.tkScaleB2 = tkinter.Scale(self.newwinCorloring, from_=0, to=255, orient=tkinter.HORIZONTAL, length=400)
                aplicar = Button(self.newwinCorloring, text="Aplicar", command=self.onAplicarColoring)
                salvar = Button(self.newwinCorloring, text="Salvar", command=self.onSalvarAlterações)
                fechar = Button(self.newwinCorloring, text="Fechar", command=self.onFecharNewWindowColring)

                instrucoes.pack()    
                Ri.pack()
                self.tkScaleR1.pack()
                Gi.pack()
                self.tkScaleG1.pack()
                Bi.pack()
                self.tkScaleB1.pack()
                Rf.pack()
                self.tkScaleR2.pack()
                Gf.pack()
                self.tkScaleG2.pack()
                Bf.pack()
                self.tkScaleB2.pack()
                aplicar.pack()
                salvar.pack()
                fechar.pack()

    # Balanço de branco
    # Feito por Beatriz Precebes <be.precebes@gmail.com>
    def apply_mask(self, matrix, mask, fill_value):
        masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
        return masked.filled()

    def apply_threshold(self, matrix, low_value, high_value):
        low_mask = matrix < low_value
        matrix = self.apply_mask(matrix, low_mask, low_value)

        high_mask = matrix > high_value
        matrix = self.apply_mask(matrix, high_mask, high_value)

        return matrix

    def white_balance(self):
        img = self.ListaAlteracoesFeitas[-1].copy()
        assert img.shape[2] == 3
        # assert percent > 0 and percent < 100
        percent = 1

        half_percent = percent / 200.0

        canais = cv2.split(img)

        canais_out = []
        for channel in canais:
            assert len(channel.shape) == 2
            
            # Percentuais baixo e altos com base no percentual de entrada
            h, w = channel.shape
            vec_size = w * h
            flat = channel.reshape(vec_size)

            assert len(flat.shape) == 1

            flat = np.sort(flat)

            n_cols = flat.shape[0]

            low_val  = flat[math.floor(n_cols * half_percent)]
            high_val = flat[math.ceil( n_cols * (1.0 - half_percent))]

            #print("Lowval: ", low_val)
            #print("Highval: ", high_val)
            
            thresholded = self.apply_threshold(channel, low_val, high_val)
            normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
            canais_out.append(normalized)

            self.cv_img = cv2.merge(canais_out)
            self.onSalvarAlterações()
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        

# FERRAMENTAS DE REALCE
    # FFT
    def onFFT(self):
        if len(self.filepath) != 0: 
            gray = cv2.cvtColor(self.cv_img,cv2.COLOR_BGR2GRAY)
            f = np.fft.fft2(gray)
            self.fshift = np.fft.fftshift(f)
            magnitude_spectrum = 20*np.log(np.abs(self.fshift))
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(magnitude_spectrum))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            self.TemFFT = 1

    # IFFT
    def onIFFT(self):
        if self.TemFFT: 
            f_ishift = np.fft.ifftshift(self.fshift)
            img_back = np.fft.ifft2(f_ishift)
            img_back = np.abs(img_back)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(img_back))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            self.TemFFT = 0


    # REALCE USANDO FILTRO DA MÉDIA
    def onFecharNewWindowRealceM(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinRM.destroy()


    def onAplicarRealceMedia(self):
        self.cv_img = cv2.add(self.ListaAlteracoesFeitas[-1], self.customBordas)
        self.onSalvarAlterações()
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onMediaRealce(self, event):
        self.VarFiltroMedia =  self.tkScaleVM.get()
        avg_blur = cv2.blur(self.ListaAlteracoesFeitas[-1],(self.VarFiltroMedia,self.VarFiltroMedia))
        self.customBordas = cv2.subtract(self.ListaAlteracoesFeitas[-1], avg_blur)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.customBordas))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def filterRealceMedia(self):
        if len(self.filepath) != 0: 
            self.newwinRM = Toplevel(self.master)

            lInst = Label(self.newwinRM, text="Escolha o tamanho do filtro da média")
            self.tkScaleVM = tkinter.Scale(self.newwinRM, from_=1, to=20, orient=tkinter.HORIZONTAL, length=200, command=self.onMediaRealce)
            bAplica = Button(self.newwinRM, text="Aplicar Realce das bordas", command=self.onAplicarRealceMedia)
            fechar = Button(self.newwinRM, text="Fechar", command=self.onFecharNewWindowRealceM)
            
            lInst.pack()
            self.tkScaleVM.pack()
            bAplica.pack()
            fechar.pack()
    

    # APLICAR O FILTRO DA GAUSSIANA (BORRAR)
    def onFecharNewWindowGauss(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinG.destroy()

    def onAplicar(self):
        self.cv_img = self.custom
        self.onSalvarAlterações()
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onGaussiana(self, event):
        self.VarFiltroMedia = self.tkScaleG.get()
        if self.VarFiltroMedia % 2 == 1:
            self.custom = cv2.GaussianBlur(self.ListaAlteracoesFeitas[-1],(self.VarFiltroMedia,self.VarFiltroMedia),1)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.custom))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def filterGauss(self):
        if len(self.filepath) != 0: 
            self.newwinG = Toplevel(self.master)

            lInst = Label(self.newwinG, text="Escolha o tamanho do filtro")
            self.tkScaleG = tkinter.Scale(self.newwinG, from_=1, to=10, orient=tkinter.HORIZONTAL, length=200, command=self.onGaussiana)
            bAplica = Button(self.newwinG, text="Aplicar filtro", command=self.onAplicar) 
            fechar = Button(self.newwinG, text="Fechar", command=self.onFecharNewWindowGauss)
                        
            lInst.pack()
            self.tkScaleG.pack()
            bAplica.pack()
            fechar.pack()


# EXTRA QUANTIFICACAO DE COR
    def onFecharNewWindowQuant(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwinQ.destroy()

    def SalvarQuantizacao(self):
        self.cv_img = self.imgQ
        self.onSalvarAlterações()
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onQuant(self):
        self.VarCor = self.tkScaleCor.get()
        im_pil = Image.fromarray(self.ListaAlteracoesFeitas[-1])
        result = im_pil.convert('P', palette=Image.ADAPTIVE, colors=self.VarCor)
        pil_image = result.convert('RGB') 
        self.imgQ = np.array(pil_image)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.imgQ))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onQuantizar(self):
        if len(self.filepath) != 0: 
            self.newwinQ = Toplevel(self.master)

            lCor = Label(self.newwinQ, text="Escolha quantidade de cores")
            self.tkScaleCor = tkinter.Scale(self.newwinQ, from_=2, to=255, orient=tkinter.HORIZONTAL, length=400)
            bAplica = Button(self.newwinQ, text="Aplicar", command=self.onQuant)
            bSalva = Button(self.newwinQ, text="Salvar", command=self.SalvarQuantizacao)
            fechar = Button(self.newwinQ, text="Fechar", command=self.onFecharNewWindowQuant)
            
            lCor.pack()
            self.tkScaleCor.pack()
            bAplica.pack()
            bSalva.pack()
            fechar.pack()



def main():
    root = Tk()
    ex = Example()
    root.mainloop()


if __name__ == '__main__':
    main()