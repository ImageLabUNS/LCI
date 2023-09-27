from setuptools import setup

setup(
    name='planti_paquete', # 
    version='0.1.0',    
    description='describir el paquete brevemente',
    url='https://github.com/fiaconis/Compy',
    author='Batman, Mujer Maravilla,  Tito',
    author_email='su_mail@gmail.com',
    license='BSD 2-clause',
    packages=['planti_paquete'],
    #En el siguiente campo listen los paquetes necesarios para que funcione el paquete
    install_requires=['pandas',
                      'numpy',
                      'plotly.express',
                      'requests',
                      'scipy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
