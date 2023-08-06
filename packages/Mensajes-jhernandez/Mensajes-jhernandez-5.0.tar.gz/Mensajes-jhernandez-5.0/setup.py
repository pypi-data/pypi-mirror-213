from setuptools import setup, find_packages
#este se usó para distribución local, lo copio y pego abajo para distribución en linea
#setup(
#    name="Mensajes",
#    version='3.0',
#    description='Un paquete para saludar y despedir',
#    author='Jesús Hernández Marcial',
#    author_email='jesus@jesus.dev',
#    url='https://www.jesus.dev',
#    #packages=['mensajes', 'mensajes.hola', 'mensajes.adios'], #paquetes de antes
#    packages=find_packages(), #automatización de paquetes primero importamos find_packages
    #sustituidmos los paquetes por  find_packages y se encontrará}
    #scripts=['test.py'], 
#    scripts=[],
#    test_suite='tests',  #ahora lo que se llamrá es la carpeta tests pero como es un paquete hay que crear una raiz
    #esto se´ria si queremos solo una paqueteriainstall_requires=['numpy>1.24.3']# esta part sirve para installar paquetes externos rquerido }
#    install_requires=[paquete.strip() 
#                      for paquete in open("requirements.txt").readlines()]# estp es si queremos instalar un 
                      # grupo de paquetes que esten en el archivo se aplica compresion de listas
#)

#python setup.py sdist  cd dist  pip install fichero 
# pip uninstall mensajes
#upgrade

#para actualizar recuerda que  pip install Mensajes-2.0.tar.gz --upgrade

#lo usaremos para prodcuir un ejecutable 
#veremos como buscar los paquetes, cargar dependencias (que nuestro paquete dependa
# de otros paquetes externos y se instalen automáticamente)  y como creart una batería de test
#para que se ejecuten 

#como transformar nuestro paquete local en un paquete para publicar en internet en pypi.org
#nossotros lo publicaremos en test.pypi.org 

setup(
    name="Mensajes-jhernandez", #primero cambiamos el nombre porque es uno común 
    version='5.0', #vambiamos la versión  y debemos crear una descripcion en el readme.md+
    long_descriptcion =  open('README.md').read(), # con el readme creado lo abrimos con este método
   
    long_description_content_type= 'text/markdown', # esto fue para evitar el error de hace rato
    #ahora ya no marca errores al hacer el build y el twine check dist/*

    #se aplica el método read() falta algo pero lo creamos despues
    description='Un paquete para saludar y despedir',
    author='Jesús Hernández Marcial',
    author_email='jesus@jesus.dev',
    url='https://www.jesus.dev',
    license_files= ['LICENSE'],  ##creamos nuestra licencia que llamará al archivo licence que crearemos
    #packages=['mensajes', 'mensajes.hola', 'mensajes.adios'], #paquetes de antes
    packages=find_packages(), #automatización de paquetes primero importamos find_packages
    #sustituidmos los paquetes por  find_packages y se encontrará}
    #scripts=['test.py'], 
    scripts=[],
    test_suite='tests',  #ahora lo que se llamrá es la carpeta tests pero como es un paquete hay que crear una raiz
    #esto se´ria si queremos solo una paqueteriainstall_requires=['numpy>1.24.3']# esta part sirve para installar paquetes externos rquerido }
    install_requires=[paquete.strip() 
                      for paquete in open("requirements.txt").readlines()],
    #tenemos que instalar los clasificadores que es lo que aparece en el repositorio que publicaremos
    #son las categorias en las que pulbicaremos hay muchos en un enlace nosotros queremos el environment
    classifiers= [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities', 
    ],
                      
                      
)

#pip install build twine --upgrade esto se tiene que instalar para armar todo el paquete 
#una vez instalado eso se coloca python -m build para instalar el paquete esto tiene que ser en donde
# #est´s el arhivo a instalar 
#ahora para checar que todos los paquetes estén correctamente instalados
#python -m twine check dist/*   $borramos los tar. gz que no ocupemos 

#al usar lo anterior  se genera un long descriptionerro por el open .read que s e usao

#una vez haciendo lo del long descrition type 
#si tenemos los paquetes que queremos subir en el dist hacemos lo siguiente 
#python -m twine upload -r testpypi dist/*


#se revisa en la liga que te dieron y ahí estatá el modulo instalado
# lo instalamos con el comando indicado y revisamos con pip list si est´s en el sistema
# despues desisntalamos con pip uninstall el nomrbe de lo que querramos desistalar 

#también desinstalamos los repositorios que se opcuparon como numpy
#ahora subiremos al respositorio oficial usando lo siguiente
#python -m twine upload dist/*