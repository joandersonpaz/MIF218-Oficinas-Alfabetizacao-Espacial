import tkinter as tk
from tkinter import messagebox

class SimuladorRelevo:
    def __init__(self, root):
        self.root = root
        self.root.title("Oficina 3: Do 3D para o 2D (Maquete e Mapa)")
        self.root.geometry("1150x750") # Aumentei um pouco para caber os botões
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        # Configurações da Grade
        self.tamanho_grade = 5
        self.tamanho_celula = 60
        self.altitudes = [[0 for _ in range(self.tamanho_grade)] for _ in range(self.tamanho_grade)]
        self.max_altitude = 4

        self.setup_ui()
        self.carregar_preset("perlin") # Começa com um exemplo para a tela não ficar vazia

    def setup_ui(self):
        # Título
        titulo = tk.Label(self.root, text="Preencha a Matriz e veja o Mapa!", font=("Arial", 16, "bold"), bg="#f0f0f0")
        titulo.pack(pady=10)

        # Frame Central
        frame_visualizacao = tk.Frame(self.root, bg="#f0f0f0")
        frame_visualizacao.pack(pady=10)

        # --- Visão 3D ---
        frame_3d = tk.LabelFrame(frame_visualizacao, text="Visão 3D (Maquete Digital)", font=("Arial", 12, "bold"), bg="#f0f0f0")
        frame_3d.pack(side=tk.LEFT, padx=10)
        
        self.canvas_3d = tk.Canvas(frame_3d, width=350, height=350, bg="#e6f2ff", highlightthickness=0)
        self.canvas_3d.pack(pady=10, padx=10)
        self.canvas_3d.bind("<Button-1>", self.clicar_3d)
        self.canvas_3d.bind("<Button-3>", self.clicar_3d_direito)

        # --- Visão 2D ---
        frame_2d = tk.LabelFrame(frame_visualizacao, text="Visão 2D (Mapa Vista de Cima)", font=("Arial", 12, "bold"), bg="#f0f0f0")
        frame_2d.pack(side=tk.LEFT, padx=10)
        
        self.canvas_2d = tk.Canvas(frame_2d, width=300, height=300, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas_2d.pack(pady=10, padx=10)
        self.canvas_2d.bind("<Button-1>", self.clicar_2d) 
        self.canvas_2d.bind("<Button-3>", self.clicar_2d_direito)

        # --- Painel de Controle ---
        frame_matriz = tk.LabelFrame(frame_visualizacao, text="Controles", font=("Arial", 12, "bold"), bg="#f0f0f0")
        frame_matriz.pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # 1. Botões de Modelos Prontos (Presets)
        tk.Label(frame_matriz, text="1. Escolha um Terreno Pronto:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)
        
        frame_botoes = tk.Frame(frame_matriz, bg="#f0f0f0")
        frame_botoes.pack()
        
        tk.Button(frame_botoes, text="Montanha", width=18, command=lambda: self.carregar_preset("ridged")).pack(pady=2)
        tk.Button(frame_botoes, text="Cânion", width=18, command=lambda: self.carregar_preset("canyons")).pack(pady=2)
        tk.Button(frame_botoes, text="Colinas", width=18, command=lambda: self.carregar_preset("hills")).pack(pady=2)
        tk.Button(frame_botoes, text="Plano (Zerar)", width=18, command=lambda: self.carregar_preset("zero")).pack(pady=2)

        # 2. Caixa de Texto para Inserção Manual
        tk.Label(frame_matriz, text="2. Ou digite sua Matriz 5x5:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=(15, 5))
        self.text_matriz = tk.Text(frame_matriz, height=6, width=22, font=("Courier", 11))
        self.text_matriz.pack(pady=5)
        
        btn_importar = tk.Button(frame_matriz, text="Gerar Mapa da Matriz", font=("Arial", 10, "bold"), command=self.importar_matriz, bg="#32CD32", fg="white")
        btn_importar.pack(pady=5)

        # Legenda
        frame_inferior = tk.Frame(self.root, bg="#e0e0e0", pady=10)
        frame_inferior.pack(fill=tk.X, side=tk.BOTTOM)

        legenda_frame = tk.Frame(frame_inferior, bg="#e0e0e0")
        legenda_frame.pack(pady=5)
        
        cores = [("0 (Vale)", "#98FB98"), ("1", "#FFFACD"), ("2", "#F4A460"), ("3", "#A0522D"), ("4 (Pico)", "#FFFFFF")]
        for texto, cor in cores:
            lbl = tk.Label(legenda_frame, text=texto, bg=cor, width=10, relief="solid", bd=1, font=("Arial", 9))
            lbl.pack(side=tk.LEFT, padx=2)

    def carregar_preset(self, tipo):
        presets = {
            "ridged": [[0, 1, 0, 0, 0], [1, 3, 2, 0, 0], [2, 4, 3, 1, 0], [1, 3, 2, 1, 0], [0, 1, 0, 0, 0]],
            "canyons": [[3, 3, 4, 3, 3], [3, 2, 1, 2, 3], [4, 1, 0, 1, 4], [3, 2, 1, 2, 3], [3, 3, 4, 3, 3]],
            "hills": [[1, 1, 2, 1, 1], [1, 2, 2, 2, 1], [2, 2, 3, 2, 2], [1, 2, 2, 2, 1], [1, 1, 2, 1, 1]],
            "zero": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "perlin": [[1, 2, 1, 0, 0], [0, 2, 3, 2, 1], [1, 3, 4, 3, 1], [0, 1, 3, 2, 0], [0, 0, 1, 1, 0]]
        }
        self.altitudes = presets[tipo]
        self.atualizar_texto_matriz()
        self.desenhar_tudo()

    def atualizar_texto_matriz(self):
        self.text_matriz.delete("1.0", tk.END)
        for linha in self.altitudes:
            self.text_matriz.insert(tk.END, " ".join(map(str, linha)) + "\n")

    def importar_matriz(self):
        texto = self.text_matriz.get("1.0", tk.END).strip()
        texto_limpo = texto.replace('[', ' ').replace(']', ' ').replace(',', ' ')
        
        try:
            numeros = [int(n) for n in texto_limpo.split()]
            if len(numeros) != 25:
                messagebox.showerror("Erro", f"Você inseriu {len(numeros)} números. A matriz precisa ter 25 números (5x5).")
                return
            
            index = 0
            for lin in range(self.tamanho_grade):
                for col in range(self.tamanho_grade):
                    valor = numeros[index]
                    if valor < 0 or valor > 4:
                        messagebox.showerror("Erro", "Os valores devem ser entre 0 e 4.")
                        return
                    self.altitudes[lin][col] = valor
                    index += 1
                    
            self.desenhar_tudo()
        except ValueError:
            messagebox.showerror("Erro de Formato", "Certifique-se de digitar apenas números inteiros.")

    def get_cor_altitude(self, altitude):
        cores = {0: "#98FB98", 1: "#FFFACD", 2: "#F4A460", 3: "#A0522D", 4: "#FFFFFF"}
        return cores.get(altitude, "#FFFFFF")

    def clicar_3d(self, event):
        col = (event.x - 50) // self.tamanho_celula
        lin = (event.y - 50) // self.tamanho_celula
        if 0 <= col < self.tamanho_grade and 0 <= lin < self.tamanho_grade:
            if self.altitudes[lin][col] < self.max_altitude:
                self.altitudes[lin][col] += 1
                self.desenhar_tudo()
                self.atualizar_texto_matriz()

    def clicar_3d_direito(self, event):
        col = (event.x - 50) // self.tamanho_celula
        lin = (event.y - 50) // self.tamanho_celula
        if 0 <= col < self.tamanho_grade and 0 <= lin < self.tamanho_grade:
            if self.altitudes[lin][col] > 0:
                self.altitudes[lin][col] -= 1
                self.desenhar_tudo()
                self.atualizar_texto_matriz()

    def clicar_2d(self, event):
        col = event.x // self.tamanho_celula
        lin = event.y // self.tamanho_celula
        if 0 <= col < self.tamanho_grade and 0 <= lin < self.tamanho_grade:
            if self.altitudes[lin][col] < self.max_altitude:
                self.altitudes[lin][col] += 1
                self.desenhar_tudo()
                self.atualizar_texto_matriz()

    def clicar_2d_direito(self, event):
        col = event.x // self.tamanho_celula
        lin = event.y // self.tamanho_celula
        if 0 <= col < self.tamanho_grade and 0 <= lin < self.tamanho_grade:
            if self.altitudes[lin][col] > 0:
                self.altitudes[lin][col] -= 1
                self.desenhar_tudo()
                self.atualizar_texto_matriz()

    def desenhar_tudo(self):
        self.desenhar_3d()
        self.desenhar_2d()

    def desenhar_2d(self):
        self.canvas_2d.delete("all")
        for lin in range(self.tamanho_grade):
            for col in range(self.tamanho_grade):
                x1 = col * self.tamanho_celula
                y1 = lin * self.tamanho_celula
                x2 = x1 + self.tamanho_celula
                y2 = y1 + self.tamanho_celula
                cor = self.get_cor_altitude(self.altitudes[lin][col])
                self.canvas_2d.create_rectangle(x1, y1, x2, y2, fill=cor, outline="black")
                self.canvas_2d.create_text(x1 + self.tamanho_celula/2, y1 + self.tamanho_celula/2, text=str(self.altitudes[lin][col]), font=("Arial", 12, "bold"))

    def desenhar_3d(self):
        self.canvas_3d.delete("all")
        offset_x = 50
        offset_y = 50
        for lin in range(self.tamanho_grade - 1, -1, -1):
            for col in range(self.tamanho_grade):
                altitude = self.altitudes[lin][col]
                x1 = offset_x + col * self.tamanho_celula
                y1 = offset_y + lin * self.tamanho_celula
                x2 = x1 + self.tamanho_celula
                y2 = y1 + self.tamanho_celula
                
                self.canvas_3d.create_rectangle(x1, y1, x2, y2, fill="#d9d9d9", outline="#bfbfbf")
                
                if altitude > 0:
                    for h in range(altitude):
                        altura_pixel = (h + 1) * 15 
                        cor = self.get_cor_altitude(h + 1)
                        self.canvas_3d.create_rectangle(x1, y1 - altura_pixel, x2, y2 - altura_pixel, fill=cor, outline="black")
                        self.canvas_3d.create_polygon(x1, y1 - altura_pixel, x1 + 10, y1 - altura_pixel - 10, x2 + 10, y1 - altura_pixel - 10, x2, y1 - altura_pixel, fill=self.get_cor_altitude(h + 1), outline="black")
                        self.canvas_3d.create_polygon(x2, y1 - altura_pixel, x2 + 10, y1 - altura_pixel - 10, x2 + 10, y2 - altura_pixel - 10, x2, y2 - altura_pixel, fill=cor, outline="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorRelevo(root)
    root.mainloop()
