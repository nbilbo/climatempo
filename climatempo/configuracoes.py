import os


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)
ESTATICOS_DIR = os.path.join(ROOT_DIR, 'estaticos')
IMGS_DIR = os.path.join(ESTATICOS_DIR, 'imgs')
ESTADOS_PATH = os.path.join(ESTATICOS_DIR, 'estados.json')
PADDING = 15
