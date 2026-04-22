import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
from Biblioteca import *

img_original = None
img_b = None

# =============================
# MOSTRAR IMAGEN 
# =============================
def mostrar(img):
    img = preparar_para_visor(img)

    h, w = img.shape[:2]
    im = Image.fromarray(img)

    max_w, max_h = 900, 700

    if w > max_w or h > max_h:
        scale = min(max_w / w, max_h / h)
        im = im.resize(
            (int(w * scale), int(h * scale)),
            resample=Image.NEAREST
        )

    imgtk = ImageTk.PhotoImage(im)
    lbl_img.config(image=imgtk)
    lbl_img.image = imgtk

    lbl_size.config(text=f"Tamaño: {w} x {h}")

# =============================
# FUNCIONES
# =============================
def abrir():
    global img_original
    ruta = filedialog.askopenfilename()
    if ruta:
        img_original = cargar_imagen(ruta)
        mostrar(img_original)

def restaurar():
    if img_original is not None:
        mostrar(img_original.copy())

def cargar_b():
    global img_b
    ruta = filedialog.askopenfilename()
    if ruta:
        img_b = cargar_imagen(ruta)

# =============================
# BLOQUES UI
# =============================
def bloque(titulo):
    f = tk.LabelFrame(panel, text=titulo, bd=2)
    f.pack(fill="x", padx=1, pady=2)
    return f

def centrar(w):
    w.pack(pady=2)

# =============================
# VENTANA
# =============================
root = tk.Tk()
root.title("Procesamiento de Imágenes")
root.geometry("1100x700")

# =============================
# PANEL IZQUIERDO
# =============================
frame_left = tk.Frame(root)
frame_left.pack(side="left", fill="y")

canvas = tk.Canvas(frame_left, width=340, highlightthickness=0)
scroll = tk.Scrollbar(frame_left, orient="vertical", command=canvas.yview)

canvas.pack(side="left", fill="y")
scroll.pack(side="right", fill="y")

panel = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=panel, anchor="nw")

canvas.configure(yscrollcommand=scroll.set)

def ajustar_ancho(event):
    canvas.itemconfig(canvas_window, width=event.width)

canvas.bind("<Configure>", ajustar_ancho)
panel.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# =============================
# PANEL DERECHO
# =============================
frame_img = tk.Frame(root)
frame_img.pack(side="left", expand=True, fill="both")

top = tk.Frame(frame_img)
top.pack(pady=10)

tk.Button(top, text="Abrir", width=15, command=abrir).pack(side="left", padx=5)
tk.Button(top, text="Restaurar", width=15, command=restaurar).pack(side="left", padx=5)

lbl_img = tk.Label(frame_img)
lbl_img.pack(expand=True)

lbl_size = tk.Label(frame_img)
lbl_size.pack()

# =============================
# CONTROLES
# =============================

b = bloque("1. Negativo")
centrar(tk.Button(b, text="Aplicar",
        command=lambda: mostrar(negativo(img_original.copy()))))

b = bloque("2. Brillo")
s = tk.Scale(b, from_=-255, to=255, orient="horizontal")
centrar(s)
centrar(tk.Button(b, text="Aplicar",
        command=lambda: mostrar(brillo(img_original.copy(), s.get()))))

b = bloque("3. Brillo por canal")
c = ttk.Combobox(b, values=["R","G","B"])
c.current(0)
centrar(c)

s2 = tk.Scale(b, from_=-255, to=255, orient="horizontal")
centrar(s2)

centrar(tk.Button(b, text="Aplicar",
        command=lambda: mostrar(brillo_canal(img_original.copy(),
        {"R":0,"G":1,"B":2}[c.get()], s2.get()))))

b = bloque("4-5-6 Escala de grises")
cg = ttk.Combobox(b, values=["Promedio","Midgray","Luminosidad"])
cg.current(0)
centrar(cg)

def aplicar_gris():
    if cg.get()=="Promedio":
        mostrar(gris_promedio(img_original))
    elif cg.get()=="Midgray":
        mostrar(gris_midgray(img_original))
    else:
        mostrar(gris_luminosidad(img_original))

centrar(tk.Button(b, text="Aplicar", command=aplicar_gris))

b = bloque("7. Umbralización")
su = tk.Scale(b, from_=0, to=255, orient="horizontal")
centrar(su)
centrar(tk.Button(b, text="Aplicar",
        command=lambda: mostrar(binarizar(img_original, su.get()))))

b = bloque("8. RGB / CMY")
esp = ttk.Combobox(b, values=["RGB","CMY"])
esp.current(0)
centrar(esp)

canal = ttk.Combobox(b)
centrar(canal)

def actualizar(*args):
    canal["values"] = ["R","G","B"] if esp.get()=="RGB" else ["C","M","Y"]
    canal.current(0)

esp.bind("<<ComboboxSelected>>", actualizar)
actualizar()

centrar(tk.Button(b, text="Aplicar",
        command=lambda: mostrar(
            canal_rgb(img_original, {"R":0,"G":1,"B":2}[canal.get()])
            if esp.get()=="RGB"
            else canal_cmy(img_original, {"C":0,"M":1,"Y":2}[canal.get()])
)))

b = bloque("9. Suma de imágenes")
centrar(tk.Button(b, text="Cargar imagen B", command=cargar_b))

alpha = tk.Scale(b, from_=0, to=1, resolution=0.1, orient="horizontal")
alpha.set(0.5)
centrar(alpha)

centrar(tk.Button(b, text="Suma",
        command=lambda: mostrar(suma_imagenes(img_original, img_b))))
centrar(tk.Button(b, text="Suma ponderada",
        command=lambda: mostrar(suma_ponderada(img_original, img_b, alpha.get()))))

b = bloque("10. Histograma")
ch = ttk.Combobox(b, values=["R","G","B"])
ch.current(0)
centrar(ch)

def hist():
    plt.hist(histograma_canal(img_original, {"R":0,"G":1,"B":2}[ch.get()]), bins=256)
    plt.show()

centrar(tk.Button(b, text="Ver", command=hist))

b = bloque("11. Recorte")
tk.Label(b, text="X inicio").pack()
xi = tk.Entry(b); centrar(xi)
tk.Label(b, text="X fin").pack()
xf = tk.Entry(b); centrar(xf)
tk.Label(b, text="Y inicio").pack()
yi = tk.Entry(b); centrar(yi)
tk.Label(b, text="Y fin").pack()
yf = tk.Entry(b); centrar(yf)

def aplicar_recorte():
    try:
        h,w = img_original.shape[:2]
        x1,x2,y1,y2 = int(xi.get()), int(xf.get()), int(yi.get()), int(yf.get())

        if x1<0 or y1<0 or x2>w or y2>h or x1>=x2 or y1>=y2:
            raise ValueError

        mostrar(recortar(img_original, x1,x2,y1,y2))
    except:
        messagebox.showerror("Error","Valores inválidos")

centrar(tk.Button(b, text="Aplicar", command=aplicar_recorte))

# =============================
# 12. ZOOM
# =============================
b = bloque("12. Zoom")

zx = tk.Scale(b, from_=0, to=100, orient="horizontal", label="Zona X (%)")
zy = tk.Scale(b, from_=0, to=100, orient="horizontal", label="Zona Y (%)")
zf = tk.Scale(b, from_=1, to=5, orient="horizontal", label="Factor Zoom")

centrar(zx)
centrar(zy)
centrar(zf)

centrar(tk.Button(b, text="Aplicar Zoom",
        command=lambda: mostrar(
            zoom(img_original,
                 zf.get(),
                 int((zx.get()/100)*img_original.shape[1]),
                 int((zy.get()/100)*img_original.shape[0]))
        )))

# =============================
# 13. REDUCCIÓN 
# =============================
b = bloque("13. Reducción")

sr = tk.Scale(b, from_=1, to=30, orient="horizontal", label="Factor")
centrar(sr)

def aplicar_reduccion():
    f = sr.get()
    img_red = reduccion(img_original, f)
    h, w = img_red.shape[:2]

    img_red = Image.fromarray(img_red).resize(
        (w * 10, h * 10),
        resample=Image.NEAREST
    )

    mostrar(np.array(img_red))

centrar(tk.Button(b, text="Aplicar", command=aplicar_reduccion))

# =============================
# 14. ROTACIÓN
# =============================
b = bloque("14. Rotación")
rot = tk.Scale(b, from_=-180, to=180, orient="horizontal")
centrar(rot)

centrar(tk.Button(b, text="Aplicar",
        command=lambda: mostrar(rotar_manual(img_original, rot.get()))))

root.mainloop()