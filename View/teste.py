import tkinter as tk
from tkinter import ttk

class NumericTreeview(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Treeview Apenas Números")
        self.geometry("300x200")

        # 1. Configurar a função de validação
        vcmd = (self.register(self.validate_numeric), '%P')
        self.entry_editor = tk.Entry(self, validate="key", validatecommand=vcmd)
        
        # Criar Treeview
        self.tree = ttk.Treeview(self, columns=('Valor'), show='headings')
        self.tree.heading('Valor', text='Valor Numérico')
        self.tree.pack(pady=10)

        # Inserir alguns dados de exemplo
        self.tree.insert('', tk.END, values=('1z'))
        self.tree.insert('', tk.END, values=('456'))
        self.tree.insert('', tk.END, values=('789'))

        # 2. Vincular evento de clique duplo
        self.tree.bind('<Double-1>', self.on_double_click)

    # Função de validação: aceita apenas dígitos
    def validate_numeric(self, P):
        """Valida se a entrada contém apenas dígitos."""
        if P.isdigit() or P == "":
            return True
        else:
            self.bell() # Toca um som de alerta
            return False

    # Função para lidar com o clique duplo
    def on_double_click(self, event):
        """Inicia a edição da célula com um Entry validado."""
        # Identificar a região e o item clicado
        region = self.tree.identify_region(event.x, event.y)
        if region == "tree":
            return
            
        column = self.tree.identify_column(event.x, event.y)
        if column != "#1": # Apenas permite editar a coluna "Valor" (primeira coluna personalizada)
            return

        item_id = self.tree.identify_row(event.x, event.y)
        if not item_id:
            return

        # Obter o valor atual e as dimensões da célula
        current_value = self.tree.item(item_id, 'values')[0]
        bbox = self.tree.bbox(item_id, column)

        # Posicionar o Entry sobre a célula
        self.entry_editor.place(x=bbox[0], y=bbox[1], w=bbox[2], h=bbox[3])
        self.entry_editor.insert(0, current_value)
        self.entry_editor.focus_set()
        
        # Vincular eventos para finalizar a edição
        self.entry_editor.bind('<Return>', lambda e: self.save_edit(item_id))
        self.entry_editor.bind('<FocusOut>', lambda e: self.save_edit(item_id))

    # Função para salvar a edição
    def save_edit(self, item_id):
        """Salva o novo valor e remove o Entry."""
        new_value = self.entry_editor.get()
        if new_value.isdigit():
            self.tree.item(item_id, values=(new_value,))
        
        self.entry_editor.place_forget()

if __name__ == '__main__':
    app = NumericTreeview()
    app.mainloop()
