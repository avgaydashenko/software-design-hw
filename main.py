from server import Server
from client import Client
from interface import Interface
import logging

logging.basicConfig(level=logging.DEBUG, format="%(filename)s, line:%(lineno)d # [%(asctime)s] %(message)s")
logging.info("start session")

Interface(handle_server=Server, handle_client=Client)