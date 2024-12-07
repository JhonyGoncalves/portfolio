import tkinter as tk
from tkinter import messagebox, filedialog
from ttkbootstrap import Style
import sqlite3
from product import Product
from db import create_tables
from datetime import datetime

class ProductManagementApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme="cyborg")
        self.root.title("Sistema de Gerenciamento de Produtos")
        self.root.geometry("800x600")
        self.root.resizable(False, False) 

        create_tables()
        self.create_frames()
        self.create_top_buttons()
        self.create_list_frame()
        self.load_products()

    def create_frames(self):
        self.top_frame = tk.Frame(self.root, bg="black", height=50)
        self.top_frame.pack(fill="x", padx=20, pady=20)

        self.middle_frame = tk.Frame(self.root, bg="black", height=200)
        self.middle_frame.pack(fill="x", padx=20, pady=20)

        self.bottom_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.bottom_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        self.bottom_frame.grid_rowconfigure(1, weight=1)
        self.bottom_frame.grid_columnconfigure(0, weight=1)

    def create_top_buttons(self):
        self.cadastrar_button = tk.Button(self.top_frame, text="Cadastrar", bg="orange", fg="black", command=self.show_register_frame)
        self.cadastrar_button.pack(side="left", padx=5, pady=5)

        self.editar_button = tk.Button(self.top_frame, text="Editar", bg="orange", fg="black", command=self.show_edit_frame)
        self.editar_button.pack(side="left", padx=5, pady=5)

        self.remover_button = tk.Button(self.top_frame, text="Remover", bg="red", fg="white", command=self.show_remove_frame)
        self.remover_button.pack(side="left", padx=5, pady=5)

        self.gerar_relatorio_button = tk.Button(self.top_frame, text="Gerar Relatório", bg="orange", fg="black", command=self.generate_report)
        self.gerar_relatorio_button.pack(side="right", padx=5, pady=5)

    def create_list_frame(self):
        self.search_bar = tk.Entry(self.bottom_frame, bg="white")
        self.search_bar.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.search_button = tk.Button(self.bottom_frame, text="Pesquisar", bg="black", fg="white", command=self.search_product)
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        self.copy_button = tk.Button(self.bottom_frame, text="Copiar ID", bg="blue", fg="white", command=self.copy_selected_id)
        self.copy_button.grid(row=0, column=2, padx=5, pady=5)

        self.tree = tk.ttk.Treeview(self.bottom_frame, columns=("ID", "Nome", "Categoria", "Localização", "Estoque", "Preço"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Localização", text="Localização")
        self.tree.heading("Estoque", text="Estoque")
        self.tree.heading("Preço", text="Preço")
        self.tree.column("ID", stretch=True, width=100, anchor="center")
        self.tree.column("Nome", stretch=True, width=150, anchor="center")
        self.tree.column("Categoria", stretch=True, width=150, anchor="center")
        self.tree.column("Localização", stretch=True, width=150, anchor="center")
        self.tree.column("Estoque", stretch=True, width=100, anchor="center")
        self.tree.column("Preço", stretch=True, width=100, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

    def copy_selected_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            if item_values:
                self.root.clipboard_clear()
                self.root.clipboard_append(item_values[0]) 
                self.root.update()
                messagebox.showinfo("Sucesso", "ID copiado para a área de transferência.")
            else:
                messagebox.showerror("Erro", "Nenhum ID encontrado na seleção.")
        else:
            messagebox.showerror("Erro", "Nenhum item selecionado.")

    def clear_middle_frame(self):
        for widget in self.middle_frame.winfo_children():
            widget.destroy()

    def show_register_frame(self):
        self.clear_middle_frame()
        
        tk.Label(self.middle_frame, text="Nome", fg="green", bg="black").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.middle_frame, bg="white")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.middle_frame, text="Categoria", fg="green", bg="black").grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = tk.Entry(self.middle_frame, bg="white")
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.middle_frame, text="Estoque", fg="blue", bg="black").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.middle_frame, bg="white")
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.middle_frame, text="Localização", fg="blue", bg="black").grid(row=1, column=2, padx=5, pady=5)
        self.location_entry = tk.Entry(self.middle_frame, bg="white")
        self.location_entry.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(self.middle_frame, text="Estoque Mínimo", fg="green", bg="black").grid(row=2, column=0, padx=5, pady=5)
        self.min_stock_entry = tk.Entry(self.middle_frame, bg="white")
        self.min_stock_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.middle_frame, text="Preço", fg="green", bg="black").grid(row=2, column=2, padx=5, pady=5)
        self.price_entry = tk.Entry(self.middle_frame, bg="white")
        self.price_entry.grid(row=2, column=3, padx=5, pady=5)

        self.register_button = tk.Button(self.middle_frame, text="Concluir", bg="green", fg="white", command=self.register_product)
        self.register_button.grid(row=3, column=0, columnspan=4, pady=10)

    def show_edit_frame(self):
        self.clear_middle_frame()
        tk.Label(self.middle_frame, text="Digite o ID do produto para editar", fg="orange", bg="black").grid(row=0, column=0, padx=5, pady=5)
        self.edit_id_entry = tk.Entry(self.middle_frame, bg="white")
        self.edit_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.edit_button = tk.Button(self.middle_frame, text="Carregar", bg="orange", fg="black", command=self.load_edit_product)
        self.edit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def show_remove_frame(self):
        self.clear_middle_frame()
        tk.Label(self.middle_frame, text="Digite o ID do produto para remover", fg="red", bg="black").grid(row=0, column=0, padx=5, pady=5)
        self.remove_id_entry = tk.Entry(self.middle_frame, bg="white")
        self.remove_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(self.middle_frame, text="Remover", bg="red", fg="white", command=self.remove_product)
        self.remove_button.grid(row=1, column=0, columnspan=2, pady=10)

    def register_product(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        quantity = self.quantity_entry.get()
        location = self.location_entry.get()
        min_stock = self.min_stock_entry.get()
        price = self.price_entry.get()

        if not all([name, category, quantity, location, min_stock, price]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        new_product = Product(name, category, min_stock, float(price))

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products (ID, name, category, acpt_stock, price)
            VALUES (?, ?, ?, ?, ?)
        """, (new_product.id, name, category, min_stock, price))

        cursor.execute("""
            INSERT INTO stock (ID, quantity, location)
            VALUES (?, ?, ?)
        """, (new_product.id, quantity, location))

        connection.commit()
        connection.close()

        self.tree.insert("", "end", values=(new_product.id, name, category, location, quantity, price))

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        cursor.execute("SELECT p.ID, p.name, p.category, s.location, s.quantity, p.price FROM products p JOIN stock s ON p.ID = s.ID")
        results = cursor.fetchall()

        connection.close()

        for row in results:
            self.tree.insert("", "end", values=row)

    def remove_product(self):
        product_id = self.remove_id_entry.get()
        if not product_id:
            messagebox.showerror("Erro", "Digite um ID válido.")
            return

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        cursor.execute("DELETE FROM products WHERE ID = ?", (product_id,))
        cursor.execute("DELETE FROM stock WHERE ID = ?", (product_id,))

        connection.commit()
        connection.close()

        self.load_products()
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")

    def load_edit_product(self):
        product_id = self.edit_id_entry.get()
        if not product_id:
            messagebox.showerror("Erro", "Digite um ID válido.")
            return

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        cursor.execute("SELECT p.name, p.category, s.quantity, s.location, p.acpt_stock, p.price FROM products p JOIN stock s ON p.ID = s.ID WHERE p.ID = ?", (product_id,))
        result = cursor.fetchone()

        connection.close()

        if not result:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        self.clear_middle_frame()

        tk.Label(self.middle_frame, text="Nome", fg="green", bg="black").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.middle_frame, bg="white")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, result[0])

        tk.Label(self.middle_frame, text="Categoria", fg="green", bg="black").grid(row=0, column=2, padx=5, pady=5)
        self.category_entry = tk.Entry(self.middle_frame, bg="white")
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)
        self.category_entry.insert(0, result[1])

        tk.Label(self.middle_frame, text="Estoque", fg="blue", bg="black").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = tk.Entry(self.middle_frame, bg="white")
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)
        self.quantity_entry.insert(0, result[2])

        tk.Label(self.middle_frame, text="Localização", fg="blue", bg="black").grid(row=1, column=2, padx=5, pady=5)
        self.location_entry = tk.Entry(self.middle_frame, bg="white")
        self.location_entry.grid(row=1, column=3, padx=5, pady=5)
        self.location_entry.insert(0, result[3])

        tk.Label(self.middle_frame, text="Estoque Mínimo", fg="green", bg="black").grid(row=2, column=0, padx=5, pady=5)
        self.min_stock_entry = tk.Entry(self.middle_frame, bg="white")
        self.min_stock_entry.grid(row=2, column=1, padx=5, pady=5)
        self.min_stock_entry.insert(0, result[4])

        tk.Label(self.middle_frame, text="Preço", fg="green", bg="black").grid(row=2, column=2, padx=5, pady=5)
        self.price_entry = tk.Entry(self.middle_frame, bg="white")
        self.price_entry.grid(row=2, column=3, padx=5, pady=5)
        self.price_entry.insert(0, result[5])

        self.update_button = tk.Button(self.middle_frame, text="Atualizar", bg="green", fg="white", command=lambda: self.update_product(product_id))
        self.update_button.grid(row=3, column=0, columnspan=4, pady=10)

    def update_product(self, product_id):
        name = self.name_entry.get()
        category = self.category_entry.get()
        quantity = self.quantity_entry.get()
        location = self.location_entry.get()
        min_stock = self.min_stock_entry.get()
        price = self.price_entry.get()

        if not all([name, category, quantity, location, min_stock, price]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE products SET name = ?, category = ?, acpt_stock = ?, price = ? WHERE ID = ?
        """, (name, category, min_stock, price, product_id))

        cursor.execute("""
            UPDATE stock SET quantity = ?, location = ? WHERE ID = ?
        """, (quantity, location, product_id))

        connection.commit()
        connection.close()

        self.load_products()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

    def search_product(self):
        search_term = self.search_bar.get()

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        query = "SELECT p.ID, p.name, p.category, s.location, s.quantity, p.price FROM products p JOIN stock s ON p.ID = s.ID WHERE p.name LIKE ? OR p.ID = ?"
        cursor.execute(query, (f"%{search_term}%", search_term))
        results = cursor.fetchall()

        connection.close()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in results:
            self.tree.insert("", "end", values=row)

    def generate_report(self):
        default_name = f"report-{datetime.now().strftime('%d-%m-%Y')}.txt"
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_name, filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        connection = sqlite3.connect('products.db')
        cursor = connection.cursor()

        cursor.execute("SELECT p.ID, p.name, p.category, s.location, s.quantity, p.price FROM products p JOIN stock s ON p.ID = s.ID WHERE s.quantity < p.acpt_stock")
        low_stock_results = cursor.fetchall()

        cursor.execute("SELECT p.ID, p.name, p.category, s.location, s.quantity, p.price FROM products p JOIN stock s ON p.ID = s.ID")
        all_results = cursor.fetchall()

        connection.close()

        with open(file_path, "w") as file:
            file.write("Relatório de Produtos\n")
            file.write("=" * 50 + "\n")
            file.write("Produtos com estoque abaixo do mínimo:\n")
            file.write("-" * 50 + "\n")
            for row in low_stock_results:
                file.write(f"ID: {row[0]}\n")
                file.write(f"Nome: {row[1]}\n")
                file.write(f"Categoria: {row[2]}\n")
                file.write(f"Localização: {row[3]}\n")
                file.write(f"Estoque: {row[4]}\n")
                file.write(f"Preço: {row[5]}\n")
                file.write("-" * 50 + "\n")

            file.write("Todos os produtos:\n")
            file.write("=" * 50 + "\n")
            for row in all_results:
                file.write(f"ID: {row[0]}\n")
                file.write(f"Nome: {row[1]}\n")
                file.write(f"Categoria: {row[2]}\n")
                file.write(f"Localização: {row[3]}\n")
                file.write(f"Estoque: {row[4]}\n")
                file.write(f"Preço: {row[5]}\n")
                file.write("-" * 50 + "\n")

        messagebox.showinfo("Sucesso", f"Relatório salvo em: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManagementApp(root)
    root.mainloop()