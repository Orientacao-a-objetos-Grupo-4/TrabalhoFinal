import customtkinter
from customtkinter import *
from tkinter import messagebox
import tkinter as tk
from PIL import Image
from Controller.UsuarioController import UsuarioController
from Controller.LivroController import LivroController
from Controller.MultaController import MultaController
from Controller.EmprestimoLivroController import EmprestimoLivroController
from datetime import date
from Untils.Enums import StatusEmprestimo, StatusMulta
from Untils.Enums import TipoUsuario

root = CTk()
class Aplication():
    def __init__(self):
        super().__init__()
        self.root = root
        self.tela_login()
        root.mainloop()

    class ItemEmprestimo:
        def __init__(self, livro):
            self._livro = livro

        def getId(self):
            return self._livro.getId()

        def getLivro(self):
            return self._livro

    #Controllers
    userCtrl = UsuarioController()
    livroCtrl = LivroController()
    multasCtrl = MultaController(clienteController=userCtrl, emprestimoController=None)
    emprestimosCtrl = EmprestimoLivroController(clienteController=userCtrl, multaController=multasCtrl, livroController=livroCtrl)
    multasCtrl._MultaController__emprestimoController = emprestimosCtrl
    usuarioLogado = None

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
                                                  
        label_title = customtkinter.CTkLabel(self.root,
                                             text="Bem-vindo ao Sistema",
                                             font=customtkinter.CTkFont(size=30, weight="bold"))
        label_title.grid(row=0, column=1, padx=0, pady=180, sticky = 'n')

        label_subtitle = customtkinter.CTkLabel(self.root,
                                                text="Por favor, faça o login para continuar",
                                                font=customtkinter.CTkFont(size=16))
        label_subtitle.grid(row=0, column=1, padx=0, pady=230, sticky='n')

        self.label_username = customtkinter.CTkEntry(self.root,
                                                     placeholder_text="Nome de Usuário",
                                                     width=250, height=40, border_width=2,
                                                     corner_radius=10)
        self.label_username.grid(row=0, column=1, padx=0, pady=280, stick='n')

        self.label_password = customtkinter.CTkEntry(self.root,
                                                     placeholder_text="Digite sua senha",
                                                     width=250, height=40, border_width=2,
                                                     corner_radius=10, show="*")
        self.label_password.grid(row=0, column=1, padx=0, pady=330, stick='n')

        button_login = customtkinter.CTkButton(self.root, text="LOGIN",
                                               fg_color="#0844f4" ,width=100,
                                               height=40, corner_radius=10,
                                               command=self.verificar_login)
        button_login.grid(row=0, column=1, padx=0, pady=390, stick='n')
        self.root.bind('<Return>', lambda e: self.verificar_login())

        self.label_status = customtkinter.CTkLabel(self.root, text="")
        self.label_status.grid(row=0, column=1, pady=430, sticky="n")

    #Função de verificação de login
    def verificar_login(self):
        usuario_login = self.label_username.get()
        senha = self.label_password.get()

        # Limpa mensagem anterior
        self.label_status.configure(text="")

        # Autentica usuário
        usuario = self.userCtrl.autenticar_usuario(usuario_login, senha)

        if usuario:
            tipo = usuario.getTipo().name  

            # Mostra mensagem de sucesso
            self.label_status.configure(
                text="✅ Login bem-sucedido!",
                text_color="green"
            )

            # Abertura de tela de acordo com o tipo
            if tipo == "FUNCIONARIO" or tipo == "ADMINISTRADOR":
                self.root.after(500, lambda: self.janela_nova(usuario))

            elif tipo == "CLIENTE":
                self.root.after(500, lambda: self.tela_usuario(usuario))
        else:
            self.label_status.configure(
                text="❌ Nome de usuário ou senha incorretos.",
                text_color="red"
            )
    
    def realizar_logout(self, janela_atual):

        janela_atual.destroy()

        self.root = CTk()
        self.tela_login()
        self.root.mainloop()

    def tela_usuario(self, usuario):
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
        about_icon = customtkinter.CTkImage(Image.open("View/images/about_icon.png"), size=(22, 22))
        close_btn_icon = customtkinter.CTkImage(Image.open("View/images/close_btn_icon.png"), size=(22, 22))
        livro_icon = customtkinter.CTkImage(Image.open("View/images/book.png"), size=(22, 22))
        logout = customtkinter.CTkImage(Image.open("View/images/logout.png"), size=(22, 22))
        
        # Indicadores de botões
        def switch_indication(indicator_lb, page):
            home_btn_indicator.configure(fg_color=menu_bar_color)
            about_btn_indicator.configure(fg_color=menu_bar_color)
            emprestimos_btn_indicator.configure(fg_color=menu_bar_color)

            indicator_lb.configure(fg_color='white')

            if menu_bar_frame.winfo_width() >= 50:
                fold_menu_bar()

            for frame in page_frame.winfo_children():
                frame.destroy()

            page()

        # Animação de extensão do menu
        def extending_animation():
            current_width = menu_bar_frame.winfo_width()
            if not current_width >= 150:
                current_width += 100
                menu_bar_frame.configure(width=current_width)
                nova_janela.after(ms=1, func=extending_animation)

        def extend_menu_bar():
            extending_animation()
            toggle_menu_btn.configure(image=close_btn_icon, command=fold_menu_bar)

        # Animação de recolhimento do menu
        def folding_animation():
            current_width = menu_bar_frame.winfo_width()
            if current_width != 50:
                current_width -= 100
                menu_bar_frame.configure(width=current_width)
                nova_janela.after(ms=8, func=folding_animation)

        def fold_menu_bar():
            folding_animation()
            toggle_menu_btn.configure(image=toggle_icon, command=extend_menu_bar)

        def livros_page_cliente():

            def load_livros_cliente():
                 for item in tv_livro_cliente.get_children():
                        tv_livro_cliente.delete(item)
            # insere os livros
                 for livro in self.livroCtrl.getLivros():
                        tv_livro_cliente.insert("", "end", iid=livro.getId(), values=(
                            livro.getId(),
                            livro.getTitulo(),
                            livro.getGenero(),
                            livro.getEditora(),
                            livro.getAutor(),
                            livro.getNExemplares()
                            ))
                        
            livros_page_fm = CTkFrame(page_frame)  
            lb = CTkLabel(livros_page_fm,
                          text=f"Bem-vindo ao Sistema {usuario.getNomeUsuario()} - [{usuario.getTipo().name}]",
                          font=("Bold", 20))
            lb.place(x=45, y=40)

            livros_page_fm.pack(fill="both", expand=True)

            nome_livro = CTkEntry(livros_page_fm, placeholder_text="Digite o nome do livro", width=200)
            nome_livro.place(x=45, y=90)

            def buscar_livro_cliente():
                livro_desejado = nome_livro.get()
                if livro_desejado == "":
                    messagebox.showerror("Erro", "Por favor, insira o título do livro a ser buscado.")
                    return
                livro =self.livroCtrl.buscarPorTitulo(livro_desejado)
                if not livro:
                    messagebox.showerror("Erro", f"Livro com título '{livro_desejado}' não encontrado.")
                    return
                else:
                    tv_livro_cliente.selection_set(livro.getId())
                    tv_livro_cliente.see(livro.getId())
                    messagebox.showinfo("Sucesso", f"Livro '{livro_desejado}' encontrado e selecionado na tabela.")
                    nome_livro.delete(0, 'end')
                    nome_livro.focus()
            
            btn_buscar = CTkButton(livros_page_fm,
                                   text="Buscar Livros",
                                   width=130,
                                   fg_color = "#63C5A1",
                                   font=("Helvetica", 14, "bold"),
                                   text_color= "white")
            btn_buscar.place(x=320, y=90)
            btn_buscar.configure(command=buscar_livro_cliente)
            
            tv_livro_cliente = tk.ttk.Treeview(livros_page_fm)
            tv_livro_cliente.place(x=40, y=160, width=750, height=400)
            tv_livro_cliente.column("#0", width=0, stretch="no")
            tv_livro_cliente['columns'] = ("ID", "Título", "Gênero", "Editora", "Autor", "Exemplares")
            tv_livro_cliente.column("ID", anchor="center", width=50)
            tv_livro_cliente.column("Título", anchor="w", width=200)
            tv_livro_cliente.column("Gênero", anchor="w", width=100)
            tv_livro_cliente.column("Editora", anchor="w", width=150)
            tv_livro_cliente.column("Autor", anchor="w", width=150)
            tv_livro_cliente.column("Exemplares", anchor="center", width=100)

            tv_livro_cliente.heading("ID", text="ID", anchor="center")
            tv_livro_cliente.heading("Título", text="Título", anchor="center")
            tv_livro_cliente.heading("Gênero", text="Gênero", anchor="center")
            tv_livro_cliente.heading("Editora", text="Editora", anchor="center")
            tv_livro_cliente.heading("Autor", text="Autor", anchor="center")
            tv_livro_cliente.heading("Exemplares", text="Exemplares", anchor="center")

            tv_livro_cliente.scrollbar = tk.Scrollbar(livros_page_fm, orient="vertical", command=tv_livro_cliente.yview)
            tv_livro_cliente.scrollbar.place(x=790, y=160, height=400)
            tv_livro_cliente.configure(yscrollcommand=tv_livro_cliente.scrollbar.set)
            
            load_livros_cliente()

            titulo_multas = CTkLabel(page_frame, text="Livros Disponíveis", font=("Bold", 16), fg_color="#CFCFCF")
            titulo_multas.place(x=40, y=130)

        def emprestimos_page():

            emprestimos_page_fm = CTkFrame(page_frame)   
            lb = CTkLabel(emprestimos_page_fm,
                          text=f"Bem-vindo ao Sistema {usuario.getNomeUsuario()} - [{usuario.getTipo().name}]",
                          font=("Bold", 20))
            lb.place(x=45, y=40)
            emprestimos_page_fm.pack(fill="both", expand=True)

            def load_emprestimos_cliente():
                 for item in tv_emprestimo_cliente.get_children():
                        tv_emprestimo_cliente.delete(item)
            
            # insere os empréstimos
                 for emprestimo in self.emprestimosCtrl.pegarEmprestimosPorUsuario(usuario.getId()):
                        if emprestimo.getMulta() == None:
                            status = ""
                            valor = ""
                        else:
                            status = emprestimo.getMulta().getStatus().name
                            valor = f"R$ {emprestimo.getMulta().getValor():.2f}"

                        tv_emprestimo_cliente.insert("", "end", iid=emprestimo.getId(), values=(
                            emprestimo.getId(),
                            emprestimo.getDataEmprestimo().strftime("%d/%m/%Y"),
                            emprestimo.getDataPrevista().strftime("%d/%m/%Y"),
                            emprestimo.getStatus().name,
                            emprestimo.getMulta().getId(),
                            status,
                            valor
                            ))
                        
            id_multa = CTkEntry(emprestimos_page_fm, placeholder_text="Digite o ID da Multa", width=200)
            id_multa.place(x=45, y=90)
                        
            def capturar_id_emprestimo(event):

                item_selecionado = tv_emprestimo_cliente.selection()
                if item_selecionado != "":
                    messagebox.showerror("Erro", item_selecionado)
                    id_emprestimo = item_selecionado[0]
                    linha_emprestimo = tv_emprestimo_cliente.item(id_emprestimo, 'values')
                    id_selecionado = linha_emprestimo[4]
                    id_multa.delete(0, END)
                    id_multa.insert(0, id_selecionado)

            def pagar_multa():
                if not id_multa.get():
                    messagebox.showerror("Erro", "Digite o ID da multa.")
                    return
                multa = self.multasCtrl.buscarPorId(id_multa.get())

                if  multa.getStatus() == StatusMulta.PAGA:
                    messagebox.showerror("Erro", "Multa ja paga.")
                else:
                    self.multasCtrl.pagarMulta(id_multa.get())
                    messagebox.showinfo("Pago", "Multa paga com sucesso.")
                    load_emprestimos_cliente()
                    
            tv_emprestimo_cliente = tk.ttk.Treeview(emprestimos_page_fm)
            tv_emprestimo_cliente.place(x=40, y=160, width=750, height=400)
            tv_emprestimo_cliente.column("#0", width=0, stretch="no")
            tv_emprestimo_cliente['columns'] = ("ID", "DataEmprestimo", "DataPrevista", "Status", "IDMulta", "StatusMulta", "ValorMulta")
            tv_emprestimo_cliente.column("ID", anchor="center", width=50)
            tv_emprestimo_cliente.column("DataEmprestimo", anchor="center", width=80)
            tv_emprestimo_cliente.column("DataPrevista", anchor="center", width=80)
            tv_emprestimo_cliente.column("Status", anchor="w", width=80)
            tv_emprestimo_cliente.column("IDMulta", width=0, stretch="no")
            tv_emprestimo_cliente.column("StatusMulta", anchor="w", width=100)
            tv_emprestimo_cliente.column("ValorMulta", anchor="center", width=80)

            tv_emprestimo_cliente.heading("ID", text="ID Empréstimo", anchor="center")
            tv_emprestimo_cliente.heading("DataEmprestimo", text="Data Empréstimo", anchor="center")
            tv_emprestimo_cliente.heading("DataPrevista", text="Data Prevista", anchor="center")
            tv_emprestimo_cliente.heading("Status", text="Status", anchor="center")
            tv_emprestimo_cliente.heading("StatusMulta", text="Multa", anchor="center")
            tv_emprestimo_cliente.heading("ValorMulta", text="Valor Multa", anchor="center")

            tv_emprestimo_cliente.scrollbar = tk.Scrollbar(emprestimos_page_fm, orient="vertical", command=tv_emprestimo_cliente.yview)
            tv_emprestimo_cliente.scrollbar.place(x=790, y=160, height=400)
            tv_emprestimo_cliente.configure(yscrollcommand=tv_emprestimo_cliente.scrollbar.set)

            load_emprestimos_cliente()

            tv_emprestimo_cliente.bind("<ButtonRelease-1>", capturar_id_emprestimo)

            titulo_emprestimos = CTkLabel(page_frame, text="Minhas Multas", font=("Bold", 16), fg_color="#CFCFCF")
            titulo_emprestimos.place(x=40, y=130)

            btn_buscar = CTkButton(emprestimos_page_fm,
                                   text="Pagar Multa",
                                   width=130,
                                   fg_color = "#63C5A1",
                                   font=("Helvetica", 14, "bold"),
                                   text_color= "white",
                                   command=pagar_multa)
            btn_buscar.place(x=320, y=90)
            
        def about_page():
            # Frame principal da página
            about_page_fm = CTkFrame(page_frame, fg_color="white")
            about_page_fm.pack(fill="both", expand=True)

            about_page_fm.grid_columnconfigure(0, weight=1)
            about_page_fm.grid_columnconfigure(1, weight=0)
            about_page_fm.grid_columnconfigure(2, weight=1)

            # Logos
            logo_nexo_img = customtkinter.CTkImage(
                light_image=Image.open("View/images/logo_about.png"),
                dark_image=Image.open("View/images/logo_about.png"),
                size=(120, 120)
            )
            logo_acervo_img = customtkinter.CTkImage(
                light_image=Image.open("View/images/logo_acervo.png"),
                dark_image=Image.open("View/images/logo_acervo.png"),
                size=(120, 120)
            )

            # Ícones dos pilares
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

            def about_nexo_content():
            # Frame central about Nexo
                frame_sobre_nexo = customtkinter.CTkFrame(about_page_fm, fg_color="transparent")
                frame_sobre_nexo.grid(row=1, column=1, sticky='nsew')

            # Título "Sobre Nós"
                label_title = customtkinter.CTkLabel(
                    frame_sobre_nexo,
                    text="Sobre Nós",
                    font=customtkinter.CTkFont(size=30, weight="bold"),
                    text_color="#012E58",
                    bg_color="transparent"
                )
                label_title.grid(row=1, column=1, sticky='w', pady=(50,0))

            # Texto principal
                label_sobre_1 = customtkinter.CTkLabel(
                    frame_sobre_nexo,
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
                label_sobre_1.grid(row=2, column=1, sticky='nw', pady=10)

            # Título Equipe
                label_sobre_2 = customtkinter.CTkLabel(
                    frame_sobre_nexo,
                    text="Equipe",
                    font=customtkinter.CTkFont(size=16, weight="bold"),
                    bg_color="transparent"
                )
                label_sobre_2.grid(row=5, column=1, sticky='w', pady=(0, 10))

            # Label Equipe
                label_equipe = customtkinter.CTkLabel(frame_sobre_nexo,
                                                    width=200,
                                                    wraplength=600,
                                                    justify="left",
                                                    bg_color="transparent",
                                                    text="• Ilca Almeida Trigueiros (CEO)\n" \
                                                        "• Gustavo Ribeiro Carpanez (Arquiteto de Dados)\n" \
                                                        "• Nathan Silva de Souza (Desenvolvedor Backend)\n" \
                                                        "• Patrick da Silva Almeida (Engenheiro de DevOps / Cloud)\n" \
                                                        "• Pedro Henrique Vicente (Desenvolvedor Frontend)\n" \
                                                        "• Pedro Paulo Reis Rodrigues (Analista de Segurança da Informação)\n" \
                                                        "• Pedro Ricardo Brandão Costa (Analista de Negócios)")
                label_equipe.grid(row=6, column=1, sticky='nw', pady=10, padx=(35,0))
            
            def about_acervo_content():

            # Frame central about Acervo
                frame_sobre_acervo = customtkinter.CTkFrame(about_page_fm, fg_color="transparent")
                frame_sobre_acervo.grid(row=1, column=1, sticky='nsew')

                frame_sobre_acervo.grid_columnconfigure(0, weight=1)

            # Título "Sobre o Acervo"
                label_title = customtkinter.CTkLabel(
                    frame_sobre_acervo,
                    text="Sobre Nós",
                    font=customtkinter.CTkFont(size=30, weight="bold"),
                    text_color="#90D6BC",
                    bg_color="transparent"
                )
                label_title.grid(row=0, column=0, sticky='w', pady=(50,0))

            # Texto principal
                label_sobre_acervo = customtkinter.CTkLabel(
                    frame_sobre_acervo,
                    text=(
                        "O AcervoMax é o nosso sistema de gestão de empréstimos e acervos, "
                        "projetado para bibliotecas de grande escala. Permite aos usuários o "
                        "controle total sobre a sua situação de empréstimos e multas, "
                        "sem a necessidade de intervenção de um bibliotecário."),
                    width=650,
                    wraplength=600,
                    justify="left")
                label_sobre_acervo.grid(row=1, column=0, sticky='w', pady=10, padx=(8,0))

            # Título secundário
                label_sobre_2 = customtkinter.CTkLabel(
                    frame_sobre_acervo,
                    text="Nossos Pilares",
                    font=customtkinter.CTkFont(size=16, weight="bold"),
                    bg_color="transparent"
                )
                label_sobre_2.grid(row=2, column=0, sticky='w', pady=0)

            # Frame dos pilares
                frame_sarch = customtkinter.CTkFrame(
                    frame_sobre_acervo,
                    fg_color="transparent",
                    width=650
                )
                frame_sarch.grid(row=3, column=0, sticky='nw', pady=(0,10), padx=(35,0))

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

        #Frame Logos
            frame_logos = customtkinter.CTkFrame(about_page_fm, fg_color="transparent")
            frame_logos.grid(row=0, column=1, pady=(50,0), padx=(0,60))

        #Logo Acervo
            btn_logo_acervo = customtkinter.CTkButton(frame_logos,
                                                      image=logo_acervo_img,
                                                      text="",
                                                      fg_color="transparent",
                                                      command=about_acervo_content)
            btn_logo_acervo.grid(row=0, column=1)

        # Logo NEXO
            btn_logo_nexo = customtkinter.CTkButton(frame_logos,
                                                    image=logo_nexo_img,
                                                    text="",
                                                    fg_color="transparent",
                                                    command=about_nexo_content)
            btn_logo_nexo.grid(row=0, column=0, padx=30)
        
            about_nexo_content()

        # Área principal das páginas
        page_frame = CTkFrame(nova_janela)
        page_frame.place(relwidth=1.0, relheight=1.0, x=50)
        livros_page_cliente()

        # Menu lateral
        menu_bar_frame = CTkFrame(nova_janela, fg_color=menu_bar_color)
        menu_bar_frame.pack(side="left", fill="y", pady=5, padx=2)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=50)

        # Botão do menu
        toggle_menu_btn = CTkButton(menu_bar_frame, image=toggle_icon, text="",
                                    fg_color=menu_bar_color, hover_color=menu_bar_color,
                                    command=extend_menu_bar, width=30, height=30)
        toggle_menu_btn.place(x=4, y=10)

        # Botão Home
        home_btn = CTkButton(menu_bar_frame, image=home_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(home_btn_indicator, livros_page_cliente),
                            width=30, height=40)
        home_btn.place(x=9, y=130)

        home_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color='white', width=3, height=40)
        home_btn_indicator.place(x=3, y=130)

        home_page_lb = CTkLabel(menu_bar_frame, text="Home", fg_color=menu_bar_color,
                                text_color="white", font=("Bold", 15))
        home_page_lb.place(x=50, y=138)
        home_page_lb.bind("<Button-1>", lambda e: switch_indication(home_btn_indicator, livros_page_cliente))

        # Botão Emprestimos
        emprestimos_btn = CTkButton(menu_bar_frame, image=livro_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(emprestimos_btn_indicator, emprestimos_page),
                            width=30, height=40)
        emprestimos_btn.place(x=9, y=195)
        
        emprestimos_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        emprestimos_btn_indicator.place(x=3, y=195)

        emprestimos_lb = CTkLabel(menu_bar_frame, text="Empréstimos", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        emprestimos_lb.place(x=50, y=203)
        emprestimos_lb.bind("<Button-1>", lambda e: switch_indication(emprestimos_btn_indicator, emprestimos_page))

        # Botão Sobre
        about_btn = CTkButton(menu_bar_frame, image=about_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(about_btn_indicator, about_page),
                            width=30, height=40)
        about_btn.place(x=9, y=260)
        
        about_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        about_btn_indicator.place(x=3, y=260)

        about_lb = CTkLabel(menu_bar_frame, text="Sobre", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        about_lb.place(x=50, y=263)
        about_lb.bind("<Button-1>", lambda e: switch_indication(about_btn_indicator, about_page))

        # Botão Logout
        logout_btn = CTkButton(menu_bar_frame, image=logout, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: self.realizar_logout(nova_janela),
                            width=30, height=40)
        logout_btn.place(x=9, y=500)
        
        logout_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        logout_btn_indicator.place(x=3, y=500)

        logout_lb = CTkLabel(menu_bar_frame, text="Logout", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        logout_lb.place(x=50, y=505)
        logout_lb.bind("<Button-1>", lambda e: self.realizar_logout(nova_janela))

        # posicionando o menu bar frame
        menu_bar_frame.pack(side="left", fill="y", pady=4, padx=3)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=50, fg_color=menu_bar_color)

        nova_janela.mainloop()

    def janela_nova(self, usuario): 
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
        multas_icon = customtkinter.CTkImage(Image.open("View/images/multas.png"), size=(25, 25))
        about_icon = customtkinter.CTkImage(Image.open("View/images/about_icon.png"), size=(22, 22))
        close_btn_icon = customtkinter.CTkImage(Image.open("View/images/close_btn_icon.png"), size=(22, 22))
        logout = customtkinter.CTkImage(Image.open("View/images/logout.png"), size=(22, 22))
        usuario_icon = customtkinter.CTkImage(Image.open("View/images/user-avatar.png"), size=(22, 22))

        # Indicadores de botões
        def switch_indication(indicator_lb, page):
            home_btn_indicator.configure(fg_color=menu_bar_color)
            multas_btn_indicator.configure(fg_color=menu_bar_color)
            about_btn_indicator.configure(fg_color=menu_bar_color)
            listar_btn_indicator.configure(fg_color=menu_bar_color)
            
            indicator_lb.configure(fg_color='white')

            #=if menu_bar_frame.winfo_width() >= 50:
                #fold_menu_bar()

            for frame in page_frame.winfo_children():
                frame.destroy()

            page()

        # Animação de extensão do menu
        def extending_animation():
            current_width = menu_bar_frame.winfo_width()
            if not current_width >= 150:
                current_width += 100
                menu_bar_frame.configure(width=current_width)
                nova_janela.after(ms=1, func=extending_animation)

        def extend_menu_bar():
            extending_animation()
            toggle_menu_btn.configure(image=close_btn_icon, command=fold_menu_bar)

        # Animação de recolhimento do menu
        def folding_animation():
            current_width = menu_bar_frame.winfo_width()
            if current_width != 50:
                current_width -= 100
                menu_bar_frame.configure(width=current_width)
                nova_janela.after(ms=8, func=folding_animation)

        def fold_menu_bar():
            folding_animation()
            toggle_menu_btn.configure(image=toggle_icon, command=extend_menu_bar)

        # Páginas

        def livros_page():  
            def load_livros():
                 for item in tv.get_children():
                        tv.delete(item)
            # insere os livros
                 for livro in self.livroCtrl.getLivros():
                        tv.insert("", "end", iid=livro.getId(), values=(
                            livro.getId(),
                            livro.getTitulo(),
                            livro.getGenero(),
                            livro.getEditora(),
                            livro.getAutor(),
                            livro.getNExemplares()
                            ))
            # Página de livros
            livros_page_fm = CTkFrame(page_frame)                     
            lb = CTkLabel(livros_page_fm,
                          text=f"Bem-vindo ao Sistema {usuario.getNomeUsuario()} - [{usuario.getTipo().name}] ",
                          font=("Bold", 20))
            lb.place(x=45, y=40)                  

            livros_page_fm.pack(fill="both", expand=True)

            nome_livro = CTkEntry(livros_page_fm,
                                  placeholder_text="Digite o nome do livro",
                                  width=200, fg_color="transparent",
                                  bg_color="transparent")
            nome_livro.place(x=45, y=80)

            # função do modal de adicionar livro
            def modal_add_livro():
                modal = CTkToplevel(nova_janela)
                modal.geometry("400x400")
                modal.title("Adicionar Livro")
                modal.grab_set()

                # Validação para número de exemplares
                def validar_numerro(valor):
                     if valor =="":
                        return True
                     return valor.isdigit()
                
                vcmd = (modal.register(validar_numerro), '%P')
                
                lbl_title = CTkLabel(modal, text="Adicionar Novo Livro", font=("Bold", 16))
                lbl_title.pack(pady=10)
                entry_titulo = CTkEntry(modal, placeholder_text="Título")
                entry_titulo.pack(pady=5)
                entry_genero = CTkEntry(modal, placeholder_text="Gênero")
                entry_genero.pack(pady=5)
                entry_editora = CTkEntry(modal, placeholder_text="Editora")
                entry_editora.pack(pady=5)
                entry_autor = CTkEntry(modal, placeholder_text="Autor")
                entry_autor.pack(pady=5)
                entry_n_exemplares = CTkEntry(modal, placeholder_text="Nº de Exemplares")
                entry_n_exemplares.pack(pady=5)

                entry_n_exemplares.configure(validate="key", validatecommand=vcmd)

                def confirmar():
                    titulo = entry_titulo.get()
                    genero = entry_genero.get()
                    editora = entry_editora.get()
                    autor = entry_autor.get()
                    nex = entry_n_exemplares.get()

                    if titulo == "" or genero == "" or editora == "" or autor == "" or nex == "":
                        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                        return

                    self.livroCtrl.criarLivro(titulo, genero, editora, autor, int(nex))

                    load_livros()

                    modal.destroy()

                btn_adicionar = CTkButton(modal,
                                          text="Adicionar",
                                          command=confirmar,
                                          width=130,
                                          fg_color = "#63C5A1",
                                          font=("Helvetica", 14, "bold"),
                                          text_color= "white")    
                btn_adicionar.pack(pady=20)

            def add_livro():
                modal_add_livro()

            def delete_livro():
                titiloDelete = nome_livro.get()
                if titiloDelete == "":
                    messagebox.showerror("Erro", "Por favor, insira o título do livro a ser removido.")
                    return
                livro = self.livroCtrl.buscarPorTitulo(titiloDelete)
                if not livro:
                    messagebox.showerror("Erro", f"Livro com título '{titiloDelete}' não encontrado.")
                    return
                self.livroCtrl.removerLivroPorId(livro.getId())
                load_livros()
                messagebox.showinfo("Sucesso", f"Livro '{titiloDelete}' removido com sucesso.")
                nome_livro.delete(0, 'end')
                nome_livro.focus()
                
            def buscar_livro():
                livro_desejado = nome_livro.get()
                if livro_desejado == "":
                    messagebox.showerror("Erro", "Por favor, insira o título do livro a ser buscado.")
                    return
                livro =self.livroCtrl.buscarPorTitulo(livro_desejado)
                if not livro:
                    messagebox.showerror("Erro", f"Livro com título '{livro_desejado}' não encontrado.")
                    return
                else:
                    tv.selection_set(livro.getId())
                    tv.see(livro.getId())
                    messagebox.showinfo("Sucesso", f"Livro '{livro_desejado}' encontrado e selecionado na tabela.")
                    nome_livro.delete(0, 'end')
                    nome_livro.focus()
                
            def modal_add_exemplares():
                modal = CTkToplevel(nova_janela)
                modal.geometry("300x300")
                modal.title("Controle de Estoque")
                modal.grab_set()

                # Validação numérica
                def validar_numero(valor):
                    return valor.isdigit() or valor == ""

                vcmd = (modal.register(validar_numero), '%P')

                CTkLabel(modal, text="Ajustar Quantidade", font=("Bold", 16)).pack(pady=10)

                entry_titulo = CTkEntry(modal, placeholder_text="Título do Livro")
                entry_titulo.pack(pady=5)

                entry_qtd = CTkEntry(modal, 
                                    placeholder_text="Quantidade a adicionar",
                                    validate="key", 
                                    validatecommand=vcmd)
                entry_qtd.pack(pady=5)

                # Atualiza o título conforme o usuário digita
                def atualizar_info(*args):
                    titulo = entry_titulo.get()
                    if titulo.strip() != "":
                        livro = self.livroCtrl.buscarPorTitulo(titulo)
                        if livro:
                            lbl_info.configure(text=f"Livro encontrado: {livro.getTitulo()}")
                        else:
                            lbl_info.configure(text="Livro não encontrado.")
                    else:
                        lbl_info.configure(text="")

                entry_titulo.bind("<KeyRelease>", atualizar_info)

                def confirmar_add():
                    titulo = entry_titulo.get()
                    quantidade = entry_qtd.get()

                    if titulo == "" or quantidade == "":
                        messagebox.showerror("Erro", "Preencha todos os campos.")
                        return

                    livro = self.livroCtrl.buscarPorTitulo(titulo)

                    if not livro:
                        messagebox.showerror("Erro", f"Livro com título '{titulo}' não encontrado.")
                        return

                    # Atualiza quantidade
                    novo_total = livro.getNExemplares() + int(quantidade)
                    livro.setNExemplares(novo_total)

                    self.livroCtrl.setNExemplares(titulo, novo_total)

                    load_livros()

                    messagebox.showinfo(
                        "Sucesso",
                        f"Foram adicionados {quantidade} exemplares ao livro '{livro.getTitulo()}'."
                    )

                    modal.destroy()

                def confirmar_rem():
                    titulo = entry_titulo.get()
                    quantidade = entry_qtd.get()

                    if titulo == "" or quantidade == "":
                        messagebox.showerror("Erro", "Preencha todos os campos.")
                        return

                    livro = self.livroCtrl.buscarPorTitulo(titulo)

                    if not livro:
                        messagebox.showerror("Erro", f"Livro com título '{titulo}' não encontrado.")
                        return

                    # Atualiza quantidade
                    novo_total = livro.getNExemplares() - int(quantidade)
                    livro.setNExemplares(novo_total)

                    self.livroCtrl.setNExemplares(titulo, novo_total)

                    load_livros()

                    messagebox.showinfo(
                        "Sucesso",
                        f"Foram removidos {quantidade} exemplares ao livro '{livro.getTitulo()}'."
                    )

                    modal.destroy()

                CTkButton(modal,
                          text="Adicionar",
                          command=confirmar_add,
                          width=130,
                          fg_color = "#63C5A1",
                          font=("Helvetica", 14, "bold"),
                          text_color= "white").pack(pady=10)
                
                CTkButton(modal,
                          text="Remover",
                          command=confirmar_rem,
                          width=130,
                          fg_color = "#63C5A1",
                          font=("Helvetica", 14, "bold"),
                          text_color= "white").pack(pady=0)

        # Botões e tabela
            btn_adcionar = CTkButton(livros_page_fm,
                                     text="Add Livros",
                                     width=130,
                                     fg_color = "#63C5A1",
                                     font=("Helvetica", 14, "bold"),
                                     text_color= "white")
            btn_adcionar.place(x=255, y=80)
            btn_adcionar.configure(command=add_livro)

            btn_remover = CTkButton(livros_page_fm,
                                    text="Remover Livros",
                                    width=130,
                                    fg_color = "#63C5A1",
                                    font=("Helvetica", 14, "bold"),
                                    text_color= "white")
            btn_remover.place(x=525, y=80)
            btn_remover.configure(command=delete_livro)

            btn_add_ex = CTkButton(livros_page_fm,
                                   text="Estoque",
                                   width=130,
                                   fg_color = "#63C5A1",
                                   font=("Helvetica", 14, "bold"),
                                   text_color= "white")
            btn_add_ex.place(x=660, y=80)
            btn_add_ex.configure(command=modal_add_exemplares)

            btn_buscar = CTkButton(livros_page_fm,
                                   text="Buscar Livros",
                                   width=130,
                                   fg_color = "#63C5A1",
                                   font=("Helvetica", 14, "bold"),
                                   text_color= "white")
            btn_buscar.place(x=390, y=80)
            btn_buscar.configure(command=buscar_livro)

            titulo_livros = CTkLabel(livros_page_fm, text="Livros Disponíveis", font=("Bold", 16))
            titulo_livros.place(x=40, y=130)
            
        # Tabela de livros
            tv = tk.ttk.Treeview(livros_page_fm)
            tv.place(x=40, y=160, width=750, height=400)
            tv.column("#0", width=0, stretch="no")
            tv['columns'] = ("ID", "Título", "Gênero", "Editora", "Autor", "Exemplares")
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

            tv.scrollbar = tk.Scrollbar(livros_page_fm, orient="vertical", command=tv.yview)
            tv.scrollbar.place(x=790, y=160, height=400)
            tv.configure(yscrollcommand=tv.scrollbar.set)
            
            load_livros()

        def multas_page():

            multas_page_fm = CTkFrame(page_frame)
            lb = CTkLabel(multas_page_fm,
                          text=f"Bem-vindo ao Sistema {usuario.getNomeUsuario()} - [{usuario.getTipo().name}] ",
                          font=("Bold", 20))
            lb.place(x=45, y=40)
            multas_page_fm.pack(fill="both", expand=True)

            id_emprestimo = customtkinter.CTkEntry(multas_page_fm,
                                                   placeholder_text="ID Emprestimo",
                                                   width=200)
            id_emprestimo.place(x=45, y=80)

            def capturar_id_emprestimo(event):
                selected_item = tv_emp.selection()
                id_empestimo = selected_item[0]
                linha_emprestimo = tv_emp.item(id_empestimo, "values")
                id_emprestimo.delete(0, 'end')
                id_emprestimo.insert(0, linha_emprestimo[0]) 

            def load_multas():
                # limpa a tabela
                for item in tv.get_children():
                    tv.delete(item)

                # lista as multas
                for multa in self.multasCtrl.getMultas():

                    cliente = multa.getCliente()

                    cliente_id = cliente.getId() if cliente else "N/A"
                    cliente_nome = cliente.getNomeUsuario() if cliente else "N/A"
                   
                    valor = f"R$ {multa.getValor():.2f}"
                    
                    status = multa.getStatus().name if multa.getStatus() else "N/A"

                    # insere na treeview
                    tv.insert("", "end", iid=multa.getId(), values=(
                        multa.getId(),
                        cliente_id,
                        cliente_nome,
                        valor,
                        status
                    ))

            def registrar_devolucao():
                emprestimo = self.emprestimosCtrl.buscarPorId(id_emprestimo.get())
                if  emprestimo == None:
                    messagebox.showerror("Erro", "Emprestimo nao encontrado")
                    return
                if emprestimo.getStatus() == StatusEmprestimo.ATIVO:
                    messagebox.showinfo("Sucesso", "Emprestimo devolvido com sucesso")
                    self.emprestimosCtrl.registrarDevolucao(id_emprestimo.get(), date.today())
                    load_emprestimos()
                    load_multas()
                else:
                    messagebox.showerror("Erro", "Emprestimo ja devolvido")

            def modal_emprestimo():
                modal = CTkToplevel(nova_janela)
                modal.geometry("400x300")
                modal.title
                modal.title("Registrar Empréstimo")

                lbl_title = CTkLabel(modal, text="Registrar Novo Empréstimo", font=("Bold", 16))
                lbl_title.pack(pady=8)

                entry_cliente_id = CTkEntry(modal, placeholder_text="ID do Cliente")
                entry_cliente_id.pack(pady=9)

                entry_livro_ids = CTkEntry(modal, placeholder_text="IDs dos Livros (separados por vírgula)")
                entry_livro_ids.pack(pady=10)

                info_livros_emp = CTkLabel(modal,
                                           text="*Digite os IDs dos livros separados por vírgula",
                                           font=("Bold",11))
                info_livros_emp.pack(pady=11)

                def confirmar_emprestimo():
                    cliente_id = entry_cliente_id.get()
                    livro_ids_str = entry_livro_ids.get()
                    livro_ids = [id_.strip() for id_ in livro_ids_str.split(",") if id_.strip()]

                    if not cliente_id or not livro_ids:
                        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
                        return

                    cliente = self.userCtrl.buscar_por_id(cliente_id)
                    if not cliente:
                        messagebox.showerror("Erro", "Cliente não encontrado.")
                        return

                    livros = []
                    for livro_id in livro_ids:
                        livro = self.livroCtrl.buscarPorId(livro_id)
                        if livro:
                            livros.append(livro)
                        else:
                            messagebox.showerror("Erro", f"Livro com ID {livro_id} não encontrado.")
                            return

                    if self.emprestimosCtrl.criarEmprestimo(cliente, livros):
                        messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso.")
                        load_emprestimos()
                    else:
                        messagebox.showerror("Erro", "Falha ao registrar o empréstimo. Não são permitidos mais de um exemplar no mesmo empréstimo.")
                        return
                    modal.destroy()

                btn_confirmar = CTkButton(modal,
                                          text="Confirmar",
                                          command=confirmar_emprestimo,
                                          width=130,
                                          fg_color = "#63C5A1",
                                          font=("Helvetica", 14, "bold"),
                                          text_color= "white")    
                btn_confirmar.pack(pady=20)
           
            def registrar_emprestimo():
                modal_emprestimo()
                
            btn_reg_devolucao = CTkButton(multas_page_fm,
                                     text="Registrar Devolução",
                                     width=160,
                                     fg_color = "#63C5A1",
                                     font=("Helvetica", 14, "bold"),
                                     text_color= "white",
                                     command=registrar_devolucao)
            btn_reg_devolucao.place(x=427, y=80)

            btn_reg_emprestimo = CTkButton(multas_page_fm,
                                     text="Registrar Emprestimo",
                                     width=160,
                                     fg_color = "#63C5A1",
                                     font=("Helvetica", 14, "bold"),
                                     text_color= "white",
                                     command=registrar_emprestimo)
            btn_reg_emprestimo.place(x=255, y=80)

            titulo_multa = CTkLabel(multas_page_fm, text="Multas Registradas",
                                    font=("Bold", 16))
            titulo_multa.place(x=40, y=345)

            colunas = ("id", "cliente_id", "cliente", "Valor", "status")

            tv = tk.ttk.Treeview(multas_page_fm, columns=colunas,
                                 show="headings",
                                 height=12)

            # Cabeçalhos
            tv.heading("id", text="ID Multa")
            tv.heading("cliente_id", text="ID Cliente")
            tv.heading("cliente", text="Nome Cliente")
            tv.heading("Valor", text="Valor")
            tv.heading("status", text="Status")

            # Larguras
            tv.column("id", width=80)
            tv.column("cliente_id", width=0, stretch="no")
            tv.column("cliente", width=140)
            tv.column("Valor", width=120)
            tv.column("status", width=100)

            tv.scrollbar = tk.Scrollbar(multas_page_fm, orient="vertical",
                                        command=tv.yview)
            tv.scrollbar.place(x=790, y=380, height=200)
            tv.configure(yscrollcommand=tv.scrollbar.set)
            tv.place(x=40, y=380, width=750, height=200)
            load_multas()
            
            def load_emprestimos():
                # limpa a tabela
                for item in tv_emp.get_children():
                    tv_emp.delete(item)

                # lista os emprestimos
                for emprestimo in self.emprestimosCtrl.getEmprestimos():

                    cliente = emprestimo.getCliente()
                    titulos = ", ".join([item.getTitulo() for item in emprestimo.getItens()]) if emprestimo.getItens() else "N/A"

                    cliente_nome = cliente.getNomeUsuario() if cliente else "N/A"

                    # insere na treeview
                    tv_emp.insert("", "end", iid=emprestimo.getId(), values=(
                        emprestimo.getId(),
                        cliente_nome,
                        titulos,
                        emprestimo.getDataEmprestimo().strftime("%d/%m/%Y"),
                        emprestimo.getDataPrevista().strftime("%d/%m/%Y"),
                        emprestimo.getStatus().name
                    ))

            titulo_emprestimos = CTkLabel(multas_page_fm,
                                          text="Empréstimos Registrados",
                                          font=("Bold", 16))
            titulo_emprestimos.place(x=40, y=125)

            colunas_emp = ("id", "cliente", "livro", "data_emp", "data_prev", "status")
            tv_emp = tk.ttk.Treeview(multas_page_fm,
                                     columns=colunas_emp,
                                     show="headings",
                                     height=8)
            # Cabeçalhos
            tv_emp.heading("id", text="ID Empréstimo")
            tv_emp.heading("cliente", text="Nome Cliente")
            tv_emp.heading("livro", text="Título do(s) Livro(s)")
            tv_emp.heading("data_emp", text="Data Empréstimo")
            tv_emp.heading("data_prev", text="Data Prevista")
            tv_emp.heading("status", text="Status")
            # Larguras
            tv_emp.column("id", width=100)
            tv_emp.column("cliente", width=140)
            tv_emp.column("livro", width=140)
            tv_emp.column("data_emp", width=120)
            tv_emp.column("data_prev", width=120)
            tv_emp.column("status", width=100)
            tv_emp.place(x=40, y=160, width=750, height=180)
            tv_emp.scrollbar = tk.Scrollbar(multas_page_fm,
                                            orient="vertical",
                                            command=tv_emp.yview)
            tv_emp.scrollbar.place(x=790, y=160, height=180)
            tv_emp.configure(yscrollcommand=tv_emp.scrollbar.set)

            load_emprestimos()
            
            tv_emp.bind("<ButtonRelease-1>", capturar_id_emprestimo)

        def listar_usuarios():

            usuarios_page_fm = CTkFrame(page_frame)
            lb = CTkLabel(usuarios_page_fm,
                          text=f"Bem-vindo ao Sistema {usuario.getNomeUsuario()} - [{usuario.getTipo().name}] ",
                          font=("Bold", 20))
            lb.place(x=45, y=40)
            usuarios_page_fm.pack(fill="both", expand=True)

            # Carregar usuários
            def load_usuarios():
                #Limpa a Treeview
                for item in tv_usu.get_children():
                    tv_usu.delete(item)
                # Insere os usuários
                for user in self.userCtrl.listar_usuarios():
                    tv_usu.insert("", "end", iid=user.getId(), values=(
                        user.getId(),
                        user.getNomeUsuario(),
                        user.getTipo().name
                    ))

            def modal_cadastro():
                modal = CTkToplevel(nova_janela)
                modal.geometry("400x400")
                modal.title("Cadastro de Usuário")
                modal.grab_set()

                lbl_title = CTkLabel(modal, text="Cadastrar Novo Usuário", font=("Bold", 16))
                lbl_title.pack(pady=10)

                entry_nome = CTkEntry(modal, placeholder_text="Nome do Usuário")
                entry_nome.pack(pady=5)

                entry_login = CTkEntry(modal, placeholder_text="Login do Usuário")
                entry_login.pack(pady=5)

                entry_senha = CTkEntry(modal, placeholder_text="Senha do Usuário", show="*")
                entry_senha.pack(pady=5)

                entry_tipo = CTkEntry(modal, placeholder_text="Tipo de Usuário (FUNCIONARIO/CLIENTE)")
                entry_tipo.pack(pady=5)

                def confirmar_cadastro():
                    nome = entry_nome.get()
                    tipo_str = entry_tipo.get().upper()

                    if nome == "" or tipo_str == "":
                        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                        return

                    if tipo_str not in ["FUNCIONARIO", "CLIENTE"]:
                        messagebox.showerror("Erro", "Tipo de usuário inválido. Use 'ADMIN' ou 'CLIENTE'.")
                        return

                    self.userCtrl.cadastrar_usuario(nomeUsuario=nome,
                                                    login=entry_login.get(),
                                                    senha=entry_senha.get(),
                                                    tipo=TipoUsuario[tipo_str],
                                                    pessoaLogada=usuario
                                                    )

                    load_usuarios()

                    modal.destroy()

                btn_cadastrar = CTkButton(modal,
                                          text="Cadastrar",
                                          command=confirmar_cadastro,
                                          width=130,
                                          fg_color = "#63C5A1",
                                          font=("Helvetica", 14, "bold"),
                                          text_color= "white")    
                btn_cadastrar.pack(pady=20)

            def cadastro_usuario():
                 modal_cadastro()
            
            titulo_usuarios = CTkLabel(usuarios_page_fm, text="Usuários Registrados", font=("Bold", 16))
            titulo_usuarios.place(x=40, y=125)

            colunas_usu = ("id", "nome", "tipo")
            tv_usu = tk.ttk.Treeview(usuarios_page_fm, columns=colunas_usu, show="headings", height=15)
            # Cabeçalhos
            tv_usu.heading("id", text="ID Usuário")
            tv_usu.heading("nome", text="Nome do Usuário")
            tv_usu.heading("tipo", text="Tipo de Usuário")
            
            # Larguras
            tv_usu.column("id", width=100)
            tv_usu.column("nome", width=200)
            tv_usu.column("tipo", width=150)

            tv_usu.place(x=40, y=160, width=750, height=350)
            tv_usu.scrollbar = tk.Scrollbar(usuarios_page_fm, orient="vertical", command=tv_usu.yview)
            tv_usu.scrollbar.place(x=790, y=160, height=350)
            tv_usu.configure(yscrollcommand=tv_usu.scrollbar.set)

                        
            btn_listar = CTkButton(usuarios_page_fm,
                                    text="Cadastrar Usuário",
                                    width=130, 
                                    fg_color = "#63C5A1", 
                                    font=("Helvetica", 14, "bold"), 
                                    text_color= "white",
                                    command=cadastro_usuario)
            btn_listar.place(x=45, y=80)

            load_usuarios()
            
        def about_page():
            # Frame principal da página
            about_page_fm = CTkFrame(page_frame, fg_color="white")
            about_page_fm.pack(fill="both", expand=True)

            about_page_fm.grid_columnconfigure(0, weight=1)
            about_page_fm.grid_columnconfigure(1, weight=0)
            about_page_fm.grid_columnconfigure(2, weight=1)

            # Logos
            logo_nexo_img = customtkinter.CTkImage(
                light_image=Image.open("View/images/logo_about.png"),
                dark_image=Image.open("View/images/logo_about.png"),
                size=(120, 120)
            )
            logo_acervo_img = customtkinter.CTkImage(
                light_image=Image.open("View/images/logo_acervo.png"),
                dark_image=Image.open("View/images/logo_acervo.png"),
                size=(120, 120)
            )

            # Ícones dos pilares
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

            def about_nexo_content():
            # Frame central about Nexo
                frame_sobre_nexo = customtkinter.CTkFrame(about_page_fm, fg_color="transparent")
                frame_sobre_nexo.grid(row=1, column=1, sticky='nsew')

            # Título "Sobre Nós"
                label_title = customtkinter.CTkLabel(
                    frame_sobre_nexo,
                    text="Sobre Nós",
                    font=customtkinter.CTkFont(size=30, weight="bold"),
                    text_color="#012E58",
                    bg_color="transparent"
                )
                label_title.grid(row=1, column=1, sticky='w', pady=(50,0))

            # Texto principal
                label_sobre_1 = customtkinter.CTkLabel(
                    frame_sobre_nexo,
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
                label_sobre_1.grid(row=2, column=1, sticky='nw', pady=10)

            # Título Equipe
                label_sobre_2 = customtkinter.CTkLabel(
                    frame_sobre_nexo,
                    text="Equipe",
                    font=customtkinter.CTkFont(size=16, weight="bold"),
                    bg_color="transparent"
                )
                label_sobre_2.grid(row=5, column=1, sticky='w', pady=(0, 10))

            # Label Equipe
                label_equipe = customtkinter.CTkLabel(frame_sobre_nexo,
                                                    width=200,
                                                    wraplength=600,
                                                    justify="left",
                                                    bg_color="transparent",
                                                    text="• Ilca Almeida Trigueiros (CEO)\n" \
                                                        "• Gustavo Ribeiro Carpanez (Arquiteto de Dados)\n" \
                                                        "• Nathan Silva de Souza (Desenvolvedor Backend)\n" \
                                                        "• Patrick da Silva Almeida (Engenheiro de DevOps / Cloud)\n" \
                                                        "• Pedro Henrique Vicente (Desenvolvedor Frontend)\n" \
                                                        "• Pedro Paulo Reis Rodrigues (Analista de Segurança da Informação)\n" \
                                                        "• Pedro Ricardo Brandão Costa (Analista de Negócios)")
                label_equipe.grid(row=6, column=1, sticky='nw', pady=10, padx=(35,0))
            
            def about_acervo_content():

            # Frame central about Acervo
                frame_sobre_acervo = customtkinter.CTkFrame(about_page_fm, fg_color="transparent")
                frame_sobre_acervo.grid(row=1, column=1, sticky='nsew')

                frame_sobre_acervo.grid_columnconfigure(0, weight=1)

            # Título "Sobre o Acervo"
                label_title = customtkinter.CTkLabel(
                    frame_sobre_acervo,
                    text="Sobre Nós",
                    font=customtkinter.CTkFont(size=30, weight="bold"),
                    text_color="#90D6BC",
                    bg_color="transparent"
                )
                label_title.grid(row=0, column=0, sticky='w', pady=(50,0))

            # Texto principal
                label_sobre_acervo = customtkinter.CTkLabel(
                    frame_sobre_acervo,
                    text=(
                        "O AcervoMax é o nosso sistema de gestão de empréstimos e acervos, "
                        "projetado para bibliotecas de grande escala. Permite aos usuários o "
                        "controle total sobre a sua situação de empréstimos e multas, "
                        "sem a necessidade de intervenção de um bibliotecário."),
                    width=650,
                    wraplength=600,
                    justify="left")
                label_sobre_acervo.grid(row=1, column=0, sticky='w', pady=10, padx=(8,0))

            # Título secundário
                label_sobre_2 = customtkinter.CTkLabel(
                    frame_sobre_acervo,
                    text="Nossos Pilares",
                    font=customtkinter.CTkFont(size=16, weight="bold"),
                    bg_color="transparent"
                )
                label_sobre_2.grid(row=2, column=0, sticky='w', pady=0)

            # Frame dos pilares
                frame_sarch = customtkinter.CTkFrame(
                    frame_sobre_acervo,
                    fg_color="transparent",
                    width=650
                )
                frame_sarch.grid(row=3, column=0, sticky='nw', pady=(0,10), padx=(35,0))

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

        #Frame Logos
            frame_logos = customtkinter.CTkFrame(about_page_fm, fg_color="transparent")
            frame_logos.grid(row=0, column=1, pady=(50,0), padx=(0,60))

        #Logo Acervo
            btn_logo_acervo = customtkinter.CTkButton(frame_logos,
                                                      image=logo_acervo_img,
                                                      text="",
                                                      fg_color="transparent",
                                                      command=about_acervo_content)
            btn_logo_acervo.grid(row=0, column=1)

        # Logo NEXO
            btn_logo_nexo = customtkinter.CTkButton(frame_logos,
                                                    image=logo_nexo_img,
                                                    text="",
                                                    fg_color="transparent",
                                                    command=about_nexo_content)
            btn_logo_nexo.grid(row=0, column=0, padx=30)
        
            about_nexo_content()

        # Área principal das páginas
        page_frame = CTkFrame(nova_janela)
        page_frame.place(relwidth=1.0, relheight=1.0, x=50)
        livros_page()

        # Menu lateral
        menu_bar_frame = CTkFrame(nova_janela, fg_color=menu_bar_color)
        menu_bar_frame.pack(side="left", fill="y", pady=5, padx=2)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=50)

        # Botão do menu
        toggle_menu_btn = CTkButton(menu_bar_frame, image=toggle_icon, text="",
                                    fg_color=menu_bar_color, hover_color=menu_bar_color,
                                    command=extend_menu_bar, width=30, height=30)
        toggle_menu_btn.place(x=4, y=10)

        # Botão Home
        home_btn = CTkButton(menu_bar_frame, image=home_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(home_btn_indicator, livros_page),
                            width=30, height=40)
        home_btn.place(x=9, y=130)

        home_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color='white', width=3, height=40)
        home_btn_indicator.place(x=3, y=130)

        home_page_lb = CTkLabel(menu_bar_frame, text="Home", fg_color=menu_bar_color,
                                text_color="white", font=("Bold", 15))
        home_page_lb.place(x=50, y=130)
        home_page_lb.bind("<Button-1>", lambda e: switch_indication(home_btn_indicator, livros_page))

        # Botão Multas
        multas_btn = CTkButton(menu_bar_frame, image=multas_icon, text="",
                                fg_color=menu_bar_color, hover_color=menu_bar_color,
                                command=lambda: switch_indication(multas_btn_indicator, multas_page),
                                width=30)
        multas_btn.place(x=9, y=195)

        multas_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        multas_btn_indicator.place(x=3, y=195)

        multas_lb = CTkLabel(menu_bar_frame, text="Multas", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        multas_lb.place(x=50, y=195)
        multas_lb.bind("<Button-1>", lambda e: switch_indication(multas_btn_indicator, multas_page))

        # Botão Usuarios
        listar_btn = CTkButton(menu_bar_frame, image=usuario_icon, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: switch_indication(listar_btn_indicator, listar_usuarios),
                            width=30, height=40)
        listar_btn.place(x=9, y=250)
        
        listar_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        listar_btn_indicator.place(x=3, y=250)

        listar_lb = CTkLabel(menu_bar_frame, text="Usuários", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        listar_lb.place(x=50, y=250)
        listar_lb.bind("<Button-1>", lambda e: switch_indication(about_btn_indicator, about_page))

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
        about_lb.place(x=50, y=310)
        about_lb.bind("<Button-1>", lambda e: switch_indication(about_btn_indicator, about_page))

        # posicionando o menu bar frame
        menu_bar_frame.pack(side="left", fill="y", pady=4, padx=3)
        menu_bar_frame.pack_propagate(False)
        menu_bar_frame.configure(width=50, fg_color=menu_bar_color)

        # Botão Logout
        logout_btn = CTkButton(menu_bar_frame, image=logout, text="",
                            fg_color=menu_bar_color, hover_color=menu_bar_color,
                            command=lambda: self.realizar_logout(nova_janela),
                            width=30, height=40)
        logout_btn.place(x=9, y=500)
        
        logout_btn_indicator = CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3 , height=40)
        logout_btn_indicator.place(x=3, y=500)

        logout_lb = CTkLabel(menu_bar_frame, text="Logout", fg_color=menu_bar_color,
                            text_color="white", font=("Bold", 15), anchor="w")
        logout_lb.place(x=50, y=505)
        logout_lb.bind("<Button-1>", lambda e: self.realizar_logout(nova_janela))

        nova_janela.mainloop()

Aplication()