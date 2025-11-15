import customtkinter
from customtkinter import *
from tkinter import messagebox
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
        image_login = customtkinter.CTkImage(light_image = Image.open("View/images/img-login.png"),
                                             dark_image= Image.open("View/images/img-login.png"),
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

        nova_janela = CTk()
        nova_janela.geometry("900x600")
        nova_janela.resizable(False, False)
        nova_janela.title("Sistema de Biblioteca")

        menu_bar_color = '#2b2b2b'

        # Ícones
        toggle_icon = customtkinter.CTkImage(Image.open("View/images/toggle_btn_icon.png"))
        home_icon = customtkinter.CTkImage(Image.open("View/images/home_icon.png"), size=(22, 22))
        livro_icon = customtkinter.CTkImage(Image.open("View/images/livro_btn3.png"), size=(25, 25))
        multas_icon = customtkinter.CTkImage(Image.open("View/images/multas_btn.png"), size=(25, 25))
        about_icon = customtkinter.CTkImage(Image.open("View/images/about_icon.png"), size=(22, 22))
        close_btn_icon = customtkinter.CTkImage(Image.open("View/images/close_btn_icon.png"), size=(22, 22))

        # Indicadores de botões
        def switch_indication(indicator_lb, page):
            home_btn_indicator.configure(fg_color=menu_bar_color)
            livro_btn_indicator.configure(fg_color=menu_bar_color)
            multas_btn_indicator.configure(fg_color=menu_bar_color)
            about_btn_indicator.configure(fg_color=menu_bar_color)

            indicator_lb.configure(fg_color='white')

            #if menu_bar_frame.winfo_width() > 45:
                #fold_menu_bar()

            for frame in page_frame.winfo_children():
                frame.destroy()

            page()

        # Animação de extensão do menu
        def extending_animation():
            current_width = menu_bar_frame.winfo_width()
            if not current_width < 200:
                current_width += 10
                menu_bar_frame.configure(width=current_width)
                nova_janela.after(ms=8, func=extending_animation)

        def extend_menu_bar():
            extending_animation()
            toggle_menu_btn.configure(image=close_btn_icon, command=fold_menu_bar)

        # Animação de recolhimento do menu
        def folding_animation():
            current_width = menu_bar_frame.winfo_width()
            if current_width != 45:
                current_width -= 10
                menu_bar_frame.configure(width=current_width)
                nova_janela.after(ms=8, func=folding_animation)

        def fold_menu_bar():
            folding_animation()
            toggle_menu_btn.configure(image=toggle_icon, command=extend_menu_bar)

        # Páginas
        def home_page():
            home_page_fm = CTkFrame(page_frame)
            lb = CTkLabel(home_page_fm,text=f"Bem-vindo ao Home Page!", font=("Bold", 20))
            lb.place(x=10, y=10)

            

            home_page_fm.pack(fill="both", expand=True)

        def livros_page():  
            def add_livro():
                    if vid.get() == "":
                        messagebox.showwarning("Entrada Inválida", "Por favor, insira um valor válido.")
                        return
                    tv.insert(parent='', index='end', iid=vid.get(), text='',
                              values=(vid.get(), "Game of Thrones", "Fantasia", "Suma de Letras", "George R. R.", "10"))
                    vid.delete(0, 'end')
                    vid.focus()   
                        
            def delete_livro():
                pass
            def buscar_livro():
                pass   

            livros_page_fm = CTkFrame(page_frame)
            lb = CTkLabel(livros_page_fm, text="Bem-vindo 'Nome do Usuário' - 'Cargo' ", font=("Bold", 20))
            lb.place(x=10, y=10)
            livros_page_fm.pack(fill="both", expand=True)

            vid = CTkEntry(livros_page_fm, placeholder_text="Digite algo...", width=200)
            vid.place(x=10, y=50)
            
            btn_adcionar = CTkButton(livros_page_fm, text="Add Livros", width=100)
            btn_adcionar.place(x=250, y=50)

            btn_remover = CTkButton(livros_page_fm, text="Remover Livros", width=120)
            btn_remover.place(x=380, y=50) 

            btn_buscar = CTkButton(livros_page_fm, text="Buscar Livros", width=120)
            btn_buscar.place(x=600, y=50)

            tv = tk.ttk.Treeview(livros_page_fm)
            tv.place(x=100, y=130, width=860, height=400)
            tv.column("#0", width=0, stretch="no")
            tv['columns'] = ("ID", "Título", "Gênero", "Editora", "Autor", "Exemplares" )
            tv.column("ID", anchor="center", width=50)
            tv.column("Título", anchor="w", width=200)
            tv.column("Gênero", anchor="center", width=100)
            tv.column("Editora", anchor="w", width=150)
            tv.column("Autor", anchor="w", width=150)
            tv.column("Exemplares", anchor="center", width=100)

            tv.heading("ID", text="ID", anchor="center")
            tv.heading("Título", text="Título", anchor="center")
            tv.heading("Gênero", text="Gênero", anchor="center")
            tv.heading("Editora", text="Editora", anchor="center")
            tv.heading("Autor", text="Autor", anchor="center")
            tv.heading("Exemplares", text="Exemplares", anchor="center")

            btn_adcionar.configure(command=add_livro)
            btn_remover.configure(command=delete_livro)
            btn_buscar.configure(command=buscar_livro)

        def multas_page():
            multas_page_fm = CTkFrame(page_frame)
            lb = CTkLabel(multas_page_fm, text="Multas", font=("Bold", 20))
            lb.place(x=100, y=200)
            multas_page_fm.pack(fill="both", expand=True)

        def about_page():
        # Frame principal da página
            about_page_fm = CTkFrame(page_frame)
            about_page_fm.pack(fill="both", expand=True)

            # Frame central
            frame_sobre = customtkinter.CTkFrame(about_page_fm)
            frame_sobre.grid(row=0, column=0, sticky='nsew', pady=80)

            # Expandir corretamente
            about_page_fm.grid_rowconfigure(0, weight=1)
            about_page_fm.grid_columnconfigure(0, weight=1)

            frame_sobre.grid_columnconfigure(0, weight=1)
            frame_sobre.grid_columnconfigure(1, weight=0)
            frame_sobre.grid_columnconfigure(2, weight=1)

            # Imagens
            logo_img = customtkinter.CTkImage(
                light_image=Image.open("View/images/logo_about.png"),
                dark_image=Image.open("View/images/logo_about.png"),
                size=(170, 170)
            )
            icon_sarch = customtkinter.CTkImage(
                light_image=Image.open("View/images/icon_sarch.png"),
                dark_image=Image.open("View/images/icon_sarch.png"),
                size=(20, 20)
            )
            icon_shield = customtkinter.CTkImage(
                light_image=Image.open("View/images/icon_shield.png"),
                dark_image=Image.open("View/images/icon_shield.png"),
                size=(20, 20)
            )
            icon_user = customtkinter.CTkImage(
                light_image=Image.open("View/images/icon_user.png"),
                dark_image=Image.open("View/images/icon_user.png"),
                size=(20, 20)
            )

            # Logo
            label_logo = customtkinter.CTkLabel(frame_sobre, image=logo_img, text="")
            label_logo.grid(row=0, column=1, pady=(20, 0))

            # Título "Sobre Nós"
            label_title = customtkinter.CTkLabel(
                frame_sobre,
                text="Sobre Nós",
                font=customtkinter.CTkFont(size=30, weight="bold"),
                text_color="#012E58",
                bg_color="transparent"
            )
            label_title.grid(row=1, column=1)

            # Texto principal
            label_sobre_1 = customtkinter.CTkLabel(
                frame_sobre,
                text=(
                    "O NexoCode é uma solução tecnológica avançada desenvolvida "
                    "para enfrentar o desafio da gestão de acervos informacionais complexos. "
                    "Sua arquitetura foi concebida com o propósito fundamental de transformar "
                    "o caos de dados em conhecimento acessível e rastreável."
                ),
                width=650,
                wraplength=600,
                justify="left",
                bg_color="transparent"
            )
            label_sobre_1.grid(row=2, column=1, sticky='nw', pady=(10, 20))

            # Título secundário
            label_sobre_2 = customtkinter.CTkLabel(
                frame_sobre,
                text="Nossos Pilares",
                font=customtkinter.CTkFont(size=16, weight="bold"),
                bg_color="transparent"
            )
            label_sobre_2.grid(row=3, column=1, sticky='w', pady=(0, 10))

            # Frame dos pilares
            frame_sarch = customtkinter.CTkFrame(
                frame_sobre,
                bg_color="transparent",
                width=650
            )
            frame_sarch.grid(row=4, column=1, sticky="nw")

            # Config grid interno
            frame_sarch.grid_columnconfigure(0, weight=0)
            frame_sarch.grid_columnconfigure(1, weight=1)

            # Bloco "Busca"
            label_img_sarch = customtkinter.CTkLabel(frame_sarch, image=icon_sarch, text="")
            label_img_sarch.grid(row=0, column=0, sticky='nw')

            label_sobre_3 = customtkinter.CTkLabel(
                frame_sarch,
                bg_color="transparent",
                text="Otimização de Busca: Algoritmos otimizados garantem a recuperação de documentos em alta velocidade.",
                wraplength=550,
                justify="left"
            )
            label_sobre_3.grid(row=0, column=1, sticky='nw', padx=10, pady=5)

            # Bloco "Segurança"
            label_img_shield = customtkinter.CTkLabel(frame_sarch, image=icon_shield, text="")
            label_img_shield.grid(row=1, column=0, sticky='nw')

            label_sobre_4 = customtkinter.CTkLabel(
                frame_sarch,
                bg_color="transparent",
                text="Integridade e Segurança: Proteção e auditoria completa dos dados sensíveis.",
                wraplength=550,
                justify="left"
            )
            label_sobre_4.grid(row=1, column=1, sticky='nw', padx=10, pady=5)

            # Bloco "Usuário"
            label_img_user = customtkinter.CTkLabel(frame_sarch, image=icon_user, text="")
            label_img_user.grid(row=2, column=0, sticky='nw')

            label_sobre_5 = customtkinter.CTkLabel(
                frame_sarch,
                bg_color="transparent",
                text="Experiência do Usuário: Interface limpa, eficiente e fácil de usar.",
                wraplength=550,
                justify="left"
            )
            label_sobre_5.grid(row=2, column=1, sticky='nw', padx=10)


        # Área principal das páginas
        page_frame = CTkFrame(nova_janela)
        page_frame.place(relwidth=1.0, relheight=1.0, x=50)
        home_page()

        # Menu lateral
        menu_bar_frame = CTkFrame(nova_janela, fg_color=menu_bar_color)
        menu_bar_frame.pack(side="left", fill="y", pady=5, padx=2)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=45)

        # Botão do menu
        toggle_menu_btn = CTkButton(menu_bar_frame, image=toggle_icon, text="",
                                    fg_color=menu_bar_color, hover_color=menu_bar_color,
                                    command=extend_menu_bar, width=30, height=30)
        toggle_menu_btn.place(x=4, y=10)

        # Botão Home
        home_btn = CTkButton(menu_bar_frame, image=home_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(home_btn_indicator, home_page),
                            width=30, height=40)
        home_btn.place(x=9, y=130)

        home_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color='white', width=3, height=40)
        home_btn_indicator.place(x=3, y=130)

        home_page_lb = CTkLabel(menu_bar_frame, text="Home", fg_color=menu_bar_color,
                                text_color="white", font=("Bold", 15), anchor="w")
        home_page_lb.place(x=45, y=130)
        home_page_lb.bind("<Button-1>", lambda e: switch_indication(home_btn_indicator, home_page))

        # Botão Livros
        livro_btn = CTkButton(menu_bar_frame, image=livro_icon, text="",
                                fg_color=menu_bar_color, hover_color=menu_bar_color,
                                command=lambda: switch_indication(livro_btn_indicator, livros_page),
                                width=30)
        livro_btn.place(x=9, y=185)

        livro_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        livro_btn_indicator.place(x=3, y=185)

        livro_lb = CTkLabel(menu_bar_frame, text="Serviços", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        livro_lb.place(x=45, y=190)
        livro_lb.bind("<Button-1>", lambda e: switch_indication(livro_btn_indicator, livros_page))
        
        # Botão Multas
        multas_btn = CTkButton(menu_bar_frame, image=multas_icon, text="",
                                fg_color=menu_bar_color, hover_color=menu_bar_color,
                                command=lambda: switch_indication(multas_btn_indicator, multas_page),
                                width=30)
        multas_btn.place(x=9, y=250)

        multas_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        multas_btn_indicator.place(x=3, y=250)

        multas_lb = CTkLabel(menu_bar_frame, text="Multas", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        multas_lb.place(x=45, y=250)
        multas_lb.bind("<Button-1>", lambda e: switch_indication(multas_btn_indicator, multas_page))

        # Botão Sobre
        about_btn = CTkButton(menu_bar_frame, image=about_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(about_btn_indicator, about_page),
                            width=30, height=40)
        about_btn.place(x=9, y=310)
        
        about_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        about_btn_indicator.place(x=3, y=310)

        about_lb = CTkLabel(menu_bar_frame, text="Sobre", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        about_lb.place(x=45, y=310)
        about_lb.bind("<Button-1>", lambda e: switch_indication(about_btn_indicator, about_page))

        # posicionando o menu bar frame
        menu_bar_frame.pack(side="left", fill="y", pady=4, padx=3)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=45, fg_color=menu_bar_color)

        nova_janela.mainloop()

Aplication()