import numpy as np # esto solo después de que se intala pip install numpy

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una prueba desde saludos.prueba()")

#esto es nuevo para lo de distribución
def generar_array(numeros): #creará un arreglo por medio de numpy
    return np.arange(numeros) #el arange nos da un rango 
    

def qpw():
    print("Qué pasó weiiiiiii desde saludos.qpw()")

class Saludo:
    def __init__(self):
        print("Hola, te slaudo desde Saludo.__init__()")

    if __name__=='__main__':
        #lo quitamos por ahora para generar un arraysaludar()
        gene=generar_array(5)
        print(gene)

        #python setup.py test