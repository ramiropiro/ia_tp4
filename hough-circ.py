#------------------------------------#
# INF404 – INTELIGENCIA ARTIFICIAL   #
# TRABAJO PRÁCTICO N° 4              #
# RAMIREZ, RAMIRO F. VINF 10400      #
#------------------------------------#

"""-------------------------------------------
- Transformación de Hough para circunferencias
-------------------------------------------"""

import numpy as np # Librería para el manejo de matrices
import cv2 # Librería de manejo de visión computacional avanzada

imagen = cv2.imread("block-frente.jpg") # Cargamos el archivo jpg en una variable de tipo imágen

# Función de OpenCV para cambiar los espectros de color de una imagen
# Cambiamos a escala de grises.
#####################################################################################################
# Primer parámetro: Variable imágen original.
# Segundo parámetro: tipo de conversión, escala de grises.
# Salida: IMÁGEN VARIABLE GRIS
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

#####################################################################################################
# Las dos siguientes funciones permiten mejorar la imágen para una mejor interpretacion
# del algoritmo de HOUGH
#####################################################################################################

# Función para realizar una ecualización de histograma sobre la imágen, esto nos permite mejorar
# el contraste, hacer las partes claras más claras y las oscuras más oscuras, y por lo tanto le es
# mas facil focalizar / localizar circunferencias al algoritmo.
#####################################################################################################
# Primer parámetro: Variable imágen gris.
# Salida: IMÁGEN VARIABLE HISTOGRAMA
histograma = cv2.equalizeHist(gris)

# Función para realizar un efecto de desenfoque o suavizado a la imagen, permitiendo obtner bordes
# más suaves y tambien ayuda al algoritmo a focalizar / localizar circunferencias.
#####################################################################################################
# Primer parámetro: Aplicamos el suavizado a la imágen histograma.
# Segundo parámetro: Valores sigma x e y, a mayores valores, más el desenfoque.
# Tercer parámetro: Tipo de borde, se busca default.
# Salida: IMÁGEN VARIABLE SUAVIZADO
suavizado = cv2.GaussianBlur(histograma, (31,41), cv2.BORDER_DEFAULT)

# Método para extraer información de la imagen, se obtiene la tupla cantidad de filas y columnas
# Primer parámetro: por medio de imágen suavizado.
# Salida: VARIABLE ALTO (no utilizable) / VARIABLE ANCHO.
alto, ancho = suavizado.shape[:2]

# Se realizan promedio y redondeos de valores en base al ancho de la imagen, para una funcionalidad
# del algoritmo mas precisa, se obtienen las variable:
#####################################################################################################
# VARIABLE minR: minimo tamaño de radio.
# VARIABLE maxR: maximo tamaño de radio.
# VARIABLE minD: minima distancia entre circunferencias.
# Esta última evita que se encuentren circunferencias fantasmas, como sobrebordes.
minR = round(ancho/65)
maxR = round(ancho/11)
minD = round(ancho/7)

# Función de transformación de Hough para circunferencias por medio de OpenCV
#####################################################################################################
# Primer parámetro: Última image procesada, IMÁGEN SUAVIZADO.
# Segundo parámetro: Método de detección, default.
# Tercer parámetro: proporción, por defecto 1, para imágenes muy grandes se puede aumentar este valor
# Cuarto parámetro: VARIABLE minD: minima distancia entre circunferencias. Explicación más arriba.
# Quinto y Sexto parámetro: Variables para eliminar detecciones de falsas circunferencias.
# Septimo parámetro: VARIABLE minR: minimo tamaño de radio. Explicación más arriba.
# Octavo parámetro: VARIABLE maxR: maximo tamaño de radio. Explicación más arriba.
# Salida: VARIABLE CIRCULOS: Devuelve un vector con los valores de todos los circulos
# detectados, en el formato (x, y, radio)
circulos = cv2.HoughCircles(suavizado, cv2.HOUGH_GRADIENT, 1, minD, param1=14, param2=45, minRadius=minR, maxRadius=maxR)

# Si se encontraron circulos
if circulos is not None:
    # Para cada valor (x,y,r) se rendondean y a tipo enteros sin coma.
    circulos = np.round(circulos[0, :]).astype("int")
    for (x, y, r) in circulos:
        # Función para dibujar las circunferencias encontradas en las coordenadas dadas
        # y del tamaño dado por r, en el color rgb (0, 255, 0), con ancho de pincel 2.
        # Sobre la imagen original.
        cv2.circle(imagen, (x, y), r, (0, 255, 0), 2)
        # Función para dibujar rectangulos, en este caso uno diminuto en para ocupar la posición de centro de
        # la circunferencia, en las coordenadas dadas, con el color rgb (0, 128, 255), y el ancho de pincel
        # -1, numero negativo implica rectangulo relleno.
        # Sobre la imágen original.
        cv2.rectangle(imagen, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

# Mostramos la imágen final, y esperamos a que se presione una tecla.
cv2.imshow("Transformacion de Hough para circunferencias", imagen)
cv2.waitKey()