import customtkinter
import time
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
        
        #Definindo o modo de aparência e o tamanho da imagem
        image_login = customtkinter.CTkImage(light_image = Image.open("View\images\img-login.png"),
                                             dark_image= Image.open("View\images\img-login.png"),
                                             size=(400, 400))
        
        #Adicionando os elementos na tela
        label_img = customtkinter.CTkLabel(self.root, image=image_login, text="")
        label_img.grid(row=0, column=0, padx=50, pady=100, sticky='n')
                                                  
        label_title = customtkinter.CTkLabel(self.root, text="Bem-vindo ao Sistema", font=customtkinter.CTkFont(size=30, weight="bold"))
        label_title.grid(row=0, column=1, padx=0, pady=180, sticky = 'n')

        label_subtitle = customtkinter.CTkLabel(self.root, text="Por favor, faça o login para continuar", font=customtkinter.CTkFont(size=16))
        label_subtitle.grid(row=0, column=1, padx=0, pady=230, sticky='n')

        self.label_username = customtkinter.CTkEntry(self.root, placeholder_text="Nome de Usuário", width=250, height=40, border_width=2, corner_radius=10)
        self.label_username.grid(row=0, column=1, padx=0, pady=280, stick='n')

        self.label_password = customtkinter.CTkEntry(self.root, placeholder_text="Digite sua senha", width=250, height=40, border_width=2, corner_radius=10, show="*")
        self.label_password.grid(row=0, column=1, padx=0, pady=330, stick='n')

        button_login = customtkinter.CTkButton(self.root, text="LOGIN", fg_color="#0844f4" ,width=100, height=40, corner_radius=10, command=self.verificar_login)
        button_login.grid(row=0, column=1, padx=0, pady=390, stick='n')

        self.label_status = customtkinter.CTkLabel(self.root, text="")
        self.label_status.grid(row=0, column=1, pady=430, sticky="n")

    #Função de verificação de login
    def verificar_login(self):
        """Verifica as credenciais ao clicar no botão"""
        usuario = self.label_username.get()
        senha = self.label_password.get()

        # Limpa mensagem anterior
        self.label_status.configure(text="")

        # Verifica se os dados estão corretos
        if usuario == "admin" and senha == "1234":
            self.label_status.configure(
                text="✅ Login bem-sucedido!",
                text_color="green"
            )
        else:
            self.label_status.configure(
                text="❌ Nome de usuário ou senha incorretos.",
                text_color="red"
            )

        

Aplication()