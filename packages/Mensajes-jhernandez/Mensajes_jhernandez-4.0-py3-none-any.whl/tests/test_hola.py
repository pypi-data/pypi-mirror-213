import unittest #importamos unitest
import numpy as np
from mensajes.hola.saludos import generar_array

class PruebasHola(unittest.TestCase): # cfeamos una clase donde haremos las pruebas de hola
    def  test_generar_array(self):
        #utilizaremos una función del numpy para ver que dos arrays son iguales
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))     #aunque parezca que np o algo no está definido, recuerda
            

        



#por regla general deberiamos de tener un fichero test para cada
#paquete que estamosc comprobando como test_jola
