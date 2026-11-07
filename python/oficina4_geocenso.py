import tkinter as tk
from tkinter import messagebox

class GeoCenso:
    def __init__(self, root):
        self.root = root
        self.root.title("Oficina 4 (7º Ano): GeoCenso - Dados e Gráficos")
        self.root.geometry("950x600")
        self.root.configure(bg="#f4f4f4")
        self.root.resizable(False, False)

        # Dados da pesquisa
        self.dados = {
            "A Pé": 0,
            "Ônibus": 0,
            "Carro": 0,
            "Bicicleta": 0
        }
        
        # Cores dos gráficos
        self.cores = {
            "A Pé": "#4682B4",     # Azul Aço
            "Ônibus": "#FF8C00",   # Laranja Escuro
            "Carro": "#32CD32",    # Verde Limão
            "Bicicleta": "#DC143C" # Carmesim
        }

        self.setup_ui()
        self.atualizar_grafico()

    def setup_ui(self):
        # ================= TÍTULO E PERGUNTA =================
        frame_topo = tk.Frame(self.root, bg="#f4f4f4")
        frame_topo.pack(pady=15)

        tk.Label(frame_topo, text="Pesquisa de Mobilidade Urbana", font=("Arial", 18, "bold"), bg="#f4f4f4").pack()
        tk.Label(frame_topo, text="Como você vem para a escola?", font=("Arial", 14), bg="#f4f4f4", fg="#555").pack(pady=5)

        # ================= FRAME CENTRAL (BOTÕES E GRÁFICO) =================
        frame_central = tk.Frame(self.root, bg="#f4f4f4")
        frame_central.pack(fill=tk.BOTH, expand=True, padx=20)

        # --- Painel Esquerdo (Botões de Votação) ---
        frame_botoes = tk.Frame(frame_central, bg="#e0e0e0", padx=20, pady=20, relief="ridge", bd=2)
        frame_botoes.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame_botoes, text="Coletar Respostas", font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=(0, 10))

        for opcao in self.dados.keys():
            btn = tk.Button(frame_botoes, text=f"+ {opcao}", font=("Arial", 12), 
                            bg=self.cores[opcao], fg="white", width=15,
                            command=lambda o=opcao: self.votar(o))
            btn.pack(pady=5)

        # Botão de Reset
        tk.Button(frame_botoes, text="Limpar Dados", font=("Arial", 10), bg="#999", fg="white", command=self.limpar_dados).pack(pady=(20, 0))

        # --- Painel Direito (Gráfico) ---
        frame_grafico = tk.Frame(frame_central, bg="#ffffff", relief="solid", bd=1)
        frame_grafico.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)

        self.canvas_grafico = tk.Canvas(frame_grafico, bg="#ffffff", width=550, height=400)
        self.canvas_grafico.pack(pady=10, padx=10)

        # ================= FRAME INFERIOR (TEXTO ESTATÍSTICO) =================
        frame_inferior = tk.Frame(self.root, bg="#e0e0e0", pady=10)
        frame_inferior.pack(side=tk.BOTTOM, fill=tk.X)

        self.lbl_resumo = tk.Label(frame_inferior, text="Total de respostas: 0", font=("Arial", 12, "bold"), bg="#e0e0e0")
        self.lbl_resumo.pack()

    def votar(self, opcao):
        self.dados[opcao] += 1
        self.atualizar_grafico()

    def limpar_dados(self):
        if messagebox.askyesno("Limpar", "Deseja apagar todos os dados da pesquisa?"):
            for chave in self.dados:
                self.dados[chave] = 0
            self.atualizar_grafico()

    def atualizar_grafico(self):
        self.canvas_grafico.delete("all")
        
        total = sum(self.dados.values())
        
        # Texto de resumo
        if total == 0:
            self.lbl_resumo.config(text="Total de respostas: 0 (Comece a coletar!)")
        else:
            # Encontra a moda (o mais votado)
            moda = max(self.dados, key=self.dados.get)
            porcentagem_moda = (self.dados[moda] / total) * 100
            self.lbl_resumo.config(text=f"Total de respostas: {total} | A maioria ({porcentagem_moda:.1f}%) usa: {moda}")

        # Configurações do desenho do gráfico
        margem_esq = 60
        margem_inf = 50
        largura_max = 450
        altura_max = 300
        
        eixo_y_base = 400 - margem_inf
        
        # Desenha os Eixos
        self.canvas_grafico.create_line(margem_esq, 50, margem_esq, eixo_y_base, width=2) # Eixo Y
        self.canvas_grafico.create_line(margem_esq, eixo_y_base, 500, eixo_y_base, width=2) # Eixo X

        if total == 0:
            return

        # Encontra o maior valor para calcular a escala do gráfico
        maior_valor = max(self.dados.values())
        if maior_valor == 0: maior_valor = 1 # Evita divisão por zero

        largura_barra = 60
        espaco_entre_barras = 40
        x_atual = margem_esq + 30

        for opcao, valor in self.dados.items():
            # Calcula a altura da barra proporcionalmente ao maior valor
            altura_barra = (valor / maior_valor) * altura_max
            
            # Desenha a barra
            x1 = x_atual
            y1 = eixo_y_base - altura_barra
            x2 = x_atual + largura_barra
            y2 = eixo_y_base
            
            self.canvas_grafico.create_rectangle(x1, y1, x2, y2, fill=self.cores[opcao], outline="black")
            
            # Desenha o valor no topo da barra
            self.canvas_grafico.create_text(x1 + largura_barra/2, y1 - 10, text=str(valor), font=("Arial", 12, "bold"))
            
            # Desenha o rótulo no eixo X
            self.canvas_grafico.create_text(x1 + largura_barra/2, eixo_y_base + 15, text=opcao, font=("Arial", 10))
            
            # Desenha a porcentagem dentro da barra (se couber)
            if valor > 0:
                porcentagem = (valor / total) * 100
                self.canvas_grafico.create_text(x1 + largura_barra/2, y2 - 15, text=f"{porcentagem:.0f}%", font=("Arial", 10), fill="white")

            x_atual += largura_barra + espaco_entre_barras

if __name__ == "__main__":
    root = tk.Tk()
    app = GeoCenso(root)
    root.mainloop()
