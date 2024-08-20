from importlib import resources
import json


class Config:

  # paquete donde se encuentra el json y el nombre del fichero.
  __config_json_path, config_json_filename = "game.assets.config","config.json"

  __config_filename = ["game","assets", "config", "config.json"]
  __instance = None 


  @staticmethod
  def instance(): 
    if Config.__instance is None:
      Config()

    return Config.__instance

  def __init__(self):
    if Config.__instance is None:
      Config.__instance = self

      with resources.path( Config.__config_json_path,Config.config_json_filename) as config_path:
        # Cargar fichero json
            with open(config_path) as f:
              self.data = json.load(f) # Contiene el fichero json almacenado.

    else:
      raise exception("Not allowed multiple instances")