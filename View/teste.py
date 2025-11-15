from customtkinter import *
from PIL import Image
import customtkinter


def janela_nova(self):
    # Fecha a janela de login
    self.root.destroy()

    nova_janela = customtkinter.CTk()
    nova_janela.geometry("900x600")
    nova_janela.title("Sistema de Biblioteca")

    menu_min_width = 45
    menu_max_width = 200
    animation_step = 15    # passo de cada iteração (ajuste para mais/menos "suavidade")
    animation_delay = 12   # ms entre passos

    menu_bar_color = '#2b2b2b'

    # Ícones (ajuste os paths conforme necessário)
    toggle_icon = customtkinter.CTkImage(Image.open("View/images/toggle_btn_icon.png"))
    close_btn_icon = customtkinter.CTkImage(Image.open("View/images/close_btn_icon.png"), size=(25,25))
    home_icon = customtkinter.CTkImage(Image.open("View/images/home_icon.png"), size=(25, 25))
    livro_icon = customtkinter.CTkImage(Image.open("View/images/livro_btn3.png"), size=(25, 25))
    multas_icon = customtkinter.CTkImage(Image.open("View/images/multas_btn.png"), size=(25, 25))
    about_icon = customtkinter.CTkImage(Image.open("View/images/about_icon.png"), size=(25, 25))

    # Estado de animação
    is_animating = {"value": False}  # dict para permitir mutação dentro de closures
    target_width = {"value": menu_min_width}  # largura que queremos atingir

    # Páginas
    def limpar_e_mostrar(page_fn):
        for child in page_frame.winfo_children():
            child.destroy()
        page_fn()

    def home_page():
        fm = customtkinter.CTkFrame(page_frame)
        lb = customtkinter.CTkLabel(fm, text="Home Page", font=("Bold", 20))
        lb.place(x=100, y=200)
        fm.pack(fill="both", expand=True)

    def livros_page():
        fm = customtkinter.CTkFrame(page_frame)
        lb = customtkinter.CTkLabel(fm, text="Livros Page", font=("Bold", 20))
        lb.place(x=100, y=200)
        fm.pack(fill="both", expand=True)

    def multas_page():
        fm = customtkinter.CTkFrame(page_frame)
        lb = customtkinter.CTkLabel(fm, text="Multas", font=("Bold", 20))
        lb.place(x=100, y=200)
        fm.pack(fill="both", expand=True)

    def about_page():
        fm = customtkinter.CTkFrame(page_frame)
        lb = customtkinter.CTkLabel(fm, text="About Page", font=("Bold", 20))
        lb.place(x=100, y=200)
        fm.pack(fill="both", expand=True)

    # Área principal das páginas
    page_frame = customtkinter.CTkFrame(nova_janela)
    page_frame.place(x=50, y=0, relwidth=1.0, relheight=1.0)
    limpar_e_mostrar(home_page)

    # Menu lateral
    menu_bar_frame = customtkinter.CTkFrame(nova_janela, fg_color=menu_bar_color)
    menu_bar_frame.pack(side="left", fill="y", pady=4, padx=3)
    menu_bar_frame.pack_propagate(False)
    menu_bar_frame.configure(width=menu_min_width)

    # Função de animação universal (faz expandir ou recolher até target_width)
    def run_animation():
        if is_animating["value"] is False:
            return  # não há animação pendente

        current = menu_bar_frame.winfo_width()
        tgt = target_width["value"]

        if current == tgt:
            is_animating["value"] = False
            # atualiza ícone do toggle conforme estado
            if tgt == menu_min_width:
                toggle_menu_btn.configure(image=toggle_icon, command=start_expand)
            else:
                toggle_menu_btn.configure(image=close_btn_icon, command=start_collapse)
            return

        # calcula próximo passo sem ultrapassar target
        if current < tgt:
            new_w = min(current + animation_step, tgt)
        else:
            new_w = max(current - animation_step, tgt)

        menu_bar_frame.configure(width=new_w)
        nova_janela.after(animation_delay, run_animation)

    # funções que disparam animação, mas evitam concorrência
    def start_expand():
        if is_animating["value"]:
            return
        is_animating["value"] = True
        target_width["value"] = menu_max_width
        # mudar ícone só depois que atingir target (o run_animation fará isso)
        run_animation()

    def start_collapse():
        if is_animating["value"]:
            return
        is_animating["value"] = True
        target_width["value"] = menu_min_width
        run_animation()

    # alterna baseado no estado atual
    def toggle_action():
        if is_animating["value"]:
            return
        if menu_bar_frame.winfo_width() <= menu_min_width:
            start_expand()
        else:
            start_collapse()

    # Indicadores de botões (apenas atualiza cor e troca página)
    def switch_indication(indicator_lb, page_fn):
        # reset indicadores
        for lbl in (home_btn_indicator, livro_btn_indicator, multas_btn_indicator, about_btn_indicator):
            lbl.configure(fg_color=menu_bar_color)
        indicator_lb.configure(fg_color='white')

        # troca a página
        limpar_e_mostrar(page_fn)

        # se a barra estiver expandida, recolhe
        if menu_bar_frame.winfo_width() > menu_min_width:
            start_collapse()

    # Botão do menu (toggle)
    toggle_menu_btn = customtkinter.CTkButton(menu_bar_frame, image=toggle_icon, text="",
                                             fg_color=menu_bar_color, hover_color=menu_bar_color,
                                             command=toggle_action, width=30, height=30)
    toggle_menu_btn.place(x=4, y=10)

    # Botão Home
    home_btn = customtkinter.CTkButton(menu_bar_frame, image=home_icon, text="",
                                       fg_color=menu_bar_color, hover_color=menu_bar_color,
                                       command=lambda: switch_indication(home_btn_indicator, home_page),
                                       width=30, height=40)
    home_btn.place(x=9, y=130)

    home_btn_indicator = customtkinter.CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3)
    home_btn_indicator.place(x=3, y=130)

    home_page_lb = customtkinter.CTkLabel(menu_bar_frame, text="Home", fg_color=menu_bar_color,
                                         text_color="white", font=("Bold", 15), anchor="w")
    home_page_lb.place(x=45, y=130)
    home_page_lb.bind("<Button-1>", lambda e: switch_indication(home_btn_indicator, home_page))

    # Botão Livros
    livro_btn = customtkinter.CTkButton(menu_bar_frame, image=livro_icon, text="",
                                        fg_color=menu_bar_color, hover_color=menu_bar_color,
                                        command=lambda: switch_indication(livro_btn_indicator, livros_page),
                                        width=30, height=40)
    livro_btn.place(x=9, y=190)

    livro_btn_indicator = customtkinter.CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3)
    livro_btn_indicator.place(x=3, y=190)

    livro_lb = customtkinter.CTkLabel(menu_bar_frame, text="Serviços", fg_color=menu_bar_color,
                                     text_color="white", font=("Bold", 15), anchor="w")
    livro_lb.place(x=45, y=190)
    livro_lb.bind("<Button-1>", lambda e: switch_indication(livro_btn_indicator, livros_page))

    # Botão Multas
    multas_btn = customtkinter.CTkButton(menu_bar_frame, image=multas_icon, text="",
                                         fg_color=menu_bar_color, hover_color=menu_bar_color,
                                         command=lambda: switch_indication(multas_btn_indicator, multas_page),
                                         width=30, height=40)
    multas_btn.place(x=9, y=250)

    multas_btn_indicator = customtkinter.CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3)
    multas_btn_indicator.place(x=3, y=250)

    multas_lb = customtkinter.CTkLabel(menu_bar_frame, text="Multas", fg_color=menu_bar_color,
                                       text_color="white", font=("Bold", 15), anchor="w")
    multas_lb.place(x=45, y=250)
    multas_lb.bind("<Button-1>", lambda e: switch_indication(multas_btn_indicator, multas_page))

    # Botão Sobre
    about_btn = customtkinter.CTkButton(menu_bar_frame, image=about_icon, text="",
                                        fg_color=menu_bar_color, hover_color=menu_bar_color,
                                        command=lambda: switch_indication(about_btn_indicator, about_page),
                                        width=30, height=40)
    about_btn.place(x=9, y=310)

    about_btn_indicator = customtkinter.CTkLabel(menu_bar_frame, text="", fg_color=menu_bar_color, width=3)
    about_btn_indicator.place(x=3, y=310)

    about_lb = customtkinter.CTkLabel(menu_bar_frame, text="Sobre", fg_color=menu_bar_color,
                                      text_color="white", font=("Bold", 15), anchor="w")
    about_lb.place(x=45, y=310)
    about_lb.bind("<Button-1>", lambda e: switch_indication(about_btn_indicator, about_page))

    nova_janela.mainloop()
