import logging
import os
from dotenv import load_dotenv

# load credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
OATH_CREATE_PLAYLIST = os.getenv("OATH_CREATE_PLAYLIST", "")

# specify csv files and directory
LINKS_DIR = "data"
RESULTS_DIR = "data/results"
PLAYLISTS_DIR = "data/results/individual_playlists"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)
