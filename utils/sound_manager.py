import os
import sys
import logging
import winsound

class SoundManager:
    def __init__(self):
        self.initialized = True

    def get_sound_path(self, sound_name):
        try:
            if getattr(sys, 'frozen', False):
                # Se estiver rodando como executável
                base_path = sys._MEIPASS
            else:
                # Se estiver rodando como script
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            sound_path = os.path.join(base_path, 'assets', 'sons', sound_name)
            
            # Log para debug
            logging.info(f"Procurando som em: {sound_path}")
            if os.path.exists(sound_path):
                logging.info("Arquivo de som encontrado!")
                return sound_path
            else:
                logging.error(f"Arquivo de som não encontrado em: {sound_path}")
                return None
        except Exception as e:
            logging.error(f"Erro ao obter caminho do som: {e}")
            return None

    def play_sound(self, sound_name):
        try:
            sound_path = self.get_sound_path(sound_name)
            if sound_path:
                # SND_ASYNC para não bloquear | SND_FILENAME para tocar arquivo
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                logging.info("Som iniciado com sucesso")
                return True
            return False
        except Exception as e:
            logging.error(f"Erro ao tocar som: {e}")
            return False