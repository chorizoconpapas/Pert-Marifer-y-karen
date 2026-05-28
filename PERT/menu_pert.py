# archivo: interfaz_grafica.py
import tkinter as tk
from tkinter import ttk, messagebox
import heapq

from setuptools import Command

# ============================================
# SISTEMA PERT - INTERFAZ GRÁFICA
# ============================================
class SistemaPERT:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema PERT/CPM")
        self.root.geometry("900x650")
        self.root.configure(bg="#2C3E50")
        
        # Datos del proyecto
        self.actividades = []
        self.grafo = {}
        self.duraciones = {}
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(
            self.root,
            text="📊 MÓDULO PERT/CPM",
            font=("Segoe UI", 22, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        titulo.pack(pady=15)
        
        # Notebook (pestañas)
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Pestaña 1: Agregar Actividades
        self.pestana_agregar = tk.Frame(notebook, bg="#34495E")
        notebook.add(self.pestana_agregar, text="➕ Agregar Actividades")
        self.crear_pestana_agregar()
        
        # Pestaña 2: Lista de Actividades
        self.pestana_lista = tk.Frame(notebook, bg="#34495E")
        notebook.add(self.pestana_lista, text="📋 Lista de Actividades")
        self.crear_pestana_lista()
        
        # Pestaña 3: Diagrama PERT
        self.pestana_diagrama = tk.Frame(notebook, bg="#34495E")
        notebook.add(self.pestana_diagrama, text="🔗 Diagrama de Red")
        self.crear_pestana_diagrama()
        
        # Pestaña 4: Resultados
        self.pestana_resultados = tk.Frame(notebook, bg="#34495E")
        notebook.add(self.pestana_resultados, text="📈 Resultados")
        self.crear_pestana_resultados()
        
        # Botón volver
        btn_volver = tk.Button(
            self.root,
            text="← Volver al Menú Principal",
            font=("Segoe UI", 10),
            bg="#E74C3C",
            fg="white",
            command=self.root.destroy,
            padx=20,
            pady=5
        )
        btn_volver.pack(pady=10)
    
    # ============================================
    # PESTAÑA: AGREGAR ACTIVIDADES
    # ============================================
    def crear_pestana_agregar(self):
        frame = tk.Frame(self.pestana_agregar, bg="#34495E")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Instrucciones
        lbl_info = tk.Label(
            frame,
            text="Ingrese las actividades del proyecto:\nFormato: Predecesores | Actividad | Duración",
            font=("Segoe UI", 11),
            bg="#34495E",
            fg="#ECF0F1"
        )
        lbl_info.pack(pady=10)
        
        # Campos de entrada
        lbl_pred = tk.Label(frame, text="Predecesores (ej: A,B o -):", bg="#34495E", fg="#BDC3C7")
        lbl_pred.pack(anchor="w", pady=5)
        self.entry_pred = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        self.entry_pred.pack(fill="x", pady=5)
        
        lbl_nom = tk.Label(frame, text="Nombre de Actividad:", bg="#34495E", fg="#BDC3C7")
        lbl_nom.pack(anchor="w", pady=5)
        self.entry_nom = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        self.entry_nom.pack(fill="x", pady=5)
        
        lbl_dur = tk.Label(frame, text="Duración:", bg="#34495E", fg="#BDC3C7")
        lbl_dur.pack(anchor="w", pady=5)
        self.entry_dur = tk.Entry(frame, font=("Segoe UI", 11), width=30)
        self.entry_dur.pack(fill="x", pady=5)
        
        # Botón agregar
        btn_agregar = tk.Button(
            frame,
            text="✅ Agregar Actividad",
            font=("Segoe UI", 11, "bold"),
            bg="#27AE60",
            fg="white",
            command=self.agregar_actividad,
            padx=20,
            pady=8
        )
        btn_agregar.pack(pady=20)
        
        # Ejemplos
        lbl_ejemplo = tk.Label(
            frame,
            text="Ejemplos:\n•Primera actividad: - | A | 5\n•Con predecesor: A | B | 3\n•Múltiples: A,B | C | 4",
            font=("Segoe UI", 9),
            bg="#34495E",
            fg="#95A5A6"
        )
        lbl_ejemplo.pack(pady=10)
    
    def agregar_actividad(self):
        predecesor = self.entry_pred.get().strip()
        nombre = self.entry_nom.get().strip().upper()
        try:
            duracion = int(self.entry_dur.get().strip())
        except:
            messagebox.showerror("Error", "La duración debe ser un número entero")
            return
        
        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre de actividad")
            return
        
        # Verificar si ya existe
        for act in self.actividades:
            if act["nombre"] == nombre:
                messagebox.showerror("Error", f"La actividad {nombre} ya existe")
                return
        
        # Agregar actividad
        actividad = {
            "predecesor": predecesor,
            "nombre": nombre,
            "duracion": duracion
        }
        self.actividades.append(actividad)
        
        # Limpiar campos
        self.entry_pred.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)
        self.entry_dur.delete(0, tk.END)
        
        messagebox.showinfo("Éxito", f"Actividad {nombre} agregada correctamente")
        self.actualizar_lista()
    
    # ============================================
    # PESTAÑA: LISTA DE ACTIVIDADES
    # ============================================
    def crear_pestana_lista(self):
        frame = tk.Frame(self.pestana_lista, bg="#34495E")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Treeview para mostrar actividades
        columnas = ("nombre", "predecesor", "duracion")
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings", height=15)
        
        self.tree.heading("nombre", text="Actividad")
        self.tree.heading("predecesor", text="Predecesores")
        self.tree.heading("duracion", text="Duración")
        
        self.tree.column("nombre", width=100, anchor="center")
        self.tree.column("predecesor", width=200, anchor="center")
        self.tree.column("duracion", width=100, anchor="center")
        
        self.tree.pack(expand=True, fill="both")
        
        # Botón eliminar
        btn_eliminar = tk.Button(
            frame,
            text="🗑️ Eliminar Seleccionada",
            font=("Segoe UI", 10),
            bg="#E74C3C",
            fg="white",
            command=self.eliminar_actividad,
            padx=20,
            pady=5
        )
        btn_eliminar.pack(pady=10)
    
    def actualizar_lista(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar actividades
        for act in self.actividades:
            self.tree.insert("", tk.END, values=(act["nombre"], act["predecesor"], act["duracion"]))
    
    def eliminar_actividad(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una actividad para eliminar")
            return
        
        for item in seleccion:
            valores = self.tree.item(item)["values"]
            nombre = valores[0]
            self.actividades = [a for a in self.actividades if a["nombre"] != nombre]
        
        self.actualizar_lista()
    
    # ============================================
    # PESTAÑA: DIAGRAMA DE RED
    # ============================================
    def crear_pestana_diagrama(self):
        frame = tk.Frame(self.pestana_diagrama, bg="#34495E")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Canvas para dibujar
        self.canvas = tk.Canvas(frame, bg="#2C3E50", width=850, height=400)
        self.canvas.pack(expand=True, fill="both")
        
        # Botón calcular
        btn_calcular = tk.Button(
            frame,
            text="🔄 Calcular y Dibujar Red",
            font=("Segoe UI", 11, "bold"),
            bg="#3498DB",
            fg="white",
            command=self.calcular_red,
            padx=20,
            pady=8
        )
        btn_calcular.pack(pady=10)
    
    def calcular_red(self):
        if not self.actividades:
            messagebox.showwarning("Advertencia", "No hay actividades agregadas")
            return
        
        # Construir grafo
        self.construir_grafo()
        
        # Calcular tiempos Early y Late
        self.calcular_tiempos()
        
        # Dibujar red
        self.dibujar_red()
    
    def construir_grafo(self):
        self.grafo = {}
        self.duraciones = {}
        
        for act in self.actividades:
            nombre = act["nombre"]
            predecesor = act["predecesor"]
            duracion = act["duracion"]
            
            self.duraciones[nombre] = duracion
            
            if nombre not in self.grafo:
                self.grafo[nombre] = []
            
            if predecesor == "-" or predecesor == "":
                continue
            
            # Agregar predecesores
            preds = [p.strip() for p in predecesor.split(",")]
            for pred in preds:
                if pred:
                    if pred not in self.grafo:
                        self.grafo[pred] = []
                    self.grafo[pred].append(nombre)
    
    def calcular_tiempos(self):
        # Calcular Early Start (ES) y Early Finish (EF)
        self.early = {}
        self.late = {}
        
        # Topological sort
        visitados = set()
        cola = []
        
        for act in self.actividades:
            nombre = act["nombre"]
            predecesor = act["predecesor"]
            if predecesor == "-" or predecesor == "":
                cola.append(nombre)
                self.early[nombre] = 0
        
        while cola:
            actual = cola.pop(0)
            if actual in visitados:
                continue
            visitados.add(actual)
            
            if actual in self.grafo:
                for sig in self.grafo[actual]:
                    if sig not in self.early:
                        self.early[sig] = 0
                    
                    nuevo_es = self.early[actual] + self.duraciones[actual]
                    if nuevo_es > self.early[sig]:
                        self.early[sig] = nuevo_es
                    
                    if sig not in visitados:
                        tiene_predecesores = False
                        for a in self.actividades:
                            if a["nombre"] == sig:
                                preds = [p.strip() for p in a["predecesor"].split(",") if p.strip()]
                                for p in preds:
                                    if p not in visitados:
                                        tiene_predecesores = True
                                        break
                        
                        if not tiene_predecesores:
                            cola.append(sig)
        
        # Calcular ruta crítica
        self.ruta_critica = []
        max_tiempo = max(self.early.values()) if self.early else 0
        
        # Encontrar actividades en ruta crítica (diferencia ES = EF)
        for act in self.actividades:
            nombre = act["nombre"]
            if nombre in self.early:
                if self.early[nombre] + self.duraciones[nombre] == max_tiempo:
                    self.ruta_critica.append(nombre)
        
        # Late Start y Late Finish = tiempo crítico - tiempo acumulado
        self.late = {}
        for nombre, tiempo in self.early.items():
            self.late[nombre] = max_tiempo - tiempo
    
    def dibujar_red(self):
        self.canvas.delete("all")
        
        if not self.actividades:
            return
        
        # Posiciones de nodos (calculadas manualmente simplificado)
        ancho = 850
        alto = 400
        
        # Obtener orden topológico para posicionar
        posiciones = {}
        x, y = 50, alto // 2
        
        # Primeras actividades
        for act in self.actividades:
            if act["predecesor"] == "-" or act["predecesor"] == "":
                posiciones[act["nombre"]] = (x, y)
        
        # Otras actividades (simplificado)
        niveles = {}
        for act in self.actividades:
            nombre = act["nombre"]
            if nombre not in niveles:
                nivel = 0
                if act["predecesor"] != "-" and act["predecesor"] != "":
                    preds = [p.strip() for p in act["predecesor"].split(",") if p.strip()]
                    nivel = max([posiciones.get(p, (0, 0))[0] for p in preds if p in posiciones] + [0])
                posiciones[nombre] = (x + nivel * 150, y + (len(niveles) % 5 - 2) * 60)
                niveles[nombre] = nivel
        
        # Dibujar flechas
        for act in self.actividades:
            nombre = act["nombre"]
            predecesor = act["predecesor"]
            
            if predecesor != "-" and predecesor != "":
                preds = [p.strip() for p in predecesor.split(",") if p.strip()]
                for pred in preds:
                    if pred in posiciones:
                        x1, y1 = posiciones[pred]
                        x2, y2 = posiciones[nombre]
                        
                        # Color de flecha (roja si es ruta crítica)
                        color = "#E74C3C" if (pred in self.ruta_critica and nombre in self.ruta_critica) else "#3498DB"
                        
                        self.canvas.create_line(x1 + 30, y1, x2 - 30, y2, arrow=tk.LAST, fill=color, width=2)
        
        # Dibujar nodos
        for nombre, (x, y) in posiciones.items():
            # Color del nodo
            color = "#E74C3C" if nombre in self.ruta_critica else "#27AE60"
            
            self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=color, outline="white", width=2)
            self.canvas.create_text(x, y, text=nombre, fill="white", font=("Segoe UI", 10, "bold"))
            
            # Duración
            duracion = self.duraciones.get(nombre, 0)
            self.canvas.create_text(x, y + 35, text=f"t={duracion}", fill="#ECF0F1", font=("Segoe UI", 9))
        
        # Mostrar leyenda
        self.canvas.create_rectangle(650, 10, 840, 70, fill="#34495E", outline="#ECF0F1")
        self.canvas.create_text(700, 25, text="Leyenda:", fill="#ECF0F1", font=("Segoe UI", 9, "bold"))
        self.canvas.create_oval(690, 35, 700, 45, fill="#27AE60", outline="white")
        self.canvas.create_text(720, 40, text="Normal", fill="#ECF0F1", font=("Segoe UI", 8))
        self.canvas.create_oval(750, 35, 760, 45, fill="#E74C3C", outline="white")
        self.canvas.create_text(790, 40, text="Crítica", fill="#ECF0F1", font=("Segoe UI", 8))
    
    # ============================================
    # PESTAÑA: RESULTADOS
    # ============================================
    def crear_pestana_resultados(self):
        frame = tk.Frame(self.pestana_resultados, bg="#34495E")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Treeview para resultados
        columnas = ("actividad", "duracion", "early_start", "early_finish", "late_start", "late_finish", "holgura")
        self.tree_resultados = ttk.Treeview(frame, columns=columnas, show="headings", height=12)
        
        titulos = ["Actividad", "Duración", "Early Start", "Early Finish", "Late Start", "Late Finish", "Holgura"]

def main():
    root = tk.Tk()
    app = SistemaPERT(root)
    root.mainloop()

if __name__ == "__main__":
    main()