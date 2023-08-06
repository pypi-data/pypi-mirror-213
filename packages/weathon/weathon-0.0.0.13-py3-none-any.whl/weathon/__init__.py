__version__ = '0.0.0.13'
__author__ = 'LiZhen'
__email__ = '16621660628@163.com'
__release_datetime__ = '2099-10-13 08:56:12'



import os
from pathlib import Path

DATA_DIR = Path.home().joinpath("data")
WEATHON_DIR = DATA_DIR.joinpath("weathon")
CACHE_DIR = WEATHON_DIR.joinpath(".cache")
os.environ["DATA_DIR"] = str(DATA_DIR)
os.environ["WEATHON_DIR"] = str(WEATHON_DIR)
os.environ["WEATHON_CACHE_DIR"] = str(CACHE_DIR)