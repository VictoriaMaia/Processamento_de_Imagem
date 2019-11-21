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
import numpy as np

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
        self.desenhoMenu = Menu(self.master, tearoff=0)    
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

        self.desenhoMenu.add_command(label="Desenhar", command=self.onDesenhar)
        # self.desenhoMenu.add_command(label="Circulo", command=self.onDesenharCir) 
        # self.desenhoMenu.add_command(label="Quadrado", command=self.onDesenharQuadrado) 
        # self.desenhoMenu.add_command(label="Linha", command=self.onDesenharLinha) 
        # self.desenhoMenu.add_command(label="Linha Tracejada", command=self.onDesenharLinhaTrac) 
        
        self.corMenu.add_command(label="Contorno", command=self.onEscolherCor_Contorno)
        self.corMenu.add_command(label="Preenchimento", command=self.onEscolherCor_Preencher)
        self.corMenu.add_command(label="Contorno e Preenchimento", command=self.onPreen_Contor)
        self.corMenu.add_command(label="Default", command=self.onDefault)

        self.linhaMenu.add_command(label="Espessura", command=self.new_winEspessura)
        self.linhaMenu.add_command(label="Default", command=self.onDefaultLinha)

        self.segmentacaoMenu.add_command(label="Threshold", command=self.onbarThre)
        # self.segmentacaoMenu.add_command(label="Default", command=self.onDefaultRGBHSV)
        # self.segmentacaoMenu.add_command(label="Watershed", command=self.onWatershed)

        # self.selecaoAreasMenu.add_command(label="Retângulo", command=self.onSelectRetangulo)
        # self.selecaoAreasMenu.add_command(label="Cortar área", command=self.onCortarArea)
        ## Colocar para ver o histograma 
        # self.correcaoDeCoresMenu.add_command(label="Historgrama", command=self.onHistogramaEq)

        # # self.filtrosMenu.add_command(label="FFT", command=self.onFFT)
        # # self.filtrosMenu.add_command(label="IFFT", command=self.onHistogramaEq)
        # self.filtrosMenu.add_command(label="Realcar com Media", command=self.filterRealceMedia)
        # self.filtrosMenu.add_command(label="Aplicar Media", command=self.filterMedia)
        # self.filtrosMenu.add_command(label="Aplicar Gaussiana", command=self.filterGauss)
        # # self.filtrosMenu.add_command(label="Imagem Original", command=self.onVoltarOriginal)
        
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


        self.ferramentaMenu.add_cascade(label= "Desenho", menu = self.desenhoMenu)
        self.ferramentaMenu.add_cascade(label= "Cor", menu = self.corMenu)
        self.ferramentaMenu.add_cascade(label= "Linha", menu = self.linhaMenu)

        

        self.master.config(menu=self.menubar)

# FUNÇÕES DE BACKUP

    def onSalvarAlterações(self):
        self.ListaAlteracoesFeitas.append(self.cv_img.copy())

    def onDesfazer(self):
        if len(self.ListaAlteracoesFeitas) > 1:
            self.ListaAlteracoesFeitas.pop()
            self.cv_img = self.ListaAlteracoesFeitas[-1]
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
        if len(self.filepath) != 0:
            filepathSave = filedialog.asksaveasfilename(initialdir = self.filepath, filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("bmp files", "*.bmp")))
            time.sleep(.5)            
            box = (self.canvas.winfo_rootx(),self.canvas.winfo_rooty(),self.canvas.winfo_rootx()+self.Im_width, self.canvas.winfo_rooty()+self.Im_height)
            grab = ImageGrab.grab(bbox = box)
            grab.save(filepathSave)
        else:
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
        grab.save("new_img"+self.filepath[-4: ])
        self.cv_img = cv2.cvtColor(cv2.imread("new_img"+self.filepath[-4: ]), cv2.COLOR_BGR2RGB)    
        self.onSalvarAlterações()
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        os.remove("new_img"+self.filepath[-4: ])



# FUNÇÕES DE VISUALIZAR RGB

    # def onDefaultRGBHSV(self):
    #     self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[0]))
    #     self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

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
                    

    def onFecharNewWindow(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwin.destroy()

    def onRGB(self):
        try:
            a,b,c = self.ListaAlteracoesFeitas[-1].shape
            self.newwin = Toplevel(self.master)
            self.newwin.geometry('200x100')
            cR = Checkbutton(self.newwin, text="Canal R", variable=self.R, command=self.oncanaisRGB)
            cG = Checkbutton(self.newwin, text="Canal G", variable=self.G, command=self.oncanaisRGB)
            cB = Checkbutton(self.newwin, text="Canal B", variable=self.B, command=self.oncanaisRGB)
            salvar = Button(self.newwin, text="Salvar alterações", command=self.salvarRGB)
            fechar = Button(self.newwin, text="Fechar", command=self.onFecharNewWindow)

            cR.pack()
            cG.pack()
            cB.pack()
            salvar.pack()
            fechar.pack()
        except:
            messagebox.showerror("Error", "Imagem não tem 3 canais")
    

# FUNÇÕES DE VISUALIZAR HSV 

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

                self.newwin = Toplevel(self.master)
                self.newwin.geometry('200x100')
                cH = Radiobutton(self.newwin, text="Canal H", value=1, command=self.cHsv)
                cS = Radiobutton(self.newwin, text="Canal S", value=2, command=self.chSv)
                cV = Radiobutton(self.newwin, text="Canal V", value=3, command=self.chsV)
                salvar = Button(self.newwin, text="Salvar alterações", command=self.onSalvarAlterações)
                fechar = Button(self.newwin, text="Fechar", command=self.onFecharNewWindow)

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
            
    def salvarDesenho(self):
        self.desenhar = 0
        self.desenho = 0
        self.desenhoLinha = 0
        self.atualizarImg()
        self.newwin.destroy()

    def fecharSemSalvar(self):
        self.desenhar = 0
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.ListaAlteracoesFeitas[-1]))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.newwin.destroy()

    def onDesenhar(self):
        if len(self.filepath) != 0:
            self.newwin = Toplevel(self.master)
            self.newwin.geometry('200x200')
            D = Button(self.newwin, text="Desenhar", command=self.onconfigDesenhos)
            circulo = Radiobutton(self.newwin, text="Circulo", value=1, command=self.onDesenharCir)
            quadrado = Radiobutton(self.newwin, text="Quadrado", value=2, command=self.onDesenharQuadrado)
            linha = Radiobutton(self.newwin, text="Linha", value=3, command=self.onDesenharLinha)
            linhaTracejada = Radiobutton(self.newwin, text="Linha Tracejada", value=4, command=self.onDesenharLinhaTrac)
            S = Button(self.newwin, text="Sair e salvar desenho", command=self.salvarDesenho)
            Sair = Button(self.newwin, text="Sair sem salvar", command=self.fecharSemSalvar)
        
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
    
########################################################
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


# FERRAMENTAS DE SEGMENTAÇÃO
    ##### THRESOLD #####
    def onthresold(self, event):
        valor = self.tkScale.get()        
        img_gray = cv2.cvtColor(self.ListaAlteracoesFeitas[-1], cv2.COLOR_BGR2GRAY) 
        ret,self.cv_img = cv2.threshold(img_gray ,valor, 255, cv2.THRESH_BINARY)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onbarThre(self):
        if len(self.filepath) != 0: 
            self.newwin = Toplevel(self.master)
            self.newwin.geometry('280x120')
            display = Label(self.newwin, text="THRESOLD")
            self.tkScale = tkinter.Scale(self.newwin, from_=0, to=255, orient=tkinter.HORIZONTAL, length=200, command=self.onthresold)
            salvar = Button(self.newwin, text="Salvar alterações", command=self.onSalvarAlterações)
            fechar = Button(self.newwin, text="Fechar", command=self.onFecharNewWindow)
            
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

        
# FERRAMENTAS DE SELÇÃO DE ÁREAS
    # def avisoSelecao(self):
    #     messagebox.showinfo("Aviso", "Clique novamente para parar de selecionar retângulos.")

    def onSelectRetangulo(self):
        if self.desenhar == 0:
            # self.avisoSelecao()
            self.desenhar = 1
            self.desenho = 1
            self.action = self.canvas.create_rectangle
        else:
            self.desenhar = 0
            self.desenho = 0
    
    def onCortarArea(self):
        # self.canvas.itemconfig(self.listObj[-1], fill="white", outline="white")
        if len(self.filepath) != 0:             
            xbegin, ybegin, xend, yend = map(int, self.canvas.coords(self.listObj[-1]))
            self.canvas.delete(self.listObj[-1])
            # print(xbegin, ybegin, xend, yend)
            self.cv_img = self.cv_img[ybegin:yend, xbegin:xend]
            self.ListaAlteracoesFeitas.append(self.cv_img.copy())
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.Im_height, self.Im_width, self.canais = self.cv_img.shape
            # print(self.Im_height, self.Im_width)
            self.canvas.config(width = self.Im_width, height = self.Im_height)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        else:
            messagebox.showerror("Error", "Não tem imagem a ser cortada")
    

# FERRAMENTAS DE CORREÇÃO DE CORES
    def onHistogramaEq(self):
        iB, iG, iR = cv2.split(self.cv_img)
        bEq = cv2.equalizeHist(iB)
        gEq = cv2.equalizeHist(iG)
        rEq = cv2.equalizeHist(iR)
        img_equalizada = cv2.merge((bEq, gEq, rEq))
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(img_equalizada))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


# FERRAMENTAS DE REALCE
    # FFT
    # def onFFT(self):
    #     if len(self.filepath) != 0: 
    #         gray = cv2.cvtColor(self.cv_img,cv2.COLOR_BGR2GRAY)
    #         fftImg = np.fft.fft2(gray)
    #         fftImg = np.log(np.abs(fftImg)+1)
    #         fftImg = fftImg/(np.max(fftImg)*255)
    #         self.photo = ImageTk.PhotoImage(image = Image.fromarray(fftImg))
    #         self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    # IFFT

    # REALCE USANDO FILTRO DA MÉDIA
    def onAplicarRealceMedia(self):
        # avg_blur = cv2.blur(self.cv_img_default,(self.VarFiltroMedia,self.VarFiltroMedia))
        # customBordas = cv2.subtract(self.cv_img_default, avg_blur)
        self.cv_img = cv2.add(self.cv_img_default, self.customBordas)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onMediaRealce(self, event):
        self.VarFiltroMedia =  self.tkScaleVM.get()
        avg_blur = cv2.blur(self.cv_img_default,(self.VarFiltroMedia,self.VarFiltroMedia))
        self.customBordas = cv2.subtract(self.cv_img_default, avg_blur)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.customBordas))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


    def filterRealceMedia(self):
        if len(self.filepath) != 0: 
            newwin = Toplevel(self.master)

            lInst = Label(newwin, text="Escolha o tamanho do filtro da média")
            self.tkScaleVM = tkinter.Scale(newwin, from_=1, to=20, orient=tkinter.HORIZONTAL, length=200, command=self.onMediaRealce)
            bAplica = Button(newwin, text="Aplicar Realce das bordas", command=self.onAplicarRealceMedia)
            
            lInst.pack()
            self.tkScaleVM.pack()
            bAplica.pack()

    # APLICAR O FILTRO DA MÉDIA (BORRAR)
    def onMedia(self, event):
        self.VarFiltroMedia = self.tkScaleM.get()
        self.cv_img = cv2.blur(self.cv_img_default,(self.VarFiltroMedia,self.VarFiltroMedia))
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


    def filterMedia(self):
        if len(self.filepath) != 0: 
            newwin = Toplevel(self.master)

            lInst = Label(newwin, text="Escolha o tamanho do filtro da média")
            self.tkScaleM = tkinter.Scale(newwin, from_=1, to=10, orient=tkinter.HORIZONTAL, length=200, command=self.onMedia)            

            lInst.pack()
            self.tkScaleM.pack()

    # APLICAR O FILTRO DA GAUSSIANA (BORRAR)
    def onGaussiana(self, event):
        self.VarFiltroMedia = self.tkScaleG.get()
        if self.VarFiltroMedia % 2 == 1:
            self.cv_img = cv2.GaussianBlur(self.cv_img_default,(self.VarFiltroMedia,self.VarFiltroMedia),1)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


    def filterGauss(self):
        if len(self.filepath) != 0: 
            newwin = Toplevel(self.master)

            lInst = Label(newwin, text="Escolha o tamanho do filtro da média")
            self.tkScaleG = tkinter.Scale(newwin, from_=1, to=10, orient=tkinter.HORIZONTAL, length=200, command=self.onGaussiana)

            lInst.pack()
            self.tkScaleG.pack()




    # VOLTAR AO ORIGINAL
    # def onVoltarOriginal(self):
    #     self.cv_img = self.cv_img_default.copy()
    #     self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
    #     self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

            
    
    




def main():
    root = Tk()
    ex = Example()
    root.mainloop()


if __name__ == '__main__':
    main()