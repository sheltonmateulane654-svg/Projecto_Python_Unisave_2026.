
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, date, timedelta
import os
import tempfile

# =====================================================
# CONFIGURACOES
# =====================================================

DB_NAME = "sx_pharmacy.db"

BG = "#F3F8F5"
CARD = "#FFFFFF"
BORDER = "#D7E7DD"
PRIMARY = "#168A5B"
TEXT = "#24352C"
MUTED = "#718477"
GREEN = "#0F766E"
RED = "#DC2626"
YELLOW = "#D99A18"

ACCOUNT_HOLDER = "SHELTON XAVIER MATEULANE"
ACCOUNT_NUMBER = "867474379"

CATEGORIES = [
    "Analgésicos", "Antibióticos", "Anti-inflamatórios",
    "Antialérgicos", "Antigripais", "Vitaminas e suplementos",
    "Medicamentos cardiovasculares", "Medicamentos digestivos",
    "Antidiabéticos", "Dermatológicos", "Oftálmicos",
    "Higiene e cuidados pessoais", "Material médico",
    "Primeiros socorros", "Outros"
]

FORMS = [
    "Comprimido", "Cápsula", "Xarope", "Suspensão oral",
    "Gotas", "Creme", "Pomada", "Gel", "Injecção",
    "Solução", "Supositório", "Spray", "Saqueta", "Unidade"
]

PAYMENTS = [
    "Numerário", "M-Pesa", "e-Mola", "POS", "Transferência"
]


# =====================================================
# APLICACAO PRINCIPAL
# =====================================================

class SXPharmacy:

    def __init__(self, root):
        self.root = root
        self.root.title("SX PHARMACY MANAGEMENT | SX TECH & DESIGN")
        self.root.geometry("1350x820")
        self.root.minsize(1080, 680)
        self.root.configure(bg=BG)

        self.db = sqlite3.connect(DB_NAME)
        self.db.execute("PRAGMA foreign_keys = ON")

        self.create_database()
        self.setup_style()
        self.build_interface()
        self.refresh_all()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # =================================================
    # BASE DE DADOS
    # =================================================

    def create_database(self):

        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            active_ingredient TEXT DEFAULT '',
            strength TEXT DEFAULT '',
            form TEXT DEFAULT '',
            presentation TEXT DEFAULT '',
            batch TEXT DEFAULT '',
            expiry TEXT DEFAULT '',
            supplier TEXT DEFAULT '',
            cost REAL DEFAULT 0,
            price REAL DEFAULT 0,
            stock INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 5,
            prescription_required TEXT DEFAULT 'Não'
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            batch TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total REAL NOT NULL,
            payment TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
        """)

        self.db.commit()

    # =================================================
    # ESTILO
    # =================================================

    def setup_style(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=CARD,
            foreground=TEXT,
            fieldbackground=CARD,
            rowheight=30,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background="#E7F1EB",
            foreground=TEXT,
            font=("Segoe UI", 9, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", PRIMARY)],
            foreground=[("selected", "#FFFFFF")]
        )

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background="#E7F1EB",
            foreground=TEXT,
            padding=(14, 10),
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", PRIMARY)],
            foreground=[("selected", "#FFFFFF")]
        )

        style.configure(
            "TCombobox",
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            padding=5
        )

    # =================================================
    # COMPONENTES
    # =================================================

    def button(self, parent, text, command,
               color=PRIMARY, width=19):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="#FFFFFF",
            activebackground=color,
            activeforeground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            width=width,
            padx=7,
            pady=9
        )

    def entry(self, parent, variable, width=30):

        return tk.Entry(
            parent,
            textvariable=variable,
            width=width,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="solid",
            bd=1,
            font=("Segoe UI", 10)
        )

    def label(self, parent, text):

        return tk.Label(
            parent,
            text=text,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9)
        )

    # =================================================
    # INTERFACE PRINCIPAL
    # =================================================

    def build_interface(self):

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=22, pady=15)

        tk.Label(
            header,
            text="SX",
            bg=BG,
            fg=PRIMARY,
            font=("Segoe UI", 32, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text=" PHARMACY MANAGEMENT",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 19, "bold")
        ).pack(side="left", pady=9)

        tk.Label(
            header,
            text="FARMÁCIA | SX TECH & DESIGN",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="right", pady=17)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(
            fill="both",
            expand=True,
            padx=17,
            pady=5
        )

        self.dashboard_tab = tk.Frame(self.tabs, bg=BG)
        self.products_tab = tk.Frame(self.tabs, bg=BG)
        self.sales_tab = tk.Frame(self.tabs, bg=BG)
        self.purchases_tab = tk.Frame(self.tabs, bg=BG)
        self.expiry_tab = tk.Frame(self.tabs, bg=BG)
        self.history_tab = tk.Frame(self.tabs, bg=BG)
        self.payment_tab = tk.Frame(self.tabs, bg=BG)

        tabs = [
            (self.dashboard_tab, "Dashboard"),
            (self.products_tab, "Medicamentos e Stock"),
            (self.sales_tab, "Vendas"),
            (self.purchases_tab, "Compras"),
            (self.expiry_tab, "Validades"),
            (self.history_tab, "Histórico"),
            (self.payment_tab, "Dados de Pagamento")
        ]

        for frame, title in tabs:
            self.tabs.add(frame, text=title)

        self.build_dashboard()
        self.build_products()
        self.build_operation(self.sales_tab, "Venda")
        self.build_operation(self.purchases_tab, "Compra")
        self.build_expiry()
        self.build_history()
        self.build_payment()

    # =================================================
    # DASHBOARD
    # =================================================

    def build_dashboard(self):

        tk.Label(
            self.dashboard_tab,
            text="PAINEL DE CONTROLO",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=20, pady=22)

        cards = tk.Frame(self.dashboard_tab, bg=BG)
        cards.pack(fill="x", padx=14)

        self.stats = {}

        items = [
            ("Medicamentos registados", "products"),
            ("Unidades em stock", "stock"),
            ("Produtos com stock baixo", "low"),
            ("Vendas de hoje (MZN)", "revenue")
        ]

        for title, key in items:

            card = tk.Frame(
                cards,
                bg=CARD,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=6,
                pady=8
            )

            tk.Label(
                card,
                text=title,
                bg=CARD,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(pady=(18, 6))

            value = tk.Label(
                card,
                text="0",
                bg=CARD,
                fg=PRIMARY,
                font=("Segoe UI", 20, "bold")
            )

            value.pack(pady=(0, 18))
            self.stats[key] = value

        tk.Label(
            self.dashboard_tab,
            text="Sistema administrativo de gestão de farmácia",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 11)
        ).pack(pady=45)

    def refresh_dashboard(self):

        today = date.today().isoformat()

        products = self.db.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        stock = self.db.execute(
            "SELECT COALESCE(SUM(stock),0) FROM products"
        ).fetchone()[0]

        low = self.db.execute(
            "SELECT COUNT(*) FROM products WHERE stock<=min_stock"
        ).fetchone()[0]

        revenue = self.db.execute("""
            SELECT COALESCE(SUM(total),0)
            FROM transactions
            WHERE kind='Venda'
            AND substr(created_at,1,10)=?
        """, (today,)).fetchone()[0]

        self.stats["products"].configure(text=str(products))
        self.stats["stock"].configure(text=str(stock))
        self.stats["low"].configure(text=str(low))
        self.stats["revenue"].configure(
            text=f"{revenue:,.2f}"
        )

    # =================================================
    # MEDICAMENTOS
    # =================================================

    def build_products(self):

        top = tk.Frame(self.products_tab, bg=BG)
        top.pack(fill="x", padx=14, pady=15)

        tk.Label(
            top,
            text="CATÁLOGO DE MEDICAMENTOS",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")

        self.search_var = tk.StringVar()

        self.entry(
            top, self.search_var, 25
        ).pack(side="right", padx=5, ipady=5)

        tk.Label(
            top,
            text="Pesquisar:",
            bg=BG,
            fg=MUTED
        ).pack(side="right")

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh_products()
        )

        cols = (
            "id", "category", "name", "ingredient",
            "strength", "form", "batch", "expiry",
            "cost", "price", "stock"
        )

        self.product_tree = ttk.Treeview(
            self.products_tab,
            columns=cols,
            show="headings"
        )

        headings = {
            "id": "ID",
            "category": "Categoria",
            "name": "Medicamento",
            "ingredient": "Princípio activo",
            "strength": "Dosagem",
            "form": "Forma",
            "batch": "Lote",
            "expiry": "Validade",
            "cost": "Compra",
            "price": "Venda",
            "stock": "Stock"
        }

        widths = {
            "id": 40,
            "category": 125,
            "name": 145,
            "ingredient": 145,
            "strength": 80,
            "form": 85,
            "batch": 80,
            "expiry": 90,
            "cost": 85,
            "price": 85,
            "stock": 60
        }

        for col in cols:
            self.product_tree.heading(
                col,
                text=headings[col]
            )
            self.product_tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        self.product_tree.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=5
        )

        bar = tk.Frame(self.products_tab, bg=BG)
        bar.pack(fill="x", padx=14, pady=12)

        self.button(
            bar, "Adicionar medicamento",
            self.add_product
        ).pack(side="left", padx=4)

        self.button(
            bar, "Editar seleccionado",
            self.edit_product
        ).pack(side="left", padx=4)

        self.button(
            bar, "Actualizar",
            self.refresh_products,
            "#64796D"
        ).pack(side="left", padx=4)

    def refresh_products(self):

        if not hasattr(self, "product_tree"):
            return

        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        term = self.search_var.get().lower()

        rows = self.db.execute(
            "SELECT * FROM products ORDER BY name"
        ).fetchall()

        for p in rows:

            if term and term not in " ".join(
                str(x) for x in p
            ).lower():
                continue

            self.product_tree.insert(
                "",
                "end",
                values=(
                    p[0], p[1], p[2], p[3], p[4],
                    p[5], p[7], p[8],
                    f"{p[10]:.2f}",
                    f"{p[11]:.2f}",
                    p[12]
                )
            )

    def product_form(self, product=None):

        win = tk.Toplevel(self.root)
        win.title("Medicamento")
        win.geometry("560x790")
        win.configure(bg=BG)
        win.transient(self.root)
        win.grab_set()

        edit = product is not None

        tk.Label(
            win,
            text="EDITAR MEDICAMENTO" if edit else "NOVO MEDICAMENTO",
            bg=BG,
            fg=PRIMARY,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=13)

        fields = [
            ("Categoria", "category", product[1] if edit else CATEGORIES[0], CATEGORIES),
            ("Nome do medicamento/produto", "name", product[2] if edit else "", None),
            ("Princípio activo", "ingredient", product[3] if edit else "", None),
            ("Dosagem/concentração", "strength", product[4] if edit else "", None),
            ("Forma farmacêutica", "form", product[5] if edit else "Comprimido", FORMS),
            ("Apresentação", "presentation", product[6] if edit else "", None),
            ("Número do lote", "batch", product[7] if edit else "", None),
            ("Data de validade (AAAA-MM-DD)", "expiry", product[8] if edit else "", None),
            ("Fornecedor", "supplier", product[9] if edit else "", None),
            ("Preço de compra (MZN)", "cost", str(product[10]) if edit else "0", None),
            ("Preço de venda (MZN)", "price", str(product[11]) if edit else "0", None),
            ("Stock (unidades)", "stock", str(product[12]) if edit else "0", None),
            ("Stock mínimo", "minimum", str(product[13]) if edit else "5", None),
            ("Exige receita? (Sim/Não)", "prescription", product[14] if edit else "Não", ["Não", "Sim"])
        ]

        # Área de edição com scroll vertical
        scroll_container = tk.Frame(win, bg=BG)
        scroll_container.pack(
            fill="both", expand=True, padx=18, pady=(0, 5)
        )

        canvas = tk.Canvas(
            scroll_container,
            bg=BG,
            highlightthickness=0,
            borderwidth=0
        )
        scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=canvas.yview
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = tk.Frame(canvas, bg=BG)
        body_window = canvas.create_window(
            (0, 0), window=body, anchor="nw"
        )

        def update_scroll_region(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_body(event):
            canvas.itemconfigure(body_window, width=event.width)

        body.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_body)

        # Scroll com a roda do rato
        def mousewheel(event):
            if event.delta:
                canvas.yview_scroll(
                    int(-1 * (event.delta / 120)), "units"
                )

        canvas.bind_all("<MouseWheel>", mousewheel)

        vars_ = {}

        for caption, key, value, options in fields:

            self.label(body, caption).pack(
                anchor="w",
                pady=(7, 3)
            )

            var = tk.StringVar(value=value)
            vars_[key] = var

            if options:
                widget = ttk.Combobox(
                    body,
                    textvariable=var,
                    values=options,
                    state="readonly",
                    width=48
                )
                widget.pack(fill="x", ipady=4)
            else:
                self.entry(
                    body, var, 50
                ).pack(fill="x", ipady=5)

        def save():

            if not messagebox.askyesno(
                "Confirmar registo",
                "Tens a certeza de que pretendes confirmar e guardar "
                "os dados deste medicamento?"
            ):
                return

            try:

                name = vars_["name"].get().strip()
                category = vars_["category"].get().strip()

                if not name or not category:
                    raise ValueError(
                        "Indica a categoria e o nome."
                    )

                expiry = vars_["expiry"].get().strip()

                if expiry:
                    datetime.strptime(expiry, "%Y-%m-%d")

                cost = float(
                    vars_["cost"].get().replace(",", ".")
                )

                price = float(
                    vars_["price"].get().replace(",", ".")
                )

                stock = int(vars_["stock"].get())
                minimum = int(vars_["minimum"].get())

                if min(cost, price, stock, minimum) < 0:
                    raise ValueError(
                        "Os valores não podem ser negativos."
                    )

                data = (
                    category,
                    name,
                    vars_["ingredient"].get().strip(),
                    vars_["strength"].get().strip(),
                    vars_["form"].get().strip(),
                    vars_["presentation"].get().strip(),
                    vars_["batch"].get().strip(),
                    expiry,
                    vars_["supplier"].get().strip(),
                    cost,
                    price,
                    stock,
                    minimum,
                    vars_["prescription"].get()
                )

                with self.db:
                    if edit:
                        self.db.execute("""
                            UPDATE products SET
                            category=?, name=?, active_ingredient=?,
                            strength=?, form=?, presentation=?,
                            batch=?, expiry=?, supplier=?, cost=?,
                            price=?, stock=?, min_stock=?,
                            prescription_required=?
                            WHERE id=?
                        """, data + (product[0],))

                    else:
                        self.db.execute("""
                            INSERT INTO products (
                                category, name, active_ingredient,
                                strength, form, presentation,
                                batch, expiry, supplier, cost,
                                price, stock, min_stock,
                                prescription_required
                            )
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """, data)

                win.destroy()
                self.refresh_all()

                messagebox.showinfo(
                    "SX PHARMACY",
                    "Registo guardado com sucesso."
                )

            except ValueError as exc:
                messagebox.showerror(
                    "Dados inválidos", str(exc)
                )

            except sqlite3.Error as exc:
                messagebox.showerror(
                    "Base de dados", str(exc)
                )

        # Botão fixo no rodapé: permanece visível mesmo ao fazer scroll
        footer = tk.Frame(win, bg=BG)
        footer.pack(fill="x", padx=18, pady=10)

        self.button(
            footer,
            "CONFIRMAR E GUARDAR",
            save,
            width=25
        ).pack(pady=3)

    def add_product(self):
        self.product_form()

    def edit_product(self):

        selected = self.product_tree.selection()

        if not selected:
            messagebox.showwarning(
                "SX PHARMACY",
                "Selecciona um registo."
            )
            return

        pid = self.product_tree.item(
            selected[0]
        )["values"][0]

        product = self.db.execute(
            "SELECT * FROM products WHERE id=?",
            (pid,)
        ).fetchone()

        self.product_form(product)

    # =================================================
    # COMPRAS E VENDAS
    # =================================================

    def build_operation(self, tab, kind):

        tk.Label(
            tab,
            text=f"REGISTAR {kind.upper()}",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=24, pady=18)

        panel = tk.Frame(
            tab,
            bg=CARD,
            padx=24,
            pady=20,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        panel.pack(fill="x", padx=24, pady=8)

        product_var = tk.StringVar()
        quantity_var = tk.StringVar(value="1")
        payment_var = tk.StringVar(value="Numerário")

        self.label(
            panel, "Medicamento/produto"
        ).pack(anchor="w")

        combo = ttk.Combobox(
            panel,
            textvariable=product_var,
            state="readonly",
            width=75
        )

        combo.pack(fill="x", pady=(5, 14))

        self.label(
            panel, "Quantidade"
        ).pack(anchor="w")

        self.entry(
            panel, quantity_var, 15
        ).pack(anchor="w", pady=5, ipady=4)

        self.label(
            panel, "Método de pagamento"
        ).pack(anchor="w", pady=(14, 3))

        ttk.Combobox(
            panel,
            textvariable=payment_var,
            values=PAYMENTS,
            state="readonly",
            width=25
        ).pack(anchor="w")

        tk.Label(
            panel,
            text=f"Titular: {ACCOUNT_HOLDER}\nConta: {ACCOUNT_NUMBER}",
            bg=CARD,
            fg=PRIMARY,
            justify="left",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=14)

        info = tk.Label(
            tab,
            text="Selecciona um produto.",
            bg=BG,
            fg=PRIMARY,
            font=("Segoe UI", 12, "bold")
        )

        info.pack(pady=12)

        def load_choices():

            rows = self.db.execute("""
                SELECT id,name,strength,form,batch,stock,expiry
                FROM products ORDER BY name
            """).fetchall()

            combo["values"] = [
                f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | Lote {p[4]} | Stock {p[5]} | Val. {p[6]}"
                for p in rows
            ]

        def calculate(*_):

            try:

                if not product_var.get():
                    info.configure(
                        text="Selecciona um produto."
                    )
                    return

                pid = int(
                    product_var.get().split("|")[0].strip()
                )

                p = self.db.execute(
                    "SELECT * FROM products WHERE id=?",
                    (pid,)
                ).fetchone()

                qty = int(quantity_var.get())

                if qty < 1:
                    raise ValueError

                unit_price = (
                    p[10] if kind == "Compra" else p[11]
                )

                info.configure(
                    text=f"{qty} unidade(s) × {unit_price:,.2f} MZN = {qty * unit_price:,.2f} MZN"
                )

            except (ValueError, IndexError, TypeError):
                info.configure(
                    text="Verifica o produto e a quantidade."
                )

        def submit():

            try:

                if not product_var.get():
                    raise ValueError(
                        "Selecciona um produto."
                    )

                pid = int(
                    product_var.get().split("|")[0].strip()
                )

                qty = int(quantity_var.get())

                if qty < 1:
                    raise ValueError(
                        "A quantidade deve ser superior a zero."
                    )

                p = self.db.execute(
                    "SELECT * FROM products WHERE id=?",
                    (pid,)
                ).fetchone()

                if not p:
                    raise ValueError(
                        "Produto não encontrado."
                    )

                if kind == "Venda":

                    if p[12] < qty:
                        raise ValueError(
                            f"Stock insuficiente. Disponível: {p[12]}."
                        )

                    if p[8]:
                        exp = datetime.strptime(
                            p[8], "%Y-%m-%d"
                        ).date()

                        if exp < date.today():
                            raise ValueError(
                                "Este lote está fora da validade."
                            )

                    if p[14] == "Sim":
                        raise ValueError(
                            "Produto sujeito a receita. "
                            "A dispensa deve ser validada por "
                            "profissional habilitado."
                        )

                price = (
                    p[10] if kind == "Compra" else p[11]
                )

                total = qty * price

                new_stock = (
                    p[12] + qty
                    if kind == "Compra"
                    else p[12] - qty
                )

                now = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                with self.db:

                    self.db.execute(
                        "UPDATE products SET stock=? WHERE id=?",
                        (new_stock, pid)
                    )

                    cursor = self.db.execute("""
                        INSERT INTO transactions (
                            kind, product_id, product_name,
                            batch, quantity, unit_price,
                            total, payment, created_at
                        )
                        VALUES (?,?,?,?,?,?,?,?,?)
                    """, (
                        kind,
                        pid,
                        p[2],
                        p[7],
                        qty,
                        price,
                        total,
                        payment_var.get(),
                        now
                    ))

                    transaction_id = cursor.lastrowid

                self.show_receipt(
                    transaction_id,
                    kind,
                    p[2],
                    p[7],
                    qty,
                    price,
                    total,
                    payment_var.get(),
                    now
                )

                product_var.set("")
                quantity_var.set("1")

                self.refresh_all()
                load_choices()
                calculate()

            except ValueError as exc:
                messagebox.showerror(
                    "Operação não concluída", str(exc)
                )

            except sqlite3.Error as exc:
                messagebox.showerror(
                    "Base de dados", str(exc)
                )

        combo.bind(
            "<<ComboboxSelected>>", calculate
        )

        quantity_var.trace_add(
            "write", calculate
        )

        self.button(
            tab,
            f"CONFIRMAR {kind.upper()}",
            submit,
            GREEN if kind == "Compra" else PRIMARY,
            25
        ).pack(pady=14)

        load_choices()

    # =================================================
    # RECIBOS
    # =================================================

    def show_receipt(
        self, transaction_id, kind, product,
        batch, quantity, unit_price, total,
        payment, created_at
    ):

        receipt = f"""
========================================
               SX PHARMACY
            SX TECH & DESIGN
========================================

             RECIBO DE {kind.upper()}

Número: REC-{transaction_id:06d}

Data: {created_at}

----------------------------------------
PRODUTO: {product}

LOTE: {batch or 'Não indicado'}

Quantidade: {quantity}

Preço unitário: {unit_price:,.2f} MZN

----------------------------------------
TOTAL: {total:,.2f} MZN

Método de pagamento: {payment}

----------------------------------------
DADOS DE PAGAMENTO

Titular: {ACCOUNT_HOLDER}

Conta: {ACCOUNT_NUMBER}

========================================
          OBRIGADO PELA PREFERÊNCIA!
========================================

Documento gerado pelo SX Pharmacy Management.
"""

        win = tk.Toplevel(self.root)
        win.title(f"Recibo REC-{transaction_id:06d}")
        win.geometry("580x720")
        win.configure(bg=BG)
        win.transient(self.root)

        tk.Label(
            win,
            text="OPERAÇÃO CONCLUÍDA",
            bg=BG,
            fg=GREEN,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=12)

        preview = tk.Text(
            win,
            font=("Consolas", 10),
            bg=CARD,
            fg=TEXT,
            relief="solid",
            bd=1,
            padx=20,
            pady=15
        )

        preview.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=8
        )

        preview.insert("1.0", receipt)
        preview.configure(state="disabled")

        def save_txt():

            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Texto", "*.txt")],
                initialfile=f"REC-{transaction_id:06d}"
            )

            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(receipt)

                messagebox.showinfo(
                    "Recibo",
                    "Recibo guardado com sucesso."
                )

        def save_pdf():

            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.pdfgen import canvas
                from reportlab.lib.units import mm

                path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF", "*.pdf")],
                    initialfile=f"REC-{transaction_id:06d}"
                )

                if not path:
                    return

                pdf = canvas.Canvas(path, pagesize=A4)
                width, height = A4

                y = height - 25 * mm

                pdf.setFont("Helvetica-Bold", 20)
                pdf.setFillColorRGB(0.09, 0.54, 0.36)
                pdf.drawCentredString(
                    width / 2, y, "SX PHARMACY"
                )

                y -= 10 * mm

                pdf.setFillColorRGB(0.15, 0.21, 0.17)
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawCentredString(
                    width / 2, y, f"RECIBO DE {kind.upper()}"
                )

                y -= 12 * mm

                pdf.setFont("Helvetica", 10)

                for line in receipt.splitlines():

                    if y < 20 * mm:
                        pdf.showPage()
                        y = height - 25 * mm
                        pdf.setFont("Helvetica", 10)

                    pdf.drawString(25 * mm, y, line[:100])
                    y -= 6 * mm

                pdf.save()

                messagebox.showinfo(
                    "PDF",
                    "Recibo PDF criado com sucesso."
                )

            except ImportError:
                messagebox.showerror(
                    "Biblioteca necessária",
                    "Instala o ReportLab usando:\npip install reportlab"
                )

            except Exception as exc:
                messagebox.showerror(
                    "Erro",
                    str(exc)
                )

        def print_receipt():

            path = os.path.join(
                tempfile.gettempdir(),
                f"REC-{transaction_id:06d}.txt"
            )

            with open(path, "w", encoding="utf-8") as f:
                f.write(receipt)

            try:
                os.startfile(path, "print")
            except Exception as exc:
                messagebox.showerror(
                    "Impressão",
                    f"Não foi possível imprimir automaticamente: {exc}"
                )

        buttons = tk.Frame(win, bg=BG)
        buttons.pack(pady=12)

        self.button(
            buttons, "GUARDAR TXT",
            save_txt, "#64796D", 14
        ).pack(side="left", padx=4)

        self.button(
            buttons, "GUARDAR PDF",
            save_pdf, PRIMARY, 14
        ).pack(side="left", padx=4)

        self.button(
            buttons, "IMPRIMIR",
            print_receipt, GREEN, 14
        ).pack(side="left", padx=4)

        self.button(
            buttons, "FECHAR",
            win.destroy, "#64796D", 12
        ).pack(side="left", padx=4)

    # =================================================
    # DADOS DE PAGAMENTO
    # =================================================

    def build_payment(self):

        tk.Label(
            self.payment_tab,
            text="DADOS DE PAGAMENTO",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", padx=25, pady=25)

        panel = tk.Frame(
            self.payment_tab,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=35,
            pady=35
        )

        panel.pack(
            anchor="nw",
            padx=25,
            pady=10
        )

        tk.Label(
            panel,
            text="TITULAR DA CONTA",
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            panel,
            text=ACCOUNT_HOLDER,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w", pady=(5, 25))

        tk.Label(
            panel,
            text="NÚMERO DE CONTA",
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            panel,
            text=ACCOUNT_NUMBER,
            bg=CARD,
            fg=PRIMARY,
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w", pady=5)

        tk.Label(
            panel,
            text="SX PHARMACY | SX TECH & DESIGN",
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(25, 0))

    # =================================================
    # VALIDADES E STOCK
    # =================================================

    def build_expiry(self):

        tk.Label(
            self.expiry_tab,
            text="CONTROLO DE VALIDADE E STOCK BAIXO",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=20, pady=17)

        cols = (
            "name", "batch", "expiry", "stock", "status"
        )

        self.expiry_tree = ttk.Treeview(
            self.expiry_tab,
            columns=cols,
            show="headings"
        )

        for c, h, w in [
            ("name", "Produto", 220),
            ("batch", "Lote", 120),
            ("expiry", "Validade", 130),
            ("stock", "Stock", 100),
            ("status", "Estado", 250)
        ]:

            self.expiry_tree.heading(c, text=h)
            self.expiry_tree.column(
                c, width=w, anchor="center"
            )

        self.expiry_tree.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=8
        )

        self.button(
            self.expiry_tab,
            "Actualizar alertas",
            self.refresh_expiry,
            "#64796D"
        ).pack(pady=10)

    def refresh_expiry(self):

        if not hasattr(self, "expiry_tree"):
            return

        for item in self.expiry_tree.get_children():
            self.expiry_tree.delete(item)

        rows = self.db.execute("""
            SELECT name,batch,expiry,stock,min_stock
            FROM products ORDER BY expiry
        """).fetchall()

        today = date.today()

        for name, batch, expiry, stock, minimum in rows:

            statuses = []

            if stock <= minimum:
                statuses.append("STOCK BAIXO")

            if expiry:
                try:
                    exp = datetime.strptime(
                        expiry, "%Y-%m-%d"
                    ).date()

                    if exp < today:
                        statuses.append("FORA DA VALIDADE")

                    elif exp <= today + timedelta(days=90):
                        statuses.append(
                            "VALIDADE PRÓXIMA (90 dias)"
                        )

                except ValueError:
                    statuses.append("DATA INVÁLIDA")

            if statuses:
                self.expiry_tree.insert(
                    "",
                    "end",
                    values=(
                        name,
                        batch,
                        expiry or "Não indicada",
                        stock,
                        " | ".join(statuses)
                    )
                )

    # =================================================
    # HISTÓRICO
    # =================================================

    def build_history(self):

        tk.Label(
            self.history_tab,
            text="HISTÓRICO DE OPERAÇÕES",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", padx=20, pady=16)

        cols = (
            "id", "kind", "product", "batch",
            "quantity", "price", "total",
            "payment", "date"
        )

        self.history_tree = ttk.Treeview(
            self.history_tab,
            columns=cols,
            show="headings"
        )

        headings = [
            "ID", "Operação", "Produto", "Lote",
            "Quantidade", "Preço unit.", "Total",
            "Pagamento", "Data/Hora"
        ]

        widths = [
            45, 85, 170, 90, 80,
            90, 100, 110, 160
        ]

        for c, h, w in zip(cols, headings, widths):

            self.history_tree.heading(c, text=h)

            self.history_tree.column(
                c,
                width=w,
                anchor="center"
            )

        self.history_tree.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=8
        )

        bar = tk.Frame(self.history_tab, bg=BG)
        bar.pack(pady=10)

        self.button(
            bar,
            "ACTUALIZAR HISTÓRICO",
            self.refresh_history,
            "#64796D"
        ).pack(side="left", padx=5)

        self.button(
            bar,
            "ABRIR RECIBO",
            self.open_historical_receipt
        ).pack(side="left", padx=5)

    def refresh_history(self):

        if not hasattr(self, "history_tree"):
            return

        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        rows = self.db.execute("""
            SELECT id,kind,product_name,batch,quantity,
                   unit_price,total,payment,created_at
            FROM transactions ORDER BY id DESC
        """).fetchall()

        for r in rows:

            self.history_tree.insert(
                "",
                "end",
                values=(
                    r[0], r[1], r[2], r[3], r[4],
                    f"{r[5]:,.2f}",
                    f"{r[6]:,.2f}",
                    r[7],
                    r[8]
                )
            )

    def open_historical_receipt(self):

        selected = self.history_tree.selection()

        if not selected:
            messagebox.showwarning(
                "SX PHARMACY",
                "Selecciona uma transação."
            )
            return

        transaction_id = self.history_tree.item(
            selected[0]
        )["values"][0]

        r = self.db.execute("""
            SELECT id,kind,product_name,batch,quantity,
                   unit_price,total,payment,created_at
            FROM transactions WHERE id=?
        """, (transaction_id,)).fetchone()

        if not r:
            messagebox.showerror(
                "Erro",
                "Transação não encontrada."
            )
            return

        self.show_receipt(
            r[0], r[1], r[2], r[3],
            r[4], r[5], r[6], r[7], r[8]
        )

    # =================================================
    # ACTUALIZACAO GERAL
    # =================================================

    def refresh_all(self):

        self.refresh_products()
        self.refresh_dashboard()
        self.refresh_expiry()
        self.refresh_history()

    # =================================================
    # FECHAR SISTEMA
    # =================================================

    def close(self):

        self.db.close()
        self.root.destroy()


# =====================================================
# EXECUTAR APLICACAO
# =====================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SXPharmacy(root)

    root.mainloop()
