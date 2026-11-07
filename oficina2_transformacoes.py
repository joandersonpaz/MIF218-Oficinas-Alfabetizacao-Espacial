import tkinter as tk
import math

class SimuladorTransformacoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Oficina 2 (7º Ano): Escalas e Transformações Geométricas")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        # Configurações do Plano Cartesiano
        self.largura_canvas = 600
        self.altura_canvas = 600
        self.origem_x = self.largura_canvas / 2
        self.origem_y = self.altura_canvas / 2
        
        # Escala do desenho na tela (1 unidade matemática = 50 pixels)
        self.escala_tela = 50 

        # Vértices originais da "Casa" (Retângulo + Telhado)
        # Base: (2,2) a (4,2); Altura: até y=4; Telhado: até y=5
        self.vertices_originais = [
            (2, 2), (4, 2), (4, 4), (3, 5), (2, 4) # Ponto inicial repetido para fechar o polígono
        ]

        self.setup_ui()
        self.atualizar_figura() # Desenha a figura inicial

    def setup_ui(self):
        # --- Painel Esquerdo (Canvas) ---
        frame_esquerdo = tk.Frame(self.root, bg="#f0f0f0")
        frame_esquerdo.pack(side=tk.LEFT, padx=20, pady=20)

        titulo = tk.Label(frame_esquerdo, text="Visualizador de Transformações", font=("Arial", 16, "bold"), bg="#f0f0f0")
        titulo.pack(pady=10)

        self.canvas = tk.Canvas(frame_esquerdo, width=self.largura_canvas, height=self.altura_canvas, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack()
        
        self.desenhar_eixos()

        # --- Painel Direito (Controles) ---
        frame_direito = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=20, relief="ridge", bd=2)
        frame_direito.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=20)

        tk.Label(frame_direito, text="Transformações Geométricas", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=(0, 20))

        # Controle de Escala
        frame_escala = tk.LabelFrame(frame_direito, text="Escala (Ampliação/Redução)", bg="#e0e0e0", font=("Arial", 10, "bold"))
        frame_escala.pack(fill=tk.X, pady=10)
        
        self.lbl_escala = tk.Label(frame_escala, text="Fator K = 1.0", font=("Arial", 11), bg="#e0e0e0")
        self.lbl_escala.pack()
        
        self.slider_escala = tk.Scale(frame_escala, from_=0.2, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, bg="#e0e0e0", command=self.atualizar_figura)
        self.slider_escala.set(1.0)
        self.slider_escala.pack(fill=tk.X, padx=10, pady=5)

        # Controle de Rotação
        frame_rotacao = tk.LabelFrame(frame_direito, text="Rotação (Graus)", bg="#e0e0e0", font=("Arial", 10, "bold"))
        frame_rotacao.pack(fill=tk.X, pady=10)
        
        self.lbl_rotacao = tk.Label(frame_rotacao, text="Ângulo = 0°", font=("Arial", 11), bg="#e0e0e0")
        self.lbl_rotacao.pack()
        
        self.slider_rotacao = tk.Scale(frame_rotacao, from_=0, to=360, resolution=5, orient=tk.HORIZONTAL, bg="#e0e0e0", command=self.atualizar_figura)
        self.slider_rotacao.set(0)
        self.slider_rotacao.pack(fill=tk.X, padx=10, pady=5)

        # Painel de Coordenadas (Matemática explícita)
        frame_info = tk.LabelFrame(frame_direito, text="Dados Matemáticos", bg="#e0e0e0", font=("Arial", 10, "bold"))
        frame_info.pack(fill=tk.X, pady=20)
        
        self.lbl_info = tk.Label(frame_info, text="", font=("Courier", 10), bg="#ffffff", justify="left", relief="sunken", padx=5, pady=5)
        self.lbl_info.pack(fill=tk.X, padx=5, pady=5)

        # Botão de Reset
        btn_reset = tk.Button(frame_direito, text="RESTAURAR ORIGINAL", font=("Arial", 11, "bold"), command=self.resetar, bg="#FF6347", fg="white")
        btn_reset.pack(pady=10, fill=tk.X)

    def desenhar_eixos(self):
        # Linhas dos eixos X e Y
        self.canvas.create_line(0, self.origem_y, self.largura_canvas, self.origem_y, fill="gray", arrow=tk.LAST)
        self.canvas.create_line(self.origem_x, self.altura_canvas, self.origem_x, 0, fill="gray", arrow=tk.LAST)
        
        # Rótulos
        self.canvas.create_text(self.largura_canvas - 15, self.origem_y - 10, text="X", font=("Arial", 12, "bold"))
        self.canvas.create_text(self.origem_x + 10, 15, text="Y", font=("Arial", 12, "bold"))
        
        # Grade de fundo
        for i in range(-5, 6):
            if i == 0: continue
            # Linhas X
            x = self.origem_x + i * self.escala_tela
            self.canvas.create_line(x, 0, x, self.altura_canvas, fill="#f0f0f0")
            # Linhas Y
            y = self.origem_y - i * self.escala_tela
            self.canvas.create_line(0, y, self.largura_canvas, y, fill="#f0f0f0")

    def transformar_ponto(self, x, y, fator_escala, angulo_graus):
        # 1. Aplica a Escala (Multiplicação das coordenadas)
        x_escalado = x * fator_escala
        y_escalado = y * fator_escala
        
        # 2. Aplica a Rotação (Matriz de rotação)
        angulo_rad = math.radians(angulo_graus)
        x_rotacionado = x_escalado * math.cos(angulo_rad) - y_escalado * math.sin(angulo_rad)
        y_rotacionado = x_escalado * math.sin(angulo_rad) + y_escalado * math.cos(angulo_rad)
        
        return x_rotacionado, y_rotacionado

    def atualizar_figura(self, event=None):
        self.canvas.delete("figura") # Limpa apenas a figura, mantendo os eixos
        
        # Obtém valores dos sliders
        fator_escala = self.slider_escala.get()
        angulo = self.slider_rotacao.get()
        
        # Atualiza os textos dos sliders
        self.lbl_escala.config(text=f"Fator K = {fator_escala}")
        self.lbl_rotacao.config(text=f"Ângulo = {angulo}°")

        coordenadas_tela = []
        
        for (x, y) in self.vertices_originais:
            # Aplica a matemática
            novo_x, novo_y = self.transformar_ponto(x, y, fator_escala, angulo)
            
            # Converte para a tela (Y da tela é invertido em relação à matemática)
            tela_x = self.origem_x + (novo_x * self.escala_tela)
            tela_y = self.origem_y - (novo_y * self.escala_tela)
            
            coordenadas_tela.extend([tela_x, tela_y])

        # Desenha o polígono transformado (Casa)
        self.canvas.create_polygon(coordenadas_tela, fill="#66b3ff", outline="black", width=2, tags="figura")
        
        # Texto informativo matemático
        texto_info = f"Vértice Original: (2, 2)\n"
        texto_info += f"Fator Escala (K): {fator_escala}\n"
        texto_info += f"Ângulo: {angulo}°\n"
        texto_info += f"-------------------------\n"
        texto_info += f"Novo X = (X * K) * cos(ang)\n          - (Y * K) * sin(ang)\n"
        texto_info += f"Novo Y = (X * K) * sin(ang)\n          + (Y * K) * cos(ang)"
        self.lbl_info.config(text=texto_info)

    def resetar(self):
        self.slider_escala.set(1.0)
        self.slider_rotacao.set(0)
        self.atualizar_figura()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorTransformacoes(root)
    root.mainloop()