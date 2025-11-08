import customtkinter
from customtkinter import *
from PIL import Image

root = CTk()

'Declarando Variáveis'

img_login = "/view/imagens/login.png"

class Aplication():
    def __init__(self):
        self.root = root
        self.tela_login()
        root.mainloop()

    def tela_login(self):
        self.root.geometry("900x600")
        self.root.resizable(False, False)
        self.root.title("Login")
        
        
        
        image_login = customtkinter.CTkImage(light_image = Image.open("TrabalhoFinal\View\images\img-login.png"),
                                             dark_image= Image.open("TrabalhoFinal\View\images\img-login.png"),
                                             size=(400, 400))
        
        label_img = customtkinter.CTkLabel(self.root, image=image_login, text="")
        label_img.grid(row=0, column=0, padx=50, pady=100, sticky='n')
                                                  
        label_title = customtkinter.CTkLabel(self.root, text="Bem-vindo ao Sistema", font=customtkinter.CTkFont(size=30, weight="bold"))
        label_title.grid(row=0, column=1, padx=0, pady=180, sticky = 'n')

        label_subtitle = customtkinter.CTkLabel(self.root, text="Por favor, faça o login para continuar", font=customtkinter.CTkFont(size=16))
        label_subtitle.grid(row=0, column=1, padx=0, pady=230, sticky='n')

        label_username = customtkinter.CTkEntry(self.root, placeholder_text="Nome de Usuário", width=250, height=40, border_width=2, corner_radius=10)
        label_username.grid(row=0, column=1, padx=0, pady=280, stick='n')

        label_password = customtkinter.CTkEntry(self.root, placeholder_text="Digite sua senha", width=250, height=40, border_width=2, corner_radius=10)
        label_password.grid(row=0, column=1, padx=0, pady=330, stick='n')

        button_login = customtkinter.CTkButton(self.root, text="Login", width=100, height=40, corner_radius=10)
        button_login.grid(row=0, column=1, padx=0, pady=390, stick='n')
        

        

Aplication()