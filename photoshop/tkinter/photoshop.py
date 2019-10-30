from tkinter import Tk, BOTH, Frame, Menu, Button, filedialog, Label, messagebox, colorchooser
from tkinter import LEFT, TOP, X, FLAT, RAISED, W
import tkinter

# from tkinter.ttk import Frame
from PIL import Image, ImageTk
import cv2


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
        self.filepath = ""
        self.rgb = 1
        self.initMenu()      

        self.canvas = tkinter.Canvas(self.master, width = self.width, height = self.height)
        self.canvas.pack()
        self.pack()


    def initMenu(self):
        self.menubar = Menu(self.master)

        # Criar menus
        self.fileMenu = Menu(self.master, tearoff=0)
        self.visualizarMenu = Menu(self.master, tearoff=0)
        self.ferramentaMenu = Menu(self.master, tearoff=0)    

        # Adicionar comando
        self.fileMenu.add_command(label="Abrir Imagem", command=self.onOpen)
        self.fileMenu.add_command(label="Informações", command=self.onInfo)
        self.fileMenu.add_command(label="Sair", command=self.onExit)
        
        self.visualizarMenu.add_command(label="RGB", command=self.onRGB)
        self.visualizarMenu.add_command(label="HSV", command=self.onHSV)

        # self.ferramentaMenu.add_command(label="Selecionar cor", command=self.onColor)
        
        # Mostrar os menus
        self.menubar.add_cascade(label="Arquivo", menu=self.fileMenu)
        self.menubar.add_cascade(label="Visualizar", menu=self.visualizarMenu)
        self.menubar.add_cascade(label= "Ferramentas", menu = self.ferramentaMenu)
        self.master.config(menu=self.menubar)

        
    def onExit(self): self.quit()

    def onOpen(self):
        self.filepath = filedialog.askopenfilename(filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("bmp files", "*.bmp")))

        if len(self.filepath) != 0:            
            self.cv_img = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_BGR2RGB)
            # self.height, self.width, self.no_channels = self.cv_img.shape

            self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            # self.canvas.bind(('<Configure>' self._resize_image))
            
            

    # def _resize_image(self,event):
    #     new_width = event.width
    #     new_height = event.height

    #     image = self.cv_img.resize((new_width, new_height))
    #     self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(image))
    #     self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

    def onInfo(self):
        if(len(self.filepath) == 0):
            messagebox.showerror("Erro", "Não tem imagem a ser informada.")
        else:
            strFormato = "Formato : " + self.filepath[-4: ] + "\n"
            for i in range(len(self.filepath)-1, -1, -1):
                    if(self.filepath[i] == '/'):
                        break        
            strNome = "Nome : " + self.filepath[i+1 : ] + "\n"
            messagebox.showinfo("Informações", strNome+strFormato)
            # escrever na imagem
            # self.canvas.create_text(20, 30, anchor=W, font="Purisa", text=strNome+strFormato)

    def onRGB(self):
        if len(self.filepath) != 0:
            if self.rgb == 0:
                img_RGB = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_HSV2BGR)
                img_RGB = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(img_RGB))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
                self.rgb = 1
    
    def onHSV(self):
        if len(self.filepath) != 0:
            if self.rgb == 1:               
                img_HSV = cv2.cvtColor(cv2.imread(self.filepath), cv2.COLOR_RGB2HSV)
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(img_HSV))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
                self.rgb = 0

    # def onColor(self):




def main():
    root = Tk()
    ex = Example()
    root.mainloop()


if __name__ == '__main__':
    main()