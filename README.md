# Visor de Imágenes con Transformaciones

Proyecto en Python con interfaz gráfica para aplicar transformaciones básicas sobre imágenes digitales en tiempo real. La aplicación usa Tkinter para la interfaz y Pillow junto con NumPy para el procesamiento de imagen.

## Descripción

La aplicación permite cargar una imagen desde el equipo y aplicar diferentes operaciones de forma interactiva. Cada transformación se ejecuta sobre la imagen original, por lo que se recomienda usar el botón Restaurar antes de aplicar otro efecto.

## Tecnologías utilizadas

- Python 3
- Tkinter
- Pillow
- NumPy
- Matplotlib

## Estructura del proyecto

- Interfaz.py: ventana principal, botones y controles de la interfaz
- Biblioteca.py: funciones de procesamiento de imágenes

## Transformaciones implementadas

- Negativo
- Ajuste de brillo general
- Ajuste de brillo por canal RGB
- Escala de grises por promedio, midgray y luminosidad
- Umbralización
- Separación de canales RGB y CMY
- Suma de imágenes
- Suma ponderada
- Histograma por canal
- Recorte
- Zoom
- Reducción de resolución
- Rotación

## Uso

1. Ejecuta la aplicación.
2. Presiona Abrir para cargar una imagen.
3. Selecciona la transformación deseada.
4. Si vas a probar otro efecto, presiona Restaurar para volver a la imagen original.

## Requisitos

- Tener Python 3 instalado.
- Contar con las librerías necesarias en el entorno virtual o en el sistema.

## Instalación

Si trabajas con un entorno virtual, activa el entorno e instala las dependencias necesarias:

1. Activar el entorno virtual.
2. Instalar Pillow, NumPy y Matplotlib.

## Ejecución

Desde la carpeta del proyecto:

1. Ejecuta Interfaz.py.
2. Usa la ventana para cargar una imagen y aplicar transformaciones.

## Nota importante

La opción Restaurar evita que los efectos se acumulen sobre la imagen cargada. Esto es especialmente importante antes de cambiar entre transformaciones con distintos parámetros.

## Autor

Kelly Palacio Marulanda

Proyecto académico de Computación Gráfica

Universidad Tecnológica de Pereira

## Estado del proyecto

- Funcional
- Interfaz completa
- Transformaciones implementadas
