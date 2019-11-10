from tkinter import Tk, BOTH, Frame, Menu, Button, filedialog, Label, messagebox, colorchooser, Toplevel
from tkinter import Checkbutton, IntVar
from tkinter import LEFT, TOP, X, FLAT, RAISED, W
import tkinter

# from tkinter.ttk import Frame
from PIL import Image, ImageTk
import cv2
import pyscreenshot as ImageGrab 
import time

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
        self.master.geometry(self.str_tamanho_janela+'+200+100')
        
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
        # self.varButtonRGB = IntVar()
    
                
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
         

        # Adicionar comando
        self.fileMenu.add_command(label="Abrir Imagem", command=self.onOpen)
        self.fileMenu.add_command(label="Salvar Imagem", command=self.onSave)
        self.fileMenu.add_command(label="Informações", command=self.onInfo)
        self.fileMenu.add_command(label="Sair", command=self.onExit)
        
        self.visualizarMenu.add_command(label="RGB", command=self.onRGB)
        self.visualizarMenu.add_command(label="HSV", command=self.onHSV)
        self.visualizarMenu.add_command(label="Default", command=self.onDefaultRGBHSV)

        self.desenhoMenu.add_command(label="Desenhar", command=self.onDesenhar)
        self.desenhoMenu.add_command(label="Circulo", command=self.onDesenharCir) 
        self.desenhoMenu.add_command(label="Quadrado", command=self.onDesenharQuadrado) 
        self.desenhoMenu.add_command(label="Linha", command=self.onDesenharLinha) 
        
        self.corMenu.add_command(label="Contorno", command=self.onEscolherCor_Contorno)
        self.corMenu.add_command(label="Preenchimento", command=self.onEscolherCor_Preencher)
        self.corMenu.add_command(label="Contorno e Preenchimento", command=self.onPreen_Contor)
        self.corMenu.add_command(label="Default", command=self.onDefault)

        self.linhaMenu.add_command(label="Espessura", command=self.new_winEspessura)
        self.linhaMenu.add_command(label="Default", command=self.onDefaultLinha)

        # self.segmentacaoMenu.add_command(label="Threshold", command=self.onthresold)
                
        # Mostrar os menus
        self.menubar.add_cascade(label="Arquivo", menu=self.fileMenu)
        self.menubar.add_cascade(label="Visualizar", menu=self.visualizarMenu)
        self.menubar.add_cascade(label= "Ferramentas", menu = self.ferramentaMenu)
        self.menubar.add_cascade(label= "Segmentação", menu = self.segmentacaoMenu)

        self.ferramentaMenu.add_cascade(label= "Desenho", menu = self.desenhoMenu)
        self.ferramentaMenu.add_cascade(label= "Cor", menu = self.corMenu)
        self.ferramentaMenu.add_cascade(label= "Linha", menu = self.linhaMenu)

        
        self.master.config(menu=self.menubar)

        
    def onExit(self): self.quit()

    def onOpen(self):
        self.filepath = filedialog.askopenfilename(filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("bmp files", "*.bmp")))

        if len(self.filepath) != 0:            
            self.cv_img = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_BGR2RGB)
            self.Im_height, self.Im_width, self.canais = self.cv_img.shape
            # self.canvas = tkinter.Canvas(self.master, width = self.Im_width, height = self.Im_height)

            self.master.geometry(str(self.Im_width)+'x'+str(self.Im_height)+'+200+100')
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.config(width = self.Im_width, height = self.Im_height)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onSave(self):
            filepathSave = filedialog.asksaveasfilename(initialdir = self.filepath, filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("bmp files", "*.bmp")))
            time.sleep(.5)            
            box = (self.canvas.winfo_rootx(),self.canvas.winfo_rooty(),self.canvas.winfo_rootx()+self.Im_width, self.canvas.winfo_rooty()+self.Im_height)
            grab = ImageGrab.grab(bbox = box)
            grab.save(filepathSave)


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
        print(box)
        grab = ImageGrab.grab(bbox = box)
        grab.save("new_img.png")
        # grab.save("new_img"+self.filepath[-4: ])
        # self.canvas.postscript(file="new_img.ps", height=self.Im_height, width=self.Im_width)
        # img = Image.open("new_img.ps") 
        # img.save("new_img.png") 
        # self.cv_img = cv2.cvtColor(cv2.imread("new_img.png"), cv2.COLOR_BGR2RGB)    
        # # self.Im_height, self.Im_width, self.canais = self.cv_img.shape
        # self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        # self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        print("imagem atualizada")
            

# FUNÇÕES DE VISUALIZAR RGB
    def onDefaultRGBHSV(self):
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def oncanaisRGB(self):
        if len(self.filepath) != 0:
            imgCopy = self.cv_img.copy()
            if (self.R.get() and self.G.get() == 0 and self.B.get() == 0): #apenas canal vermelho
                imgCopy[:,:,1] = 0
                imgCopy[:,:,2] = 0                

            elif (self.G.get() and self.R.get() == 0 and self.B.get() == 0): #apenas canal verde
                imgCopy[:,:,0] = 0
                imgCopy[:,:,2] = 0  

            elif (self.B.get() and self.R.get() == 0 and self.G.get() == 0): #apenas canal azul
                imgCopy[:,:,0] = 0
                imgCopy[:,:,1] = 0  
            
            elif (self.B.get() and self. R.get() and self.G.get() == 0): #apenas canal azul e vermelho
                imgCopy[:,:,1] = 0 
            
            elif (self.B.get() and self.G.get() and self.R.get() == 0): #apenas canal azul e verde
                imgCopy[:,:,0] = 0 
            
            elif (self.R.get() and self.G.get() and self.B.get() == 0): #apenas canal vermelho e verde
                imgCopy[:,:,2] = 0 
                        
            elif (self.R.get() == 0 and self.G.get() == 0 and self.B.get() == 0): #apagou geral
                imgCopy[:,:,0] = 0
                imgCopy[:,:,1] = 0  
                imgCopy[:,:,2] = 0  
            
            elif (self.R.get() and self.G.get() and self.B.get()): #Tudo
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(imgCopy))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)    
                return
                
            
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(imgCopy))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


    def onRGB(self):
        newwin = Toplevel(self.master)
        newwin.geometry('200x100')
        cR = Checkbutton(newwin, text="Canal R", variable=self.R, command=self.cRGB)
        cG = Checkbutton(newwin, text="Canal G", variable=self.G, command=self.cRGB)
        cB = Checkbutton(newwin, text="Canal B", variable=self.B, command=self.cRGB)
        cR.pack()
        cG.pack()
        cB.pack()
    
    def cRGB(self):
        self.oncanaisRGB()

# FUNÇÕES DE VISUALIZAR HSV
    def oncanaisHSV(self):
        if len(self.filepath) != 0:
            imgCopy = self.cv_img.copy()
            imgCopy = cv2.cvtColor(imgCopy, cv2.COLOR_RGB2HSV)

            if (self.H.get() and self.S.get() == 0 and self.V.get() == 0): #apenas canal vermelho
                imgCopy[:,:,1] = 0
                imgCopy[:,:,2] = 0                

            elif (self.S.get() and self.H.get() == 0 and self.V.get() == 0): #apenas canal verde
                imgCopy[:,:,0] = 0
                imgCopy[:,:,2] = 0  

            elif (self.V.get() and self.H.get() == 0 and self.S.get() == 0): #apenas canal azul
                imgCopy[:,:,0] = 0
                imgCopy[:,:,1] = 0  
            
            elif (self.V.get() and self. R.get() and self.S.get() == 0): #apenas canal azul e vermelho
                imgCopy[:,:,1] = 0 
            
            elif (self.V.get() and self.S.get() and self.H.get() == 0): #apenas canal azul e verde
                imgCopy[:,:,0] = 0 
            
            elif (self.H.get() and self.S.get() and self.V.get() == 0): #apenas canal vermelho e verde
                imgCopy[:,:,2] = 0 
                        
            elif (self.H.get() == 0 and self.S.get() == 0 and self.V.get() == 0): #apagou geral
                imgCopy[:,:,0] = 0
                imgCopy[:,:,1] = 0  
                imgCopy[:,:,2] = 0  
            
            elif (self.H.get() and self.S.get() and self.V.get()): #Tudo
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(imgCopy))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)    
                return
                
            
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(imgCopy))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)


    def onHSV(self):
        newwin = Toplevel(self.master)
        newwin.geometry('200x100')
        cH = Checkbutton(newwin, text="Canal H", variable=self.H, command=self.cHSV)
        cS = Checkbutton(newwin, text="Canal S", variable=self.S, command=self.cHSV)
        cV = Checkbutton(newwin, text="Canal V", variable=self.V, command=self.cHSV)
        cH.pack()
        cS.pack()
        cV.pack()
    
    def cHSV(self):
        self.oncanaisHSV()

# FUNÇÕES DE DESENHO

    def onDesenhar(self):
        if self.desenhar == 0:
            self.desenhar = 1
        else:
            self.desenhar = 0
            self.desenho = 0
            self.desenhoLinha = 0
            if len(self.filepath) != 0:
                self.atualizarImg()
    
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
    
# PEGAR MOVIMENTOS DO MOUSE PARA DESENHO

    def onStart(self, event):
        if self.desenhar != 0: #desenhar circulo
            # print("ui")
            self.start = event
            self.drawn = None

    def onGrow(self, event):      
        if self.desenhar != 0: 
            self.canvas = event.widget
            if self.drawn: self.canvas.delete(self.drawn)
            if(self.desenho != 0):
                if(self.desenhoLinha == 1):
                    self.objectId = self.canvas.create_line(self.start.x, self.start.y, event.x, event.y, fill=self.outline, width=self.tamLinha)
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

    # def onthresold(self):



def main():
    root = Tk()
    ex = Example()
    root.mainloop()


if __name__ == '__main__':
    main()