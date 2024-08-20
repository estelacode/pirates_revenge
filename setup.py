from setuptools import setup


setup(
    name = "game", # nombre del juego
    version = "0.0.1",  # version del juego
    packages = ["game"], # paquetes que publica o utiliza
    entry_points = {"console_scripts":["game = game.__main__:main"]}, # puntos de entrada, por donde vamos a llamar a la aplicacion.
    install_requires = ["pygame"] # Paquetes  que se requieren
)