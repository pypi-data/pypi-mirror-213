import setuptools 
from pathlib import Path

long_desc = Path("README.md").read_text()
setuptools.setup(
    name="holamundoplayerRM",
    version="0.0.1",
    long_description=long_desc,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"] #Carpetas que queremos ignorar
    )
)

# Luego para poder publicar debemos escribir en consola:
# python setup.py sdists (sorce distribution) bdists_wheel (build distribution)
# Esto nos generará 2 empaquetados (build y dist) además de una carpeta que se llama holamundoplayer.egg-info

# Para subir el paqueta a pypi escribimos:
# twine upload dist/*
# Luego señalar usuario y contraseña
