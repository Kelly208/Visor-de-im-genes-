import numpy as np
from PIL import Image

# =========================
# 0. CARGA Y VISUALIZACIÓN
# =========================
def cargar_imagen(ruta):
    img = Image.open(ruta).convert("RGB")
    return np.array(img)

def preparar_para_visor(img):
    return np.clip(img, 0, 255).astype(np.uint8)


# =========================
# 1. NEGATIVO
# =========================
def negativo(img):
    return 255 - img


# =========================
# 2. BRILLO GENERAL
# =========================
def brillo(img, valor):
    imgf = img.astype(np.float32)
    salida = np.clip(imgf + valor, 0, 255)
    return salida.astype(np.uint8)


# =========================
# 3. BRILLO POR CANAL
# =========================
def brillo_canal(img, canal, valor):
    salida = img.astype(np.float32).copy()
    salida[:, :, canal] = np.clip(salida[:, :, canal] + valor, 0, 255)
    return salida.astype(np.uint8)


# =========================
# 4. GRISES PROMEDIO
# =========================
def gris_promedio(img):
    imgf = img.astype(np.float32)
    gris = (imgf[:, :, 0] + imgf[:, :, 1] + imgf[:, :, 2]) / 3
    return gris.astype(np.uint8)


# =========================
# 5. GRISES MIDGRAY
# =========================
def gris_midgray(img):
    imgf = img.astype(np.float32)
    mx = np.max(imgf, axis=2)
    mn = np.min(imgf, axis=2)
    gris = (mx + mn) / 2
    return gris.astype(np.uint8)


# =========================
# 6. GRISES LUMINOSIDAD
# =========================
def gris_luminosidad(img):
    imgf = img.astype(np.float32)
    gris = 0.299*imgf[:, :, 0] + 0.587*imgf[:, :, 1] + 0.114*imgf[:, :, 2]
    return np.clip(gris, 0, 255).astype(np.uint8)


# =========================
# 7. BINARIZACIÓN
# =========================
def binarizar(img, T=128):
    gris = gris_luminosidad(img)
    return np.where(gris >= T, 255, 0).astype(np.uint8)


# =========================
# 8. CANALES RGB (GENÉRICO)
# =========================
def canal_rgb(img, canal):
    salida = np.zeros_like(img)
    salida[:, :, canal] = img[:, :, canal]
    return salida


# =========================
# 9. CANALES CMY (GENÉRICO)
# =========================
def canal_cmy(img, canal):
    salida = img.copy()
    salida[:, :, canal] = 0
    return salida


# =========================
# 10. SUMA DE IMÁGENES
# =========================
def suma_imagenes(img1, img2):
    h, w = img1.shape[:2]
    img2 = np.array(Image.fromarray(img2).resize((w, h)))

    A = img1.astype(np.float32)
    B = img2.astype(np.float32)

    return np.clip((A + B) / 2, 0, 255).astype(np.uint8)


# =========================
# 11. SUMA PONDERADA
# =========================
def suma_ponderada(img1, img2, alpha=0.5):
    h, w = img1.shape[:2]
    img2 = np.array(Image.fromarray(img2).resize((w, h)))

    A = img1.astype(np.float32)
    B = img2.astype(np.float32)

    salida = alpha*A + (1 - alpha)*B
    return np.clip(salida, 0, 255).astype(np.uint8)


# =========================
# 12. HISTOGRAMA POR CANAL
# =========================
def histograma_canal(img, canal):
    if img.max() <= 1.0:
        img = (img * 255).astype(np.uint8)

    return img[:, :, canal].ravel()


# =========================
# 13. RECORTE
# =========================
def recortar(img, xi, xf, yi, yf):
    return img[yi:yf, xi:xf]


# =========================
# 14. ZOOM
# =========================
def zoom(img, factor, cx=None, cy=None):
    h, w = img.shape[:2]

    if cx is None:
        cx = w // 2
    if cy is None:
        cy = h // 2

    # tamaño del recorte (más pequeño = más zoom)
    nh = int(h / factor)
    nw = int(w / factor)

    x1 = max(0, cx - nw // 2)
    x2 = min(w, cx + nw // 2)

    y1 = max(0, cy - nh // 2)
    y2 = min(h, cy + nh // 2)

    recorte = img[y1:y2, x1:x2]

    # reescalar a tamaño original
    zoomed = np.array(Image.fromarray(recorte).resize((w, h)))

    return zoomed


# =========================
# 15. REDUCCIÓN
# =========================
def reduccion(img, f):
    return img[::f, ::f]

# =========================
# 16. ROTACIÓN (USANDO PIL)
# =========================
def rotar_manual(img, ang):
    return np.array(Image.fromarray(img).rotate(ang, expand=True))


# =========================
# 17. TRASLACIÓN
# =========================
def traslacion(img, dx, dy):
    h, w = img.shape[:2]
    salida = np.zeros_like(img)

    x1d = max(0, dx)
    y1d = max(0, dy)
    x2d = min(w, w + dx)
    y2d = min(h, h + dy)

    x1s = max(0, -dx)
    y1s = max(0, -dy)
    x2s = x1s + (x2d - x1d)
    y2s = y1s + (y2d - y1d)

    if x2d > x1d and y2d > y1d:
        salida[y1d:y2d, x1d:x2d] = img[y1s:y2s, x1s:x2s]

    return salida