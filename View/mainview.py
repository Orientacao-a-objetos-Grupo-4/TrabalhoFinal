import customtkinter
from customtkinter import *
import tkinter as tk
from PIL import Image

root = CTk()

class Aplication():
    def __init__(self):
        super().__init__()
        self.root = root
        #self.tela_login()
        self.janela_nova()
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
                text_color="green")
            self.root.after(1000, self.janela_nova)
        else:
            self.label_status.configure(
                text="❌ Nome de usuário ou senha incorretos.",
                text_color="red"
            )
            
    def janela_nova(self):
    # Fecha completamente a janela de login
        self.root.destroy()

        # Nova janela principal
        nova_janela = CTk()
        nova_janela.geometry("400x600")
        nova_janela.title("Sistema de Biblioteca")

        menu_bar_color = '#2b2b2b'

        # Ícones (mantidos como PhotoImage padrão, CTk também aceita)
        toggle_icon = customtkinter.CTkImage(Image.open("View/images/toggle_btn_icon.png"), size=(25, 25))
        home_icon = customtkinter.CTkImage(Image.open("View/images/home_icon.png"), size=(20, 20))
        livro_icon = customtkinter.CTkImage(Image.open("View/images/livro_btn3.png"), size=(20, 20))
        contact_icon = customtkinter.CTkImage(Image.open("View/images/contact_icon.png"), size=(20, 20))
        about_icon = customtkinter.CTkImage(Image.open("View/images/about_icon.png"), size=(20, 20))

        # Se quiser realmente carregar imagens:
        # toggle_icon = CTkImage(Image.open("View/images/toggle_btn_icon.png"), size=(25,25))
        # home_icon = CTkImage(Image.open("View/images/home_icon.png"), size=(25,25))
        # ...

        def switch_indication(indicator_lb):
            home_btn_indicator.configure(fg_color=menu_bar_color)
            livro_btn_indicator.configure(fg_color=menu_bar_color)
            about_btn_indicator.configure(fg_color=menu_bar_color)
            indicator_lb.configure(fg_color='white')

        # Menu lateral
        menu_bar_frame = CTkFrame(nova_janela, fg_color=menu_bar_color, corner_radius=0)
        menu_bar_frame.pack(side='left', fill='y', pady=4, padx=3)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=55)

        # Botão de alternar menu
        toggle_menu_btn = CTkButton(menu_bar_frame, image=toggle_icon, text='',
                                    fg_color=menu_bar_color, hover_color=menu_bar_color,
                                    width=30, height=40)
        toggle_menu_btn.place(x=4, y=10)

        # Botão Home
        home_btn = CTkButton(menu_bar_frame, image=home_icon, text='',
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            width=30, height=35,
                            command=lambda: switch_indication(home_btn_indicator))
        home_btn.place(x=9, y=128)

        home_btn_indicator = CTkLabel(menu_bar_frame, text='', fg_color='white', width=3)
        home_btn_indicator.place(x=3, y=130)

        # Botão Livros
        livro_btn = CTkButton(menu_bar_frame, image=livro_icon, text='',
                                fg_color=menu_bar_color, hover_color=menu_bar_color,
                                width=30, height=35,
                                command=lambda: switch_indication(livro_btn_indicator))
        livro_btn.place(x=9, y=190)

        livro_btn_indicator = CTkLabel(menu_bar_frame, text='', fg_color=menu_bar_color, width=3)
        livro_btn_indicator.place(x=3, y=190)

        # Botão About
        about_btn = CTkButton(menu_bar_frame, image=about_icon, text='',
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            width=30, height=35,
                            command=lambda: switch_indication(about_btn_indicator))
        about_btn.place(x=9, y=250)

        about_btn_indicator = CTkLabel(menu_bar_frame, text='', fg_color=menu_bar_color, width=3)
        about_btn_indicator.place(x=3, y=250)

        nova_janela.mainloop()

Aplication()