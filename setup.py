from setuptools import setup, find_packages

setup(
    name='LCI', # 
    version='0.0.2',    
    description='This is a package of the LCI',
    url='https://github.com/ImageLabUNS/LCI',
    author='Laboratorio de ciencia de las imagenes - UNS',
    author_email='imaglabsuns@gmail.com',
    license='BSD 2-clause',
    packages= find_packages(),#['LCI'],
    #En el siguiente campo listen los paquetes necesarios para que funcione el paquete
    install_requires=[
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
