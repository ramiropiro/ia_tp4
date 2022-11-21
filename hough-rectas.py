#------------------------------------#
# INF404 – INTELIGENCIA ARTIFICIAL   #
# TRABAJO PRÁCTICO N° 4              #
# RAMIREZ, RAMIRO F. VINF 10400      #
#------------------------------------#

"""----------------------------------
- Transformación de Hough para rectas
----------------------------------"""

import numpy as np # Librería para el manejo de matrices
import cv2 # Librería de manejo de visión computacional avanzada

imagen = cv2.imread("block-lado.jpg") # Cargamos el archivo jpg en una variable de tipo imágen

# Función de OpenCV para cambiar los espectros de color de una imagen
# Cambiamos a escala de grises.
#####################################################################################################
# Primer parámetro: Variable imágen original.
# Segundo parámetro: tipo de conversión, escala de grises.
# Salida: IMÁGEN VARIABLE GRIS
gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)

# Función de OpenCV para la detección de bordes
# Esta función incluye sub procesos a la imágen como el suavizado que se realizaba por separado con
# GaussianBlur en el de circunferencias, además, aplica un filtro de Sobel, el cual consta
# de mediciones sobre la imágen para hacer énfasis en los bordes.
#####################################################################################################
# Primer parámetro: Variable imágen escala de grises.
# Segundo y Tercer parametro: Thresholds. Límites para la detección, a más alto los números más
#                             lineas se detectan.
# Tercer parámetro: valor de apertura para el algoritmo de Sobel.
# Salida: VARIABLE bordes: Devuelve una imágen con todos los bordes resaltados y aplicados como
#         información dentro de la imágen.
bordes = cv2.Canny(gris,50,150,apertureSize = 3)

# Función de transformación de Hough para rectas por medio de OpenCV
#####################################################################################################
# Primer parámetro: Última image procesada, IMÁGEN BORDES. Anteriormente procesada por Canny.
# Segundo y Tercer parámetro: valores de precisión de rho y theta.
# Cuarto parámetro: Valor mínimo para ser considerado una linea.
# Salida: VARIABLE LINEAS: Devuelve un vector con la tupla de valores de todos las lineas
# detectadas, en el formato (p, 0), donde p es la distancia de la coordenada origen (0,0) borde
# superior izquierdo, y 0 es el ángulo de rotación de la linea en radianes.
lineas = cv2.HoughLines(bordes,1,np.pi/180,200)

# Para cada linea encontrada se definen las posiciones
for i in range(0, len(lineas)):
    for rho,theta in lineas[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        # Función para dibujar las lineas encontradas en las coordenadas dadas
        # con el color rgb (0, 128, 255), con ancho de pincel 2.
        # Sobre la imagen original.
        cv2.line(imagen,(x1,y1),(x2,y2),(0,128,255),2)

# Mostramos la imágen final, y esperamos a que se presione una tecla.
cv2.imshow("Transformacion de Hough para rectas", cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB))
cv2.waitKey()