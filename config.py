import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

logging_path = 'log.txt'
CACHE_DIR = os.getenv("HF_HOME")

#other paras
MAX_REFERENCE_NUM = 10
