import tkinter as tk
from tkinter import messagebox

class SimuladorAlgoritmo:
    def __init__(self, root):
        self.root = root
        self.root.title("Oficina 1 (6º Ano): Programando o Robô Cartesiano")
        self.root.geometry("950x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        # Configurações da Grelha
        self.tamanho_celula = 40
        self.linhas = 10
        self.colunas = 10
        
        # Posição inicial
        self.robo_x = 0  
        self.robo_y = 0  
        self.start_x = 0
        self.start_y = 0
        self.direcao = 0

        self.algoritmo = []
        self.executando = False
        self.passo_atual = 0

        self.setup_ui()
        self.desenhar_grelha()

    def setup_ui(self):
        # ================= FRAME ESQUERDO =================
        frame_esquerdo = tk.Frame(self.root, bg="#f0f0f0")
        frame_esquerdo.pack(side=tk.LEFT, padx=20, pady=20)

        titulo = tk.Label(frame_esquerdo, text="Plano Cartesiano", font=("Arial", 16, "bold"), bg="#f0f0f0")
        titulo.pack(pady=5)

        tamanho_canvas = self.linhas * self.tamanho_celula + 60
        self.canvas = tk.Canvas(frame_esquerdo, width=tamanho_canvas, height=tamanho_canvas, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack()

        # ================= FRAME DIREITO =================
        frame_direito = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=20, relief="ridge", bd=2)
        frame_direito.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=20)

        tk.Label(frame_direito, text="Escreva o Algoritmo", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=(0, 10))

        frame_posicao = tk.LabelFrame(frame_direito, text="1. Onde o robô começa?", bg="#e0e0e0", font=("Arial", 10, "bold"))
        frame_posicao.pack(fill=tk.X, pady=5)

        frame_xy = tk.Frame(frame_posicao, bg="#e0e0e0")
        frame_xy.pack(pady=5)

        tk.Label(frame_xy, text="X:", font=("Arial", 11, "bold"), bg="#e0e0e0").grid(row=0, column=0, padx=2)
        self.entry_x = tk.Entry(frame_xy, width=3, font=("Arial", 11, "bold"), justify="center")
        self.entry_x.insert(0, "0")
        self.entry_x.grid(row=0, column=1, padx=5)

        tk.Label(frame_xy, text="Y:", font=("Arial", 11, "bold"), bg="#e0e0e0").grid(row=0, column=2, padx=2)
        self.entry_y = tk.Entry(frame_xy, width=3, font=("Arial", 11, "bold"), justify="center")
        self.entry_y.insert(0, "0")
        self.entry_y.grid(row=0, column=3, padx=5)

        btn_definir = tk.Button(frame_posicao, text="Definir Posição", font=("Arial", 10, "bold"), command=self.definir_posicao_inicial, bg="#00CED1", fg="white")
        btn_definir.pack(pady=5)

        frame_prog = tk.LabelFrame(frame_direito, text="2. Adicione os comandos", bg="#e0e0e0", font=("Arial", 10, "bold"))
        frame_prog.pack(fill=tk.X, pady=10)

        btn_frame = tk.Frame(frame_prog, bg="#e0e0e0")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Frente", font=("Arial", 11, "bold"), command=lambda: self.adicionar_comando("F"), bg="#ccffcc", width=8).grid(row=0, column=0, padx=2)
        tk.Button(btn_frame, text="Esquerda", font=("Arial", 11, "bold"), command=lambda: self.adicionar_comando("E"), bg="#ffcccc", width=8).grid(row=0, column=1, padx=2)
        tk.Button(btn_frame, text="Direita", font=("Arial", 11, "bold"), command=lambda: self.adicionar_comando("D"), bg="#ccccff", width=8).grid(row=0, column=2, padx=2)

        self.label_algoritmo = tk.Label(frame_prog, text="[ Vazio ]", font=("Courier", 11, "bold"), bg="#ffffff", relief="sunken", width=30, height=4, wraplength=250, justify="left", anchor="nw")
        self.label_algoritmo.pack(pady=10, padx=5)

        btn_executar = tk.Button(frame_direito, text="EXECUTAR ALGORITMO", font=("Arial", 12, "bold"), command=self.executar_algoritmo, bg="#32CD32", fg="white", width=25, height=2)
        btn_executar.pack(pady=10)
        self.btn_executar = btn_executar 
        
        btn_limpar = tk.Button(frame_direito, text="LIMPAR TUDO", font=("Arial", 11, "bold"), command=self.limpar_algoritmo, bg="#FF6347", fg="white", width=25)
        btn_limpar.pack(pady=5)

    def definir_posicao_inicial(self):
        if self.executando:
            return
        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
            if 0 <= x <= 9 and 0 <= y <= 9:
                self.start_x = x
                self.start_y = y
                self.robo_x = x
                self.robo_y = y
                self.direcao = 0 
                self.algoritmo = [] 
                self.atualizar_label_algoritmo()
                self.desenhar_grelha()
            else:
                messagebox.showerror("Erro", "As coordenadas devem estar entre 0 e 9.")
        except ValueError:
            messagebox.showerror("Erro", "Digite apenas números inteiros.")

    def desenhar_grelha(self):
        self.canvas.delete("all")
        offset = 30 # Margem para os eixos
        
        # Desenha as linhas da grade
        for i in range(self.linhas + 1):
            y = offset + i * self.tamanho_celula
            self.canvas.create_line(offset, y, offset + self.colunas * self.tamanho_celula, y, fill="#e0e0e0")
        for j in range(self.colunas + 1):
            x = offset + j * self.tamanho_celula
            self.canvas.create_line(x, offset, x, offset + self.linhas * self.tamanho_celula, fill="#e0e0e0")

        # EIXO X (Abscissa)
        for c in range(self.colunas):
            x = offset + c * self.tamanho_celula + self.tamanho_celula / 2
            y = offset + self.linhas * self.tamanho_celula + 15
            self.canvas.create_text(x, y, text=str(c), font=("Arial", 10, "bold"), fill="blue")

        # EIXO Y (Ordenada)
        for l in range(self.linhas):
            x = offset - 15
            y = offset + (self.linhas - 1 - l) * self.tamanho_celula + self.tamanho_celula / 2
            self.canvas.create_text(x, y, text=str(l), font=("Arial", 10, "bold"), fill="blue")

        # Desenha o Tesouro
        tesouro_x = offset + 7 * self.tamanho_celula + self.tamanho_celula / 2
        tesouro_y = offset + (self.linhas - 1 - 7) * self.tamanho_celula + self.tamanho_celula / 2
        self.canvas.create_text(tesouro_x, tesouro_y, text="X", font=("Arial", 24, "bold"), fill="gold")

        # ================= DESENHA A ROSA DOS VENTOS =================
        cx, cy = 90, 80 # Posição no canto superior esquerdo
        raio_bussola = 18
        
        # Círculo externo
        self.canvas.create_oval(cx-raio_bussola, cy-raio_bussola, cx+raio_bussola, cy+raio_bussola, outline="gray", width=2)
        
        # Setas (Norte, Sul, Leste, Oeste)
        self.canvas.create_line(cx, cy, cx, cy-raio_bussola-8, arrow=tk.LAST, fill="red", width=2) # N
        self.canvas.create_line(cx, cy, cx, cy+raio_bussola+8, arrow=tk.LAST, fill="blue", width=2) # S
        self.canvas.create_line(cx, cy, cx+raio_bussola+8, cy, arrow=tk.LAST, fill="green", width=2) # L
        self.canvas.create_line(cx, cy, cx-raio_bussola-8, cy, arrow=tk.LAST, fill="orange", width=2) # O
        
        # Letras
        self.canvas.create_text(cx, cy-raio_bussola-18, text="N", font=("Arial", 10, "bold"), fill="red")
        self.canvas.create_text(cx, cy+raio_bussola+18, text="S", font=("Arial", 10, "bold"), fill="blue")
        self.canvas.create_text(cx+raio_bussola+18, cy, text="L", font=("Arial", 10, "bold"), fill="green")
        self.canvas.create_text(cx-raio_bussola-18, cy, text="O", font=("Arial", 10, "bold"), fill="orange")
        
        # Centro
        self.canvas.create_oval(cx-2, cy-2, cx+2, cy+2, fill="black")
        # =========================================================

        self.desenhar_robo()
        self.root.update_idletasks() 

    def desenhar_robo(self):
        offset = 30
        x_centro = offset + self.robo_x * self.tamanho_celula + self.tamanho_celula / 2
        y_centro = offset + (self.linhas - 1 - self.robo_y) * self.tamanho_celula + self.tamanho_celula / 2
        raio = self.tamanho_celula / 2 - 5

        if self.direcao == 0: # Norte
            pontos = [x_centro, y_centro - raio, x_centro - raio, y_centro + raio, x_centro + raio, y_centro + raio]
            cor = "#ff6666"
        elif self.direcao == 1: # Leste
            pontos = [x_centro + raio, y_centro, x_centro - raio, y_centro - raio, x_centro - raio, y_centro + raio]
            cor = "#66b3ff"
        elif self.direcao == 2: # Sul
            pontos = [x_centro, y_centro + raio, x_centro + raio, y_centro - raio, x_centro - raio, y_centro - raio]
            cor = "#66ff66"
        else: # Oeste
            pontos = [x_centro - raio, y_centro, x_centro + raio, y_centro + raio, x_centro + raio, y_centro - raio]
            cor = "#ffcc66"

        self.canvas.create_polygon(pontos, fill=cor, outline="black", width=2)
        self.canvas.create_text(x_centro, y_centro, text=f"({self.robo_x},{self.robo_y})", font=("Arial", 7, "bold"))

    def adicionar_comando(self, comando):
        if self.executando:
            return
        self.algoritmo.append(comando)
        self.atualizar_label_algoritmo()

    def atualizar_label_algoritmo(self):
        texto = ""
        for i, cmd in enumerate(self.algoritmo):
            destaque = "▶ " if self.executando and i == self.passo_atual else ""
            if cmd == "F": texto += f"{destaque}FRENTE\n"
            elif cmd == "E": texto += f"{destaque}ESQ\n"
            elif cmd == "D": texto += f"{destaque}DIR\n"
        if texto == "":
            texto = "[ Vazio ]"
        self.label_algoritmo.config(text=texto)

    def limpar_algoritmo(self):
        if self.executando:
            return
        self.algoritmo = []
        self.robo_x = self.start_x
        self.robo_y = self.start_y
        self.direcao = 0
        self.passo_atual = 0
        self.atualizar_label_algoritmo()
        self.desenhar_grelha()

    def executar_algoritmo(self):
        if not self.algoritmo or self.executando:
            return
        
        self.btn_executar.config(state=tk.DISABLED, bg="#a0a0a0")
        self.executando = True
        self.passo_atual = 0
        self.robo_x = self.start_x
        self.robo_y = self.start_y
        self.direcao = 0
        self.atualizar_label_algoritmo()
        self.desenhar_grelha()
        
        self.root.after(1000, self.executar_passo_atual)

    def executar_passo_atual(self):
        if self.passo_atual >= len(self.algoritmo):
            self.finalizar_execucao()
            return
            
        cmd = self.algoritmo[self.passo_atual]
        
        if cmd == "E":
            self.direcao = (self.direcao - 1) % 4
        elif cmd == "D":
            self.direcao = (self.direcao + 1) % 4
        elif cmd == "F":
            nova_x, nova_y = self.robo_x, self.robo_y
            if self.direcao == 0: nova_y += 1
            elif self.direcao == 1: nova_x += 1
            elif self.direcao == 2: nova_y -= 1
            elif self.direcao == 3: nova_x -= 1

            if 0 <= nova_x <= 9 and 0 <= nova_y <= 9:
                self.robo_x, self.robo_y = nova_x, nova_y
            else:
                messagebox.showwarning("Erro de Lógica", "O robô tentou sair do plano cartesiano!\nAjuste seu algoritmo.")
                self.finalizar_execucao()
                return

        self.passo_atual += 1
        self.atualizar_label_algoritmo()
        self.desenhar_grelha()
        
        self.root.after(1000, self.executar_passo_atual)

    def finalizar_execucao(self):
        self.executando = False
        self.passo_atual = 0
        self.atualizar_label_algoritmo()
        self.btn_executar.config(state=tk.NORMAL, bg="#32CD32")
        
        if self.robo_x == 7 and self.robo_y == 7:
            messagebox.showinfo("Sucesso!", "Parabéns! Seu algoritmo levou o robô até o tesouro!")
        else:
            messagebox.showinfo("Fim do Algoritmo", "O algoritmo terminou, mas o robô não chegou no X.\nTente novamente!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorAlgoritmo(root)
    root.mainloop()
