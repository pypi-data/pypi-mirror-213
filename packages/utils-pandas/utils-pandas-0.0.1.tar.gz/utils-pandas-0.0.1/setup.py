from setuptools import setup
import os

# Carregar o conteúdo do arquivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='utils-pandas',
    version='0.0.1',
    description='Pacote Python destinado a criar novas funcionalidades para o Pandas',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['utils-pandas'],
    install_requires=[],
)
