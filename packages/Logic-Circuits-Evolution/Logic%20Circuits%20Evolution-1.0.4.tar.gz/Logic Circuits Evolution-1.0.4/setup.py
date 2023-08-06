from setuptools import setup, find_packages


setup(
    name="Logic Circuits Evolution",
    version="1.0.4",
    description="Modulo Python dedicado a evolução de circuitos lógicos através de algoritmos genéticos",
    author="Humberto Távora, Stefan Blawid, Yasmin Maria",
    packages=find_packages(),
    install_requires=[
        'random',
        'datetime',
        'bisect'
    ]
    )

